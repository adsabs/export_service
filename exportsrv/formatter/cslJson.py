# -*- coding: utf-8 -*-

from exportsrv.formatter.format import Format

# This class accepts JSON object created by Solr and reformats it
# for the CSL processor. To use
#    jsonForCSL = CSLJson(jsonFromSolr).get()
# For custom formatting we only need the Author section filled, hence
# use
#    jsonForCSL = CSLJson(jsonFromSolr).get_author()

class CSLJson(Format):

    def __get_cls_author_editor_list(self, a_doc, field='author'):
        """
        format authors/editors
        
        :param a_doc: 
        :return: 
        """
        author_list = []
        if field in a_doc:
            for author in a_doc[field]:
                author_parts = author.split(', ')
                oneAuthor = {}
                oneAuthor['family'] = author_parts[0]
                if (len(author_parts) >= 2):
                    oneAuthor['given'] = author_parts[1]
                author_list.append(oneAuthor)
        # only for author, if no author list available, include placeholder
        if len(author_list) == 0 and field == 'author':
            author_list.append({'family':'No author'})
        return author_list


    def __get_doc_type(self, doc_type):
        """
        convert document type from solr to csl
        
        :param doc_type: 
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
                  'dataset':'software','instrument':'software','service':'software'}
        return fields.get(doc_type, '')


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
        data['author'] = self.__get_cls_author_editor_list(a_doc)
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
        data['author'] = self.__get_cls_author_editor_list(a_doc, field='author')
        editor = self.__get_cls_author_editor_list(a_doc, field='editor')
        if editor:
            data['editor'] = editor
        data['container-title'] = self.__get_doc_pub(a_doc)
        data['container-title-short'] = ''
        data['volume'] = a_doc.get('volume', '')
        data['issue'] = a_doc.get('issue', '')
        data['series'] = a_doc.get('series', '')
        # both eid and page go into the page field in solr
        page = ''.join(a_doc.get('page', ''))
        eid = a_doc.get('eid', '')
        # if there is a page_range, assign it to page, only needed for icarus and ieee
        # if no page range, assign page here, but not eid
        data['page'] = a_doc.get('page_range', page if page != eid else '')
        # assign page to page-first, again not eid
        # all formats except icarus and ieee only display first page
        data['page-first'] = page if page != eid else ''
        # now save eid in number, so this page, page-first contain page only, not eid
        # and number contains eid
        data['number'] = eid
        data['type'] = self.__get_doc_type(a_doc.get('doctype', ''))
        data['locator'] = a_doc.get('bibcode')
        data['genre'] = str(a_doc.get('bibcode')[4:13]).strip('.')
        data['publisher'] = a_doc.get('publisher', '')
        # to fill the school field for thesis types
        if a_doc.get('doctype') in ['phdthesis', 'mastersthesis']:
            data['publisher-place'] = ''.join(a_doc.get('aff', []))
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
        if data['type'] == 'software':
            if len(data['DOI']) == 0 and len(eid) > 0:
                data['DOI'] = eid
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
