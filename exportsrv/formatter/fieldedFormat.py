#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
# for the various fielded (formerly known as tagged) Export formats we are supporting.
# 1- To get ADS (formerly known as generic tagged abstract) format use
#    fieldedADS = FieldedFormat(jsonFromSolr).getADSFielded()
# 2- To get EndNote format use
#    fieldedADS = FieldedFormat(jsonFromSolr).getEndNoteFielded()
# 3- To get ProCite format use
#    fieldedProCite = FieldedFormat(jsonFromSolr).getProCiteFielded()
# 4- To get Refman format use
#    fieldedRefman = FieldedFormat(jsonFromSolr).getRefmanFielded()
# 5- To get RefWorks format use
#    fieldedRefWorks = FieldedFormat(jsonFromSolr).getRefWorksFielded()
# 6- To get MEDLARS format use
#    fieldedMEDLARS = FieldedFormat(jsonFromSolr).getMEDLARSFielded()

class FieldedFormat:
    
    # Fielded (formerly known as tagged)
    EXPORT_FORMAT_ADS = 'ADS'
    EXPORT_FORMAT_ENDNOTE = 'EndNote'
    EXPORT_FORMAT_PROCITE = 'ProCite'
    EXPORT_FORMAT_REFMAN = 'Refman'
    EXPORT_FORMAT_REFWORKS = 'RefWorks'
    EXPORT_FORMAT_MEDLARS = 'MEDLARS'

    REGEX_PUB_RAW = dict([
        (re.compile(r"(\;?\s*\<ALTJOURNAL\>.*\</ALTJOURNAL\>\s*)"), r""),  # remove these
        (re.compile(r"(\;?\s*\<CONF_METADATA\>.*\<CONF_METADATA\>\s*)"), r""),
        (re.compile(r"(?:\<ISBN\>)(.*)(?:\</ISBN\>)"), r"\1"),  # get value inside the tag for these
        (re.compile(r"(?:\<NUMPAGES\>)(.*)(?:</NUMPAGES>)"), r"\1"),
    ])

    status = -1
    from_solr = {}


    def __init__(self, from_solr):
        """

        :param from_solr:
        """
        self.from_solr = from_solr
        if (self.from_solr.get('responseHeader')):
            self.status = self.from_solr['responseHeader'].get('status', self.status)


    def get_status(self):
        """

        :return: status of solr query
        """
        return self.status


    def get_num_docs(self):
        """

        :return: number of docs returned by solr query
        """
        if (self.status == 0):
            if (self.from_solr.get('response')):
                return self.from_solr['response'].get('numFound', 0)
        return 0


    def __get_doc_type(self, solr_type, export_format):
        """
        from solr to each fielded document type
        
        :param solr_type: 
        :param export_format: 
        :return: 
        """
        fields = {}
        if (export_format == self.EXPORT_FORMAT_ENDNOTE):
            fields = {'article': 'Journal Article', 'book': 'Book', 'inbook': 'Book Section',
                      'proceedings': 'Journal Article', 'inproceedings': 'Conference Proceedings',
                      'abstract': 'Conference Paper', 'misc': 'Journal Article', 'eprint': 'Electronic Article',
                      'talk': 'Conference Paper', 'software':'Miscellaneous', 'proposal':'Miscellaneous',
                      'pressrelease':'Journal Article', 'circular':'Journal Article', 'newsletter':'Journal Article',
                      'catalog':'Journal Article', 'phdthesis':'Thesis', 'mastersthesis':'Thesis',
                      'techreport':'Report', 'intechreport':'Report'}
        elif (export_format == self.EXPORT_FORMAT_PROCITE):
            fields = {'article': 'Journal', 'book': 'Book, Whole', 'inbook': 'Book Chapter',
                      'proceedings': 'Journal', 'inproceedings': 'Conference',
                      'abstract': 'Conference', 'misc': 'Journal', 'eprint': 'Preprint',
                      'talk': 'Conference', 'software':'Miscellaneous', 'proposal':'Miscellaneous',
                      'pressrelease':'Journal', 'circular':'Journal', 'newsletter':'Journal',
                      'catalog':'Journal', 'phdthesis':'Thesis/Dissertation', 'mastersthesis':'Thesis/Dissertation',
                      'techreport':'Report', 'intechreport':'Report'}
        elif (export_format == self.EXPORT_FORMAT_REFMAN):
            fields = {'article': 'JOUR', 'book': 'BOOK', 'inbook': 'CHAP',
                      'proceedings': 'JOUR', 'inproceedings': 'CONF',
                      'abstract': 'CONF', 'misc': 'JOUR', 'eprint': 'Preprint',
                      'talk': 'CONF', 'software':'MISC', 'proposal':'MISC',
                      'pressrelease':'JOUR', 'circular':'JOUR', 'newsletter':'JOUR',
                      'catalog':'JOUR', 'phdthesis':'Thesis/Dissertation', 'mastersthesis':'Thesis/Dissertation',
                      'techreport':'RPRT', 'intechreport':'RPRT'}
        elif (export_format == self.EXPORT_FORMAT_REFWORKS):
            fields = {'article': 'Journal', 'book': 'Book, Whole', 'inbook': 'Book, Chapter',
                      'proceedings': 'Journal', 'inproceedings': 'Conference Proceeding',
                      'abstract': 'Conference Proceeding', 'misc': 'Journal', 'eprint': 'Preprint',
                      'talk': 'Conference Proceeding', 'software':'Generic', 'proposal':'Generic',
                      'pressrelease':'Journal', 'circular':'Journal', 'newsletter':'Journal',
                      'catalog':'Journal', 'phdthesis':'Thesis/Dissertation', 'mastersthesis':'Thesis/Dissertation',
                      'techreport':'Report', 'intechreport':'Report'}
        elif (export_format == self.EXPORT_FORMAT_MEDLARS):
            fields = {'article': 'Journal Article', 'book': 'Book', 'inbook': 'Book Chapter',
                      'proceedings': 'Journal Article', 'inproceedings': 'Conference',
                      'abstract': 'Conference', 'misc': 'Journal Article', 'eprint': 'Preprint',
                      'talk': 'Conference', 'software':'Miscellaneous', 'proposal':'Miscellaneous',
                      'pressrelease':'Journal Article', 'circular':'Journal Article', 'newsletter':'Journal Article',
                      'catalog':'Journal Article', 'phdthesis':'Thesis', 'mastersthesis':'Thesis',
                      'techreport':'Report', 'intechreport':'Report'}
        return fields.get(solr_type, '')


    def __format_date(self, solr_date, export_format):
        """

        :param solr_date:
        :param export_format:
        :return:
        """
        # solr_date has the format 2017-12-01T00:00:00Z
        date_time = datetime.strptime(solr_date, '%Y-%m-%dT%H:%M:%SZ')
        formats = {self.EXPORT_FORMAT_ADS: '%m/%Y', self.EXPORT_FORMAT_ENDNOTE: '%B %d, %Y',
                   self.EXPORT_FORMAT_PROCITE: '%Y/%m/X%d', self.EXPORT_FORMAT_REFMAN: '%Y/%m/X%d',
                   self.EXPORT_FORMAT_REFWORKS: '%Y/%m/X%d', self.EXPORT_FORMAT_MEDLARS: '%Y %b %d'}
        return date_time.strftime(formats[export_format]).replace('X0', 'X').replace('X', '')


    def __format_line_wrapped(self, text):
        """

        :param text:
        :return:
        """
        return fill(text, width=72)


    def __get_tags(self, export_format):
        """
        convert from solr to each fielded types' tags
        
        :param export_format: 
        :return: 
        """
        if (export_format == self.EXPORT_FORMAT_ADS):
            return (OrderedDict([('bibcode', '%R'), ('title', '%T'), ('author', '%A'),
                                 ('aff', '%F'), ('pub', '%J'), ('volume', '%V'),
                                 ('date', '%D'), ('page', '%P'), ('keyword', '%K'),
                                 ('', '%G'), ('copyright', '%C'), ('links', '%I'),
                                 ('url', '%U'), ('comment', '%X'), ('', '%S'),
                                 ('abstract', '%B'), ('doi', '%Y DOI:')]))
        if (export_format == self.EXPORT_FORMAT_ENDNOTE):
            return (OrderedDict([('doctype', '%0'), ('title', '%T'), ('author', '%A'),
                                 ('aff', '%+'), ('pub', '%B'), ('volume', '%V'),
                                 ('year', '%D'), ('date', '%8'), ('keyword', '%K'),
                                 ('url', '%U'), ('comment', '%Z'), ('abstract', '%X'),
                                 ('doi', '%3')]))
        if (export_format == self.EXPORT_FORMAT_PROCITE):
            return (OrderedDict([('doctype', 'TY  -'), ('title', 'T1  -'), ('author', 'A1  -'),
                                 ('pub', 'JO  -'), ('volume', 'VL  -'), ('date', 'Y1  -'),
                                 ('page', 'SP  -'), ('keyword', 'KW  -'), ('url', 'UR  -'),
                                 ('abstract', 'N2  -'), ('doi', 'DO  -'), ('endRecord', 'ER  -')]))
        if (export_format == self.EXPORT_FORMAT_REFMAN):
            return (OrderedDict([('doctype', 'TY  -'), ('title', 'T1  -'), ('author', 'A1  -'),
                                 ('pub', 'JO  -'), ('volume', 'VL  -'), ('date', 'Y1  -'),
                                 ('page', 'SP  -'), ('keyword', 'KW  -'), ('url', 'UR  -'),
                                 ('abstract', 'N2  -'), ('doi', 'DO  -'), ('endRecord', 'ER  -')]))
        if (export_format == self.EXPORT_FORMAT_REFWORKS):
            return (OrderedDict([('doctype', 'RT'), ('title', 'T1'), ('author', 'A1'),
                                 ('aff', 'AD'), ('pub', 'JF'), ('volume', 'VO'),
                                 ('year', 'YR'), ('date', 'FD'), ('page', 'SP'),
                                 ('keyword', 'K1'), ('url', 'LK'), ('comment', 'NO'),
                                 ('abstract', 'AB'), ('doi', 'DO DOI:')]))
        if (export_format == self.EXPORT_FORMAT_MEDLARS):
            return (OrderedDict([('doctype', 'PT  -'), ('title', 'TI  -'), ('author', 'AU  -'),
                                 ('pub', 'TA  -'), ('pub_raw', 'SO  -'), ('volume', 'VI  -'),
                                 ('date', 'DP  -'), ('url', '4099-'), ('abstract', 'AB  -')]))


    def __add_author_list(self, a_doc, export_format, tag):
        """
        format authors
        
        :param a_doc: 
        :param export_format: 
        :param tag: 
        :return: 
        """
        if 'author' not in a_doc:
            return ''

        if (export_format == self.EXPORT_FORMAT_ADS):
            separator = ';'
            result = tag + ' '
            for author in a_doc['author']:
                result += author + separator
            # do not need the last separator
            if (len(result) > len(separator)):
                result = result[:-len(separator)]
            return self.__format_line_wrapped(result) + '\n'

        if (export_format == self.EXPORT_FORMAT_ENDNOTE) or (export_format == self.EXPORT_FORMAT_PROCITE) or \
            (export_format == self.EXPORT_FORMAT_REFMAN) or (export_format == self.EXPORT_FORMAT_REFWORKS) or \
            (export_format == self.EXPORT_FORMAT_MEDLARS):
            separator = '\n'
            result = ''
            for author in a_doc['author']:
                result += tag + ' ' + author + separator
            # do not need the last separator
            if (len(result) > len(separator)):
                result = result[:-len(separator)]
            return result + '\n'

        return ''


    def __get_affiliation_list(self, a_doc, export_format, tag):
        """
        format affiliation

        :param a_doc:
        :param export_format:
        :param tag:
        :return:
        """
        if ('aff') not in a_doc:
            return ''

        counter = [''.join(i) for i in product(ascii_uppercase, repeat=2)]
        separator = ', '

        if (len(tag) > 0):
            affiliation_list = tag + ' '
        else:
            affiliation_list = ''

        for affiliation, i in zip(a_doc['aff'], range(len(a_doc['aff']))):
            affiliation_list += counter[i] + '(' + affiliation + ')' + separator
        # do not need the last separator
        if (len(affiliation_list) > len(separator)):
            affiliation_list = affiliation_list[:-len(separator)]

        if (export_format == self.EXPORT_FORMAT_ADS):
            return self.__format_line_wrapped(affiliation_list) + '\n'

        return affiliation_list + '\n'


    def __add_doc_links_property(self, a_doc, tag):
        """
        format links that are defined in the property field
        :param a_doc: 
        :param tag:
        :return: 
        """
        link_dict = OrderedDict([
            ('TOC', ['TOC', 'Table of Contents']),
            ('LIBRARYCATALOG', ['LIBRARY', 'Library Entry']),
        ])
        link_list = ''
        next_line = ';\n'
        for link in link_dict:
            if link in a_doc.get('property', ''):
                link_list += tag + ' ' + link_dict[link][0] + ': ' + link_dict[link][1] + next_line
        return link_list


    def __add_doc_links_esource(self, a_doc, tag):
        """
        format links that are defined in the esource field

        :param a_doc:
        :param tag:
        :return:
        """
        link_dict = OrderedDict([
            # (link type:[name, access])
            ('EPRINT_HTML', 'arXiv Article'),
            ('AUTHOR_HTML', 'Author Article'),
            ('PUB_HTML', 'Publisher Article'),
            ('ADS_SCAN', 'Scanned Article (GIF)'),
            ('EPRINT_PDF', 'arXiv PDF'),
            ('AUTHOR_PDF', 'Author PDF'),
            ('PUB_PDF', 'Publisher PDF'),
            ('ADS_PDF', 'ADS PDF'),
        ])
        link_list = ''
        next_line = ';\n'
        for link in link_dict:
            if link.upper() in a_doc.get('esources', ''):
                link_list += tag + ' ' + link + ': ' + link_dict[link] + next_line
        return link_list


    def __add_doc_links_data(self, a_doc, tag):
        """
        format links that are defined in the data field

        :param a_doc:
        :param tag:
        :return:
        """
        link_dict = OrderedDict([
                        ('ARI', 'Astronomisches Rechen-Institut'),
                        ('SIMBAD', 'SIMBAD Database at the CDS'),
                        ('NED', 'NASA/IPAC Extragalactic Database'),
                        ('CDS', 'Strasbourg Astronomical Data Center'),
                        ('Vizier', 'VizieR Catalog Service'),
                        ('GCPD', 'The General Catalogue of Photometric Data'),
                        ('Author', 'Author Hosted Dataset'),
                        ('PDG', 'Particle Data Group'),
                        ('MAST', 'Mikulski Archive for Space Telescopes'),
                        ('HEASARC', '''NASA's High Energy Astrophysics Science Archive Research Center'''),
                        ('INES', 'IUE Newly Extracted Spectra'),
                        ('IBVS', 'Information Bulletin on Variable Stars'),
                        ('Astroverse', 'CfA Dataverse'),
                        ('ESA', 'ESAC Science Data Center'),
                        ('NExScI', 'NASA Exoplanet Archive'),
                        ('PDS', 'The NASA Planetary Data System'),
                        ('AcA', 'Acta Astronomica Data Files'),
                        ('ISO', 'Infrared Space Observatory'),
                        ('ESO', 'European Southern Observatory'),
                        ('CXO', 'Chandra X-Ray Observatory'),
                        ('NOAO', 'National Optical Astronomy Observatory'),
                        ('XMM', 'XMM Newton Science Archive'),
                        ('Spitzer', 'Spitzer Space Telescope'),
                        ('PASA', 'Publication of the Astronomical Society of Australia Datasets'),
                        ('ATNF', 'Australia Telescope Online Archive'),
                        ('KOA', 'Keck Observatory Archive'),
                        ('Herschel', 'Herschel Science Center'),
                        ('GTC', 'Gran Telescopio CANARIAS Public Archive'),
                        ('BICEP2', 'BICEP/Keck Data'),
                        ('ALMA', 'Atacama Large Millimeter/submillimeter Array'),
                        ('CADC', 'Canadian Astronomy Data Center'),
                        ('Zenodo', 'Zenodo Archive'),
                        ('TNS', 'Transient Name Server'),
                ])
        data_dict = {}
        for d in a_doc.get('data', ''):
            data_dict[d.split(':')[0]] = int(d.split(':')[1])
        link_list = ''
        next_line = ';\n'
        for link in link_dict:
            if link in data_dict.keys():
                link_list += tag + ' ' + link + ': ' + link_dict[link] + next_line
        return link_list


    def __add_doc_links(self, a_doc, tag):
        """
        format links

        :param a_doc:
        :param tag:
        :return:
        """
        link_dict = OrderedDict([
            # (link type:[include if, name, has count])
            ('abstract', [len(a_doc.get('abstract', '')), 'ABSTRACT', 'Abstract']),
            ('citations', [a_doc.get('citation_count', 0), 'CITATIONS', 'Citations to the Article']),
            ('reference', [len(a_doc.get('reference', '')), 'REFERENCES', 'References in the Article']),
            ('coreads', [a_doc.get('read_count', ''), 'Co-Reads', 'Co-Reads']),
        ])
        link_list = ''
        next_line = ';\n'
        for link in link_dict:
            if (link_dict[link][0] > 0):
                link_list += tag + ' ' + link_dict[link][1] + ': ' + link_dict[link][2] + next_line

        link_list += self.__add_doc_links_property(a_doc, tag)
        link_list += self.__add_doc_links_esource(a_doc, tag)
        link_list += self.__add_doc_links_data(a_doc, tag)
        return link_list


    def __add_keywords(self, a_doc, export_format, tag):
        """
        format keywords

        :param a_doc:
        :param export_format:
        :param tag:
        :return:
        """
        if 'keyword' not in a_doc:
            return ''

        separator = {self.EXPORT_FORMAT_ADS:', ', self.EXPORT_FORMAT_ENDNOTE:'; ', self.EXPORT_FORMAT_PROCITE:'/ ',
                     self.EXPORT_FORMAT_REFMAN:'\n', self.EXPORT_FORMAT_REFWORKS:'\n'}

        if (export_format == self.EXPORT_FORMAT_ADS) or (export_format == self.EXPORT_FORMAT_ENDNOTE) or (export_format == self.EXPORT_FORMAT_PROCITE):
            result = tag + ' '
            for keyword in a_doc['keyword']:
                result += keyword + separator[export_format]
            # do not need the last separator
            if (len(result) > len(separator[export_format])):
                result = result[:-len(separator[export_format])]
            return self.__format_line_wrapped(result) + '\n'

        if (export_format == self.EXPORT_FORMAT_REFMAN) or (export_format == self.EXPORT_FORMAT_REFWORKS):
            result = ''
            for keyword in a_doc['keyword']:
                result += tag + ' ' + keyword + separator[export_format]
            # do not need the last separator
            if (len(result) > len(separator[export_format])):
                result = result[:-len(separator[export_format])]
            return result + '\n'
        return ''


    def __add_clean_pub_raw(self, a_doc):
        """
        parse pub_raw and eliminate tags

        :param a_doc:
        :return:
        """
        pub_raw = ''.join(a_doc.get('pub_raw', ''))
        # proceed only if necessary
        if ('<' in pub_raw) and ('>' in pub_raw):
            for key in self.REGEX_PUB_RAW:
                pub_raw = key.sub(self.REGEX_PUB_RAW[key], pub_raw)
        return pub_raw


    def __add_in(self, field, value):
        """
        add the value into the return structure, only if a value was defined in Solr

        :param field:
        :param value:
        :return:
        """
        if (((isinstance(value, unicode)) or (isinstance(value, str))) and (len(value) > 0)) or \
           ((isinstance(value, int)) and (value is not None)):
            return field + ' ' + value + '\n'
        return ''


    def __get_doc(self, index, fields, export_format):
        """

        :param index:
        :param fields:
        :param export_format:
        :return:
        """
        result = ''
        a_doc = self.from_solr['response'].get('docs')[index]
        for field in fields:
            if (field == 'title') or (field == 'page') or (field == 'doi'):
                result += self.__add_in(fields[field], ''.join(a_doc.get(field, '')))
            elif (field == 'author'):
                result += self.__add_author_list(a_doc, export_format, fields[field])
            elif (field == 'doctype'):
                result += self.__add_in(fields[field], self.__get_doc_type(a_doc.get(field, ''), export_format))
            elif (field == 'date'):
                result += self.__add_in(fields[field], self.__format_date(a_doc.get(field, ''), export_format))
            elif (field == 'abstract'):
                result += self.__add_in(fields[field], self.__format_line_wrapped(a_doc.get(field, '')))
            elif (field == 'aff'):
                result += self.__get_affiliation_list(a_doc, export_format, fields[field])
            elif (field == 'keyword'):
                result += self.__add_keywords(a_doc, export_format, fields[field])
            elif (field == 'comment'):
                result += self.__add_in(fields[field], self.__format_line_wrapped(''.join(a_doc.get(field, ''))))
            elif (field == 'url'):
                result += self.__add_in(fields[field], current_app.config['EXPORT_SERVICE_BBB_PATH'] + '/' + a_doc.get('bibcode', ''))
            elif (field == 'endRecord'):
                result += self.__add_in(fields[field], ' ')
            elif (field == 'pub_raw'):
                result += self.__add_in(fields[field], self.__add_clean_pub_raw(a_doc))
            elif (field == 'links'):
                result += self.__add_doc_links(a_doc, fields[field])
            else:
                result += self.__add_in(fields[field], a_doc.get(field, ''))
        # line feed once the doc is complete
        return result + '\n\n'


    def __get_fielded(self, export_format):
        """
        for each document from Solr, get the fields, and format them accordingly

        :param export_format: 
        :return: 
        """
        num_docs = 0
        results = []
        if (self.status == 0):
            fields = self.__get_tags(export_format)
            num_docs = self.get_num_docs()
            for index in range(num_docs):
                results += self.__get_doc(index, fields, export_format)
        result_dict = {}
        result_dict['msg'] = 'Retrieved {} abstracts, starting with number 1.'.format(num_docs)
        result_dict['export'] = ''.join(result for result in results)
        return result_dict


    def get_ads_fielded(self):
        """
        :return: ads formatted export
        """
        return self.__get_fielded(self.EXPORT_FORMAT_ADS)


    def get_endnote_fielded(self):
        """
        :return: endnote formatted export
        """
        return self.__get_fielded(self.EXPORT_FORMAT_ENDNOTE)


    def get_procite_fielded(self):
        """
        :return: procite formatted export
        """
        return self.__get_fielded(self.EXPORT_FORMAT_PROCITE)


    def get_refman_fielded(self):
        """
        :return: refman formatted export
        """
        return self.__get_fielded(self.EXPORT_FORMAT_REFMAN)


    def get_refworks_fielded(self):
        """
        :return: refworks formatted export
        """
        return self.__get_fielded(self.EXPORT_FORMAT_REFWORKS)


    def get_medlars_fielded(self):
        """
        :return: medlars formatted export
        """
        return self.__get_fielded(self.EXPORT_FORMAT_MEDLARS)

