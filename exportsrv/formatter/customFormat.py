# -*- coding: utf-8 -*-

from datetime import datetime
from flask import current_app
from textwrap import fill
import re
from html import escape

from exportsrv.formatter.format import Format
from exportsrv.formatter.ads import adsFormatter, adsOrganizer
from exportsrv.formatter.cslJson import CSLJson
from exportsrv.formatter.csl import CSL
from exportsrv.formatter.toLaTex import encode_laTex, encode_laTex_author
from exportsrv.formatter.strftime import strftime
from exportsrv.utils import get_eprint, replace_html_entity

# This class accepts JSON object created by Solr and can reformats it
# for the user define Custom Format Export.
# To get custom formatted data first pass in the custom format string
# to parse it and determine the Solr fields needed
#    custom_format = CustomFormat(customFormatStr)
#    custom_format.get_solr_fields()
# Next pass the fields to Solr and get the JSON code back and finaly use
#    custom_format.set_json_from_solr(jsonFromSolr)
#    custom_format.getCustomFormat()

class CustomFormat(Format):

    REGEX_AUTHOR = re.compile(r'%[\\>/=]?(\d*\.?\d*)(\w)')
    REGEX_PUB_MACRO = re.compile(r'(^\\[a-z]*$)')
    REGEX_FIRST_AUTHOR = re.compile(r'%(\^)(\w)')
    REGEX_AFF = re.compile(r'%(\d*)F')
    REGEX_ENUMERATION = re.compile(r'(%zn)')
    REGEX_COMMAND = [
        re.compile(r'(%Z(?:Encoding|Linelength):[\w\-]+\s?)'),
        re.compile(r'(%Z(?:Header|Footer|AuthorSep):\".+?\"\s?)'),
        re.compile(r'(%Z(?:Markup):\w+)'),
        re.compile(r'(%Z(?:EOL):\".*\"\s?)'),
    ]
    REGEX_CUSTOME_FORMAT = re.compile(
        r'''(                                                   # start of capture group 1
            %                                                   # literal "%"
            (?:[\\>/=])?                                        # field encoding
            (?:                                                 # first option
            (?:\d+|\*)?                                         # width
            (?:\.(?:\d+|\*))?                                   # precision
            (?:\^)?
            p{0,2}[AaBcCdDeEfFGgHhiIJjKLlMmNnOopPQqRSTUuVWXxY]  # type
            )
        )''', flags=re.X
    )

    def __init__(self, custom_format):
        """

        :param custom_format:
        """
        Format.__init__(self, None)
        self.parsed_spec = []
        self.from_cls = {}
        self.author_count = {}
        self.custom_format = custom_format
        self.export_format = adsFormatter.unicode
        self.line_length = 0
        self.header = ''
        self.footer = ''
        self.author_sep = ''
        self.markup_strip = False
        self.enumeration = False
        self.line_feed = self.__get_linefeed()
        self.__parse()


    def get_solr_fields(self):
        """
        from the user specified specifiers, compile a list of fields to get from Solr
        
        :return: 
        """
        solr_fields = ''
        for element in self.parsed_spec:
            if element[2] not in solr_fields:
                solr_fields += element[2] + ','
        # make sure we always bring back the bibcode
        # note that if at some point we allow alternative bibcode to be part
        # of custom formating this line fails, but until then we should be OK
        if 'bibcode' not in solr_fields:
            solr_fields += 'bibcode,'
        # the same as bibstem
        if 'bibstem' not in solr_fields:
            solr_fields += 'bibstem,'
        # don't need the last comma
        return solr_fields[:-len(',')]


    def __get_linefeed(self):
        """

        :return:
        """
        if self.export_format == adsFormatter.html:
            return '<br / >'
        return '\n'


    def __get_num_authors(self):
        """

        :return:
        """
        num_authors = []
        for a_doc in self.from_solr['response'].get('docs'):
            if 'author' in a_doc:
                num_authors.append(len(a_doc['author']))
            else:
                num_authors.append(0)
        return num_authors

    
    def set_json_from_solr(self, from_solr):
        """
        save the data from Solr, and go through it
        for every author format call CSL to style the authors
        
        :param from_solr: 
        :return: 
        """
        self.from_solr = from_solr
        if (self.from_solr.get('responseHeader')):
            self.status = self.from_solr['responseHeader'].get('status', self.status)
        json_for_csl = CSLJson(self.from_solr).get_author()
        for element in self.parsed_spec:
            if (element[2] == 'author'):
                # my mac has been formatted for case-insensitive
                # so need to make lower case doubled to be different
                # shall continue with this eventhough on the Linux side we shall be OK
                if (element[1][-1].isupper()):
                    csl_file_name = 'ads-author-' + element[1][-1]
                else:
                    csl_file_name = 'ads-author-' + element[1][-1] + element[1][-1]
                key = element[1]
                self.from_cls[key] = CSL(json_for_csl, csl_file_name).get(adsOrganizer.bibliography)
                self.author_count[key] = self.__get_num_authors()


    def __get_solr_field(self, specifier):
        """
        from specifier to Solr fields
        
        :param specifier: 
        :return: 
        """
        fieldDict = {
            'A': 'author',
            'a': 'author',
            'B': 'abstract',
            'c': 'citation_count',
            'C': 'copyright',
            'd': 'doi',
            'D': 'pubdate',
            'e': 'author',
            'F': 'aff',
            'f': 'author',
            'G': 'author',
            'g': 'author',
            'H': 'author',
            'h': 'author',
            'I': 'author',
            'i': 'author',
            'J': 'pub',
            'j': 'pub',
            'K': 'keyword',
            'L': 'author',
            'l': 'author',
            'M': 'author',
            'm': 'author',
            'N': 'author',
            'n': 'author',
            'O': 'author',
            'o': 'author',
            'p': 'page,page_range',
            'P': 'lastpage,page_range',  # Last Page
            'pp':'page_range,page',      # page_range is specified in the custom format, but if not available and page is then return that
            'pc':'page_count',
            'Q': 'pub_raw',
            'q': 'pub',
            'R': 'bibcode',
            'S': 'issue',
            'T': 'title',
            'U': 'url',
            'u': 'url',
            'V': 'volume',
            'W': 'doctype',
            'X': 'eid,identifier',
            'x': 'comment',
            'Y': 'year'
        }
        specifier = ''.join(re.findall(r'([AaBcCdDeEfFGgHhiIJjKLlMmNnOopPQqRSTUuVWXxY]{1,2})', specifier))
        return fieldDict.get(specifier, '')


    def __set_export_format(self, format):
        """
        format can be one of the followings: unicode, html, latex
        
        :param format: 
        :return: 
        """
        # support all the forms Unicode, unicode, utf-8, UTF-8
        if (format.lower() == 'unicode') or (format.lower() == 'utf-8'):
            self.export_format = adsFormatter.unicode
        elif (format == 'html'):
            self.export_format = adsFormatter.html
        elif (format == 'latex'):
            self.export_format = adsFormatter.latex
        elif (format == 'csv'):
            self.export_format = adsFormatter.csv
        else:
            self.export_format = adsFormatter.unicode


    def __parse_enumeration(self):
        """
        see if enumeration specifier has been defined in the custom format string

        :return:
        """
        matches = self.REGEX_ENUMERATION.findall(self.custom_format)
        if (len(matches) >= 1):
            for match in matches:
                self.enumeration = True


    def __parse_command(self):
        """
        see if command specifier has been defined in the custom format string

        :return:
        """
        for token in self.REGEX_COMMAND:
            matches = token.findall(self.custom_format)
            if (len(matches) >= 1):
                for match in matches:
                    self.custom_format = self.custom_format.replace(match, '', len(match))
                    # remove %Z and split on :
                    parts = match[2:].strip().split(':')
                    if (len(parts) == 2):
                        if (parts[0] == 'Encoding'):
                            self.__set_export_format(parts[1])
                        elif (parts[0] == 'Linelength'):
                            self.line_length = int(parts[1])
                        elif (parts[0] == 'Header'):
                            self.header = parts[1].replace('"', '').encode().decode('unicode_escape')
                        elif (parts[0] == 'Footer'):
                            self.footer = parts[1].replace('"', '').encode().decode('unicode_escape')
                        elif (parts[0] == 'AuthorSep'):
                            self.author_sep = parts[1].replace('"', '').encode().decode('unicode_escape')
                        elif (parts[0] == 'Markup'):
                            self.markup_strip = (parts[1].lower() == 'strip')
                        elif (parts[0] == 'EOL'):
                            self.line_feed = parts[1].replace('"', '').encode().decode('unicode_escape')


    def __escape(self):
        """
        tabs are not rendered in the UI so replace them with four spaces
        linefeeds, tabs, and backslash are escaped, so remove the escape
        :return:
        """
        self.custom_format = re.sub(r'(\\n\b)', '\n', re.sub(r'(\\t\b)', "    ", self.custom_format).replace('\\\\', '\\'))


    def __for_csv(self):
        """
        see if the encoding is csv, then there would be no line wrapping
        and if the header line is not defined by user, create the header
        :return:
        """
        if (self.export_format == adsFormatter.csv):
            # no line wrapping in csv format
            self.line_length = 0
            if len(self.header) == 0:
                header = ''
                for field in self.parsed_spec:
                    header += '"' + field[2] + '",'
                # eliminate the last comma
                header = header[:-1]
                self.header = header
            self.custom_format = self.custom_format + ','


    def __parse(self):
        """
        parse the custom format string to identify the requested fields

        :return:
        """
        self.parsed_spec = []
        self.__parse_command()
        self.__parse_enumeration()
        for m in self.REGEX_CUSTOME_FORMAT.finditer(self.custom_format):
            self.parsed_spec.append(tuple((m.start(1), m.group(1), self.__get_solr_field(m.group(1)))))
        # we have %p, %pp, and %pc, when doing replace, %p causes other two to be replaced
        # re did not work, so pushing %p to the end to be the last item to get replaced
        self.parsed_spec = sorted(self.parsed_spec, key=lambda tup: tup[1] == '%p')
        self.__escape()
        self.__for_csv()


    def __format_date(self, solr_date, date_format):
        """

        :param solr_date:
        :param date_format:
        :return:
        """
        # solr_date has the format 2017-12-01
        date_time = datetime.strptime(solr_date.replace('-00', '-01'), '%Y-%m-%d')
        formats = {'D': '%m/%Y', 'Y': '%Y'}
        return strftime(date_time, formats[date_format])


    def __format_url(self, bibcode, url_format):
        """

        :param bibcode:
        :param url_format:
        :return:
        """
        # U: has form: <a href="url">bibcode</a>
        # u: has the form: url/bibcode
        formats = {'U': u'<a href="{}/{}">{}</a>', 'u': u'{}/{}'}
        path = current_app.config['EXPORT_SERVICE_FROM_BBB_URL']
        if (len(bibcode) > 0):
            return formats[url_format].format(path, bibcode, bibcode)
        return ''


    def __format_line_wrapped(self, text, index):
        """

        :param text:
        :param index:
        :return:
        """
        if (self.enumeration):
            text = self.REGEX_ENUMERATION.sub(str(index+1), text)

        if (self.line_length == 0):
            # no linewrap here
            result = text
        else:
            # note that fill removes all the linefeeds at the end of the string,
            # but not the ones in the middle
            # so we can take two approaches, one is to count how many \n appear at the end
            # and then add them in before returning, or add a character or two to the end of
            # of the text and remove them after it has been filled, to give to illusion of
            # \n not at the end of string, if there were any
            result = fill(text+'<END>', width=self.line_length, replace_whitespace=False, subsequent_indent=' ' * 12)
            result = result[:-len('<END>')]
        # in csv format there is a comma at the very end, remove that before adding the linefeed
        if (self.export_format == adsFormatter.csv):
            result = result[:-1]

        return result


    def __get_affiliation_list(self, a_doc):
        """

        :param a_doc:
        :return:
        """
        if ('aff') in a_doc:
            # if a limit of number of affiliation to display is set
            match = self.REGEX_AFF.findall(self.custom_format)
            if (len(''.join(match)) >= 1):
                count = int(''.join(match))
            else:
                count = len(a_doc['aff'])

            counter = self.generate_counter_id(count)
            separator = '; '
            affiliation_list = ''
            for affiliation, i in zip(a_doc['aff'], range(count)):
                affiliation_list += counter[i] + '(' + affiliation + ')' + separator
            # do not need the last separator
            if (len(affiliation_list) > len(separator)):
                affiliation_list = affiliation_list[:-len(separator)]
            return affiliation_list
        return ''


    def __get_n_authors(self, author_list, separator, n_parts_author, before_last, format):
        """

        :param author_list:
        :param separator:
        :param n_parts_author:
        :param before_last:
        :param format:
        :return:
        """
        split_parts = author_list.replace(before_last, '').split(separator)
        return self.__replace_author_separator(separator.join(split_parts[:n_parts_author]), format)

    def __get_first_author(self, author_list, format):
        """

        :param author_list:
        :param format:
        :return:
        """
        # formats that have a comma between last name and first/middle names
        # so that each are author is two elements hence return two elements
        if format in ['A','a','e','G','I','i','L','l','N']:
            split_parts = author_list.split(', ')
            return ', '.join(split_parts[0:2])
        # formats that have no comma between last name and first/middle names
        # or only display last name, hence once split each is an element
        # return one element
        if format in ['f','g','M','m','n','O','o']:
            split_parts = author_list.split(', ')
            return split_parts[0]
        # seprator is space here, and only last name so a one-element needs to be returned
        if format in ['H','h']:
            split_parts = author_list.split(' ')
            return split_parts[0]
        return author_list


    def __replace_author_separator(self, author_list, format):
        """
        check if a user specified separator needs to be applied
        :param format:
        :return:
        """
        if len(self.author_sep) == 0:
            return author_list
        # formats that have no comma between last name and first/middle names
        # or only display last name, hence once split each is an one element
        if format in ['f','g', 'H', 'h', 'M', 'm', 'n', 'O', 'o']:
            split_parts = author_list.split(', ')
            return self.author_sep.join(split_parts)
        # seprator here is space and since only last names are displayed
        # one part is one author
        if format in ['H', 'h']:
            split_parts = author_list.split(' ')
            return self.author_sep.join(split_parts)
        # formats that have a comma between last name and first/middle names
        # so that each are author is two elements
        if format in ['A','a','e','G','I','i','L','l','N']:
            # need to replace commas only up to and or & if any
            if ' and ' in author_list:
                end_index = author_list.find(' and ') + 1
            elif ' & ' in author_list:
                end_index = author_list.find(' & ') + 1
            else:
                end_index = len(author_list)
            # find indices of everyother comma
            sep_index = [m.start() for m in re.finditer(', ', author_list[:end_index])][1::2]
            # replace them
            author_list_slice = []
            for i,j in zip([-len(', ')]+sep_index, sep_index+[len(author_list)]):
                author_list_slice.append(author_list[i+len(', '):j])
            return self.author_sep.join(author_list_slice)
        return author_list



    def __get_author_list_abbreviated(self, author_list, num_authors, format, m):
        """
        Formats	First Author	Second Author..	Before Last	    abbreviated
        A	        As in db	    As in db	    and	            first author,..., m authors and xx colleagues
        G	        lastname f. i.	lastname f. i.	                first author, et al.
        H	        lastname	    lastname	    and	            display requested number of authors
        I	        lastname, f. i.	f. i. lastname	and	            first author, and xx colleagues
        L	        lastname, f. i.	lastname, f. i.	and	            first author, and xx colleagues
        N	        lastname, f. i.	lastname, f. i.		            first author, and xx colleagues
        O           f. i lastname   f. i lastname   and             first author, and xx colleagures
        l	        lastname, f. i.	lastname, f. i.	&	            first author, et al.
        M	        lastname	    lastname	and	                first author, et al.
        m	        lastname	    lastname	&	                first author, et al.
        n	        lastname	    +
        a	        As in db	    As in db	    &	            first author,..., m authors et al.
        g	        lastname, f.i.	lastname, f.i.	and	            first author, and xx colleagues
        h	        lastname	    lastname	    and	            first author \\emph{et al.}
        i	        lastname, f. i.	f. i. lastname	&	            first author, et al.
        o           f. i lastname   f. i lastname   &               first author, et al.

        n.m: Maximum number of entries in field (optional).
        If the number of authors in the list is larger than n, the list will be truncated and returned as
        "author1, author2, ..., authorm, et al.". If m is not specified, n.1 is assumed.

        :param author_list:
        :param num_authors:
        :param format:
        :param m:
        :return:
        """
        format_etal = u'{}, et al.'
        format_etal_no_comma = u'{} et al.'
        format_n_authors = u'{}'
        format_with_n_colleagues = u'{}, and {} colleagues'
        format_escape_emph = u'{} \\emph{{et al.}}'
        format_plus = u'{},+'

        if (format == 'n'):
            authors = author_list.split(',')
            return format_plus.format(authors[0])
        if format in ['A', 'I', 'L', 'N', 'e', 'O']:
            authors = author_list.replace(' and', '').split(', ')
            if (format == 'A') or (format == 'L') or (format == 'N') or (format == 'e') :
                return format_with_n_colleagues.format(', '.join(authors[:m*2]), num_authors-m)
            elif (format == 'I'):
                # here the first author is lastname comma first and middle initials
                # the rest are first and middle initials, no comma, lastname
                # hence first author needs two parts concatenated, the rest only 1
                return format_with_n_colleagues.format(', '.join(authors[:1+m]), num_authors-m)
            elif (format == 'O'):
                return format_with_n_colleagues.format(', '.join(authors[:m]), num_authors-m)
        if (format == 'G'):
            # return n authors (LastName, first and middle initials) et. al. - list is seprated by comma
            return format_etal.format(self.__get_n_authors(author_list, u',', m*2, u'', format))
        if (format == 'i'):
            # here the first author is lastname comma first and middle initials
            # the rest are first and middle initials, no comma, lastname
            # hence first author needs two parts concatenated, the rest only 1
            return format_etal.format(self.__get_n_authors(author_list, u',', 1+m, u'', format))
        if (format == 'o'):
            return format_etal.format(self.__get_n_authors(author_list, u',', m, u'', format))
        if (format == 'M') or (format == 'm'):
            # return n authors (LastName) et. al. - list is separated by a comma
            # no comma before et al
            return format_etal_no_comma.format(self.__get_n_authors(author_list, u',', m, u', and', format))
        if (format == 'f') :
            return format_escape_emph.format(self.__get_n_authors(author_list, u',', m, u', and', format))
        if (format == 'g'):
            # return n authors (LastName) et. al. - list is separated by a comma
            return format_etal.format(self.__get_n_authors(author_list, u',', m, u', and', format))
        if (format == 'H'):
            # return the asked number of authors - list is separated by space,
            # there is an and before the last author
            authors = author_list.replace(' and', '').split(' ')
            return format_n_authors.format(' '.join(authors[:m]))
        if (format == 'a') or (format == 'l'):
            # return n author(s) et. al. - list is separated by a comma
            return format_etal.format(self.__get_n_authors(author_list, u',', m*2, u' \\&', format))
        if (format == 'h'):
            # return the asked number of authors - list is separated by space,
            # there is an and before the last author
            authors = author_list.replace(' &', '').split(' ')
            return format_n_authors.format(' '.join(authors[:m]))
        return author_list


    def __get_author_list(self, format, index):
        """

        :param format:
        :param index:
        :return:
        """
        authors = self.from_cls.get(format)[index]
        count = self.author_count.get(format)[index]
        # see if author list needs to get abbreviated
        # n.m: Maximum number of entries in author field (optional).
        # If the number of authors in the list is larger than n, the list will be truncated to m entries.
        # If.m is not specified, n.1 is assumed.
        matches = self.REGEX_AUTHOR.findall(format)
        if (len(matches) >= 1):
            # format n is a special case
            if (matches[0][1] == 'n'):
                return self.__get_author_list_abbreviated(authors, count, matches[0][1], 0)
            # so is the format for H and h if not abbreviated
            elif ((matches[0][1] == 'H') or (matches[0][1] == 'h')) and len(matches[0][0]) == 0:
                return self.__get_author_list_abbreviated(authors, count, matches[0][1], 1)
            elif (len(matches[0][0]) > 0):
                abbreviated = matches[0][0].split('.')
                n = int(str(abbreviated[0]))
                if (len(abbreviated) > 1):
                    m = int(str(abbreviated[1]))
                else:
                    m = 1
                if (count <= n) or (count <= m):
                    return self.__replace_author_separator(authors, format[-1])
                else:
                    return self.__get_author_list_abbreviated(authors, count, matches[0][1], m)
        # see if it is a first author format
        matches = self.REGEX_FIRST_AUTHOR.findall(format)
        if len(matches) >= 1:
            return self.__get_first_author(authors, format[-1])
        return self.__replace_author_separator(authors, format[-1])


    def __get_keywords(self, a_doc):
        """

        :param a_doc:
        :return:
        """
        if ('keyword') in a_doc:
            separator = ', '
            keyword_list = ''
            for keyword in a_doc['keyword']:
                keyword_list += keyword + separator
            # do not need the last separator
            if (len(keyword_list) > len(separator)):
                keyword_list = keyword_list[:-len(separator)]
            return keyword_list
        return ''

    
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
        return pub_raw


    def __get_publication(self, format, a_doc):
        """

        :param format:
        :param a_doc:
        :return:
        """
        format = format[-1]
        if (format == 'J'):
            # returns the journal name
            return a_doc.get('pub', '')
        if (format == 'j'):
            # returns an AASTeX macro for the journal if available, otherwise
            # returns the journal name
            journal_macros = dict([(k, v) for k, v in current_app.config['EXPORT_SERVICE_AASTEX_JOURNAL_MACRO']])
            return journal_macros.get(self.get_bibstem(a_doc.get('bibstem', '')), a_doc.get('pub', ''))
        if (format == 'Q'):
            # returns the full journal information
            return self.__add_clean_pub_raw(a_doc)
        if (format == 'q'):
            # returns the journal abbreviation
            return self.get_pub_abbrev(a_doc.get('bibstem', ''))
        return ''


    def __get_page(self, field, a_doc):
        """

        :param field:
        :param a_doc:
        :return:
        """
        if field == 'page,page_range':
            if 'page_range' in a_doc:
                page_range = a_doc.get('page_range').split('-')
                return page_range[0]
            if 'page' in a_doc:
                return ''.join(a_doc.get('page'))
        if field == 'lastpage,page_range':
            if 'page_range' in a_doc:
                page_range = a_doc.get('page_range').split('-')
                if len(page_range) > 1:
                    return page_range[1]
        if field == 'page_range,page':
            if 'page_range' in a_doc:
                page_range = a_doc.get('page_range')
                return page_range
            if 'page' in a_doc:
                return ''.join(a_doc.get('page'))
        return ''


    def __encode_latex(self, value, field):
        """

        :param value:
        :param field:
        :return:
        """
        if (field == 'author'):
            return encode_laTex_author(value)
        # do not encode publication when the format is a macro or if it is bibcode
        if ((field == 'pub') and (self.REGEX_PUB_MACRO.match(value))) or (field == 'bibcode'):
            return value
        return encode_laTex(value)


    def __markup_strip(self, value):
        """
        # see if HTML markup found in input fields (such as <SUB>) needs to be removed
        :param value:
        :return:
        """
        return re.sub(r'<.*?>', '', value)


    def __encode(self, value, field, field_format=None):
        """

        :param value:
        :param field:
        :param format:
        :return:
        """
        if self.markup_strip:
            value = self.__markup_strip(value)

        # first check for field encoding
        if field_format is not None:
            if '\\' in field_format:
                return self.__encode_latex(value, field)
            if '>' in field_format:
                return escape(value)
            if '=' in field_format:
                return value.encode('hex')
            if '/' in field_format:
                # This encoding converts the characters &, ?, and + to the hex encoded values.
                # get more information about this from Alberto later
                value = value.replace(' ', '+').replace('"', '%22')
                return value

        # if no field encoding defined, check for global encoding
        if (self.export_format == adsFormatter.unicode):
            if field == 'abstract':
                # per alberto translate <P /> to blank lines, and <BR /> to a newline
                value = value.replace('<P />', '\n\n').replace('<BR />', '\n')
            if field in ['abstract', 'title']:
                value = replace_html_entity(value, adsFormatter.unicode)
            return value
        if (self.export_format == adsFormatter.html):
            return escape(value)
        if (self.export_format == adsFormatter.latex):
            # per alberto for bibtex translate <P /> to \\
            if field == 'abstract':
                value = value.replace('<P />', '\\\\').replace('<BR />', '\\')
            return self.__encode_latex(value, field)

        return value


    def __match_punctuation(self, list_str):
        """
        make sure we have matching punctuations in all the strings in the list
        otherwise remove all non matching ones
        also consider the case when there is a "startpage-endpage" and when the endpage is missing
        we attempt to remove any punctuation on both sides, but if the right side is a comma, dont remove it
        :param list_str:
        :return:
        """
        pattern = []
        punctuation = {'(':')', '{':'}', '[':']', '"':'"'}
        for str in list_str:
            for left, right in punctuation.items():
                count = 0
                for char in str:
                    if char == left:
                        count += 1
                    elif char == right:
                        count -= 1
                if count != 0:
                    if char == '"':
                        if count % 2 != 0:
                            str = str.replace(left, '')
                    else:
                        if left in str:
                            str = str.replace(left, '')
                        elif right in str:
                            str = str.partition(right)[0]
                # take care of a special case when string starts and finishes with a comma
                # if found remove the one from the beginning
                if str.startswith(',') and str.endswith(','):
                    str = str[1:]
                elif str.startswith('\\,') and str.endswith('\\,'):
                    str = str[2:]
            # another special case is when last page is eliminated, so keep the comma
            if str.startswith('-') and str.endswith(','):
                str = str[:-1]
            pattern.append(str)
        return pattern


    def __add_in(self, result, field, value):
        """

        :param result:
        :param field:
        :param value:
        :return:
        """
        precede = r'([\\]?[\(|\{|\[|\"]?(\\(it|bf|sc|em)\s)?[\\|\s|,|-]?'
        succeed = r'[\\|,]?[\)|\}|\]|\"]?[\\|,]?)'

        # in the csv format we add double quotes followed by a comma
        # whether there is a value or not
        if self.export_format == adsFormatter.csv:
            if (len(value) > 0):
                insert_value = '"' + self.__encode(value, field[2], field[1]) + '",'
            else:
                insert_value = '"",'
            pattern = self.__match_punctuation([elem[0] for elem in re.findall((precede.encode() + field[1].encode('unicode-escape') + succeed.encode()).decode('utf8'), result.replace('\\n ', ''))])
            for p in pattern:
                result = result.replace(p, insert_value)
            return result

        if (len(value) > 0):
            return result.replace(field[1], self.__encode(value, field[2], field[1]))
        else:
            pattern = self.__match_punctuation([elem[0] for elem in re.findall((precede.encode() + field[1].encode('unicode-escape') + succeed.encode()).decode('utf8'), result.replace('\\n ', ''))])
            for p in pattern:
                # check for the spearator, if it is the same on both side, eliminate the one at the end
                if p[0] == p[-1] and len(p) > 1:
                    p = p[:-1]
                result = result.replace(p, '')
            return result


    def __get_doc(self, index):
        """

        :param index: index to the docs structure returned from solr
        :return:
        """
        result = self.custom_format
        a_doc = self.from_solr['response'].get('docs')[index]
        for field in self.parsed_spec:
            if (field[2] == 'title') or (field[2] == 'doi') or (field[2] == 'comment'):
                result = self.__add_in(result, field, ''.join(a_doc.get(field[2], '')))
            elif (field[2] == 'author'):
                result = self.__add_in(result, field, self.__get_author_list(field[1], index))
            elif (field[2] == 'doctype'):
                result = self.__add_in(result, field, a_doc.get(field[2], ''))
            elif (field[2] == 'pubdate'):
                result = self.__add_in(result, field, self.__format_date(a_doc.get(field[2], ''), field[1][-1]))
            elif (field[2] == 'aff'):
                result = self.__add_in(result, field, self.__get_affiliation_list(a_doc))
            elif (field[2] == 'keyword'):
                result = self.__add_in(result, field, self.__get_keywords(a_doc))
            elif (field[2] == 'url'):
                result = self.__add_in(result, field, self.__format_url(a_doc.get('bibcode', ''), field[1][-1]))
            elif (field[2] == 'abstract') or (field[2] == 'copyright') or (field[2] == 'bibcode') or \
                 (field[2] == 'volume') or (field[2] == 'year') or (field[2] == 'issue'):
                result = self.__add_in(result, field, a_doc.get(field[2], ''))
            elif (field[2] == 'pub') or (field[2] == 'pub_raw'):
                result = self.__add_in(result, field, self.__get_publication(field[1], a_doc))
            elif (field[2] == 'citation_count') or (field[2] == 'page_count'):
                result = self.__add_in(result, field, str(a_doc.get(field[2], '')))
            elif (field[2] == 'eid,identifier'):
                result = self.__add_in(result, field, get_eprint(a_doc))
            elif (field[2] == 'page,page_range') or (field[2] == 'lastpage,page_range') or (field[2] == 'page_range,page'):
                result = self.__add_in(result, field, self.__get_page(field[2], a_doc))
        result += self.line_feed

        return self.__format_line_wrapped(result, index)


    def get(self):
        """
        
        :return: result of formatted records in a dict
        """
        num_docs = 0
        results = []
        if (self.status == 0):
            if len(self.header) > 0:
                results.append(self.header + self.__get_linefeed())
            num_docs = self.get_num_docs()
            for index in range(num_docs):
                results.append(self.__get_doc(index))
            if len(self.footer) > 0:
                results.append(self.__get_linefeed() + self.footer)
        result_dict = {}
        result_dict['msg'] = 'Retrieved {} abstracts, starting with number 1.'.format(num_docs)
        result_dict['export'] = ''.join(result for result in results)
        return result_dict
