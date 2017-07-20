#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from citeproc import Citation, CitationItem
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import formatter
from citeproc.py2compat import *
from citeproc.source.json import CiteProcJSON
import re
import os

from adsutils.ads_utils import get_pub_abbreviation

from ads import adsFormatter, adsOrganizer
from toLaTex import encodeLaTex, encodeLaTexAuthor, htmlToLaTex

# This class accepts JSON and sends it to citeproc library to get reformated
# We are supporting 7 complete cls (formatting all the fields) and 13 syles that
# only format authors, used for custom format
# citeproc provides the plain and html export format, and for export we also need
# latex that is implemented.

class CSL:
    citationItem = []
    bibcodeList = []

    def __init__(self, forCSL, cslStyle, exportFormat=adsFormatter.unicode):
        self.forCSL = forCSL
        self.cslStyle = cslStyle
        self.exportFormat = exportFormat

        # Update the container-title if needed for the specific style
        self.__updateContainerTitle()

        # Process the JSON data to generate a citaproc-py BibliographySource.
        bibSource = CiteProcJSON(self.forCSL)

        cslStyleFullPath = os.path.realpath(__file__ + "/../../cslStyles/")

        # load a CSL style (from the current directory)
        bibStyle = CitationStylesStyle(os.path.join(cslStyleFullPath, cslStyle+'.csl'), validate=False)

        # Create the citaproc-py bibliography, passing it the:
        # * CitationStylesStyle,
        # * BibliographySource (CiteProcJSON in this case), and
        # * a formatter (plain, html, or you can write a custom formatter)
        # we are going to have CSL format everything using html and then format it as we need to match the
        # classic output
        self.bibliography = CitationStylesBibliography(bibStyle, bibSource, formatter.html)

        # Processing citations in a document needs to be done in two passes as for some
        # CSL styles, a citation can depend on the order of citations in the
        # bibliography and thus on citations following the current one.
        # For this reason, we first need to register all citations with the
        # CitationStylesBibliography.

        for item in self.forCSL:
            citation = Citation([CitationItem(item['id'])])
            self.citationItem.append(citation)
            self.bibliography.register(citation)
            # this is actually a bibcode that was passed in, but we have to use
            # one of CSLs predefined ids
            self.bibcodeList.append(''.join(item.get('locator', '')))

    def __updateContainerTitle(self):
        # for mnras we need abbreviation of the journal names
        # available from adsutils
        if (self.cslStyle == 'mnras'):
            for data in self.forCSL:
                journal = data['container-title']
                abbreviation = get_pub_abbreviation(journal, numBest=1, exact=True)
                if (len(abbreviation) > 0):
                    journal = abbreviation[0][1].strip('.')
                data['container-title'] = journal
        # for AASTex we need a macro of the journal names
        if (self.cslStyle == 'aastex'):
            journalMacros = dict([(k, v) for k, v in current_app.config['EXPORT_SERVICE_AASTEX_JOURNAL_MACRO']])
            for data in self.forCSL:
                data['container-title'] = journalMacros.get(data['container-title'].replace('The ', ''), data['container-title'])

    def __updateAuthorEtAl(self, author, bibcode):
        # for Icarus we need to add # authors beside the first author
        # in case more authors were available CSL would turn it into first author name et. al.
        # hence, from CSL we get something like Siltala, J. et al.\
        # but we need to turn it to Siltala, J., and 12 colleagues
        if (self.cslStyle == 'Icarus'):
            if (' et al.\\' in author):
                for data in self.forCSL:
                    if (data['locator'] == bibcode):
                        return author.replace(' et al.\\', ', and {} colleagues'.format(len(data['author']) - 1))
        elif (self.cslStyle == 'soph'):
            if ('et al.' in author):
                return author.replace('et al.', 'and, ...')
        return author

    def __updateAuthorEtAlAddEmph(self, author):
        # for Solar Physics we need to put et al. in \emph, which was not do able on the CLS
        # side, and hence we need to add it here
        # but note that it only applies if the output format is in latex format
        if (self.cslStyle == 'soph'):
            if ('et al.' in author) and (self.exportFormat == adsFormatter.latex):
                return author.replace('et al.', '\emph{et al.}')
        return author

    def __updateBeforeLastAuthor(self, author):
        # there is a bug in CSL that does not insert the last comma, so we have to do it ourselves.
        if (self.cslStyle == 'mnras') or (self.cslStyle == 'aastex'):
            return author.replace(' et al.', ', et al.')
        if (self.cslStyle == 'soph'):
            return author.replace(' and', ', and')
        return author

    def __tokenizeCita(self, cita):
        regex = re.compile(r'^(.*)\(?(\d{4})\)?')
        # cita (citation) is author(s) followed by year inside a parentheses
        # first remove the parentheses and then split the author and year fields
        cita = regex.findall(cita[1:-1])
        citaAuthor, citaYear = cita[0]
        return citaAuthor.strip(' '), citaYear.strip(' ')

    def __tokenizeBiblio(self, biblio):
        regex = re.compile(r'^(.*?)(\d+.*)')
        # split the author and rest of biblio
        biblio = regex.findall(biblio)
        biblioAuthor, biblioRest = biblio[0]
        return biblioAuthor, biblioRest.strip(' ')

    def __formatOutput(self, cita, biblio, bibcode):
        # not yet verified that CLS is formatted correctly
        if (self.cslStyle == 'apsj') or (self.cslStyle == 'aspc') or (self.cslStyle == 'aasj'):
            return ''

        citaAuthor, citaYear = self.__tokenizeCita(cita)
        biblioAuthor, biblioRest = self.__tokenizeBiblio(biblio)
        # some adjustments to the what is returned from CSL that we can not do with CSL
        citaAuthor = htmlToLaTex(self.__updateBeforeLastAuthor(self.__updateAuthorEtAlAddEmph(citaAuthor)))
        biblioAuthor = htmlToLaTex(self.__updateBeforeLastAuthor(self.__updateAuthorEtAl(str(biblioAuthor), bibcode)))
        biblioRest = htmlToLaTex(biblioRest)

        # encode latex stuff
        if (self.exportFormat == adsFormatter.latex):
            citaAuthor = citaAuthor.replace(" &", " \&")
            biblioAuthor = encodeLaTexAuthor(biblioAuthor)
            biblioRest = encodeLaTex(biblioRest).decode('string_escape').replace('\{', '{').replace('\}', '}')

        formatStyle = {
            'mnras': u'\\bibitem[\\protect\\citaauthoryear{{{}}}{{{}}}]{{{}}} {}{}',
            'Icarus': u'\\bibitem[{}({})]{{{}}} {}{}',
            'soph': u'\\bibitem[{}({})]{{{}}}{}{}',
            'aastex': u'\\bibitem[{}({})]{{{}}} {}{}',
            'apsj': u'({}{}){{{}}}{}{}',
            'aspc': u'({}{}){{{}}}{}{}',
            'aasj': u'({}{}){{{}}}{}{}',
        }
        return formatStyle[self.cslStyle].format(citaAuthor, citaYear, bibcode, biblioAuthor, biblioRest)

    def get(self, exportOrganizer=adsOrganizer.plain):
        if (exportOrganizer == adsOrganizer.plain):
            if (self.exportFormat == adsFormatter.unicode) or (self.exportFormat == adsFormatter.latex):
                results = ''
                for cita, item, bibcode in zip(self.citationItem, self.bibliography.bibliography(), self.bibcodeList):
                    results += (self.__formatOutput(str(self.bibliography.cite(cita, '')), str(item), bibcode)) + '\n'
                return results
        elif (exportOrganizer == adsOrganizer.citationANDbibliography):
            results = ''
            for cita, item, bibcode in zip(self.citationItem, self.bibliography.bibliography(), self.bibcodeList):
                results += (bibcode + '\n' + str(self.bibliography.cite(cita, '')) + '\n' + str(item)) + '\n'
            return results
        elif (exportOrganizer == adsOrganizer.bibliography):
            results = []
            for item in self.bibliography.bibliography():
                results.append(htmlToLaTex(str(item)))
            return results
        return None
