#!/usr/bin/env python
#  -*- coding: utf-8 -*-


# This class accepts JSON object created by Solr and reformats it
# for the CSL processor. To use
#    jsonForCSL = CSLJson(jsonFromSolr).get()
# For custom formatting we only need the Author section filled, hence
# use
#    jsonForCSL = CSLJson(jsonFromSolr).getAuthor()

class CSLJson:
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
    # format authors
    def __getCSLAuthorList(self, aDoc):
        authorList = []
        for author in aDoc['author']:
            authorParts = author.split(', ')
            oneAuthor = {}
            oneAuthor['family'] = authorParts[0]
            if (len(authorParts) >= 2):
                oneAuthor['given'] = authorParts[1]
            authorList.append(oneAuthor)
        return authorList

    # convert document type from solr to csl
    def __getDocType(self, solrType):
        fields = {'article': 'article-journal', 'book': 'book', 'inbook': 'chapter',
                  'proceedings': 'paper-conference', 'inproceedings': 'paper-conference',
                  'abstract': 'article', 'misc': 'article-journal', 'eprint': 'article',
                  'talk':'paper-conference','software':'article','proposal':'paper-conference',
                  'pressrelease':'paper-conference', 'circular':'article', 'newsletter':'article',
                  'catalog':'article','phdthesis':'thesis','mastersthesis':'thesis',
                  'techreport':'report', 'intechreport':'report'}
        return fields.get(solrType, '')

    # get a JSON code for one document fill in only Author section
    # this is used for custom formatting
    def __getDocJSONAuthor(self, index):
        aDoc = self.fromSolr['response'].get('docs')[index]
        data = {}
        data['id'] = 'ITEM-{0}'.format(index + 1)
        data['author'] = self.__getCSLAuthorList(aDoc)
        data['type'] = self.__getDocType(aDoc.get('doctype', ''))
        return data

    # get a JSON code for one document
    def __getDocJSON(self, index):
        aDoc = self.fromSolr['response'].get('docs')[index]
        data = {}
        data['id'] = 'ITEM-{0}'.format(index + 1)
        data['issued'] = ({'date-parts': [[int(aDoc['year'])]]})
        data['title'] = ''.join(aDoc.get('title', ''))
        data['author'] = self.__getCSLAuthorList(aDoc)
        data['container-title'] = aDoc.get('pub', '')
        data['container-title-short'] = ''
        data['volume'] = aDoc.get('volume', '')
        data['issue'] = aDoc.get('issue', '')
        data['page'] = ''.join(aDoc.get('page', ''))
        data['type'] = self.__getDocType(aDoc.get('doctype', ''))
        data['locator'] = aDoc.get('bibcode')
        data['genre'] = str(aDoc.get('bibcode')[4:13]).strip('.')
        return data

    # return the JSON code that has authors only
    def getAuthor(self):
        cslList = []
        if (self.status == 0):
            for index in range(self.getNumDocs()):
                cslList.append(self.__getDocJSONAuthor(index))
        return cslList

    # return the JSON code that includes all the fields to build full citation and bibliography
    def get(self):
        cslList = []
        if (self.status == 0):
            for index in range(self.getNumDocs()):
                cslList.append(self.__getDocJSON(index))
        return cslList
