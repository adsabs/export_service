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

EXPORT_FORMAT_REF_XML = 'ReferenceXML'
EXPORT_FORMAT_DUBLIN_XML = 'DublinXML'

# This class accepts JSON object created by Solr and can reformats it
# for the XML Export formats we are supporting.
# 1- To get Dublin Core XML use
#    dublinXML = XMLFormat(jsonFromSolr).getDublinXML()
# 2- To get Reference XML without Abstract use
#    referenceXML = XMLFormat(jsonFromSolr).getReferenceXML()
# 3- To get Reference XML with Abstract use
#    referenceXML = XMLFormat(jsonFromSolr).getReferenceXML(True)

class XMLFormat:
    status = -1
    fromSolr = {}

    def __init__(self, fromSolr):
        self.fromSolr = fromSolr
        if (self.fromSolr.get('responseHeader')):
            self.status = self.fromSolr['responseHeader'].get('status', self.status)

    def getStatus(self):
        return self.status

    def getNumDocs(self):
        if (self.status == 0):
            if (self.fromSolr.get('response')):
                return self.fromSolr['response'].get('numFound', 0)
        return 0

    def __formatDate(self, solrDate, exportFormat):
        # solrDate has the format 2017-12-01T00:00:00Z
        dateTime = datetime.strptime(solrDate, '%Y-%m-%dT%H:%M:%SZ')
        formats = {EXPORT_FORMAT_DUBLIN_XML: '%Y-%m-%d', EXPORT_FORMAT_REF_XML: '%b %Y'}
        return dateTime.strftime(formats[exportFormat])

    def __formatLineWrapped(self, text):
        return fill(text, width=72)

    # format authors
    def __addAuthorList(self, aDoc, parent, tag):
        if 'author' not in aDoc:
            return
        for author in aDoc['author']:
            ET.SubElement(parent, tag).text = author

    # format affilation
    def __addAffiliationList(self, aDoc, parent, field):
        if ('aff') not in aDoc:
            return ''
        counter = [''.join(i) for i in product(ascii_uppercase, repeat=2)]
        separator = ', '
        affiliationList = ''
        for affiliation, i in zip(aDoc['aff'], range(len(aDoc['aff']))):
            affiliationList += counter[i] + '(' + affiliation + ')' + separator
        # do not need the last separator
        if (len(affiliationList) > len(separator)):
            affiliationList = affiliationList[:-len(separator)]
        ET.SubElement(parent, field).text = self.__formatLineWrapped(affiliationList)

    # add a link to xml structure
    def __addDocALink(self, parent, linkType, linkName, linkURL, count=''):
        record = ET.SubElement(parent, "link")
        record.set('type', linkType)
        ET.SubElement(record, 'name').text = linkName
        ET.SubElement(record, 'url').text = linkURL
        if (len(count) > 0):
            ET.SubElement(record, 'count').text = count

    # format links_data
    def __addLinksDataDocLinks(self, aDoc, parent):
        linkDict = OrderedDict([
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

        linksType = ''
        count = 1
        for linksData in aDoc['links_data']:
            link = ast.literal_eval(linksData)
            if (link['type'] in linkDict.keys()):
                # need to count the items for multiple ones (i.e., data)
                if (linksType == link['type']):
                    count += 1
                else:
                    count = 1
                linksType = link['type']
                linksURL = 'later'  # eventually it is going to be this => link['url']
                if (linksType == 'simbad') or (linksType == ' ned'):
                    self.__addDocALink(parent, linkType=linkDict[linksType][0], linkName=linkDict[linksType][1], linkURL=linksURL, count=link['instances'])
                if (linksType == 'data'):
                    self.__addDocALink(parent, linkType=linkDict[linksType][0], linkName=linkDict[linksType][1], linkURL=linksURL, count=str(count))
                else:
                    self.__addDocALink(parent, linkType=linkDict[linksType][0], linkName=linkDict[linksType][1], linkURL=linksURL)

    # format links
    def __addDocLinks(self, aDoc, parent):
        linkDict =  OrderedDict([
                        ('abstract',['ABSTRACT','Abstract', 'abstract']),
                        ('citation_count', ['CITATIONS', 'Citations to the Article', 'citations']),
                        ('reference',['REFERENCES','References in the Article','references']),
                        ('coreads',['Co-Reads','Co-Reads','coreads']),
                        ('links_data', []),
                    ])

        linkURLFormat = current_app.config.get('EXPORT_SERVICE_LINK_URL_FORMAT')
        for link in linkDict:
            if (link == 'abstract'):
                if (len(aDoc.get(link, '')) > 0):
                    self.__addDocALink(parent, linkDict[link][0], linkDict[link][1], linkURLFormat.format(aDoc.get('bibcode', ''), linkDict[link][2]))
            elif (link == 'citation_count'):
                count = aDoc.get(link, '')
                if (count > 0):
                    self.__addDocALink(parent, linkDict[link][0], linkDict[link][1], linkURLFormat.format(aDoc.get('bibcode', ''), linkDict[link][2]), str(count))
            elif (link == 'reference'):
                count = len(aDoc.get(link, ''))
                if (count > 0):
                    self.__addDocALink(parent, linkDict[link][0], linkDict[link][1], linkURLFormat.format(aDoc.get('bibcode', ''), linkDict[link][2]), str(count))
            elif (link == 'coreads'):
                self.__addDocALink(parent, linkDict[link][0], linkDict[link][1], linkURLFormat.format(aDoc.get('bibcode', ''), linkDict[link][2]))
            elif (link == 'links_data'):
                if 'links_data' in aDoc:
                    self.__addLinksDataDocLinks(aDoc, parent)
    # format keyword
    def __addKeywords(self, aDoc, parent, exportFormat):
        if 'keyword' not in aDoc:
            return
        if (exportFormat == EXPORT_FORMAT_REF_XML):
            record = ET.SubElement(parent, "keywords")
            for keyword in aDoc['keyword']:
                ET.SubElement(record, 'keyword').text = keyword
        elif (exportFormat == EXPORT_FORMAT_DUBLIN_XML):
            ET.SubElement(parent, 'dc:subject').text = self.__formatLineWrapped(', '.join(aDoc.get('keyword', '')))

    # parse pub_raw and eliminate tags
    def __addCleanPubRaw(self, aDoc):
        pubRaw = ''.join(aDoc.get('pub_raw', ''))
        # proceed only if necessary
        if ('<' in pubRaw) and ('>' in pubRaw):
            tokens = dict([
                (r"(\;?\s*\<ALTJOURNAL\>.*\</ALTJOURNAL\>\s*)",     r""),          # remove these
                (r"(\;?\s*\<CONF_METADATA\>.*\<CONF_METADATA\>\s*)",r""),
                (r"(?:\<ISBN\>)(.*)(?:\</ISBN\>)",                  r"\1"),        # get value inside the tag for these
                (r"(?:\<NUMPAGES\>)(.*)(?:</NUMPAGES>)",            r"\1"),
            ])
            for key in tokens:
                regex = re.compile(key)
                pubRaw = regex.sub(tokens[key], pubRaw)
        return pubRaw

    # format pub_raw
    def __addPubRaw(self, aDoc, parent, field, exportFormat):
        if 'pub_raw' not in aDoc:
            return
        pubRaw = self.__addCleanPubRaw(aDoc)
        if (exportFormat == EXPORT_FORMAT_REF_XML):
            # for reference only if pub_raw is a eprint it gets output it
            if (pubRaw.find('arXiv') > 0):
                pubRaw = pubRaw.replace('eprint ', '')
                ET.SubElement(parent, field).text = pubRaw
        elif (exportFormat == EXPORT_FORMAT_DUBLIN_XML):
            # for dublin both types of pub_raw are exported
            # we could have something like this is Solr
            # "pub_raw":"Sensing and Imaging, Volume 18, Issue 1, article id. #17, <NUMPAGES>12</NUMPAGES> pp."
            # where we remoe the tag and output it, or something like this
            # "pub_raw":"eprint arXiv:astro-ph/0003081"
            # that gets output as is
            regex = re.compile("(\<.*?\>)")
            pubRaw = regex.sub('', pubRaw).replace('eprint ', '')
            ET.SubElement(parent, field).text = self.__formatLineWrapped(pubRaw)

    # from solr to each types' tags
    def __getFields(self, exportFormat):
        if (exportFormat == EXPORT_FORMAT_REF_XML):
            fields = [('bibcode', 'bibcode'), ('title', 'title'), ('author', 'author'),
                      ('aff', 'affiliation'), ('pub', 'journal'), ('volume', 'volume'),
                      ('date', 'pubdate'), ('page', 'page'), ('', 'lastpage'),
                      ('keyword', 'keywords'), ('', 'origin'), ('copyright', 'copyright'),
                      ('link', 'link'), ('url', 'url'), ('comment', 'comment'),
                      ('', 'score'), ('citation_count', 'citations'), ('abstract', 'abstract'),
                      ('doi', 'DOI'), ('pub_raw', 'eprintid')]
        elif (exportFormat == EXPORT_FORMAT_DUBLIN_XML):
            fields = [('bibcode', 'dc:identifier'), ('title', 'dc:title'), ('author', 'dc:creator'),
                      ('pub_raw', 'dc:source'), ('date', 'dc:date'), ('keyword', 'dc:subject'),
                      ('copyright', 'dc:rights'), ('url', 'dc:relation'), ('abstract', 'dc:description'),
                      ('doi', 'dc:identifier')]
        else:
            fields = []
        return OrderedDict(fields)

    # add the value into the return structure, only if a value was defined in Solr
    def __addIn(self, parent, field, value):
        if (len(value) > 0):
            ET.SubElement(parent, field).text = value

    # for each document from Solr, get the fields, and format them accordingly for Dublin format
    def __getDocDublinXML(self, index, parent):
        aDoc = self.fromSolr['response'].get('docs')[index]
        fields = self.__getFields(EXPORT_FORMAT_DUBLIN_XML)
        record = ET.SubElement(parent, "record")
        for field in fields:
            if (field == 'bibcode') or (field == 'copyright'):
                self.__addIn(record, fields[field], aDoc.get(field, ''))
            elif (field == 'title') or (field == 'doi'):
                self.__addIn(record, fields[field], ''.join(aDoc.get(field, '')))
            elif (field == 'author'):
                self.__addAuthorList(aDoc, record, fields[field])
            elif (field == 'pub_raw'):
                self.__addPubRaw(aDoc, record, fields[field], EXPORT_FORMAT_DUBLIN_XML)
            elif (field == 'date'):
                self.__addIn(record, fields[field], self.__formatDate(aDoc.get(field, ''), EXPORT_FORMAT_DUBLIN_XML))
            elif (field == 'keyword'):
                self.__addKeywords(aDoc, record, EXPORT_FORMAT_DUBLIN_XML)
            elif (field == 'url'):
                self.__addIn(record, fields[field], current_app.config.get('EXPORT_SERVICE_BBB_PATH') + '/' + aDoc.get('bibcode', ''))
            elif (field == 'abstract'):
                self.__addIn(record, fields[field], self.__formatLineWrapped(aDoc.get(field, '')))

    # for each document from Solr, get the fields, and format them accordingly for Reference format
    def __getDocReferenceXML(self, index, parent, includeAbs):
        aDoc = self.fromSolr['response'].get('docs')[index]
        fields = self.__getFields(EXPORT_FORMAT_REF_XML)
        record = ET.SubElement(parent, "record")
        for field in fields:
            if (field == 'bibcode') or (field == 'pub') or (field == 'volume') or \
                    (field == 'copyright') or (field == 'eprintid'):
                self.__addIn(record, fields[field], aDoc.get(field, ''))
            elif (field == 'title') or (field == 'page') or (field == 'doi'):
                self.__addIn(record, fields[field], ''.join(aDoc.get(field, '')))
            elif (field == 'author'):
                self.__addAuthorList(aDoc, record, fields[field])
            elif (field == 'aff'):
                self.__addAffiliationList(aDoc, record, fields[field])
            elif (field == 'date'):
                self.__addIn(record, fields[field], self.__formatDate(aDoc.get(field, ''), EXPORT_FORMAT_REF_XML))
            elif (field == 'pub_raw'):
                self.__addPubRaw(aDoc, record, fields[field], EXPORT_FORMAT_REF_XML)
            elif (field == 'keyword'):
                self.__addKeywords(aDoc, record, EXPORT_FORMAT_REF_XML)
            elif (field == 'url'):
                self.__addIn(record, fields[field], current_app.config.get('EXPORT_SERVICE_BBB_PATH') + '/' + aDoc.get('bibcode', ''))
            elif (field == 'citation_count'):
                self.__addIn(record, fields[field], str(aDoc.get(field, '')))
            elif (field == 'abstract') and (includeAbs):
                self.__addIn(record, fields[field], self.__formatLineWrapped(aDoc.get(field, '')))
            elif (field == 'link'):
                self.__addDocLinks(aDoc, record)

    # setup the outer xml structure
    def __getXML(self, exportFormat, includeAsb=False):
        if (self.status == 0):
            records = ET.Element("records")
            attribs = OrderedDict(current_app.config.get('EXPORT_SERVICE_RECORDS_SET_XML'))
            for attrib in attribs:
                records.set(attrib, attribs[attrib])
            records.set('retrieved', str(self.getNumDocs()))
            if (exportFormat == EXPORT_FORMAT_REF_XML):
                for index in range(self.getNumDocs()):
                    self.__getDocReferenceXML(index, records, includeAsb)
            elif (exportFormat == EXPORT_FORMAT_DUBLIN_XML):
                for index in range(self.getNumDocs()):
                    self.__getDocDublinXML(index, records)
            formatXML = ET.tostring(records, encoding='utf8', method='xml')
            formatXML = ('>\n<'.join(formatXML.split('><')))
            formatXML = formatXML.replace('</record>', '</record>\n')
            return formatXML
        return ''

    def getReferenceXML(self, includeAsb=False):
        return self.__getXML(EXPORT_FORMAT_REF_XML, includeAsb)

    def getDublinXML(self):
        return self.__getXML(EXPORT_FORMAT_DUBLIN_XML)

