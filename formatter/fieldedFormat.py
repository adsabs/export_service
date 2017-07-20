#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from datetime import datetime
from flask import current_app
from textwrap import fill
from itertools import product
from string import ascii_uppercase

import re

# Fielded (formerly known as tagged)
EXPORT_FORMAT_ADS = 'ADS'
EXPORT_FORMAT_ENDNOTE = 'EndNote'
EXPORT_FORMAT_PROCITE = 'ProCite'
EXPORT_FORMAT_REFMAN = 'Refman'
EXPORT_FORMAT_REFWORKS = 'RefWorks'
EXPORT_FORMAT_MEDLARS = 'MEDLARS'

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

    # from solr to each fielded document type
    def __getDocType(self, solrType, exportFormat):
        fields = {}
        if (exportFormat == EXPORT_FORMAT_ENDNOTE):
            fields = {'article': 'Journal Article', 'book': 'Book', 'inbook': 'Book Section',
                      'proceedings': 'Journal Article', 'inproceedings': 'Conference Proceedings',
                      'abstract': 'Conference Paper', 'misc': 'Journal Article', 'eprint': 'Electronic Article',
                      'talk': 'Conference Paper', 'software':'Miscellaneous', 'proposal':'Miscellaneous',
                      'pressrelease':'Journal Article', 'circular':'Journal Article', 'newsletter':'Journal Article',
                      'catalog':'Journal Article', 'phdthesis':'Thesis', 'mastersthesis':'Thesis',
                      'techreport':'Report', 'intechreport':'Report'}
        elif (exportFormat == EXPORT_FORMAT_PROCITE):
            fields = {'article': 'Journal', 'book': 'Book, Whole', 'inbook': 'Book Chapter',
                      'proceedings': 'Journal', 'inproceedings': 'Conference',
                      'abstract': 'Conference', 'misc': 'Journal', 'eprint': 'Preprint',
                      'talk': 'Conference', 'software':'Miscellaneous', 'proposal':'Miscellaneous',
                      'pressrelease':'Journal', 'circular':'Journal', 'newsletter':'Journal',
                      'catalog':'Journal', 'phdthesis':'Thesis/Dissertation', 'mastersthesis':'Thesis/Dissertation',
                      'techreport':'Report', 'intechreport':'Report'}
        elif (exportFormat == EXPORT_FORMAT_REFMAN):
            fields = {'article': 'JOUR', 'book': 'BOOK', 'inbook': 'CHAP',
                      'proceedings': 'JOUR', 'inproceedings': 'CONF',
                      'abstract': 'CONF', 'misc': 'JOUR', 'eprint': 'Preprint',
                      'talk': 'CONF', 'software':'MISC', 'proposal':'MISC',
                      'pressrelease':'JOUR', 'circular':'JOUR', 'newsletter':'JOUR',
                      'catalog':'JOUR', 'phdthesis':'Thesis/Dissertation', 'mastersthesis':'Thesis/Dissertation',
                      'techreport':'RPRT', 'intechreport':'RPRT'}
        elif (exportFormat == EXPORT_FORMAT_REFWORKS):
            fields = {'article': 'Journal', 'book': 'Book, Whole', 'inbook': 'Book, Chapter',
                      'proceedings': 'Journal', 'inproceedings': 'Conference Proceeding',
                      'abstract': 'Conference Proceeding', 'misc': 'Journal', 'eprint': 'Preprint',
                      'talk': 'Conference Proceeding', 'software':'Generic', 'proposal':'Generic',
                      'pressrelease':'Journal', 'circular':'Journal', 'newsletter':'Journal',
                      'catalog':'Journal', 'phdthesis':'Thesis/Dissertation', 'mastersthesis':'Thesis/Dissertation',
                      'techreport':'Report', 'intechreport':'Report'}
        elif (exportFormat == EXPORT_FORMAT_MEDLARS):
            fields = {'article': 'Journal Article', 'book': 'Book', 'inbook': 'Book Chapter',
                      'proceedings': 'Journal Article', 'inproceedings': 'Conference',
                      'abstract': 'Conference', 'misc': 'Journal Article', 'eprint': 'Preprint',
                      'talk': 'Conference', 'software':'Miscellaneous', 'proposal':'Miscellaneous',
                      'pressrelease':'Journal Article', 'circular':'Journal Article', 'newsletter':'Journal Article',
                      'catalog':'Journal Article', 'phdthesis':'Thesis', 'mastersthesis':'Thesis',
                      'techreport':'Report', 'intechreport':'Report'}


        return fields.get(solrType, '')

    def __formatDate(self, solrDate, exportFormat):
        # solrDate has the format 2017-12-01T00:00:00Z
        dateTime = datetime.strptime(solrDate, '%Y-%m-%dT%H:%M:%SZ')
        formats = {EXPORT_FORMAT_ADS: '%m/%Y', EXPORT_FORMAT_ENDNOTE: '%B %d, %Y',
                   EXPORT_FORMAT_PROCITE: '%Y/%m/X%d', EXPORT_FORMAT_REFMAN: '%Y/%m/X%d',
                   EXPORT_FORMAT_REFWORKS: '%Y/%m/X%d', EXPORT_FORMAT_MEDLARS: '%Y %b %d'}
        return dateTime.strftime(formats[exportFormat]).replace('X0', 'X').replace('X', '')

    def __formatLineWrapped(self, text):
        return fill(text, width=72)

    # from solr to each fielded types' tags
    def __getTags(self, exportFormat):
        if (exportFormat == EXPORT_FORMAT_ADS):
            return (OrderedDict([('bibcode', '%R'), ('title', '%T'), ('author', '%A'),
                                 ('aff', '%F'), ('pub', '%J'), ('volume', '%V'),
                                 ('date', '%D'), ('page', '%P'), ('keyword', '%K'),
                                 ('', '%G'), ('copyright', '%C'), ('', '%I'),
                                 ('url', '%U'), ('comment', '%X'), ('', '%S'),
                                 ('abstract', '%B'), ('doi', '%Y DOI:')]))
        if (exportFormat == EXPORT_FORMAT_ENDNOTE):
            return (OrderedDict([('doctype', '%0'), ('title', '%T'), ('author', '%A'),
                                 ('aff', '%+'), ('pub', '%B'), ('volume', '%V'),
                                 ('year', '%D'), ('date', '%8'), ('keyword', '%K'),
                                 ('url', '%U'), ('comment', '%Z'), ('abstract', '%X'),
                                 ('doi', '%3')]))
        if (exportFormat == EXPORT_FORMAT_PROCITE):
            return (OrderedDict([('doctype', 'TY  -'), ('title', 'T1  -'), ('author', 'A1  -'),
                                 ('pub', 'JO  -'), ('volume', 'VL  -'), ('date', 'Y1  -'),
                                 ('page', 'SP  -'), ('keyword', 'KW  -'), ('url', 'UR  -'),
                                 ('abstract', 'N2  -'), ('doi', 'DO  -'), ('endRecord', 'ER  -')]))
        if (exportFormat == EXPORT_FORMAT_REFMAN):
            return (OrderedDict([('doctype', 'TY  -'), ('title', 'T1  -'), ('author', 'A1  -'),
                                 ('pub', 'JO  -'), ('volume', 'VL  -'), ('date', 'Y1  -'),
                                 ('page', 'SP  -'), ('keyword', 'KW  -'), ('url', 'UR  -'),
                                 ('abstract', 'N2  -'), ('doi', 'DO  -'), ('endRecord', 'ER  -')]))
        if (exportFormat == EXPORT_FORMAT_REFWORKS):
            return (OrderedDict([('doctype', 'RT'), ('title', 'T1'), ('author', 'A1'),
                                 ('aff', 'AD'), ('pub', 'JF'), ('volume', 'VO'),
                                 ('year', 'YR'), ('date', 'FD'), ('page', 'SP'),
                                 ('keyword', 'K1'), ('url', 'LK'), ('comment', 'NO'),
                                 ('abstract', 'AB'), ('doi', 'DO DOI:')]))
        if (exportFormat == EXPORT_FORMAT_MEDLARS):
            return (OrderedDict([('doctype', 'PT  -'), ('title', 'TI  -'), ('author', 'AU  -'),
                                 ('pub', 'TA  -'), ('pub_raw', 'SO  -'), ('volume', 'VI  -'),
                                 ('date', 'DP  -'), ('url', '4099-'), ('abstract', 'AB  -')]))

    # format authors
    def __addAuthorList(self, aDoc, exportFormat, tag):
        if 'author' not in aDoc:
            return ''

        if (exportFormat == EXPORT_FORMAT_ADS):
            separator = ';'
            result = tag + ' '
            for author in aDoc['author']:
                result += author + separator
            # do not need the last separator
            if (len(result) > len(separator)):
                result = result[:-len(separator)]
            return self.__formatLineWrapped(result) + '\n'

        if (exportFormat == EXPORT_FORMAT_ENDNOTE) or (exportFormat == EXPORT_FORMAT_PROCITE) or \
            (exportFormat == EXPORT_FORMAT_REFMAN) or (exportFormat == EXPORT_FORMAT_REFWORKS) or \
            (exportFormat == EXPORT_FORMAT_MEDLARS):
            separator = '\n'
            result = ''
            for author in aDoc['author']:
                result += tag + ' ' + author + separator
            # do not need the last separator
            if (len(result) > len(separator)):
                result = result[:-len(separator)]
            return result + '\n'

        return ''

    # format affiliation
    def __getAffiliationList(self, aDoc, exportFormat, tag):
        if ('aff') not in aDoc:
            return ''

        counter = [''.join(i) for i in product(ascii_uppercase, repeat=2)]
        separator = ', '

        if (len(tag) > 0):
            affiliationList = tag + ' '
        else:
            affiliationList = ''

        for affiliation, i in zip(aDoc['aff'], range(len(aDoc['aff']))):
            affiliationList += counter[i] + '(' + affiliation + ')' + separator
        # do not need the last separator
        if (len(affiliationList) > len(separator)):
            affiliationList = affiliationList[:-len(separator)]

        if (exportFormat == EXPORT_FORMAT_ADS):
            return self.__formatLineWrapped(affiliationList) + '\n'

        return affiliationList + '\n'

    # format keywords
    def __addKeywords(self, aDoc, exportFormat, tag):
        if 'keyword' not in aDoc:
            return ''

        separator = {EXPORT_FORMAT_ADS:', ', EXPORT_FORMAT_ENDNOTE:'; ', EXPORT_FORMAT_PROCITE:'/ ',
                     EXPORT_FORMAT_REFMAN:'\n', EXPORT_FORMAT_REFWORKS:'\n'}

        if (exportFormat == EXPORT_FORMAT_ADS) or (exportFormat == EXPORT_FORMAT_ENDNOTE) or (exportFormat == EXPORT_FORMAT_PROCITE):
            result = tag + ' '
            for keyword in aDoc['keyword']:
                result += keyword + separator[exportFormat]
            # do not need the last separator
            if (len(result) > len(separator[exportFormat])):
                result = result[:-len(separator[exportFormat])]
            return self.__formatLineWrapped(result) + '\n'

        if (exportFormat == EXPORT_FORMAT_REFMAN) or (exportFormat == EXPORT_FORMAT_REFWORKS):
            result = ''
            for keyword in aDoc['keyword']:
                result += tag + ' ' + keyword + separator[exportFormat]
            # do not need the last separator
            if (len(result) > len(separator[exportFormat])):
                result = result[:-len(separator[exportFormat])]
            return result + '\n'

        return ''

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

    # add the value into the return structure, only if a value was defined in Solr
    def __addIn(self, field, value):
        if (((isinstance(value, unicode)) or (isinstance(value, str))) and (len(value) > 0)) or \
           ((isinstance(value, int)) and (value is not None)):
            return field + ' ' + value + '\n'
        return ''

    def __getDoc(self, index, fields, exportFormat):
        result = ''
        aDoc = self.fromSolr['response'].get('docs')[index]
        for field in fields:
            if (field == 'title') or (field == 'page') or (field == 'doi'):
                result += self.__addIn(fields[field], ''.join(aDoc.get(field, '')))
            elif (field == 'author'):
                result += self.__addAuthorList(aDoc, exportFormat, fields[field])
            elif (field == 'doctype'):
                result += self.__addIn(fields[field], self.__getDocType(aDoc.get(field, ''), exportFormat))
            elif (field == 'date'):
                result += self.__addIn(fields[field], self.__formatDate(aDoc.get(field, ''), exportFormat))
            elif (field == 'abstract'):
                result += self.__addIn(fields[field], self.__formatLineWrapped(aDoc.get(field, '')))
            elif (field == 'aff'):
                result += self.__getAffiliationList(aDoc, exportFormat, fields[field])
            elif (field == 'keyword'):
                result += self.__addKeywords(aDoc, exportFormat, fields[field])
            elif (field == 'comment'):
                result += self.__addIn(fields[field], self.__formatLineWrapped(''.join(aDoc.get(field, ''))))
            elif (field == 'url'):
                result += self.__addIn(fields[field], current_app.config['EXPORT_SERVICE_BBB_PATH'] + '/' + aDoc.get('bibcode', ''))
            elif (field == 'endRecord'):
                result += self.__addIn(fields[field], ' ')
            elif (field == 'pub_raw'):
                result += self.__addIn(fields[field], self.__addCleanPubRaw(aDoc))
            else:
                result += self.__addIn(fields[field], aDoc.get(field, ''))

        # line feed once the doc is complete
        return result + '\n\n'

    # for each document from Solr, get the fields, and format them accordingly
    def __getFielded(self, exportFormat):
        results = ''
        if (self.status == 0):
            fields = self.__getTags(exportFormat)
            numDocs = self.getNumDocs()
            results = ('\n\nRetrieved {} abstracts, starting with number 1.\n\n\n'.format(numDocs))
            for index in range(numDocs):
                results += self.__getDoc(index, fields, exportFormat)
        return results

    def getADSFielded(self):
        return self.__getFielded(EXPORT_FORMAT_ADS)

    def getEndNoteFielded(self):
        return self.__getFielded(EXPORT_FORMAT_ENDNOTE)

    def getProCiteFielded(self):
        return self.__getFielded(EXPORT_FORMAT_PROCITE)

    def getRefmanFielded(self):
        return self.__getFielded(EXPORT_FORMAT_REFMAN)

    def getRefWorksFielded(self):
        return self.__getFielded(EXPORT_FORMAT_REFWORKS)

    def getMEDLARSFielded(self):
        return self.__getFielded(EXPORT_FORMAT_MEDLARS)

