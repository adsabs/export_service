#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from datetime import datetime
from flask import current_app
from textwrap import fill
from itertools import product
from string import ascii_uppercase
import re

from toLaTex import encodeLaTex, encodeLaTexAuthor

# This class accepts JSON object created by Solr and reformats it
# for the BibTex Export formats we are supporting
# 1- To get Reference BibTex without Abstract use
#    referenceXML = BibTexFormat(jsonFromSolr).getReferenceBibTex()
# 2- To get Reference BibTex with Abstract use
#    referenceXML = BibTexFormat(jsonFromSolr).getReferenceBibTex(True)

class BibTexFormat:
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

    # from solr to BibTex document type
    def __getDocType(self, solrType):
        fields = {'article':'@ARTICLE', 'circular':'@ARTICLE', 'newsletter':'@ARTICLE',
                  'eprint':'@ARTICLE', 'catalog':'@ARTICLE',
                  'book':'@BOOK', 
                  'inbook':'@INBOOK',
                  'proceedings':'@PROCEEDINGS', 
                  'inproceedings':'@INPROCEEDINGS', 'abstract':'@INPROCEEDINGS', 'talk':'@INPROCEEDINGS', 
                  'misc':'@MISC', 'software':'@MISC','proposal':'@MISC', 'pressrelease':'@MISC',
                  'phdthesis':'@PHDTHESIS','mastersthesis':'@MASTERSTHESIS',
                  'techreport':'@TECHREPORT', 'intechreport':'@TECHREPORT'}
        return fields.get(solrType, '')

    def __formatDate(self, solrDate):
        # solrDate has the format 2017-12-01T00:00:00Z
        dateTime = datetime.strptime(solrDate, '%Y-%m-%dT%H:%M:%SZ')
        return dateTime.strftime('%b')

    def __formatLineWrapped(self, left, right, formatStyle):
        wrapped = fill(right, width=72, subsequent_indent=' ' * 8)
        return formatStyle.format(left, wrapped)

    # exported fields for various document types
    def __getFields(self, aDoc):
        docTypeBibTex = self.__getDocType(aDoc.get('doctype', ''))
        if (docTypeBibTex == '@ARTICLE'):
            fields = [('author', 'author'), ('title', 'title'), ('pub', 'journal'),
                      ('keyword', 'keywords'), ('year', 'year'), ('month', 'month'),
                      ('volume', 'volume'), ('eid', 'eid'), ('page', 'pages'),
                      ('abstract', 'abstract'), ('doi', 'doi'), ('bibcode', 'adsurl'),
                      ('adsnotes', 'adsnote')]
        elif (docTypeBibTex == '@BOOK'):
            fields = [('author', 'author'), ('title', 'title'), ('pub_raw', 'booktitle'),
                      ('year', 'year'), ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        elif (docTypeBibTex == '@INBOOK'):
            fields = [('author', 'author'), ('title', 'title'), ('keyword', 'keywords'),
                      ('pub_raw', 'booktitle'), ('year', 'year'), ('editor', 'editor'),
                      ('page', 'pages'), ('abstract', 'abstract'), ('doi', 'doi'),
                      ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        elif (docTypeBibTex == '@PROCEEDINGS'):
            fields = [('title', 'title'), ('keyword', 'keywords'), ('pub_raw', 'booktitle'),
                      ('year', 'year'), ('editor', 'editor'), ('series', 'series'),
                      ('volume', 'volume'), ('month', 'month'), ('doi', 'doi'),
                      ('abstract', 'abstract'), ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        elif (docTypeBibTex == '@INPROCEEDINGS'):
            fields = [('author', 'author'), ('title', 'title'), ('keyword', 'keywords'),
                      ('pub_raw', 'booktitle'), ('year', 'year'), ('editor', 'editor'),
                      ('series', 'series'), ('volume', 'volume'), ('month', 'month'),
                      ('eid', 'eid'), ('page', 'pages'), ('abstract', 'abstract'),
                      ('doi', 'doi'), ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        elif (docTypeBibTex == '@MISC'):
            fields = [('author', 'author'), ('title', 'title'), ('keyword', 'keywords'),
                      ('pub', 'howpublished'), ('year', 'year'), ('month', 'month'),
                      ('eid', 'eprint'), ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        elif (docTypeBibTex == '@PHDTHESIS') or (docTypeBibTex == '@MASTERSTHESIS'):
            fields = [('author', 'author'), ('title', 'title'), ('keyword', 'keywords'),
                      ('aff', 'school'), ('year', 'year'), ('month', 'month'),
                      ('bibcode', 'adsurl'),('adsnotes', 'adsnote')]
        elif (docTypeBibTex == '@TECHREPORT'):
            fields = [('author', 'author'), ('title', 'title'), ('pub', 'journal'),
                      ('keyword', 'keywords'), ('pub_raw', 'booktitle'), ('year', 'year'),
                      ('editor', 'editor'), ('month', 'month'), ('volume', 'volume'),
                      ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        else:
            fields = []
        return OrderedDict(fields)

    # format authors
    def __getAuthorList(self, aDoc):
        if 'author' not in aDoc:
            return ''
        andStr = ' and '
        authorList = ''
        regex = re.compile(r'([A-Z])\w*')
        for author in aDoc['author']:
            authorParts = author.split(', ')
            authorList += '{' + authorParts[0] + '}'
            if (len(authorParts) >= 2):
                authorList += ", " +  '. '.join(regex.findall(authorParts[1])) + '.' + andStr
        if (authorList.endswith(andStr)):
            authorList = authorList[:-len(andStr)]
        return encodeLaTexAuthor(authorList)

    # format affiliation
    def __getAffiliationList(self, aDoc):
        if ('aff') not in aDoc:
            return ''
        counter = [''.join(i) for i in product(ascii_uppercase, repeat=2)]
        separator = ', '
        affiliationList = ''
        addCount = not (aDoc.get('doctype', '') in ['phdthesis'])
        for affiliation, i in zip(aDoc['aff'], range(len(aDoc['aff']))):
            if (addCount):
                affiliationList += counter[i] + '(' + affiliation + ')' + separator
            else:
                affiliationList += affiliation + separator
        # do not need the last separator
        if (len(affiliationList) > len(separator)):
            affiliationList = affiliationList[:-len(separator)]
        return encodeLaTex(affiliationList)

    # format keywords
    def __addKeywords(self, aDoc):
        if 'keyword' not in aDoc:
            return ''
        return encodeLaTex(', '.join(aDoc.get('keyword', '')))

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
    def __addIn(self, field, value, outputFormat):
        if (((isinstance(value, unicode)) or (isinstance(value, str))) and (len(value) > 0)) or \
           ((isinstance(value, int)) and (value is not None)):
            return outputFormat.format(field, value) + ',\n'
        return ''

    # add the value into the return structure, only if a value was defined in Solr
    def __addInWrapped(self, field, value, outputFormat):
        if (len(value) > 0):
            return self.__formatLineWrapped(field, value, outputFormat) + ',\n'
        return ''

    # for each document from Solr, get the fields, and format them accordingly
    def __getDoc(self, index, includeAbs):
        formatStyleBracketQuotes = u'{0:>12} = "{{{1}}}"'
        formatStyleBracket = u'{0:>12} = {{{1}}}'
        formatStyle = u'{0:>12} = {1}'

        aDoc = self.fromSolr['response'].get('docs')[index]
        text = self.__getDocType(aDoc.get('doctype', '')) + '{' + aDoc.get('bibcode', '')  + ',\n'

        fields = self.__getFields(aDoc)
        for field in fields:
            if (field == 'author'):
                text += self.__addInWrapped(fields[field], self.__getAuthorList(aDoc), formatStyleBracket)
            elif (field == 'title'):
                text += self.__addInWrapped(fields[field], encodeLaTex(''.join(aDoc.get(field, ''))), formatStyleBracketQuotes)
            elif (field == 'aff'):
                text += self.__addInWrapped(fields[field], self.__getAffiliationList(aDoc), formatStyleBracket)
            elif (field == 'pub_raw'):
                text += self.__addInWrapped(fields[field], self.__addCleanPubRaw(aDoc), formatStyleBracket)
            elif (field == 'pub') or (field == 'doi'):
                text += self.__addIn(fields[field], ''.join(aDoc.get(field, '')), formatStyleBracket)
            elif (field == 'keyword'):
                text += self.__addInWrapped(fields[field], self.__addKeywords(aDoc), formatStyleBracket)
            elif (field == 'year') or (field == 'volume'):
                text += self.__addIn(fields[field], int(aDoc.get(field, '')) if aDoc.get(field, '') else None, formatStyle)
            elif (field == 'month'):
                text += self.__addIn(fields[field], self.__formatDate(aDoc.get('date', '')), formatStyle)
            elif (field == 'abstract') and (includeAbs):
                text += self.__addInWrapped(fields[field], encodeLaTex(aDoc.get(field, '')), formatStyleBracketQuotes)
            elif (field == 'eid'):
                text += self.__addIn(fields[field], aDoc.get(field, ''), formatStyleBracket)
            elif (field == 'page'):
                text += self.__addIn(fields[field], ''.join(aDoc.get(field, '')), formatStyleBracket)
            elif (field == 'bibcode'):
                text += self.__addIn(fields[field], current_app.config['EXPORT_SERVICE_BBB_PATH'] + '/' + aDoc.get(field, ''), formatStyleBracket)
            elif (field == 'adsnotes'):
                text += self.__addIn(fields[field], current_app.config['EXPORT_SERVICE_ADS_NOTES'], formatStyleBracket)
        # remove the last comma,
        text = text[:-len(',\n')] + '\n'

        return text + '}\n\n'

    def get(self, includeAbs=False):
        refBibTex = ''
        if (self.status == 0):
            numDocs = self.getNumDocs()
            refBibTex = ('\n\nRetrieved {} abstracts, starting with number 1.\n\n\n'.format(numDocs))
            for index in range(numDocs):
                refBibTex += self.__getDoc(index, includeAbs)
        return refBibTex
