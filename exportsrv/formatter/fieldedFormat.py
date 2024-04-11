# -*- coding: utf-8 -*-

import os
from collections import OrderedDict
from datetime import datetime
from flask import current_app
from textwrap import fill
import re

from exportsrv.formatter.format import Format
from exportsrv.utils import get_eprint
from exportsrv.formatter.strftime import strftime

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

class FieldedFormat(Format):

    # Fielded (formerly known as tagged)
    EXPORT_FORMAT_ADS = 'ADS'
    EXPORT_FORMAT_ENDNOTE = 'EndNote'
    EXPORT_FORMAT_PROCITE = 'ProCite'
    EXPORT_FORMAT_REFMAN = 'Refman'
    EXPORT_FORMAT_REFWORKS = 'RefWorks'
    EXPORT_FORMAT_MEDLARS = 'MEDLARS'

    REGEX_PUB_RAW = dict([
        (re.compile(r"(\;?\s*\<ALTJOURNAL\>.*\</ALTJOURNAL\>\s*)"), r""),  # remove these
        (re.compile(r"(\;?\s*\<CONF_METADATA\>.*\<CONF_METADATA\>\s*)"), r""),
        (re.compile(r"(?:\<ISBN\>)(.*)(?:\</ISBN\>)"), r"\1"),  # get value inside the tag for these
        (re.compile(r"(?:\<NUMPAGES\>)(.*)(?:</NUMPAGES>)"), r"\1"),
    ])

    re_conference_locations = None

    def __get_doc_type(self, solr_type, export_format):
        """
        from solr to each fielded document type

        :param solr_type:
        :param export_format:
        :return:
        """
        fields = {}
        if (export_format == self.EXPORT_FORMAT_ENDNOTE):
            fields = {'article': 'Journal Article', 'book': 'Book', 'inbook': 'Book Section',
                      'proceedings': 'Conference Proceedings', 'inproceedings': 'Conference Proceedings',
                      'abstract': 'Conference Paper', 'misc': 'Journal Article', 'eprint': 'Electronic Article',
                      'talk': 'Conference Paper',
                      'software':'Miscellaneous', 'proposal':'Miscellaneous', 'dataset':'Miscellaneous',
                      'pressrelease':'Journal Article', 'circular':'Journal Article', 'newsletter':'Journal Article',
                      'catalog':'Journal Article', 'phdthesis':'Thesis', 'mastersthesis':'Thesis',
                      'techreport':'Report', 'intechreport':'Report',
                      'bookreview': 'Journal Article', 'erratum': 'Journal Article', 'obituary': 'Journal Article',
                      'editorial': 'Journal Article'}
        elif (export_format == self.EXPORT_FORMAT_PROCITE):
            fields = {'article': 'Journal', 'book': 'Book, Whole', 'inbook': 'Book Chapter',
                      'proceedings': 'Journal', 'inproceedings': 'Conference',
                      'abstract': 'Conference', 'misc': 'Journal', 'eprint': 'Preprint',
                      'talk': 'Conference',
                      'software':'Miscellaneous', 'proposal':'Miscellaneous', 'dataset':'Miscellaneous',
                      'pressrelease':'Journal', 'circular':'Journal', 'newsletter':'Journal',
                      'catalog':'Journal', 'phdthesis':'Thesis/Dissertation', 'mastersthesis':'Thesis/Dissertation',
                      'techreport':'Report', 'intechreport':'Report',
                      'bookreview': 'Journal', 'erratum': 'Journal', 'obituary': 'Journal', 'editorial': 'Journal'}
        elif (export_format == self.EXPORT_FORMAT_REFMAN):
            fields = {'article': 'JOUR', 'book': 'BOOK', 'inbook': 'CHAP',
                      'proceedings': 'JOUR', 'inproceedings': 'CONF',
                      'abstract': 'CONF', 'misc': 'JOUR', 'eprint': 'Preprint',
                      'talk': 'CONF',
                      'software':'MISC', 'proposal':'MISC', 'dataset':'MISC',
                      'pressrelease':'JOUR', 'circular':'JOUR', 'newsletter':'JOUR',
                      'catalog':'JOUR', 'phdthesis':'Thesis/Dissertation', 'mastersthesis':'Thesis/Dissertation',
                      'techreport':'RPRT', 'intechreport':'RPRT',
                      'bookreview': 'JOUR', 'erratum': 'JOUR', 'obituary': 'JOUR', 'editorial': 'JOUR'}
        elif (export_format == self.EXPORT_FORMAT_REFWORKS):
            fields = {'article': 'Journal', 'book': 'Book, Whole', 'inbook': 'Book, Chapter',
                      'proceedings': 'Journal', 'inproceedings': 'Conference Proceeding',
                      'abstract': 'Conference Proceeding', 'misc': 'Journal', 'eprint': 'Preprint',
                      'talk': 'Conference Proceeding',
                      'software':'Generic', 'proposal':'Generic', 'dataset':'Generic',
                      'pressrelease':'Journal', 'circular':'Journal', 'newsletter':'Journal',
                      'catalog':'Journal', 'phdthesis':'Thesis/Dissertation', 'mastersthesis':'Thesis/Dissertation',
                      'techreport':'Report', 'intechreport':'Report',
                      'bookreview': 'Journal', 'erratum': 'Journal', 'obituary': 'Journal', 'editorial': 'Journal'}
        elif (export_format == self.EXPORT_FORMAT_MEDLARS):
            fields = {'article': 'Journal Article', 'book': 'Book', 'inbook': 'Book Chapter',
                      'proceedings': 'Journal Article', 'inproceedings': 'Conference',
                      'abstract': 'Conference', 'misc': 'Journal Article', 'eprint': 'Preprint',
                      'talk': 'Conference',
                      'software':'Miscellaneous', 'proposal':'Miscellaneous', 'dataset':'Miscellaneous',
                      'pressrelease':'Journal Article', 'circular':'Journal Article', 'newsletter':'Journal Article',
                      'catalog':'Journal Article', 'phdthesis':'Thesis', 'mastersthesis':'Thesis',
                      'techreport':'Report', 'intechreport':'Report',
                      'bookreview': 'Journal Article', 'erratum': 'Journal Article', 'obituary': 'Journal Article',
                      'editorial': 'Journal Article'}
        return fields.get(solr_type, '')


    def __format_date(self, solr_date, export_format):
        """

        :param solr_date:
        :param export_format:
        :return:
        """
        # solr_date has the format 2017-12-01
        date_time = datetime.strptime(solr_date.replace('-00', '-01'), '%Y-%m-%d')
        formats = {self.EXPORT_FORMAT_ADS: '%m/%Y', self.EXPORT_FORMAT_ENDNOTE: '%B %d, %Y',
                   self.EXPORT_FORMAT_PROCITE: '%Y/%m/X%d', self.EXPORT_FORMAT_REFMAN: '%Y/%m/X%d',
                   self.EXPORT_FORMAT_REFWORKS: '%Y/%m/X%d', self.EXPORT_FORMAT_MEDLARS: '%Y %b %d'}
        return strftime(date_time, formats[export_format]).replace('X0', 'X').replace('X', '')


    def __format_line_wrapped(self, text):
        """

        :param text:
        :return:
        """
        return fill(text, width=72)


    def __get_tags(self, export_format):
        """
        convert from solr to each fielded types' tags

        :param export_format:
        :return:
        """
        if (export_format == self.EXPORT_FORMAT_ADS):
            return (OrderedDict([('bibcode', '%R'), ('title', '%T'), ('author', '%A'),
                                 ('aff', '%F'), ('pub', '%J'), ('volume', '%V'),
                                 ('pubdate', '%D'), ('page', '%P'), ('lastpage', '%L'),
                                 ('keyword', '%K'), ('', '%G'), ('copyright', '%C'),
                                 ('links', '%I'), ('url', '%U'), ('comment', '%X'),
                                 ('', '%S'), ('abstract', '%B'), ('publisher', '%H'),
                                 ('doi', '%Y DOI:'), ('eprintid', '%Y eprintid:')]))
        if (export_format == self.EXPORT_FORMAT_ENDNOTE):
            return (OrderedDict([('doctype', '%0'), ('title', '%T'), ('author', '%A'),
                                 ('editor', '%E'), ('aff', '%+'), ('pub', '%J or %B'),
                                 ('pub_raw', '%C'), ('volume', '%V'), ('year', '%D'),
                                 ('pubdate', '%8'), ('page', '%P'), ('keyword', '%K'),
                                 ('url', '%U'), ('comment', '%Z'), ('abstract', '%X'),
                                 ('publisher', '%I'), ('doi', '%R'), ('eprintid', '%= eprint:'),
                                 ('issn', '%@')]))
        if (export_format == self.EXPORT_FORMAT_PROCITE):
            return (OrderedDict([('doctype', 'TY  -'), ('title', 'TI  -'), ('author', 'AU  -'),
                                 ('aff', 'AD  -'), ('pub', 'JO  -'), ('volume', 'VL  -'),
                                 ('pubdate', 'Y1  -'), ('page', 'SP  -'), ('lastpage', 'EP  -'),
                                 ('keyword', 'KW  -'), ('url', 'UR  -'), ('abstract', 'N2  -'),
                                 ('publisher', 'PB  -'), ('doi', 'DO  -'),('eprintid', 'C1  - eprint:'),
                                 ('issn', 'SN  -'), ('endRecord', 'ER  -')]))
        if (export_format == self.EXPORT_FORMAT_REFMAN):
            return (OrderedDict([('doctype', 'TY  -'), ('title', 'TI  -'), ('author', 'AU  -'),
                                 ('aff', 'AD  -'), ('pub', 'JO  -'), ('volume', 'VL  -'),
                                 ('pubdate', 'Y1  -'), ('page', 'SP  -'), ('lastpage', 'EP  -'),
                                 ('keyword', 'KW  -'), ('url', 'UR  -'), ('abstract', 'N2  -'),
                                 ('publisher', 'PB  -'), ('doi', 'DO  -'), ('eprintid', 'C1  - eprint:'),
                                 ('issn', 'SN  -'), ('endRecord', 'ER  -')]))
        if (export_format == self.EXPORT_FORMAT_REFWORKS):
            return (OrderedDict([('doctype', 'RT'), ('title', 'T1'), ('author', 'A1'),
                                 ('editor', 'A2'), ('aff', 'AD'), ('pub', 'JF'),
                                 ('volume', 'VO'), ('year', 'YR'), ('pubdate', 'FD'),
                                 ('page', 'SP'), ('lastpage', 'OP'), ('keyword', 'K1'),
                                 ('url', 'LK'), ('comment', 'NO'), ('abstract', 'AB'),
                                 ('publisher', 'PB'),  ('doi', 'DO DOI:'), ('eprintid', 'DO eprintid:'),
                                 ('issn', 'SN')]))
        if (export_format == self.EXPORT_FORMAT_MEDLARS):
            return (OrderedDict([('doctype', 'PT  -'), ('title', 'TI  -'), ('author', 'AU  -'),
                                 ('aff', 'AD  -'), ('bibstem', 'TA  -'), ('pub_raw', 'SO  -'),
                                 ('volume', 'VI  -'), ('pubdate', 'DP  -'), ('page', 'PG  -'),
                                 ('url', '4099-'), ('abstract', 'AB  -'), ('issn', 'IS  -')]))


    def __add_author_list(self, a_doc, export_format, tag):
        """
        format authors

        :param a_doc:
        :param export_format:
        :param tag:
        :return:
        """
        if 'author' not in a_doc:
            return ''

        if (export_format == self.EXPORT_FORMAT_ADS):
            separator = '; '
            result = tag + ' '
            for author in a_doc['author']:
                result += author + separator
            # do not need the last separator
            if (len(result) > len(separator)):
                result = result[:-len(separator)]
            return self.__format_line_wrapped(result) + '\n'

        if (export_format == self.EXPORT_FORMAT_ENDNOTE) or (export_format == self.EXPORT_FORMAT_PROCITE) or \
            (export_format == self.EXPORT_FORMAT_REFMAN) or (export_format == self.EXPORT_FORMAT_REFWORKS) or \
            (export_format == self.EXPORT_FORMAT_MEDLARS):
            separator = '\n'
            result = ''
            for author in a_doc['author']:
                result += tag + ' ' + author + separator
            # do not need the last separator
            if (len(result) > len(separator)):
                result = result[:-len(separator)]
            return result + '\n'

        return ''


    def __add_editor_list(self, a_doc, export_format, tag):
        """
        format editors

        :param a_doc:
        :param export_format:
        :param tag:
        :return:
        """
        if 'editor' not in a_doc:
            return ''

        # only endnote and refworks output editor
        if (export_format == self.EXPORT_FORMAT_ENDNOTE) or (export_format == self.EXPORT_FORMAT_REFWORKS):
            separator = '\n'
            result = ''
            for editor in a_doc['editor']:
                result += tag + ' ' + editor + separator
            # do not need the last separator
            if (len(result) > len(separator)):
                result = result[:-len(separator)]
            return result + '\n'

        return ''


    def __get_affiliation_list(self, a_doc, export_format, tag):
        """
        format affiliation

        :param a_doc:
        :param export_format:
        :param tag:
        :return:
        """
        if ('aff') not in a_doc:
            return ''

        counter = self.generate_counter_id(len(a_doc['aff']))
        separator = ', '

        affiliation_list = ''
        for affiliation, i in zip(a_doc['aff'], range(len(a_doc['aff']))):
            if (affiliation != '-'):
                affiliation_list += counter[i] + '(' + affiliation + ')' + separator
        # do not need the last separator
        if (len(affiliation_list) > len(separator)):
            affiliation_list = affiliation_list[:-len(separator)]

        # if no affiliation was defined
        if (len(affiliation_list) == 0):
            return ''

        # if there is a tag, added to the beginning
        if (len(tag) > 0):
            affiliation_list = tag + ' ' + affiliation_list

        if (export_format == self.EXPORT_FORMAT_ADS):
            return self.__format_line_wrapped(affiliation_list) + '\n'

        return affiliation_list + '\n'


    def __add_doc_links_property(self, a_doc, tag):
        """
        format links that are defined in the property field
        :param a_doc:
        :param tag:
        :return:
        """
        link_dict = OrderedDict([
            ('TOC', ['TOC', 'Table of Contents']),
            ('LIBRARYCATALOG', ['LIBRARY', 'Library Entry']),
        ])
        link_list = ''
        next_line = ';\n'
        for link in link_dict:
            if link in a_doc.get('property', ''):
                link_list += tag + ' ' + link_dict[link][0] + ': ' + link_dict[link][1] + next_line
        return link_list


    def __add_doc_links_esource(self, a_doc, tag):
        """
        format links that are defined in the esource field

        :param a_doc:
        :param tag:
        :return:
        """
        link_dict = OrderedDict([
            # (link type:[name, access])
            ('EPRINT_HTML', 'arXiv Article'),
            ('AUTHOR_HTML', 'Author Article'),
            ('PUB_HTML', 'Publisher Article'),
            ('ADS_SCAN', 'Scanned Article (GIF)'),
            ('EPRINT_PDF', 'arXiv PDF'),
            ('AUTHOR_PDF', 'Author PDF'),
            ('PUB_PDF', 'Publisher PDF'),
            ('ADS_PDF', 'ADS PDF'),
        ])
        link_list = ''
        next_line = ';\n'
        for link in link_dict:
            if link.upper() in a_doc.get('esources', ''):
                link_list += tag + ' ' + link + ': ' + link_dict[link] + next_line
        return link_list


    def __add_doc_links_data(self, a_doc, tag):
        """
        format links that are defined in the data field

        :param a_doc:
        :param tag:
        :return:
        """
        link_dict = OrderedDict([
                        ('ARI', 'Astronomisches Rechen-Institut'),
                        ('SIMBAD', 'SIMBAD Database at the CDS'),
                        ('NED', 'NASA/IPAC Extragalactic Database'),
                        ('CDS', 'Strasbourg Astronomical Data Center'),
                        ('Vizier', 'VizieR Catalog Service'),
                        ('GCPD', 'The General Catalogue of Photometric Data'),
                        ('Author', 'Author Hosted Dataset'),
                        ('PDG', 'Particle Data Group'),
                        ('MAST', 'Mikulski Archive for Space Telescopes'),
                        ('HEASARC', '''NASA's High Energy Astrophysics Science Archive Research Center'''),
                        ('INES', 'IUE Newly Extracted Spectra'),
                        ('IBVS', 'Information Bulletin on Variable Stars'),
                        ('Astroverse', 'CfA Dataverse'),
                        ('ESA', 'ESAC Science Data Center'),
                        ('NExScI', 'NASA Exoplanet Archive'),
                        ('PDS', 'The NASA Planetary Data System'),
                        ('AcA', 'Acta Astronomica Data Files'),
                        ('ISO', 'Infrared Space Observatory'),
                        ('ESO', 'European Southern Observatory'),
                        ('CXO', 'Chandra X-Ray Observatory'),
                        ('NOAO', 'National Optical Astronomy Observatory'),
                        ('XMM', 'XMM Newton Science Archive'),
                        ('Spitzer', 'Spitzer Space Telescope'),
                        ('PASA', 'Publication of the Astronomical Society of Australia Datasets'),
                        ('ATNF', 'Australia Telescope Online Archive'),
                        ('KOA', 'Keck Observatory Archive'),
                        ('Herschel', 'Herschel Science Center'),
                        ('GTC', 'Gran Telescopio CANARIAS Public Archive'),
                        ('BICEP2', 'BICEP/Keck Data'),
                        ('ALMA', 'Atacama Large Millimeter/submillimeter Array'),
                        ('CADC', 'Canadian Astronomy Data Center'),
                        ('Zenodo', 'Zenodo Archive'),
                        ('TNS', 'Transient Name Server'),
                ])
        data_dict = {}
        for d in a_doc.get('data', ''):
            data_dict[d.split(':')[0]] = int(d.split(':')[1])
        link_list = ''
        next_line = ';\n'
        for link in link_dict:
            if link in data_dict.keys():
                link_list += tag + ' ' + link + ': ' + link_dict[link] + next_line
        return link_list


    def __add_doc_links(self, a_doc, tag):
        """
        format links

        :param a_doc:
        :param tag:
        :return:
        """
        link_dict = OrderedDict([
            # (link type:[include if, name, has count])
            ('abstract', [len(a_doc.get('abstract', '')), 'ABSTRACT', 'Abstract']),
            ('citations', [a_doc.get('num_citations', 0), 'CITATIONS', 'Citations to the Article']),
            ('reference', [a_doc.get('num_references', 0), 'REFERENCES', 'References in the Article']),
            ('coreads', [a_doc.get('read_count', 0), 'Co-Reads', 'Co-Reads']),
        ])
        link_list = ''
        next_line = ';\n'
        for link in link_dict:
            if (link_dict[link][0] > 0):
                link_list += tag + ' ' + link_dict[link][1] + ': ' + link_dict[link][2] + next_line

        link_list += self.__add_doc_links_property(a_doc, tag)
        link_list += self.__add_doc_links_esource(a_doc, tag)
        link_list += self.__add_doc_links_data(a_doc, tag)
        return link_list


    def __add_keywords(self, a_doc, export_format, tag):
        """
        format keywords

        :param a_doc:
        :param export_format:
        :param tag:
        :return:
        """
        if 'keyword' not in a_doc:
            return ''

        separator = {self.EXPORT_FORMAT_ADS:', ', self.EXPORT_FORMAT_ENDNOTE:'; ', self.EXPORT_FORMAT_PROCITE:'/ ',
                     self.EXPORT_FORMAT_REFMAN:'\n', self.EXPORT_FORMAT_REFWORKS:'\n'}

        if (export_format == self.EXPORT_FORMAT_ADS) or (export_format == self.EXPORT_FORMAT_ENDNOTE) or (export_format == self.EXPORT_FORMAT_PROCITE):
            result = tag + ' '
            for keyword in a_doc['keyword']:
                result += keyword + separator[export_format]
            # do not need the last separator
            if (len(result) > len(separator[export_format])):
                result = result[:-len(separator[export_format])]
            return self.__format_line_wrapped(result) + '\n'

        if (export_format == self.EXPORT_FORMAT_REFMAN) or (export_format == self.EXPORT_FORMAT_REFWORKS):
            result = ''
            for keyword in a_doc['keyword']:
                result += tag + ' ' + keyword + separator[export_format]
            # do not need the last separator
            if (len(result) > len(separator[export_format])):
                result = result[:-len(separator[export_format])]
            return result + '\n'
        return ''


    def __add_comment(self, a_doc):
        """

        :param a_doc:
        :return:
        """
        if a_doc.get('doctype', '') == 'eprint':
            pubnote = ''.join(a_doc.get('pubnote', ''))
            if len(pubnote) > 0:
                return pubnote

        comment = ''
        if 'comment' in a_doc:
            comment = ''.join(a_doc.get('comment', ''))
            if 'isbn' in a_doc:
                comment += ' ISBN: <ISBN>' + ', '.join(a_doc.get('isbn', '')) + '</ISBN>'
        return comment


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


    def __add_abstract(self, a_doc):
        """

        :param a_doc:
        :return:
        """
        # 9/21/2020 from Alberto
        # seeing how we have other markup in this output format (<SUB>, <SUP>, <A>, etc)
        # I would keep this markup as well, rather than replace it. This will generate an abstract
        # that fits in a single line and then can be post-processed by the end user as needed
        # return a_doc.get('abstract', '').replace('<P />', '\n').replace('<BR />', '\n')
        return a_doc.get('abstract', '')


    def __get_page(self, a_doc, export_format):
        """

        :param a_doc:
        :param export_format:
        :return:
        """
        # these formats display page range if available
        if (export_format == self.EXPORT_FORMAT_ENDNOTE) or (export_format == self.EXPORT_FORMAT_MEDLARS):
            page_range = a_doc.get('page_range', None)
            if page_range:
                return page_range
        # return first page
        return ''.join(a_doc.get('page', ''))


    def __get_last_page(self, page_range, export_format):
        """

        :param page_range:
        :param export_format:
        :return:
        """
        if not ((export_format == self.EXPORT_FORMAT_ENDNOTE) or (export_format == self.EXPORT_FORMAT_MEDLARS)):
            if (len(page_range) > 0) and ('-' in page_range):
                parts = page_range.split('-')
                if (len(parts[1]) > 0):
                    return parts[1]
        return ''


    def __add_in(self, field, value):
        """
        add the value into the return structure, only if a value was defined in Solr

        :param field:
        :param value:
        :return:
        """
        if ((isinstance(value, str) or isinstance(value, bytes)) and (len(value) > 0)) or \
           (isinstance(value, int) and (value is not None)):
            return field + ' ' + value + '\n'
        return ''


    def __add_pub(self, a_doc, export_format, tag):
        """

        :param a_doc:
        :param export_format:
        :param tag:
        :return:
        """
        if export_format == self.EXPORT_FORMAT_ENDNOTE:
            # there is an exception for endnote
            # depending on doctype different tags for Secondary Title is displayed
            # per Alberto, abstract is similar to proceedings 4/10/2024
            doctype = a_doc.get('doctype', '')
            if doctype in ['inbook', 'proceedings', 'inproceedings', 'abstract']:
                # Book or Conference Name
                tag = "%B"
            else:
                # Journal Name
                tag = "%J"
        return self.__add_in(tag, ''.join(a_doc.get('pub', '')))


    def __get_conf_loc(self, pub_raw):
        """
        return conference location

        :param pub_raw:
        :return:
        """
        match = self.re_conference_locations.search(pub_raw)
        if match:
            return match.group(1)
        return None


    def __get_doc(self, index, fields, export_format):
        """

        :param index:
        :param fields:
        :param export_format:
        :return:
        """
        result = ''
        a_doc = self.from_solr['response'].get('docs')[index]
        for field in fields:
            if field in ['title', 'doi', 'isbn', 'pubnote', 'issn']:
                result += self.__add_in(fields[field], ''.join(a_doc.get(field, '')))
            elif (field == 'pub'):
                result += self.__add_pub(a_doc, export_format, fields[field])
            elif (field == 'page'):
                result += self.__add_in(fields[field], self.__get_page(a_doc, export_format))
            elif (field == 'lastpage'):
                result += self.__add_in(fields[field], self.__get_last_page(a_doc.get('page_range', ''), export_format))
            elif (field == 'author'):
                result += self.__add_author_list(a_doc, export_format, fields[field])
            elif (field == 'editor'):
                result += self.__add_editor_list(a_doc, export_format, fields[field])
            elif (field == 'doctype'):
                result += self.__add_in(fields[field], self.__get_doc_type(a_doc.get(field, ''), export_format))
            elif (field == 'pubdate'):
                result += self.__add_in(fields[field], self.__format_date(a_doc.get(field, ''), export_format))
            elif (field == 'abstract'):
                # 9/18/2020 as per request of a user, no line wrapping abstract
                result += self.__add_in(fields[field], self.__add_abstract(a_doc))
            elif (field == 'aff'):
                result += self.__get_affiliation_list(a_doc, export_format, fields[field])
            elif (field == 'keyword'):
                result += self.__add_keywords(a_doc, export_format, fields[field])
            elif (field == 'comment'):
                result += self.__add_in(fields[field], self.__format_line_wrapped(self.__add_comment(a_doc)))
            elif (field == 'url'):
                result += self.__add_in(fields[field], current_app.config['EXPORT_SERVICE_FROM_BBB_URL'] + '/' + a_doc.get('bibcode', ''))
            elif (field == 'endRecord'):
                result += (fields[field] + '\n')
            elif (field == 'pub_raw'):
                if export_format == self.EXPORT_FORMAT_ENDNOTE:
                    if a_doc.get('doctype', '') in ['proceedings', 'inproceedings', 'abstract']:
                        result += self.__add_in(fields[field], self.__get_conf_loc(a_doc.get(field, '')))
                else:
                    result += self.__add_in(fields[field], self.__add_clean_pub_raw(a_doc))
            elif (field == 'links'):
                result += self.__add_doc_links(a_doc, fields[field])
            elif (field == 'eprintid'):
                result += self.__add_in(fields[field], get_eprint(a_doc))
            elif (field == 'bibstem'):
                result += self.__add_in(fields[field], a_doc.get(field, ['', ''])[0])
            elif (field == 'publisher'):
                result += self.__add_in(fields[field], a_doc.get(field, ''))
            else:
                result += self.__add_in(fields[field], a_doc.get(field, ''))
        # line feed once the doc is complete
        return result + '\n\n'


    def __get_fielded(self, export_format):
        """
        for each document from Solr, get the fields, and format them accordingly

        :param export_format:
        :return:
        """
        num_docs = 0
        results = []
        if (self.status == 0):
            fields = self.__get_tags(export_format)
            num_docs = self.get_num_docs()
            for index in range(num_docs):
                results += self.__get_doc(index, fields, export_format)
        result_dict = {}
        result_dict['msg'] = 'Retrieved {} abstracts, starting with number 1.'.format(num_docs)
        result_dict['export'] = ''.join(result for result in results)
        return result_dict


    def __setup_conf_loc(self):
        """
        4/10/2024 for now read the conference locations from the text file
        for EndNote format, soon it should be in solr
        """
        try:
            with open(os.path.dirname(__file__) + '/data/conf_loc.dat', 'r') as file:
                conference_locations = [line.strip() for line in file.readlines()]
                conference_locations.sort(key=lambda x: (-len(x), x))
                # replacing commas with \W to allow any punctuation (ie, Vienna, Austria and Vienna. Austria)
                self.re_conference_locations = re.compile(r'(%s)[\s,\.]+' % '|'.join(conference_locations).replace(',','\W'))
        except:
            current_app.logger.error('Error: unable to read conference location data file.')
            self.re_conference_locations = None

    def get_ads_fielded(self):
        """
        :return: ads formatted export
        """
        return self.__get_fielded(self.EXPORT_FORMAT_ADS)


    def get_endnote_fielded(self):
        """
        :return: endnote formatted export
        """
        self.__setup_conf_loc()
        return self.__get_fielded(self.EXPORT_FORMAT_ENDNOTE)


    def get_procite_fielded(self):
        """
        :return: procite formatted export
        """
        return self.__get_fielded(self.EXPORT_FORMAT_PROCITE)


    def get_refman_fielded(self):
        """
        :return: refman formatted export
        """
        return self.__get_fielded(self.EXPORT_FORMAT_REFMAN)


    def get_refworks_fielded(self):
        """
        :return: refworks formatted export
        """
        return self.__get_fielded(self.EXPORT_FORMAT_REFWORKS)


    def get_medlars_fielded(self):
        """
        :return: medlars formatted export
        """
        return self.__get_fielded(self.EXPORT_FORMAT_MEDLARS)

