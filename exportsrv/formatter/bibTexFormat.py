# -*- coding: utf-8 -*-

from collections import OrderedDict
from datetime import datetime
from flask import current_app
from textwrap import fill
import re
import json

from exportsrv.formatter.toLaTex import encode_laTex, encode_laTex_author
from exportsrv.formatter.format import Format
from exportsrv.utils import get_eprint
from exportsrv.formatter.strftime import strftime

# This class accepts JSON object created by Solr and reformats it
# for the BibTex Export formats we are supporting
# 1- To get Reference BibTex without Abstract use
#    referenceXML = BibTexFormat(jsonFromSolr).getReferenceBibTex()
# 2- To get Reference BibTex with Abstract use
#    referenceXML = BibTexFormat(jsonFromSolr).getReferenceBibTex(True)

class BibTexFormat(Format):

    REGEX_AUTHOR = re.compile(r'([A-Z])\w*')
    REGEX_PUB_RAW = dict([
        (re.compile(r"(\;?\s*\<ALTJOURNAL\>.*\</ALTJOURNAL\>\s*)"), r""),  # remove these
        (re.compile(r"(\;?\s*\<CONF_METADATA\>.*\<CONF_METADATA\>\s*)"), r""),
        (re.compile(r"(?:\<ISBN\>)(.*)(?:\</ISBN\>)"), r"\1"),  # get value inside the tag for these
        (re.compile(r"(?:\<NUMPAGES\>)(.*)(?:</NUMPAGES>)"), r"\1"),
    ])
    REGEX_KEY = re.compile(
        r'''(                   # start of capture group 1
            %                   # literal "%"
            (?:                 # first option
            (?:\d+|\*)?         # width
            [HqRY]              # type
            )
        )''', flags=re.X
    )

    def __init__(self, from_solr, keyformat):
        """

        :param keyformat:
        """
        Format.__init__(self, from_solr)
        self.keyformat = keyformat
        self.parsed_spec = []
        for m in self.REGEX_KEY.finditer(self.keyformat):
            self.parsed_spec.append(tuple((m.start(1), m.group(1), self.__get_solr_field(m.group(1)))))

    def __get_solr_field(self, specifier):
        """
        from specifier to Solr fields

        :param specifier:
        :return:
        """
        fieldDict = {
            'H': 'author',
            'q': 'pub',
            'R': 'bibcode',
            'Y': 'year'
        }
        specifier = ''.join(re.findall(r'([HqRY])', specifier))
        return fieldDict.get(specifier, '')


    def __get_doc_type(self, solr_type):
        """
        convert from solr to BibTex document type

        :param solr_type:
        :return:
        """
        fields = {'article':'@ARTICLE', 'circular':'@ARTICLE', 'newsletter':'@ARTICLE',
                  'bookreview':'@ARTICLE', 'erratum':'@ARTICLE', 'obituary':'@ARTICLE',
                  'eprint':'@ARTICLE', 'catalog':'@ARTICLE',
                  'book':'@BOOK', 
                  'inbook':'@INBOOK',
                  'proceedings':'@PROCEEDINGS', 
                  'inproceedings':'@INPROCEEDINGS', 'abstract':'@INPROCEEDINGS',
                  'misc':'@MISC', 'software':'@MISC','proposal':'@MISC', 'pressrelease':'@MISC',
                  'talk':'@MISC',
                  'phdthesis':'@PHDTHESIS','mastersthesis':'@MASTERSTHESIS',
                  'techreport':'@TECHREPORT', 'intechreport':'@TECHREPORT'}
        return fields.get(solr_type, '')


    def __format_date(self, solr_date):
        """

        :param solr_date:
        :return:
        """
        # solr_date has the format 2017-12-01
        date_time = datetime.strptime(solr_date.replace('-00', '-01'), '%Y-%m-%d')
        return strftime(date_time, '%b')


    def __format_line_wrapped(self, left, right, format_style):
        """

        :param left:
        :param right:
        :param format_style:
        :return:
        """
        # for authors and editors break it on the `and` only
        if left in ['author', 'editor']:
            wrapped = "\n        ".join(re.findall(r'.{1,72}(?:and|$)', right))
        else:
            wrapped = fill(right, width=72, subsequent_indent=' ' * 8)
        return format_style.format(left, wrapped)


    def __get_fields(self, a_doc):
        """
        exported fields for various document types

        :param a_doc:
        :return:
        """
        doc_type_bibtex = self.__get_doc_type(a_doc.get('doctype', ''))
        if (doc_type_bibtex == '@ARTICLE'):
            fields = [('author', 'author'), ('title', 'title'), ('pub', 'journal'),
                      ('keyword', 'keywords'), ('year', 'year'), ('month', 'month'),
                      ('volume', 'volume'), ('issue', 'number'), ('eid', 'eid'),
                      ('page_range', 'pages'), ('abstract', 'abstract'), ('doi', 'doi'),
                      ('eprintid', 'archivePrefix|eprint'), ('arxiv_class', 'primaryClass'),
                      ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        elif (doc_type_bibtex == '@BOOK'):
            fields = [('author', 'author'), ('title', 'title'),
                      ('year', 'year'), ('volume', 'volume'), ('doi', 'doi'),
                      ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        elif (doc_type_bibtex == '@INBOOK'):
            fields = [('author', 'author'), ('title', 'title'), ('keyword', 'keywords'),
                      ('pub_raw', 'booktitle'), ('year', 'year'), ('editor', 'editor'),
                      ('volume', 'volume'), ('series', 'series'), ('eid', 'eid'),
                      ('page_range', 'pages'), ('abstract', 'abstract'), ('doi', 'doi'),
                      ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        elif (doc_type_bibtex == '@PROCEEDINGS'):
            fields = [('title', 'title'), ('keyword', 'keywords'), ('pub', 'booktitle'),
                      ('year', 'year'), ('editor', 'editor'), ('series', 'series'),
                      ('volume', 'volume'), ('month', 'month'), ('doi', 'doi'),
                      ('eprintid', 'archivePrefix|eprint'), ('arxiv_class', 'primaryClass'),
                      ('abstract', 'abstract'), ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        elif (doc_type_bibtex == '@INPROCEEDINGS'):
            fields = [('author', 'author'), ('title', 'title'), ('keyword', 'keywords'),
                      ('pub', 'booktitle'), ('year', 'year'), ('editor', 'editor'),
                      ('series', 'series'), ('volume', 'volume'), ('month', 'month'),
                      ('eid', 'eid'), ('page_range', 'pages'), ('abstract', 'abstract'),
                      ('doi', 'doi'), ('eprintid', 'archivePrefix|eprint'), ('arxiv_class', 'primaryClass'),
                      ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        elif (doc_type_bibtex == '@MISC'):
            fields = [('author', 'author'), ('title', 'title'), ('keyword', 'keywords'),
                      ('pub', 'howpublished'), ('year', 'year'), ('month', 'month'),
                      ('eid', 'eid'), ('page_range', 'pages'), ('doi', 'doi'),
                      ('eprintid', 'archivePrefix|eprint'), ('arxiv_class', 'primaryClass'),
                      ('version', 'version'), ('publisher', 'publisher'),
                      ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        elif (doc_type_bibtex == '@PHDTHESIS') or (doc_type_bibtex == '@MASTERSTHESIS'):
            fields = [('author', 'author'), ('title', 'title'), ('keyword', 'keywords'),
                      ('aff', 'school'), ('year', 'year'), ('month', 'month'),
                      ('bibcode', 'adsurl'),('adsnotes', 'adsnote')]
        elif (doc_type_bibtex == '@TECHREPORT'):
            fields = [('author', 'author'), ('title', 'title'), ('pub_raw', 'journal'),
                      ('keyword', 'keywords'), ('pub', 'booktitle'), ('year', 'year'),
                      ('editor', 'editor'), ('series', 'series'), ('month', 'month'),
                      ('eid', 'eid'), ('page_range', 'pages'), ('volume', 'volume'),
                      ('doi', 'doi'), ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        else:
            fields = []
        return OrderedDict(fields)

    def __get_author_list(self, a_doc, field, maxauthor):
        """
        format authors/editors

        :param a_doc:
        :param field:
        :param maxauthor:
        :return:
        """
        if field not in a_doc:
            return ''
        and_str = ' and '
        author_list = ''
        author_count = 0
        for author in a_doc[field]:
            author_parts = encode_laTex_author(author).split(',', 1)
            author_list += '{' + author_parts[0] + '}'
            if (len(author_parts) == 2):
                author_list += ',' +  author_parts[1]
            author_count += 1
            # if reached number of required authors return
            # zero author is indication of all available authors
            if author_count == maxauthor and not maxauthor == 0:
                return author_list
            author_list += and_str
        author_list = author_list[:-len(and_str)]
        return author_list


    def __get_author_lastname_list(self, a_doc, maxauthor):
        """
        format authors

        :param a_doc:
        :param field:
        :param maxauthor:
        :return:
        """
        if 'author' not in a_doc:
            return ''
        author_list = ''
        author_count = 0
        for author in a_doc['author']:
            author_parts = author.split(',', 1)
            author_list += author_parts[0]
            author_count += 1
            if author_count == maxauthor:
                return author_list
        return author_list


    def __get_affiliation_list(self, a_doc):
        """
        format affiliation

        :param a_doc:
        :return:
        """
        if ('aff') not in a_doc:
            return ''
        counter = self.generate_counter_id(len(a_doc['aff']))
        separator = ', '
        affiliation_list = ''
        addCount = not (a_doc.get('doctype', '') in ['phdthesis', 'mastersthesis'])
        for affiliation, i in zip(a_doc['aff'], range(len(a_doc['aff']))):
            if (addCount):
                affiliation_list += counter[i] + '(' + affiliation + ')' + separator
            else:
                affiliation_list += affiliation + separator
        # do not need the last separator
        if (len(affiliation_list) > len(separator)):
            affiliation_list = affiliation_list[:-len(separator)]
        return encode_laTex(affiliation_list)


    def __add_keywords(self, a_doc):
        """
        format keywords

        :param a_doc:
        :return:
        """
        if 'keyword' not in a_doc:
            return ''
        return encode_laTex(', '.join(a_doc.get('keyword', '')))


    def __get_journal(self, a_doc):
        """
        finds a macro for the journal if available, otherwise
        returns the journal name
        note that for doctype = software this field is ignored

        :param journal:
        :return:
        """
        if a_doc.get('doctype', '') == 'software':
            return None
        journal_macros = dict([(k, v) for k, v in current_app.config['EXPORT_SERVICE_AASTEX_JOURNAL_MACRO']])
        return journal_macros.get(self.get_main_bibstem(a_doc.get('bibstem', '')), encode_laTex(''.join(a_doc.get('pub', ''))))


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
        return encode_laTex(pub_raw)


    def __add_page(self, a_doc):
        """

        :param a_doc:
        :return:
        """
        page = ''.join(a_doc.get('page_range', ''))
        if len(page) == 0:
            page = ''.join(a_doc.get('page', ''))
        return page


    def __add_in(self, field, value, output_format):
        """
        add the value into the return structure, only if a value was defined in Solr
        
        :param field: 
        :param value: 
        :param output_format: 
        :return: 
        """
        if (((isinstance(value, unicode)) or (isinstance(value, str))) and (len(value) > 0)) or \
           ((isinstance(value, int)) and (value is not None)):
            return output_format.format(field, value) + ',\n'
        return ''


    def __add_in_eprint(self, fields, values, output_format):
        """
        add in the values of eprint

        :param fields:
        :param values:
        :param output_format:
        :return:
        """
        field = fields.split('|')
        value = values.split(':')
        if len(field) != 2 and len(value) != 2:
            return ''
        result = ''
        for f, v in zip(field, value):
            result += self.__add_in(f, v, output_format)
        return result


    def __add_in_arxiv_class(self, field, value, output_format):
        """

        :param field:
        :param value:
        :param output_format:
        :return:
        """
        if (len(value) >= 1):
            return self.__add_in(field, value[0], output_format)
        return ''


    def __add_in_wrapped(self, field, value, output_format):
        """
        add the value into the return structure, only if a value was defined in Solr
        
        :param field: 
        :param value: 
        :param output_format: 
        :return: 
        """
        if (len(value) > 0):
            return self.__format_line_wrapped(field, value, output_format) + ',\n'
        return ''


    def __get_key(self, a_doc):
        """

        :param a_doc:
        :return:
        """
        key = self.keyformat
        for field in self.parsed_spec:
            if (field[2] == 'author'):
                match = re.search(r'%(\d)H', field[1])
                if match:
                    maxauthor = int(match.group(1))
                else:
                    maxauthor = 1
                key = key.replace(field[1], self.__get_author_lastname_list(a_doc, maxauthor))
            elif (field[2] == 'year'):
                key = key.replace(field[1], a_doc.get('year', ''))
            elif (field[2] == 'bibcode'):
                key = key.replace(field[1], a_doc.get('bibcode', ''))
            elif (field[2] == 'pub'):
                key = key.replace(field[1], self.get_pub_abbrev(a_doc.get('pub', ''), a_doc.get('bibcode', '')))
        return key

    def __get_doc(self, index, include_abs, maxauthor):
        """
        for each document from Solr, get the fields, and format them accordingly

        :param index:
        :param include_abs:
        :param maxauthor:
        :return:
        """
        format_style_bracket_quotes = u'{0:>13} = "{{{1}}}"'
        format_style_bracket = u'{0:>13} = {{{1}}}'
        format_style_quotes = u'{0:>13} = "{1}"'
        format_style = u'{0:>13} = {1}'

        a_doc = self.from_solr['response'].get('docs')[index]
        text = self.__get_doc_type(a_doc.get('doctype', '')) + '{' + self.__get_key(a_doc) + ',\n'

        fields = self.__get_fields(a_doc)
        for field in fields:
            if (field == 'author') or (field == 'editor'):
                text += self.__add_in_wrapped(fields[field], self.__get_author_list(a_doc, field, maxauthor), format_style_bracket)
            elif (field == 'title'):
                text += self.__add_in(fields[field], encode_laTex(''.join(a_doc.get(field, ''))), format_style_bracket_quotes)
            elif (field == 'aff'):
                text += self.__add_in_wrapped(fields[field], self.__get_affiliation_list(a_doc), format_style_bracket)
            elif (field == 'pub_raw'):
                text += self.__add_in(fields[field], self.__add_clean_pub_raw(a_doc), format_style_bracket)
            elif (field == 'pub'):
                text += self.__add_in(fields[field], self.__get_journal(a_doc), format_style_bracket)
            elif (field == 'doi'):
                text += self.__add_in(fields[field], ''.join(a_doc.get(field, '')), format_style_bracket)
            elif (field == 'keyword'):
                text += self.__add_in(fields[field], self.__add_keywords(a_doc), format_style_bracket)
            elif (field == 'year'):
                text += self.__add_in(fields[field], a_doc.get(field, '') if a_doc.get(field, '') else None, format_style_quotes)
            elif (field == 'volume') or (field == 'issue'):
                text += self.__add_in(fields[field], a_doc.get(field, '') if a_doc.get(field, '') else None, format_style_bracket)
            elif (field == 'month'):
                text += self.__add_in(fields[field], self.__format_date(a_doc.get('pubdate', '')), format_style_quotes)
            elif (field == 'abstract') and (include_abs):
                text += self.__add_in_wrapped(fields[field], encode_laTex(a_doc.get(field, '')), format_style_bracket_quotes)
            elif (field == 'eid'):
                text += self.__add_in(fields[field], a_doc.get(field, ''), format_style_bracket)
            elif (field == 'page_range'):
                text += self.__add_in(fields[field], self.__add_page(a_doc), format_style_bracket)
            elif (field == 'bibcode'):
                text += self.__add_in(fields[field], current_app.config['EXPORT_SERVICE_FROM_BBB_URL'] + '/' + a_doc.get(field, ''), format_style_bracket)
            elif (field == 'adsnotes'):
                text += self.__add_in(fields[field], current_app.config['EXPORT_SERVICE_ADS_NOTES'], format_style_bracket)
            elif (field == 'eprintid'):
                text += self.__add_in_eprint(fields[field], get_eprint(a_doc), format_style_bracket)
            elif (field == 'arxiv_class'):
                text += self.__add_in_arxiv_class(fields[field], a_doc.get(field, ''), format_style_bracket)
            elif (field == 'series') or (field == 'version') or (field == 'publisher'):
                text += self.__add_in(fields[field], ''.join(a_doc.get(field, '')), format_style_bracket)

        # remove the last comma,
        text = text[:-len(',\n')] + '\n'

        return text + '}\n\n'


    def get(self, include_abs, maxauthor):
        """
        
        :param include_abs: if ture include abstract
        :return: result of formatted records in a dict
        """
        num_docs = 0
        ref_BibTex = []
        if (self.status == 0):
            num_docs = self.get_num_docs()
            for index in range(num_docs):
                ref_BibTex.append(self.__get_doc(index, include_abs, maxauthor))
        result_dict = {}
        result_dict['msg'] = 'Retrieved {} abstracts, starting with number 1.'.format(num_docs)
        result_dict['export'] = ''.join(record for record in ref_BibTex)
        return result_dict
