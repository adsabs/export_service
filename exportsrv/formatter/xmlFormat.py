#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from collections import OrderedDict
from datetime import datetime
from flask import current_app
from textwrap import fill
from itertools import product
from string import ascii_uppercase
import re
import ast
import json


# This class accepts JSON object created by Solr and can reformats it
# for the XML Export formats we are supporting.
# 1- To get Dublin Core XML use
#    dublinXML = XMLFormat(jsonFromSolr).get_dublincore_xml()
# 2- To get Reference XML without Abstract use
#    referenceXML = XMLFormat(jsonFromSolr).get_reference_xml()
# 3- To get Reference XML with Abstract use
#    referenceXML = XMLFormat(jsonFromSolr).get_reference_xml(True)

class XMLFormat:

    EXPORT_FORMAT_REF_XML = 'ReferenceXML'
    EXPORT_FORMAT_DUBLIN_XML = 'DublinXML'

    EXPORT_SERVICE_RECORDS_SET_XML = [('xmlns', 'http://ads.harvard.edu/schema/abs/1.1/abstracts'),
                                      ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
                                      ('xsi:schemaLocation',
                                       'http://ads.harvard.edu/schema/abs/1.1/abstracts http://ads.harvard.edu/schema/abs/1.1/abstracts.xsd')]

    REGEX_REMOVE_TAGS_PUB_RAW = re.compile("(\<.*?\>)")
    REGEX_PUB_RAW = dict([
        (re.compile(r"(\;?\s*\<ALTJOURNAL\>.*\</ALTJOURNAL\>\s*)"), r""),  # remove these
        (re.compile(r"(\;?\s*\<CONF_METADATA\>.*\<CONF_METADATA\>\s*)"), r""),
        (re.compile(r"(?:\<ISBN\>)(.*)(?:\</ISBN\>)"), r"\1"),  # get value inside the tag for these
        (re.compile(r"(?:\<NUMPAGES\>)(.*)(?:</NUMPAGES>)"), r"\1"),
    ])

    status = -1
    from_solr = {}

    def __init__(self, from_solr):
        self.from_solr = from_solr
        if (self.from_solr.get('responseHeader')):
            self.status = self.from_solr['responseHeader'].get('status', self.status)


    def get_status(self):
        return self.status


    def get_num_docs(self):
        if (self.status == 0):
            if (self.from_solr.get('response')):
                return self.from_solr['response'].get('numFound', 0)
        return 0


    def __format_date(self, solr_date, export_format):
        # solr_date has the format 2017-12-01T00:00:00Z
        dateTime = datetime.strptime(solr_date, '%Y-%m-%dT%H:%M:%SZ')
        formats = {self.EXPORT_FORMAT_DUBLIN_XML: '%Y-%m-%d', self.EXPORT_FORMAT_REF_XML: '%b %Y'}
        return dateTime.strftime(formats[export_format])


    def __format_line_wrapped(self, text):
        return fill(text, width=72)


    # format authors
    def __add_author_list(self, a_doc, parent, tag):
        if 'author' not in a_doc:
            return
        for author in a_doc['author']:
            ET.SubElement(parent, tag).text = author


    # format affilation
    def __add_affiliation_list(self, a_doc, parent, field):
        if ('aff') not in a_doc:
            return ''
        counter = [''.join(i) for i in product(ascii_uppercase, repeat=2)]
        separator = ', '
        affiliation_list = ''
        for affiliation, i in zip(a_doc['aff'], range(len(a_doc['aff']))):
            affiliation_list += counter[i] + '(' + affiliation + ')' + separator
        # do not need the last separator
        if (len(affiliation_list) > len(separator)):
            affiliation_list = affiliation_list[:-len(separator)]
        ET.SubElement(parent, field).text = self.__format_line_wrapped(affiliation_list)


    # add a link to xml structure
    def __add_doc_a_link(self, parent, link_type, link_name, link_url, count=''):
        record = ET.SubElement(parent, "link")
        record.set('type', link_type)
        ET.SubElement(record, 'name').text = link_name
        ET.SubElement(record, 'url').text = link_url
        if (len(count) > 0):
            ET.SubElement(record, 'count').text = count


    # format links_data
    def __add_links_data_doc_links(self, a_doc, parent):
        link_dict = OrderedDict([
                    ('data',['DATA','On-line Data']),
                    ('electr',['EJOURNAL','Electronic On-line Article (HTML)']),
                    ('gif',['GIF','Scanned Article (GIF)']),
                    ('article',['ARTICLE','Full Printable Article (PDF/Postscript)']),
                    ('preprint',['PREPRINT','arXiv e-print']),
                    ('arXiv',['','']),
                    ('simbad',['SIMBAD','SIMBAD Objects']),
                    ('ned',['NED','NED Objects']),
                    ('openurl',['OPENURL','Library Link Server']),
                ])

        links_type = ''
        count = 1
        for linksData in a_doc['links_data']:
            link = ast.literal_eval(linksData)
            if (link['type'] in link_dict.keys()):
                # need to count the items for multiple ones (i.e., data)
                if (links_type == link['type']):
                    count += 1
                else:
                    count = 1
                links_type = link['type']
                links_url = 'later'  # eventually it is going to be this => link['url']
                if (links_type == 'simbad') or (links_type == ' ned'):
                    self.__add_doc_a_link(parent, link_type=link_dict[links_type][0], link_name=link_dict[links_type][1], link_url=links_url, count=link['instances'])
                if (links_type == 'data'):
                    self.__add_doc_a_link(parent, link_type=link_dict[links_type][0], link_name=link_dict[links_type][1], link_url=links_url, count=str(count))
                else:
                    self.__add_doc_a_link(parent, link_type=link_dict[links_type][0], link_name=link_dict[links_type][1], link_url=links_url)


    # format links
    def __add_doc_links(self, a_doc, parent):
        link_dict =  OrderedDict([
                        #(key:[link type, name,endpoint])
                        ('abstract',['ABSTRACT','Abstract', 'abstract']),
                        ('citation_count', ['CITATIONS', 'Citations to the Article', 'citations']),
                        ('reference',['REFERENCES','References in the Article','references']),
                        ('coreads',['Co-Reads','Co-Reads','coreads']),
                        ('refereed_citation',['REFCIT', 'Refereed Citations to the Article', 'noendpointyet']),
                        ('links_data', []),
                    ])

        link_url_format = current_app.config.get('EXPORT_SERVICE_LINK_URL_FORMAT')
        for link in link_dict:
            if (link == 'abstract'):
                if (len(a_doc.get(link, '')) > 0):
                    self.__add_doc_a_link(parent, link_dict[link][0], link_dict[link][1], link_url_format.format(a_doc.get('bibcode', ''), link_dict[link][2]))
            elif (link == 'citation_count'):
                count = a_doc.get(link, '')
                if (count > 0):
                    self.__add_doc_a_link(parent, link_dict[link][0], link_dict[link][1], link_url_format.format(a_doc.get('bibcode', ''), link_dict[link][2]), str(count))
            elif (link == 'reference'):
                count = len(a_doc.get(link, ''))
                if (count > 0):
                    self.__add_doc_a_link(parent, link_dict[link][0], link_dict[link][1], link_url_format.format(a_doc.get('bibcode', ''), link_dict[link][2]), str(count))
            elif (link == 'coreads'):
                count = a_doc.get('read_count', '')
                if (count > 0):
                    self.__add_doc_a_link(parent, link_dict[link][0], link_dict[link][1], link_url_format.format(a_doc.get('bibcode', ''), link_dict[link][2]))
            elif (link == 'refereed_citation'):
                count = a_doc.get('citation_count', '')
                if (count > 0):
                    self.__add_doc_a_link(parent, link_dict[link][0], link_dict[link][1], link_url_format.format(a_doc.get('bibcode', ''), link_dict[link][2]), str(count))
            elif (link == 'links_data'):
                if 'links_data' in a_doc:
                    self.__add_links_data_doc_links(a_doc, parent)


    # format keyword
    def __add_keywords(self, a_doc, parent, export_format):
        if 'keyword' not in a_doc:
            return
        if (export_format == self.EXPORT_FORMAT_REF_XML):
            record = ET.SubElement(parent, "keywords")
            for keyword in a_doc['keyword']:
                ET.SubElement(record, 'keyword').text = keyword
        elif (export_format == self.EXPORT_FORMAT_DUBLIN_XML):
            ET.SubElement(parent, 'dc:subject').text = self.__format_line_wrapped(', '.join(a_doc.get('keyword', '')))


    # parse pub_raw and eliminate tags
    def __add_clean_pub_raw(self, a_doc):
        pub_raw = ''.join(a_doc.get('pub_raw', ''))
        # proceed only if necessary
        if ('<' in pub_raw) and ('>' in pub_raw):
            for key in self.REGEX_PUB_RAW:
                pub_raw = key.sub(self.REGEX_PUB_RAW[key], pub_raw)
        return pub_raw


    # format pub_raw
    def __add_pub_raw(self, a_doc, parent, field, export_format):
        if 'pub_raw' not in a_doc:
            return
        pub_raw = self.__add_clean_pub_raw(a_doc)
        if (export_format == self.EXPORT_FORMAT_REF_XML):
            # for reference only if pub_raw is a eprint it gets output it
            if (pub_raw.find('arXiv') > 0):
                pub_raw = pub_raw.replace('eprint ', '')
                ET.SubElement(parent, field).text = pub_raw
        elif (export_format == self.EXPORT_FORMAT_DUBLIN_XML):
            # for dublin both types of pub_raw are exported
            # we could have something like this is Solr
            # "pub_raw":"Sensing and Imaging, Volume 18, Issue 1, article id. #17, <NUMPAGES>12</NUMPAGES> pp."
            # where we remove the tag and output it, or something like this
            # "pub_raw":"eprint arXiv:astro-ph/0003081"
            # that gets output as is
            pub_raw = self.REGEX_REMOVE_TAGS_PUB_RAW.sub('', pub_raw).replace('eprint ', '')
            ET.SubElement(parent, field).text = self.__format_line_wrapped(pub_raw)


    # from solr to each types' tags
    def __get_fields(self, export_format):
        if (export_format == self.EXPORT_FORMAT_REF_XML):
            fields = [('bibcode', 'bibcode'), ('title', 'title'), ('author', 'author'),
                      ('aff', 'affiliation'), ('pub', 'journal'), ('volume', 'volume'),
                      ('date', 'pubdate'), ('page', 'page'), ('', 'lastpage'),
                      ('keyword', 'keywords'), ('', 'origin'), ('copyright', 'copyright'),
                      ('link', 'link'), ('url', 'url'), ('comment', 'comment'),
                      ('', 'score'), ('citation_count', 'citations'), ('abstract', 'abstract'),
                      ('doi', 'DOI'), ('pub_raw', 'eprintid')]
        elif (export_format == self.EXPORT_FORMAT_DUBLIN_XML):
            fields = [('bibcode', 'dc:identifier'), ('title', 'dc:title'), ('author', 'dc:creator'),
                      ('pub_raw', 'dc:source'), ('date', 'dc:date'), ('keyword', 'dc:subject'),
                      ('copyright', 'dc:rights'), ('url', 'dc:relation'), ('abstract', 'dc:description'),
                      ('doi', 'dc:identifier')]
        else:
            fields = []
        return OrderedDict(fields)


    # add the value into the return structure, only if a value was defined in Solr
    def __add_in(self, parent, field, value):
        if (len(value) > 0):
            ET.SubElement(parent, field).text = value


    # for each document from Solr, get the fields, and format them accordingly for Dublin format
    def __get_doc_dublin_xml(self, index, parent):
        a_doc = self.from_solr['response'].get('docs')[index]
        fields = self.__get_fields(self.EXPORT_FORMAT_DUBLIN_XML)
        record = ET.SubElement(parent, "record")
        for field in fields:
            if (field == 'bibcode') or (field == 'copyright'):
                self.__add_in(record, fields[field], a_doc.get(field, ''))
            elif (field == 'title') or (field == 'doi'):
                self.__add_in(record, fields[field], ''.join(a_doc.get(field, '')))
            elif (field == 'author'):
                self.__add_author_list(a_doc, record, fields[field])
            elif (field == 'pub_raw'):
                self.__add_pub_raw(a_doc, record, fields[field], self.EXPORT_FORMAT_DUBLIN_XML)
            elif (field == 'date'):
                self.__add_in(record, fields[field], self.__format_date(a_doc.get(field, ''), self.EXPORT_FORMAT_DUBLIN_XML))
            elif (field == 'keyword'):
                self.__add_keywords(a_doc, record, self.EXPORT_FORMAT_DUBLIN_XML)
            elif (field == 'url'):
                self.__add_in(record, fields[field], current_app.config.get('EXPORT_SERVICE_BBB_PATH') + '/' + a_doc.get('bibcode', ''))
            elif (field == 'abstract'):
                self.__add_in(record, fields[field], self.__format_line_wrapped(a_doc.get(field, '')))


    # for each document from Solr, get the fields, and format them accordingly for Reference format
    def __get_doc_reference_xml(self, index, parent, includeAbs):
        a_doc = self.from_solr['response'].get('docs')[index]
        fields = self.__get_fields(self.EXPORT_FORMAT_REF_XML)
        record = ET.SubElement(parent, "record")
        for field in fields:
            if (field == 'bibcode') or (field == 'pub') or (field == 'volume') or \
               (field == 'copyright') or (field == 'eprintid'):
                self.__add_in(record, fields[field], a_doc.get(field, ''))
            elif (field == 'title') or (field == 'page') or (field == 'doi'):
                self.__add_in(record, fields[field], ''.join(a_doc.get(field, '')))
            elif (field == 'author'):
                self.__add_author_list(a_doc, record, fields[field])
            elif (field == 'aff'):
                self.__add_affiliation_list(a_doc, record, fields[field])
            elif (field == 'date'):
                self.__add_in(record, fields[field], self.__format_date(a_doc.get(field, ''), self.EXPORT_FORMAT_REF_XML))
            elif (field == 'pub_raw'):
                self.__add_pub_raw(a_doc, record, fields[field], self.EXPORT_FORMAT_REF_XML)
            elif (field == 'keyword'):
                self.__add_keywords(a_doc, record, self.EXPORT_FORMAT_REF_XML)
            elif (field == 'url'):
                self.__add_in(record, fields[field], current_app.config.get('EXPORT_SERVICE_BBB_PATH') + '/' + a_doc.get('bibcode', ''))
            elif (field == 'citation_count'):
                self.__add_in(record, fields[field], str(a_doc.get(field, '')))
            elif (field == 'abstract') and (includeAbs):
                self.__add_in(record, fields[field], self.__format_line_wrapped(a_doc.get(field, '')))
            elif (field == 'link'):
                self.__add_doc_links(a_doc, record)


    def __get_xml(self, export_format, include_abs=False):
        """
        setup the outer xml structure

        :param export_format:
        :param include_abs:
        :return:
        """
        num_docs = 0
        format_xml = ''
        if (self.status == 0):
            num_docs = self.get_num_docs()
            records = ET.Element("records")
            attribs = OrderedDict(self.EXPORT_SERVICE_RECORDS_SET_XML)
            for attrib in attribs:
                records.set(attrib, attribs[attrib])
            records.set('retrieved', str(num_docs))
            if (export_format == self.EXPORT_FORMAT_REF_XML):
                for index in range(self.get_num_docs()):
                    self.__get_doc_reference_xml(index, records, include_abs)
            elif (export_format == self.EXPORT_FORMAT_DUBLIN_XML):
                for index in range(self.get_num_docs()):
                    self.__get_doc_dublin_xml(index, records)
            format_xml = ET.tostring(records, encoding='utf8', method='xml')
            format_xml = ('>\n<'.join(format_xml.split('><')))
            format_xml = format_xml.replace('</record>', '</record>\n')
        result_dict = {}
        result_dict['msg'] = 'Retrieved {} abstracts, starting with number 1.'.format(num_docs)
        result_dict['export'] = format_xml
        return json.dumps(result_dict)


    def get_reference_xml(self, include_abs=False):
        """
        :param include_abs: 
        :return: reference xml format with or without abstract
        """
        return self.__get_xml(self.EXPORT_FORMAT_REF_XML, include_abs)


    def get_dublincore_xml(self):
        """
        :return: dublin xml format
        """
        return self.__get_xml(self.EXPORT_FORMAT_DUBLIN_XML)

