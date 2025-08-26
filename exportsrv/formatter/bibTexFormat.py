# -*- coding: utf-8 -*-

from collections import OrderedDict
from datetime import datetime
from flask import current_app
from textwrap import fill
import re
import json
from unidecode import unidecode

from exportsrv.formatter.format import Format
from exportsrv.formatter.ads import adsJournalFormat, adsOutputFormat
from exportsrv.formatter.toLaTex import encode_laTex, encode_laTex_author, encode_latex_doi
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
        r'''(            # start of capture group 1
            %                   # literal "%"
            (?:                 # first option
            (?:\d+|\*)?         # width
            [HqRXY]             # type
            )
        )''', flags=re.X
    )
    ENUMERATION_KEY = '%zm'
    REGEX_ENUMERATION = re.compile(r'(%s)'%ENUMERATION_KEY)

    def __init__(self, from_solr, keyformat):
        """

        :param keyformat:
        """
        Format.__init__(self, from_solr)
        self.keyformat = keyformat
        self.parsed_spec = []
        for m in self.REGEX_KEY.finditer(self.keyformat):
            self.parsed_spec.append(tuple((m.start(1), m.group(1), self.__get_solr_field(m.group(1)))))
        self.enumeration = False
        matches = self.REGEX_ENUMERATION.findall(self.keyformat)
        if (len(matches) >= 1):
            self.enumeration = True
            self.keyformat = self.keyformat.replace(self.ENUMERATION_KEY, '')
        self.enumerated_keys = []

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
            'X': 'eprintid',
            'Y': 'year'
        }
        specifier = ''.join(re.findall(r'([HqRXY])', specifier))
        return fieldDict.get(specifier, '')


    def __get_doc_type(self, solr_type):
        """
        convert from solr to BibTex document type

        :param solr_type:
        :return:
        """
        try:
            has_publisher = self.from_solr['response'].get('docs')[0].get('publisher')
        except:
            has_publisher = None

        fields = {'article':'@ARTICLE', 'circular':'@ARTICLE', 'newsletter':'@ARTICLE',
                  'bookreview':'@ARTICLE', 'erratum':'@ARTICLE', 'obituary':'@ARTICLE',
                  'eprint':'@ARTICLE', 'catalog':'@ARTICLE', 'editorial':'@ARTICLE',
                  'book':'@BOOK', 
                  'inbook':'@INCOLLECTION',
                  'proceedings':'@PROCEEDINGS', 
                  'inproceedings':'@INPROCEEDINGS', 'abstract':'@INPROCEEDINGS',
                  'misc':'@MISC', 'proposal':'@MISC', 'pressrelease':'@MISC',
                  'talk':'@MISC', 'software':'@software', 'dataset':'@dataset',
                  'phdthesis':'@PHDTHESIS','mastersthesis':'@MASTERSTHESIS',
                  'techreport':'@TECHREPORT', 'intechreport':'@MISC','instrument':'@MISC','service':'@MISC'}
        doc_type = fields.get(solr_type, '')
        if doc_type == '@TECHREPORT' and not has_publisher:
            doc_type = '@MISC'
        return doc_type


    def __format_date(self, solr_date):
        """

        :param solr_date:
        :return:
        """
        # solr_date has the format 2017-12-01
        date_time = datetime.strptime(solr_date.replace('-00', '-01'), '%Y-%m-%d')
        # 2/7/2020 as per Alberto, month should be lower case
        return strftime(date_time, '%b').lower()


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
                      ('year', 'year'), ('volume', 'volume'),
                      ('publisher', 'publisher'), ('doi', 'doi'),
                      ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        elif (doc_type_bibtex == '@INCOLLECTION'):
            fields = [('author', 'author'), ('title', 'title'), ('keyword', 'keywords'),
                      ('pub', 'booktitle'), ('year', 'year'), ('editor', 'editor'),
                      ('volume', 'volume'), ('series', 'series'), ('publisher', 'publisher'),
                      ('eid', 'eid'), ('page_range', 'pages'), ('abstract', 'abstract'),
                      ('doi', 'doi'), ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        elif (doc_type_bibtex == '@PROCEEDINGS'):
            fields = [('title', 'title'), ('keyword', 'keywords'), ('pub', 'booktitle'),
                      ('year', 'year'), ('editor', 'editor'), ('series', 'series'),
                      ('volume', 'volume'), ('month', 'month'), ('publisher', 'publisher'),
                      ('doi', 'doi'), ('eprintid', 'archivePrefix|eprint'), ('arxiv_class', 'primaryClass'),
                      ('abstract', 'abstract'), ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        elif (doc_type_bibtex == '@INPROCEEDINGS'):
            fields = [('author', 'author'), ('title', 'title'), ('keyword', 'keywords'),
                      ('pub', 'booktitle'), ('year', 'year'), ('editor', 'editor'),
                      ('series', 'series'), ('volume', 'volume'), ('month', 'month'),
                      ('publisher', 'publisher'), ('eid', 'eid'), ('page_range', 'pages'),
                      ('abstract', 'abstract'), ('doi', 'doi'), ('eprintid', 'archivePrefix|eprint'),
                      ('arxiv_class', 'primaryClass'), ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        elif (doc_type_bibtex == '@MISC'):
            fields = [('author', 'author'), ('title', 'title'), ('keyword', 'keywords'),
                      ('pub_raw', 'howpublished'), ('year', 'year'), ('month', 'month'),
                      ('eid', 'eid'), ('page_range', 'pages'), ('doi', 'doi'),
                      ('eprintid', 'archivePrefix|eprint'), ('arxiv_class', 'primaryClass'),
                      ('version', 'version'), ('publisher', 'publisher'),
                      ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        elif (doc_type_bibtex == '@PHDTHESIS') or (doc_type_bibtex == '@MASTERSTHESIS'):
            fields = [('author', 'author'), ('title', 'title'), ('keyword', 'keywords'),
                      ('aff', 'school'), ('year', 'year'), ('month', 'month'),
                      ('bibcode', 'adsurl'),('adsnotes', 'adsnote')]
        elif (doc_type_bibtex == '@TECHREPORT'):
             fields = [('author', 'author'), ('title', 'title'), ('publisher', 'institution'),
                       ('keyword', 'keywords'), ('year', 'year'),
                       ('eid', 'number'), ('pub_raw', 'howpublished'),
                       ('doi', 'doi'), ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]
        # 1/31/2024 as per Edwin adding software and dataset export format
        elif doc_type_bibtex in ['@software', '@dataset']:
            fields = [('author', 'author'), ('title', 'title'),
                      ('pub_raw', 'howpublished'), ('year', 'year'), ('month', 'month'),
                      ('eid', 'eid'), ('doi', 'doi'),
                      ('version', 'version'), ('publisher', 'publisher'),
                      ('bibcode', 'adsurl'), ('adsnotes', 'adsnote')]

        else:
            fields = []
        return OrderedDict(fields)


    def __get_author_list(self, a_doc, field, max_author, author_cutoff):
        """
        format authors/editors

        :param a_doc:
        :param field: author or editor
        :param max_author:
        :param author_cutoff:
        :return:
        """
        if field not in a_doc:
            return ''
        and_str = ' and '
        author_list = ''
        # if number of authors exceed the maximum that we display, cut to shorter list
        # only if max_author is none zero, zero is indication of return all available authors
        cut_authors = (len(a_doc[field]) > author_cutoff) and not max_author == 0
        for author, i in zip(a_doc[field], range(len(a_doc[field]))):
            # there should be up to only two commas, just in case there is not
            author_parts = encode_laTex_author(author).split(',', 2)
            author_list += '{' + author_parts[0] + '}'
            if (len(author_parts) == 2):
                author_list += ',' +  author_parts[1]
            # there is suffix, insert it first
            elif (len(author_parts) == 3):
                author_list += ',' + author_parts[2] + ',' + author_parts[1]
            if cut_authors and i + 1 == max_author:
                # if reached number of required authors return
                return author_list + " and et al."
            author_list += and_str
        author_list = author_list[:-len(and_str)]
        return author_list


    def __get_author_lastname_list(self, a_doc, max_author):
        """
        format authors

        :param a_doc:
        :param field:
        :param max_author:
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
            if author_count == max_author:
                return author_list
        return author_list


    def __get_affiliation_list(self, a_doc, max_author, author_cutoff):
        """
        format affiliation

        :param a_doc:
        :return:
        """
        if 'aff' not in a_doc:
            return ''
        counter = self.generate_counter_id(len(a_doc['aff']))
        separator = ', '
        affiliation_list = ''
        # if number of affiliations exceed the maximum that we display, cut to shorter list
        # only if max_author is none zero (note number of authors and number of affiliations displayed should match),
        # zero is indication of return all available affiliations
        cut_affiliations = (len(a_doc['aff']) > author_cutoff) and not max_author == 0
        addCount = not (a_doc.get('doctype', '') in ['phdthesis', 'mastersthesis'])
        for affiliation, i in zip(a_doc['aff'], range(len(a_doc['aff']))):
            if (addCount):
                affiliation_list += counter[i] + '(' + affiliation + ')' + separator
            else:
                affiliation_list += affiliation + separator
            if cut_affiliations and i + 1 == max_author:
                # if reached number of required affiliations stop
                break
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


    def __get_journal(self, a_doc, journal_format):
        """
        let client decide on the format of journal, macro if one is available, abbreviated journal name, or full journal name
        note that for doctype = software this field is ignored

        :param a_doc:
        :param journal_format
        :return:
        """
        doctype = a_doc.get('doctype', '')

        if doctype in ['software', 'dataset']:
            return None

        # apply user preference only if pub is assigned to journal field
        # pub is displayed for booktitle and how_published, in which case it should appears in full
        need_full_pub = ['inbook', 'proceedings', 'inproceedings', 'abstract', 'misc', 'proposal', 'pressrelease', 'talk']
        if doctype in need_full_pub:
            return encode_laTex(''.join(a_doc.get('pub', '')))

        # use macro (default)
        if journal_format == adsJournalFormat.macro or journal_format == adsJournalFormat.default:
            journal_macros = dict([(k, v) for k, v in current_app.config['EXPORT_SERVICE_AASTEX_JOURNAL_MACRO']])
            return journal_macros.get(self.get_bibstem(a_doc.get('bibstem', '')), encode_laTex(''.join(a_doc.get('pub', ''))))
        elif journal_format == adsJournalFormat.abbreviated:
            return encode_laTex(Format(None).get_pub_abbrev(a_doc.get('bibstem', '')))
        elif journal_format == adsJournalFormat.full:
            return encode_laTex(''.join(a_doc.get('pub', '')))


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


    def __add_abstract(self, a_doc):
        """
        
        :param a_doc: 
        :return: 
        """
        abstract = a_doc.get('abstract', '').replace('<P />', '\\\\').replace('<BR />', '\\')
        return encode_laTex(abstract)
        
    def __add_in(self, field, value, output_format):
        """
        add the value into the return structure, only if a value was defined in Solr
        
        :param field: 
        :param value: 
        :param output_format: 
        :return: 
        """
        if (((isinstance(value, str)) or (isinstance(value, bytes))) and (len(value) > 0)) or \
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
        field_parts = fields.split('|')
        value_parts = values.split(':')
        if len(field_parts) != 2 and len(value_parts) != 2:
            return ''
        result = ''
        for f, v in zip(field_parts, value_parts):
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


    def __field_wrapped(self, field, value, output_format):
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


    def __format_key(self, a_doc):
        """
        format keyformat for a_doc document

        :param a_doc:
        :return:
        """
        key = self.keyformat
        for field in self.parsed_spec:
            if (field[2] == 'author'):
                match = re.search(r'%(\d)H', field[1])
                if match:
                    max_author = int(match.group(1))
                else:
                    max_author = 1
                authors = self.__get_author_lastname_list(a_doc, max_author)
                # need to make sure the key is returned in ascii format
                key = key.replace(field[1], unidecode(authors))
            elif (field[2] == 'year'):
                key = key.replace(field[1], a_doc.get('year', ''))
            elif (field[2] == 'bibcode'):
                key = key.replace(field[1], a_doc.get('bibcode', ''))
            elif (field[2] == 'pub'):
                key = key.replace(field[1], self.get_bibstem(a_doc.get('bibstem', '')))
            elif (field[2] == 'eprintid'):
                key = key.replace(field[1], get_eprint(a_doc))
        key = key.replace(' ', '')
        # if no values in the key, return the default, bibcode
        if len(key) == 0:
            key = a_doc.get('bibcode', '')
        return key


    def __get_key(self, index):
        """

        :param index:
        :return:
        """
        # if enumeration is on, keys have been formatted already, so grab it from the list
        # otherwise format the key and return it
        if self.enumeration:
            return self.enumerated_keys[index]
        return self.__format_key(self.from_solr['response'].get('docs')[index])


    def __get_doc(self, index, include_abs, max_author, author_cutoff, journal_format):
        """
        for each document from Solr, get the fields, and format them accordingly

        :param index:
        :param include_abs:
        :param max_author:
        :param author_cutoff:
        :param journal_format:
        :return:
        """
        format_style_bracket_quotes = u'{0:>13} = "{{{1}}}"'
        format_style_bracket = u'{0:>13} = {{{1}}}'
        format_style_quotes = u'{0:>13} = "{1}"'
        format_style = u'{0:>13} = {1}'

        a_doc = self.from_solr['response'].get('docs')[index]
        text = self.__get_doc_type(a_doc.get('doctype', '')) + '{' + self.__get_key(index) + ',\n'
        fields = self.__get_fields(a_doc)
        for field in fields:
            if (field == 'author') or (field == 'editor'):
                text += self.__add_in(fields[field], self.__get_author_list(a_doc, field, max_author, author_cutoff), format_style_bracket)
            elif (field == 'title'):
                text += self.__add_in(fields[field], encode_laTex(''.join(a_doc.get(field, ''))), format_style_bracket_quotes)
            elif (field == 'aff'):
                text += self.__field_wrapped(fields[field], self.__get_affiliation_list(a_doc, max_author, author_cutoff), format_style_bracket)
            elif (field == 'pub_raw'):
                # pub_raw goes to howpublished when doc_type is @misc
                # we want to display pub_raw in howpublished only if publisher data is not available
                doc_type_bibtex = self.__get_doc_type(a_doc.get('doctype', ''))
                if doc_type_bibtex in ['@MISC', '@software', 'dataset'] and a_doc.get('publisher', ''):
                    continue
                text += self.__add_in(fields[field], self.__add_clean_pub_raw(a_doc), format_style_bracket)
            elif (field == 'pub'):
                text += self.__add_in(fields[field], self.__get_journal(a_doc, journal_format), format_style_bracket)
            elif (field == 'doi'):
                # 8/5/22 checked couple of sites including https://citation.crosscite.org/ that do not escape doi
                # so remove escaping doi, and let the underscore be dealt with on the latex side
                # text += self.__add_in(fields[field], encode_latex_doi(''.join(a_doc.get(field, ''))), format_style_bracket)
                text += self.__add_in(fields[field], ''.join(a_doc.get(field, '')), format_style_bracket)
            elif (field == 'keyword'):
                text += self.__add_in(fields[field], self.__add_keywords(a_doc), format_style_bracket)
            elif (field == 'year'):
                text += self.__add_in(fields[field], a_doc.get(field, '') if a_doc.get(field, '') else None, format_style)
            elif (field == 'volume') or (field == 'issue'):
                text += self.__add_in(fields[field], a_doc.get(field, '') if a_doc.get(field, '') else None, format_style_bracket)
            elif (field == 'month'):
                text += self.__add_in(fields[field], self.__format_date(a_doc.get('pubdate', '')), format_style)
            elif (field == 'abstract') and (include_abs):
                text += self.__field_wrapped(fields[field], self.__add_abstract(a_doc), format_style_bracket_quotes)
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
        return text + '}'


    def __enumerate_keys(self):
        """
        when enumeration is specified create all keys at once
        go through the list, creating key, check to see if it exists
        if found, attached a, b, c, ... to it

        :return:
        """
        self.enumerated_keys = []
        for i, a_doc in enumerate(self.from_solr['response'].get('docs')):
            new_key = self.__format_key(a_doc)
            count = sum(new_key == key[:-1] or new_key == key for key in self.enumerated_keys)
            if count == 0:
                self.enumerated_keys.append(new_key)
            # if there is an element exactly like new_key
            # update it with adding an `a` to it, and then add this one to the end with 'b' attached to it
            elif count == 1:
                self.enumerated_keys[self.enumerated_keys.index(new_key)] = new_key + 'a'
                self.enumerated_keys.append(new_key + 'b')
            # if more than one element is found
            # add this one to the end with the next character attached to i
            else:
                self.enumerated_keys.append(new_key + str(chr(ord('a') + count)))
        return self.enumerated_keys


    def get(self, include_abs, max_author, author_cutoff, journal_format, output_format):
        """
        
        :param include_abs: if ture include abstract
        :param max_author:
        :param author_cutoff:
        :param journal_format:
        :return: result of formatted records in a dict
        """
        num_docs = 0
        references = []
        bibcodes = []
        if (self.status == 0):
            num_docs = self.get_num_docs()
            if self.enumeration:
                self.__enumerate_keys()
            for index in range(num_docs):
                references.append(self.__get_doc(index, include_abs, max_author, author_cutoff, journal_format))
                bibcodes.append(self.from_solr['response'].get('docs')[index]['bibcode'])
        return self.formatted_export(output_format, num_docs, references, bibcodes, '\n\n')
