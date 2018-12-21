# -*- coding: utf-8 -*-

from exportsrv.formatter.format import Format

# This class accepts JSON object created by Solr and reformats it
# for the CSL processor. To use
#    jsonForCSL = CSLJson(jsonFromSolr).get()
# For custom formatting we only need the Author section filled, hence
# use
#    jsonForCSL = CSLJson(jsonFromSolr).get_author()

class CSLJson(Format):

    def __get_cls_author_list(self, a_doc):
        """
        format authors
        
        :param a_doc: 
        :return: 
        """
        author_list = []
        if 'author' in a_doc:
            for author in a_doc['author']:
                author_parts = author.split(', ')
                oneAuthor = {}
                oneAuthor['family'] = author_parts[0]
                if (len(author_parts) >= 2):
                    oneAuthor['given'] = author_parts[1]
                author_list.append(oneAuthor)
        if len(author_list) == 0:
            author_list.append({'family':'No author'})
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
                  'talk':'paper-conference','software':'software','proposal':'paper-conference',
                  'pressrelease':'paper-conference', 'circular':'article', 'newsletter':'article',
                  'catalog':'article','phdthesis':'thesis','mastersthesis':'thesis',
                  'techreport':'report', 'intechreport':'report',
                  'bookreview': 'article-journal', 'erratum': 'article-journal', 'obituary': 'article-journal'}
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
        data['publisher'] = a_doc.get('publisher', '')
        data['version'] = a_doc.get('version', '')
        data['DOI'] = ''.join(a_doc.get('doi', ''))
        # for the aastex format if the record is software,
        # according to alberto we are either displaying DOI or eid
        # \bibitem[...]{bibcode}  {authors} {year}, {title}, {version}, {publisher}, (doi:{doi}|{eid})
        # there is no best variable to assign this either of these to, so go with 'keyword' for now
        if len(data['DOI']) > 0:
            data['keyword'] = 'doi:' + data['DOI']
        elif len(a_doc.get('eid', '')) > 0:
            data['keyword'] = a_doc.get('eid', '')
        else:
            data['keyword'] = ''
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
