# -*- coding: utf-8 -*-

from flask import current_app
from citeproc import Citation, CitationItem
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import formatter
from citeproc.py2compat import *
from citeproc.source.json import CiteProcJSON
import re
import os

from exportsrv.formatter.ads import adsFormatter, adsOrganizer
from exportsrv.formatter.format import Format
from exportsrv.formatter.toLaTex import encode_laTex, encode_laTex_author, html_to_laTex

# This class accepts JSON and sends it to citeproc library to get reformated
# We are supporting 7 complete cls (formatting all the fields) and 13 syles that
# only format authors, used for custom format
# citeproc provides the plain and html export format, and for export we also need
# latex that is implemented.

class CSL:

    REGEX_TOKENIZE_CITA = re.compile(r'^(.*)\(?(\d{4})\)?')
    REGEX_TOKENIZE_BIBLIO = re.compile(r'^(.*?)(\\?\s*\d+.*)')


    def __init__(self, for_cls, csl_style, export_format=adsFormatter.unicode):
        """

        :param for_cls: input data for this class
        :param csl_style: export journal style
        :param export_format: export format
        """
        self.for_cls = for_cls
        self.csl_style = csl_style
        self.export_format = export_format
        self.citation_item = []
        self.bibcode_list = []

        self.__update_title()

        # Process the JSON data to generate a citaproc-py BibliographySource.
        bib_source = CiteProcJSON(self.for_cls)

        csl_style_fullpath = os.path.realpath(__file__ + "/../../cslstyles")

        # load a CSL style (from the current directory)
        bib_style = CitationStylesStyle(os.path.join(csl_style_fullpath + '/' + csl_style), validate=False)

        # Create the citaproc-py bibliography, passing it the:
        # * CitationStylesStyle,
        # * BibliographySource (CiteProcJSON in this case), and
        # * a formatter (plain, html, or you can write a custom formatter)
        # we are going to have CSL format everything using html and then format it as we need to match the
        # classic output
        self.bibliography = CitationStylesBibliography(bib_style, bib_source, formatter.html)

        # Processing citations in a document needs to be done in two passes as for some
        # CSL styles, a citation can depend on the order of citations in the
        # bibliography and thus on citations following the current one.
        # For this reason, we first need to register all citations with the
        # CitationStylesBibliography.

        for item in self.for_cls:
            citation = Citation([CitationItem(item['id'])])
            self.citation_item.append(citation)
            self.bibliography.register(citation)
            # this is actually a bibcode that was passed in, but we have to use
            # one of CSLs predefined ids
            self.bibcode_list.append(''.join(item.get('locator', '')))


    def __update_title(self):
        """
        Update the container-title if needed for the specific style
        also apply latex encoding if needed for both title and container-title

        :return:
        """
        # for mnras we need abbreviation of the journal names
        # available from adsutils
        if (self.csl_style == 'mnras'):
            for data in self.for_cls:
                data['container-title'] = Format(None).get_pub_abbrev(data['bibstem'])
                data['title'] = encode_laTex(data['title'])
        # for AASTex we need a macro of the journal names
        elif (self.csl_style == 'aastex') or (self.csl_style == 'aasj') or (self.csl_style == 'aspc'):
            journal_macros = dict([(k, v) for k, v in current_app.config['EXPORT_SERVICE_AASTEX_JOURNAL_MACRO']])
            for data in self.for_cls:
                data['container-title'] = journal_macros.get(Format(None).get_bibstem(data['bibstem']), encode_laTex(data['container-title']))
                data['title'] = encode_laTex(data['title'])
        # for SoPh we use journal abbreviation for some special journals only
        elif (self.csl_style == 'soph'):
            journal_abbrevation = current_app.config['EXPORT_SERVICE_SOPH_JOURNAL_ABBREVIATION']
            for data in self.for_cls:
                data['container-title'] = journal_abbrevation.get(Format(None).get_bibstem(data['bibstem']), encode_laTex(data['container-title']))
                data['title'] = encode_laTex(data['title'])
        # for the rest just run title and container-title through latex encoding
        elif (self.csl_style == 'icarus') or (self.csl_style == 'apsj'):
            for data in self.for_cls:
                data['container-title'] = encode_laTex(data['container-title'])
                data['title'] = encode_laTex(data['title'])


    def __update_author_etal(self, author, the_rest, bibcode):
        """

        :param author:
        :param bibcode:
        :return:
        """
        # for icarus we need to add # authors beside the first author
        # in case more authors were available CSL would turn it into first author name et. al.
        # hence, from CSL we get something like Siltala, J. et al.\
        # but we need to turn it to Siltala, J., and 12 colleagues
        if (self.csl_style == 'icarus'):
            if (' et al.' in author):
                for data in self.for_cls:
                    if (data['locator'] == bibcode):
                        author = author.replace(' et al.', ', and {} colleagues'.format(len(data['author']) - 1))
                        the_rest = the_rest.lstrip('\\')
        elif (self.csl_style == 'soph'):
            if ('et al.' in author):
                author = author.replace('et al.', 'and, ...')
        return author, the_rest


    def __update_author_etal_add_emph(self, author):
        """

        :param author:
        :return:
        """
        # for Solar Physics we need to put et al. in \emph, which was not do able on the CLS
        # side, and hence we need to add it here
        # but note that it only applies if the output format is in latex format
        if (self.csl_style == 'soph'):
            if ('et al.' in author) and (self.export_format == adsFormatter.latex):
                return author.replace('et al.', '\emph{et al.}')
        return author


    def __tokenize_cita(self, cita):
        """

        :param cita: citation
        :return:
        """
        # cita (citation) is author(s) followed by year inside a parentheses
        # first remove the parentheses and then split the author and year fields
        cita = self.REGEX_TOKENIZE_CITA.findall(cita[1:-1])
        cita_author, cita_year = cita[0]
        return cita_author.strip(' ').rstrip('('), cita_year.strip(' ')


    def __tokenize_biblio(self, biblio):
        """

        :param biblio: bibliography
        :return:
        """
        # split the author and rest of biblio
        biblio = self.REGEX_TOKENIZE_BIBLIO.findall(biblio)
        biblio_author, biblio_rest = biblio[0]
        return biblio_author, biblio_rest


    def __format_output(self, cita, biblio, bibcode, index):
        """

        :param cita:
        :param biblio:
        :param bibcode:
        :param index:
        :return:
        """
        # apsj is a special case, display biblio as csl has format, just adjust translate characters for LaTex
        if (self.csl_style == 'apsj'):
            cita_author, cita_year = '', ''
            biblio_author = cita
            biblio_rest = biblio.replace(cita,'')
            # do not need this, but since we are sending the format all the fields, empty bibcode
            bibcode = ''
        else:
            cita_author, cita_year = self.__tokenize_cita(cita)
            biblio_author, biblio_rest = self.__tokenize_biblio(biblio)

        # encode author if latex format
        if (self.export_format == adsFormatter.latex):
            cita_author = encode_laTex_author(cita_author)
            biblio_author = encode_laTex_author(biblio_author)

        # some adjustments to the what is returned from CSL that we can not do with CSL
        cita_author = html_to_laTex(self.__update_author_etal_add_emph(cita_author))
        biblio_author, biblio_rest = self.__update_author_etal(biblio_author, biblio_rest, bibcode)
        biblio_author = html_to_laTex(biblio_author)
        biblio_rest = html_to_laTex(biblio_rest)

        format_style = {
            'mnras': u'\\bibitem[\\protect\\citeauthoryear{{{}}}{{{}}}]{{{}}} {}{}',
            'icarus': u'\\bibitem[{}({})]{{{}}} {}{}',
            'soph': u'\\bibitem[{}({})]{{{}}}{}{}',
            'aastex': u'\\bibitem[{}({})]{{{}}} {}{}',
            'aspc': u'\\bibitem[{}({})]{{{}}} {}{}',
            'aasj': u'\\bibitem[{}({})]{{{}}} {}{}',
            'apsj': u'{}{}{}{}{}'
        }
        return format_style[self.csl_style].format(cita_author, cita_year, bibcode, biblio_author, biblio_rest)


    def get(self, export_organizer=adsOrganizer.plain):
        """

        :param export_organizer: output format, default is plain
        :return: for adsOrganizer.plain returns the result of formatted records in a dict
        """
        results = []
        if (export_organizer == adsOrganizer.plain):
            num_docs = 0
            if (self.export_format == adsFormatter.unicode) or (self.export_format == adsFormatter.latex):
                num_docs = len(self.bibcode_list)
                for cita, item, bibcode, i in zip(self.citation_item, self.bibliography.bibliography(), self.bibcode_list, range(len(self.bibcode_list))):
                    results.append(self.__format_output(str(self.bibliography.cite(cita, '')), str(item), bibcode, i+1) + '\n')
            result_dict = {}
            result_dict['msg'] = 'Retrieved {} abstracts, starting with number 1.'.format(num_docs)
            result_dict['export'] = ''.join(result for result in results)
            return result_dict
        if (export_organizer == adsOrganizer.citation_bibliography):
            for cita, item, bibcode in zip(self.citation_item, self.bibliography.bibliography(), self.bibcode_list):
                results.append(bibcode + '\n' + str(self.bibliography.cite(cita, '')) + '\n' + str(item) + '\n')
            return ''.join(result for result in results)
        if (export_organizer == adsOrganizer.bibliography):
            for item in self.bibliography.bibliography():
                results.append(html_to_laTex(str(item)))
            return results
        return None
