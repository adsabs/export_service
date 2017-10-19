#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask import current_app
from itertools import product
from textwrap import fill
from string import ascii_uppercase
import re
import cgi

from adsutils.ads_utils import get_pub_abbreviation

from ads import adsFormatter, adsOrganizer
from cslJson import CSLJson
from csl import CSL
from toLaTex import encodeLaTex, encodeLaTexAuthor

# This class accepts JSON object created by Solr and can reformats it
# for the user define Custom Format Export.
# To get custom formatted data first pass in the custom format string
# to parse it and determine the Solr fields needed
#    customFormat = CustomFormat(customFormatStr)
#    customFormat.getSolrFields()
# Next pass the fields to Solr and get the JSON code back and finaly use
#    customFormat.setJSONFromSolr(jsonFromSolr)
#    customFormat.getCustomFormat()

class CustomFormat:
    customFormat = ''
    parsedSpec = []
    status = -1
    fromCSL = {}
    authorCount = {}

    def __init__(self, customFormat):
        self.customFormat = customFormat
        self.exportFormat = adsFormatter.unicode
        self.lineLength = 80
        self.header = ''
        self.footer = ''
        self.Enumeration = False
        self.__parse()

    # from the user specified specifiers, compile a list of fields to get from Solr
    def getSolrFields(self):
        solrFields = ''
        for element in self.parsedSpec:
            if element[2] not in solrFields:
                solrFields += element[2] + ','
        # make sure we always bring back the bibcode
        # note that if at some point we allow alternative bibcode to be part
        # of custom formating this line fails, but until then we should be OK
        if 'bibcode' not in solrFields:
            solrFields += 'bibcode,'
        # don't need the last comma
        return solrFields[:-len(',')]

    def __getNumAuthors(self):
        numAuthors = []
        for aDoc in self.fromSolr['response'].get('docs'):
            numAuthors.append(len(aDoc['author']))
        return numAuthors

    # save the data from Solr, and go through it
    # for every author format call CSL to style the authors
    def setJSONFromSolr(self, fromSolr):
        self.fromSolr = fromSolr
        if (self.fromSolr.get('responseHeader')):
            self.status = self.fromSolr['responseHeader'].get('status', self.status)
        jsonForCSL = CSLJson(self.fromSolr).getAuthor()
        for element in self.parsedSpec:
            if (element[2] == 'author'):
                # my mac has been formatted for case-insensitive
                # so need to make lower case doubled to be different
                # shall continue with this eventhough on the Linux side we shall be OK
                if (element[1][-1].isupper()):
                    cslFileName = 'ads-author-' + element[1][-1]
                else:
                    cslFileName = 'ads-author-' + element[1][-1] + element[1][-1]
                key = element[1]
                self.fromCSL[key] = CSL(jsonForCSL, cslFileName).get(adsOrganizer.bibliography)
                self.authorCount[key] = self.__getNumAuthors()

    def getStatus(self):
        return self.status

    def getNumDocs(self):
        if (self.status == 0):
            if (self.fromSolr.get('response')):
                return self.fromSolr['response'].get('numFound', 0)
        return 0

    # from specifier to Solr fields
    def __getSolrField(self, specifier):
        fieldDict = {
            'A': 'author',
            'a': 'author',
            'B': 'abstract',
            'c': 'citation_count',
            'C': 'copyright',
            'd': 'doi',
            'D': 'date',
            'F': 'aff',
            'G': 'author',
            'g': 'author',
            'H': 'author',
            'h': 'author',
            'I': 'author',
            'J': 'pub',
            'j': 'pub',
            'K': 'keyword',
            'L': 'author',
            'l': 'author',
            'M': 'author',
            'm': 'author',
            'N': 'author',
            'n': 'author',
            'O': '',  # Object Names
            'p': 'page',
            'P': 'lastpage',  # Last Page
            'Q': 'pub_raw',
            'q': 'pub',
            'R': 'bibcode',
            'T': 'title',
            'U': 'url',
            'u': 'url',
            'V': 'volume',
            'W': 'doctype',
            'X': 'pub_raw',
            'x': 'comment',
            'Y': 'year'
        }
        specifier = specifier[-1]
        return fieldDict.get(specifier, '')

    def __setExportFormat(self, format):
        # format can be one of the followings: unicode, html, latex
        if (format == 'unicode'):
            self.exportFormat = adsFormatter.unicode
        elif (format == 'html'):
            self.exportFormat = adsFormatter.html
        elif (format == 'latex'):
            self.exportFormat = adsFormatter.latex
        else:
            self.exportFormat = adsFormatter.unicode

    # see if enumeration specifier has been defined in the custom format string
    def __parseEnumeration(self):
        matches = re.findall(r'(%z)', self.customFormat)
        if (len(matches) >= 1):
            for match in matches:
                self.customFormat = re.sub(match, '', self.customFormat)
                self.Enumeration = True

    # see if commond specifier has been defined in the custom format string
    def __parseCommand(self):
        command = [
            r'(%Z(?:Encoding|Linelength):(?:unicode|html|latex|\d+)\s?)',
            r'(%Z(?:Header|Footer):\".+?\"\s?)',
        ]
        for token in command:
            matches = re.findall(token, self.customFormat)
            if (len(matches) >= 1):
                for match in matches:
                    self.customFormat = self.customFormat.replace(match, '', len(match))
                    # remove %Z and split on :
                    parts = match[2:].split(':')
                    if (len(parts) == 2):
                        if (parts[0] == 'Encoding'):
                            self.__setExportFormat(parts[1])
                        elif (parts[0] == 'Linelength'):
                            self.lineLength = int(parts[1])
                        elif (parts[0] == 'Header'):
                            self.header = parts[1].replace('"', '').decode('string_escape')
                        elif (parts[0] == 'Footer'):
                            self.footer = parts[1].replace('"', '').decode('string_escape')

    # parse the custom format string to identify the requested fields
    def __parse(self):
        cfmt = '''(                                     # start of capture group 1
            %                                           # literal "%"
            (?:                                         # first option
            (?:\d+|\*)?                                 # width
            (?:\.(?:\d+|\*))?                           # precision
            [AaBcCdDEFGgHhIJjKLlMmNnOpPQqRSTUuVWXxY]    # type
            )
        )'''
        self.parsedSpec = []
        self.__parseCommand()
        self.__parseEnumeration()
        for m in re.finditer(cfmt, self.customFormat, flags=re.X):
            self.parsedSpec.append(tuple((m.start(1), m.group(1), self.__getSolrField(m.group(1)))))

    def __formatDate(self, solrDate, dateFormat):
        # solrDate has the format 2017-12-01T00:00:00Z
        dateTime = datetime.strptime(solrDate, '%Y-%m-%dT%H:%M:%SZ')
        formats = {'D': '%Xm/%Y', 'Y': '%Y'}
        return dateTime.strftime(formats[dateFormat]).replace('X0', 'X').replace('X', '')

    def __formatURL(self, bibcode, urlFormat):
        # U: has form: <a href="url">bibcode</a>
        # u: has the form: url/bibcode
        formats = {'U': u'<a href="{}">{}</a>', 'u': u'{}/{}'}
        path = current_app.config['EXPORT_SERVICE_BBB_PATH']
        if (len(bibcode) > 0):
            return formats[urlFormat].format(path, bibcode)
        return ''

    def __formatLineWrapped(self, text, index):
        # remove line break if any
        text = text.replace('\\n', '')

        formatStyle = u'{0:>2} {1}'
        if (self.lineLength == 0):
            # no linewrap here, so just adjust the linefeed if exists
            if (self.Enumeration):
                result = formatStyle.format(index+1, text)
            else:
                result = text
        else:
            if (self.Enumeration):
                wrapped = fill(text, width=self.lineLength, subsequent_indent=' ' * 4, replace_whitespace=False)
                result = formatStyle.format(index+1, wrapped)
            else:
                result = fill(text, width=self.lineLength, replace_whitespace=False)
        return result + '\n'

    def __getAffiliationList(self, aDoc):
        if ('aff') in aDoc:
            counter = [''.join(i) for i in product(ascii_uppercase, repeat=2)]
            separator = '; '
            affiliationList = ''
            for affiliation, i in zip(aDoc['aff'], range(len(aDoc['aff']))):
                affiliationList += counter[i] + '(' + affiliation + ')' + separator
            # do not need the last separator
            if (len(affiliationList) > len(separator)):
                affiliationList = affiliationList[:-len(separator)]
            return affiliationList
        return ''

    def __getNAuthors(self, authorList, n, separator, nPartsAuthor, beforeLast):
        splitParts = authorList.replace(beforeLast, '').split(separator)
        if (n == 1):
            return separator.join(splitParts[:nPartsAuthor])
        if (len(beforeLast) == 0):
            beforeLast = ' '
        return separator.join(splitParts[:(n - 1) * nPartsAuthor]) + beforeLast + separator.join(splitParts[(n - 1) * nPartsAuthor:n * nPartsAuthor])

    def __getAuthorListShorten(self, authorList, numAuthors, format, m, n):

        # Formats	First Author	Second Author..	Before Last	    shorten
        # A	        As in db	    As in db	    and	            first author, et al.
        # G	        lastname f. i.	lastname f. i.	                first author, et al.
        # H	        lastname	    lastname	    and	            display requested number of authors
        # I	        lastname f. i.	f. i. lastname	and	            first author, and xx colleagues
        # L	        lastname, f. i.	lastname, f. i.	and	            first author, and xx colleagues
        # N	        lastname, f. i.	lastname, f. i.		            first author, and xx colleagues
        # l	        lastname, f. i.	lastname, f. i.	&	            first author, et al.
        # M	        lastname	    lastname	and	                first author, et al.
        # m	        lastname	    lastname	&	                first author, et al.
        # n	        lastname	    +
        # a	        lastname
        # g	        lastname, f.i.	lastname, f.i.	and	            first author, and xx colleagues
        # h	        lastname	    lastname	    and	            first author \emph{et al.}

        # n.m: Maximum number of entries in field (optional).
        # If the number of authors in the list is larger than n, the list will be truncated and returned as
        # "author1, author2, ..., authorm, et al.". If m is not specified, n.1 is assumed.

        formatEtAl = u'{}, et al.'
        formatNAuthors = u'{} and {}'
        formatWithNColleagues = u'{}, and {} colleagues'
        formatEscapeEmph = u'{} \emph{{et al.}}'
        formatPlus = u'{}+'

        if (numAuthors <= n) or (numAuthors <= m):
            return authorList
        if (format == 'A'):
            # in db we have LastName, FirstName (or FirstInitial.) MiddleInitial.
            # hence the first part is the LastName
            return formatEtAl.format(self.__getNAuthors(authorList, n, u',', 2, u', and'))
        if (format == 'G'):
            # return LastName et. al. - list is separated by a space
            return formatEtAl.format(self.__getNAuthors(authorList, n, u' ', 2, u''))
        if (format == 'M'):
            # return n authors (LastName) et. al. - list is separated by a comma
            return formatEtAl.format(self.__getNAuthors(authorList, n, u',', 1, u', and'))
        if (format == 'm'):
            # return n authors (LastName) et. al. - list is separated by a space
            return formatEtAl.format(self.__getNAuthors(authorList, n, u',', 1, u', \&'))
        if (format == 'H'):
            # return the asked number of authors - list is separated by space,
            # there is an and before the last author
            authors = authorList.split(' ')
            if (m == 1):
                return authors[0]
            else:
                authors.remove('and')
                return formatNAuthors.format(' '.join(authors[:m-1]), authors[m])
        if (format == 'I'):
            # return LastName and count - list is separated by a space
            authors = authorList.split(',')
            return formatWithNColleagues.format(authors[0], numAuthors-1)
        if (format == 'L') or (format == 'N') or (format == 'g'):
            # return LastName and count list is separated by a comma
            authors = authorList.split(',')
            return formatWithNColleagues.format(authors[0], numAuthors-1)
        if (format == 'l'):
            # return n author(s) et. al. - list is separated by a comma
            return formatEtAl.format(self.__getNAuthors(authorList, n, u',', 2, u' \&'))
        if (format == 'h'):
            authors = authorList.split(' ')
            return formatEscapeEmph.format(authors[0])
        if (format == 'n'):
            authors = authorList.split(' ')
            return formatPlus.format(authors[0])
        if (format == 'a'):
            # return first authors Lastname only
            # this is already done at the CSL level so just return what was passed in
            return authorList
        return authorList

    def __getAuthorList(self, format, index):
        authors = self.fromCSL.get(format)[index]
        count = self.authorCount.get(format)[index]
        # see if author list needs to get shorten
        # n.m: Maximum number of entries in author field (optional).
        # If the number of authors in the list is larger than n, the list will be truncated to m entries.
        # If.m is not specified, n.1 is assumed.
        matches = re.findall(r'%(\d*\.?\d*)(\w)', format)
        if (len(matches) >= 1) and (len(matches[0][0]) > 0):
            shorten = matches[0][0].split('.')
            if (len(shorten) > 1):
                return self.__getAuthorListShorten(authors, count, matches[0][1], int(str(shorten[0])), int(str(shorten[1])))
            else:
                return self.__getAuthorListShorten(authors, count, matches[0][1], int(str(shorten[0])), 1)
        return authors

    def __getKeywords(self, aDoc):
        if ('keyword') in aDoc:
            separator = ', '
            keywordList = ''
            for keyword in aDoc['keyword']:
                keywordList += keyword + separator
            # do not need the last separator
            if (len(keywordList) > len(separator)):
                keywordList = keywordList[:-len(separator)]
            return keywordList
        return ''

    # parse pub_raw and eliminate tags
    def __addCleanPubRaw(self, aDoc):
        pubRaw = ''.join(aDoc.get('pub_raw', ''))
        # proceed only if necessary
        if ('<' in pubRaw) and ('>' in pubRaw):
            tokens = dict([
                (r"(\;?\s*\<ALTJOURNAL\>.*\</ALTJOURNAL\>\s*)",     r""),          # remove these
                (r"(\;?\s*\<CONF_METADATA\>.*\<CONF_METADATA\>\s*)",r""),
                (r"(?:\<ISBN\>)(.*)(?:\</ISBN\>)",                  r"\1"),        # get value inside the tag for these
                (r"(?:\<NUMPAGES\>)(.*)(?:</NUMPAGES>)",            r"\1"),
            ])
            for key in tokens:
                regex = re.compile(key)
                pubRaw = regex.sub(tokens[key], pubRaw)
        return pubRaw

    def __getPublication(self, format, aDoc):
        format = format[-1]
        if (format == 'J'):
            # returns the journal name
            return aDoc.get('pub', '')
        if (format == 'j'):
            # returns an AASTeX macro for the journal if available, otherwise
            # returns the journal name
            journalMacros = dict([(k, v) for k, v in current_app.config['EXPORT_SERVICE_AASTEX_JOURNAL_MACRO']])
            return journalMacros.get(aDoc.get('pub', '').replace('The ', ''), aDoc.get('pub', ''))
        if (format == 'Q'):
            # returns the full journal information
            return self.__addCleanPubRaw(aDoc)
        if (format == 'q'):
            # returns the journal abbreviation
            abbreviation = get_pub_abbreviation(aDoc.get('pub', ''), numBest=1, exact=True)
            if (len(abbreviation) > 0):
                return abbreviation[0][1].strip('.')
            return ''
        return ''

    def __encode(self, text, name):
        if (self.exportFormat == adsFormatter.unicode):
            return text
        elif (self.exportFormat == adsFormatter.html):
            return cgi.escape(text)
        elif (self.exportFormat == adsFormatter.latex):
            if (name == 'author'):
                return encodeLaTexAuthor(text)
            # do not encode publication since it could be the macro
            if (name == 'pub'):
                return text
            else:
                return encodeLaTex(text)
        return text

    def __addIn(self, result, field, value):
        if (len(value) > 0):
            return result.replace(field[1], self.__encode(value, field[2]))
        else:
            precede = r'(\\?[\(|\{|\[|\"]?(\\\\[a-z]{2}\s)?[\\|\s|,|-]?'
            succeed = r'[\\|,]?[\)|\}|\]|\"]?[\\|,]?)'
            return re.sub(precede + field[1] + succeed, '', result)

    def __getDoc(self, index):
        result = self.customFormat
        aDoc = self.fromSolr['response'].get('docs')[index]
        for field in self.parsedSpec:
            if (field[2] == 'title') or (field[2] == 'page') or (field[2] == 'lastpage') or \
               (field[2] == 'doi') or (field[2] == 'comment'):
                result = self.__addIn(result, field, ''.join(aDoc.get(field[2], '')))
            elif (field[2] == 'author'):
                result = self.__addIn(result, field, self.__getAuthorList(field[1], index))
            elif (field[2] == 'doctype'):
                result = self.__addIn(result, field, self.__getDocType(aDoc.get(field[2], '')))
            elif (field[2] == 'date'):
                result = self.__addIn(result, field, self.__formatDate(aDoc.get(field[2], ''), field[1][-1]))
            elif (field[2] == 'aff'):
                result = self.__addIn(result, field, self.__getAffiliationList(aDoc))
            elif (field[2] == 'keyword'):
                result = self.__addIn(result, field, self.__getKeywords(aDoc))
            elif (field[2] == 'url'):
                result = self.__addIn(result, field, self.__formatURL(aDoc.get('bibcode', ''), field[1][-1]))
            elif (field[2] == 'abstract') or (field[2] == 'copyright') or (field[2] == 'bibcode') or \
                 (field[2] == 'volume') or (field[2] == 'year'):
                result = self.__addIn(result, field, aDoc.get(field[2], ''))
            elif (field[2] == 'pub') or (field[2] == 'pub_raw'):
                result = self.__addIn(result, field, self.__getPublication(field[1], aDoc))
            elif (field[2] == 'citation_count'):
                result = self.__addIn(result, field, str(aDoc.get(field[2], '')))
        return self.__formatLineWrapped(result, index)

    def get(self):
        results = []
        if (self.status == 0):
            results.append(self.header + '\n')
            for index in range(self.getNumDocs()):
                results.append(self.__getDoc(index))
            results.append('\n' + self.footer)
        return ''.join(result for result in results)
