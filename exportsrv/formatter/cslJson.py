#!/usr/bin/env python
#  -*- coding: utf-8 -*-


# This class accepts JSON object created by Solr and reformats it
# for the CSL processor. To use
#    jsonForCSL = CSLJson(jsonFromSolr).get()
# For custom formatting we only need the Author section filled, hence
# use
#    jsonForCSL = CSLJson(jsonFromSolr).get_author()

class CSLJson:
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


    def __get_cls_author_list(self, a_doc):
        """
        format authors
        
        :param a_doc: 
        :return: 
        """
        author_list = []
        for author in a_doc['author']:
            author_parts = author.split(', ')
            oneAuthor = {}
            oneAuthor['family'] = author_parts[0]
            if (len(author_parts) >= 2):
                oneAuthor['given'] = author_parts[1]
            author_list.append(oneAuthor)
        return author_list


    def __get_doc_type(self, solr_type):
        """
        convert document type from solr to csl
        
        :param solr_type: 
        :return: 
        """
        fields = {'article': 'article-journal', 'book': 'book', 'inbook': 'chapter',
                  'proceedings': 'paper-conference', 'inproceedings': 'paper-conference',
                  'abstract': 'article', 'misc': 'article-journal', 'eprint': 'article',
                  'talk':'paper-conference','software':'article','proposal':'paper-conference',
                  'pressrelease':'paper-conference', 'circular':'article', 'newsletter':'article',
                  'catalog':'article','phdthesis':'thesis','mastersthesis':'thesis',
                  'techreport':'report', 'intechreport':'report'}
        return fields.get(solr_type, '')


    def __get_doc_json_author(self, index):
        """
        get a JSON code for one document fill in only Author section
        this is used for custom formatting
        
        :param index: 
        :return: 
        """
        a_doc = self.from_solr['response'].get('docs')[index]
        data = {}
        data['id'] = 'ITEM-{0}'.format(index + 1)
        data['author'] = self.__get_cls_author_list(a_doc)
        data['type'] = self.__get_doc_type(a_doc.get('doctype', ''))
        return data


    def __get_doc_json(self, index):
        """
        get a JSON code for one document
        
        :param index: 
        :return: 
        """
        a_doc = self.from_solr['response'].get('docs')[index]
        data = {}
        data['id'] = 'ITEM-{0}'.format(index + 1)
        data['issued'] = ({'date-parts': [[int(a_doc['year'])]]})
        data['title'] = ''.join(a_doc.get('title', ''))
        data['author'] = self.__get_cls_author_list(a_doc)
        data['container-title'] = a_doc.get('pub', '')
        data['container-title-short'] = ''
        data['volume'] = a_doc.get('volume', '')
        data['issue'] = a_doc.get('issue', '')
        data['page'] = ''.join(a_doc.get('page', ''))
        data['type'] = self.__get_doc_type(a_doc.get('doctype', ''))
        data['locator'] = a_doc.get('bibcode')
        data['genre'] = str(a_doc.get('bibcode')[4:13]).strip('.')
        return data


    def get_author(self):
        """
        returns JSON code that has authors only

        :return:
        """
        csl_list = []
        if (self.status == 0):
            for index in range(self.get_num_docs()):
                csl_list.append(self.__get_doc_json_author(index))
        return csl_list


    def get(self):
        """
        returns JSON code that includes all the fields to build full citation and bibliography

        :return:
        """
        csl_list = []
        if (self.status == 0):
            for index in range(self.get_num_docs()):
                csl_list.append(self.__get_doc_json(index))
        return csl_list
