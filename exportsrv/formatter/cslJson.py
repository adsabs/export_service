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
        fields = {'article':'article', 'book':'book', 'inbook':'chapter',
                  'proceedings':'paper-conference', 'inproceedings':'paper-conference',
                  'misc':'report', 'circular':'report' ,'newsletter':'report',
                  'techreport':'report', 'intechreport':'report',
                  'abstract': 'article-journal', 'bookreview':'review-book',
                  'talk':'speech', 'software':'software', 'eprint':'manuscript',
                  'pressrelease':'entry', 'catalog':'entry',
                  'phdthesis':'thesis','mastersthesis':'thesis',
                  'proposal':'personal_communication', 'editorial':'personal_communication', 
                  'erratum':'personal_communication', 'obituary':'personal_communication',
                  'dataset':'software'}
        return fields.get(solr_type, '')


    def __get_doc_pub(self, a_doc):
        """
        some formats require pub_raw some pub, all is assigned into one variable for csl

        :param a_doc:
        :return:
        """
        if a_doc.get('doctype', '') in ['techreport', 'misc', 'newsletter', 'book']:
            return a_doc.get('pub_raw', '')
        return a_doc.get('pub', '')


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
        data['container-title'] = self.__get_doc_pub(a_doc)
        data['container-title-short'] = ''
        data['volume'] = a_doc.get('volume', '')
        data['issue'] = a_doc.get('issue', '')
        # both eid and page go into the page field in solr
        # eid can be of the form E1.7-23-18 which crashes csl having two dashes
        # since it parses it and tries to determine the first page and the last page
        # before and after the dash, hence accepts only one dash in the page field
        # renaming the page to eid produces tones of warning
        # so instead of eid went with PMCID that is a known identifier
        data['PMCID'] = ''.join(a_doc.get('page', ''))
        # lets keep the data in the page as well, even though it is not being used
        if data['PMCID'].count('-') > 1:
            data['page-first'] = data['PMCID'].replace('-', ' ')
        else:
            data['page-first'] = data['PMCID']
        # if there is a page_range, assign it to page, only needed for icarus
        data['page'] = a_doc.get('page_range', '')
        data['type'] = self.__get_doc_type(a_doc.get('doctype', ''))
        data['locator'] = a_doc.get('bibcode')
        data['genre'] = str(a_doc.get('bibcode')[4:13]).strip('.')
        data['publisher'] = a_doc.get('publisher', '')
        data['version'] = a_doc.get('version', '')
        data['DOI'] = ''.join(a_doc.get('doi', ''))
        if len(data['DOI']) > 0:
            # attach doi: here since, please see little further down, if doctype is software
            # and there is no doi, if there is eid then eid is going to be displayed in the same location
            # obviously, eid should not be prefixed with doi
            data['DOI'] = 'doi:' + data['DOI']
        # 18/9/20202 as per Alberto displaying doi, if available, for all doctypes and all cls formats
        # from edwin: if there is no volume and page,
        # and there is DOI, display DOI.
        # hence DOI is assigned to volume, to be displayed in the same location, only if this is not software
        # if len(data['volume']) == 0 and len(data['page']) == 0 and len(data['DOI']) > 0 and data['type'] != 'software':
        #     data['volume'] = 'doi:' + data['DOI']
        # if the record is software,
        # according to alberto we are either displaying DOI or eid
        # \bibitem[...]{bibcode}  {authors} {year}, {title}, {version}, {publisher}, (doi:{doi}|{eid})
        # there is no best variable to assign this either of these to, so go with 'keyword' for now
        # 1/31/2024 adding dataset doctype as per Edwin
        if data['type'] in ['software', 'dataset']:
            if len(data['DOI']) == 0 and len(a_doc.get('eid', '')) > 0:
                data['DOI'] = a_doc.get('eid', '')
            else:
                data['DOI'] = ''
        data['bibstem'] = a_doc.get('bibstem', [''])
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
