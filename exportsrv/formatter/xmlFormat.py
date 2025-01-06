# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from collections import OrderedDict
from datetime import datetime
from flask import current_app
from textwrap import fill
import re

from exportsrv.formatter.format import Format
from exportsrv.formatter.ads import adsOutputFormat
from exportsrv.utils import get_eprint
from exportsrv.formatter.strftime import strftime

# This class accepts JSON object created by Solr and can reformat it
# for the XML Export formats we are supporting.
# 1- To get Dublin Core XML use
#    dublinXML = XMLFormat(jsonFromSolr).get_dublincore_xml()
# 2- To get Reference XML without Abstract use
#    referenceXML = XMLFormat(jsonFromSolr).get_reference_xml()
# 3- To get Reference XML with Abstract use
#    referenceXML = XMLFormat(jsonFromSolr).get_reference_xml(True)
# 4- To get JATS XML use
#    referenceXML = XMLFormat(jsonFromSolr).get_jats_xml(True)

class XMLFormat(Format):

    EXPORT_FORMAT_REF_XML = 'ReferenceXML'
    EXPORT_FORMAT_REF_ABS_XML = 'ReferenceAbsXML'
    EXPORT_FORMAT_DUBLIN_XML = 'DublinXML'
    EXPORT_FORMAT_JATS_XML = 'JATSXML'

    EXPORT_SERVICE_RECORDS_SET_XML_REF = [('xmlns', 'https://ads.harvard.edu/schema/abs/1.1/references'),
                                          ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
                                          ('xsi:schemaLocation', 'https://ads.harvard.edu/schema/abs/1.1/references https://ads.harvard.edu/schema/abs/1.1/references.xsd')]

    EXPORT_SERVICE_RECORDS_SET_XML_REF_ABS = [('xmlns', 'https://ads.harvard.edu/schema/abs/1.1/abstracts'),
                                              ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
                                              ('xsi:schemaLocation', 'https://ads.harvard.edu/schema/abs/1.1/abstracts https://ads.harvard.edu/schema/abs/1.1/abstracts.xsd')]

    EXPORT_SERVICE_RECORDS_SET_XML_DUBLIN = [('xmlns', 'https://ads.harvard.edu/schema/abs/1.1/dc'),
                                             ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
                                             ('xmlns:dc', 'http://purl.org/dc/elements/1.1/'),
                                             ('xsi:schemaLocation', 'https://ads.harvard.edu/schema/abs/1.1/dc https://ads.harvard.edu/schema/abs/1.1/dc.xsd')]

    EXPORT_SERVICE_RECORDS_SET_XML_JATS = [('xmlns', 'https://ads.harvard.edu/schema/abs/1.1/jats'),
                                           ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
                                           ('xsi:schemaLocation', 'https://ads.harvard.edu/schema/abs/1.0/jats https://ads.harvard.edu/schema/abs/1.0/jats.xsd')]

    re_year = re.compile(r'([12]+[09]\d\d)')

    re_xml_header = re.compile(u"\<\?xml .+?>")

    def __format_date(self, solr_date, xml_export_format):
        """

        :param solr_date:
        :param xml_export_format:
        :return:
        """
        # solr_date has the format 2017-12-01
        dateTime = datetime.strptime(solr_date.replace('-00', '-01'), '%Y-%m-%d')
        formats = {self.EXPORT_FORMAT_DUBLIN_XML: '%Y-%m-%d', self.EXPORT_FORMAT_REF_XML: '%b %Y', self.EXPORT_FORMAT_REF_ABS_XML: '%b %Y'}
        return strftime(dateTime, formats[xml_export_format])


    def __format_line_wrapped(self, text):
        """

        :param text:
        :return:
        """
        # 3/2 for now do not wrap text, it is way too slow
        return text
        # return fill(text, width=72, break_on_hyphens=False)


    def __add_author_list(self, a_doc, parent, tag):
        """
        format authors

        :param a_doc:
        :param parent:
        :param tag:
        :return:
        """
        if 'author' not in a_doc:
            return
        for author in a_doc['author']:
            ET.SubElement(parent, tag).text = author


    def __add_affiliation_list(self, a_doc, parent, field):
        """
        format affilation

        :param a_doc:
        :param parent:
        :param field:
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
        if (len(affiliation_list) > 0):
            ET.SubElement(parent, field).text = self.__format_line_wrapped(affiliation_list)


    def __add_doc_a_link(self, parent, link_type, link_name, link_url, count='', access=''):
        """
        add a link to xml structure

        :param parent:
        :param link_type:
        :param link_name:
        :param link_url:
        :param count:
        :param access:
        :return:
        """
        record = ET.SubElement(parent, "link")
        record.set('type', link_type)
        if (len(access) > 0):
            record.set('access', access)
        ET.SubElement(record, 'name').text = link_name
        ET.SubElement(record, 'url').text = link_url
        if (len(count) > 0):
            ET.SubElement(record, 'count').text = count


    def __add_doc_links_property(self, a_doc, parent):
        """
        format links that are defined in the property field
        :param a_doc:
        :param parent:
        :return:
        """
        link_url_format = current_app.config['EXPORT_SERVICE_RESOLVE_URL'] + '/{bibcode}/{link_type}'
        bibcode = a_doc.get('bibcode', '')

        link_dict = OrderedDict([
            ('TOC', ['TOC', 'Table of Contents']),
            ('LIBRARYCATALOG', ['LIBRARY', 'Library Entry']),
        ])
        for link in link_dict:
            if link in a_doc.get('property', ''):
                self.__add_doc_a_link(parent=parent, link_type=link_dict[link][0], link_name=link_dict[link][1],
                                      link_url=link_url_format.format(bibcode=bibcode, link_type=link.lower()))


    def __add_doc_links_esource(self, a_doc, parent):
        """
        format links that are defined in the esource field

        :param a_doc:
        :param parent:
        :return:
        """
        link_url_format = current_app.config['EXPORT_SERVICE_RESOLVE_URL'] + '/{bibcode}/{link_type}'
        bibcode = a_doc.get('bibcode', '')

        link_dict = OrderedDict([
            # (link type:[name, access])
            ('eprint_html', ['arXiv Article', '']),
            ('author_html', ['Author Article', '']),
            ('pub_html', ['Publisher Article', '']),
            ('ads_scan', ['Scanned Article (GIF)', '']),
            ('eprint_pdf', ['arXiv PDF', 'eprint_openaccess']),
            ('author_pdf', ['Author PDF', 'author_openaccess']),
            ('pub_pdf', ['Publisher PDF', 'pub_openaccess']),
            ('ads_pdf', ['ADS PDF', 'ads_openaccess']),
        ])
        for link in link_dict:
            if link.upper() in a_doc.get('esources', ''):
                self.__add_doc_a_link(parent=parent, link_type=link.upper(), link_name=link_dict[link][0],
                                      link_url=link_url_format.format(bibcode=bibcode, link_type=link.upper()),
                                      access='open' if link_dict[link][1].upper() in a_doc.get('property', '') else '')


    def __add_doc_links_data(self, a_doc, parent):
        """
        format links that are defined in the data field

        :param a_doc:
        :param parent:
        :return:
        """
        link_url_format = current_app.config['EXPORT_SERVICE_RESOLVE_URL'] + '/{bibcode}/{link_type}'
        bibcode = a_doc.get('bibcode', '')
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
                        ('Chandra', 'Chandra X-Ray Observatory'),
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
                        ('IRSA', 'NASA/IPAC Infrared Science Archive'),
                        ('Github', 'Git Repository Hosting Service'),
                        ('Dryad', 'International Repository of Research Data'),
                        ('Figshare', 'Online Open Access Repository'),
                        ('JWST', 'JWST Proposal Info'),
                        ('PANGAEA', 'Digital Data Library and a Data Publisher for Earth System Science'),
                        ('protocols', 'Collaborative Platform and Preprint Server for Science Methods and Protocols'),
                        ('BAVJ', 'Data of the German Association for Variable Stars'),
        ])
        data_dict = {}
        for d in a_doc.get('data', ''):
            data_dict[d.split(':')[0]] = int(d.split(':')[1])
        for link in link_dict:
            if link in data_dict.keys():
                self.__add_doc_a_link(parent=parent, link_type=link, link_name=link_dict[link],
                                      link_url=link_url_format.format(bibcode=bibcode, link_type=link),
                                      count=str(data_dict[link]))


    def __add_doc_links(self, a_doc, parent):
        """
        format links

        :param a_doc:
        :param parent:
        :return:
        """
        link_url_format = current_app.config['EXPORT_SERVICE_RESOLVE_URL'] + '/{bibcode}/{link_type}'
        bibcode = a_doc.get('bibcode', '')
        link_dict =  OrderedDict([
                        #(link type:[include if, name, has count])
                        ('abstract', [len(a_doc.get('abstract', '')), 'abstract', False]),
                        ('citations', [a_doc.get('num_citations', 0), 'Citations to the Article', 'citations', True]),
                        ('reference', [a_doc.get('num_references', 0), 'References in the Article', 'references', True]),
                        ('coreads', [a_doc.get('read_count', 0), 'Co-Reads', False]),
        ])
        for link in link_dict:
            if (link_dict[link][0] > 0):
                self.__add_doc_a_link(parent=parent, link_type=link, link_name=link_dict[link][1],
                                      link_url=link_url_format.format(bibcode=bibcode, link_type=link),
                                      count=str(link_dict[link][0]) if link_dict[link][2] else '')

        self.__add_doc_links_property(a_doc, parent)
        self.__add_doc_links_esource(a_doc, parent)
        self.__add_doc_links_data(a_doc, parent)


    def __add_keywords(self, a_doc, parent, xml_export_format):
        """
        format keyword

        :param a_doc:
        :param parent:
        :param xml_export_format:
        :return:
        """
        if 'keyword' not in a_doc:
            return
        if (xml_export_format == self.EXPORT_FORMAT_REF_ABS_XML):
            record = ET.SubElement(parent, "keywords")
            for keyword in a_doc['keyword']:
                ET.SubElement(record, 'keyword').text = keyword
        elif (xml_export_format == self.EXPORT_FORMAT_DUBLIN_XML):
            ET.SubElement(parent, 'dc:subject').text = self.__format_line_wrapped(', '.join(a_doc.get('keyword', '')))


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


    def __add_pub_raw(self, a_doc, parent, field, xml_export_format):
        """
        format pub_raw

        :param a_doc:
        :param parent:
        :param field:
        :param xml_export_format:
        :return:
        """
        if 'pub_raw' not in a_doc:
            return
        pub_raw = self.__add_clean_pub_raw(a_doc)
        if (xml_export_format == self.EXPORT_FORMAT_REF_XML) or (xml_export_format == self.EXPORT_FORMAT_REF_ABS_XML):
            ET.SubElement(parent, field).text = pub_raw

        elif (xml_export_format == self.EXPORT_FORMAT_DUBLIN_XML):
            # for dublin both types of pub_raw are exported
            # we could have something like this is Solr
            # "pub_raw":"Sensing and Imaging, Volume 18, Issue 1, article id. #17, <NUMPAGES>12</NUMPAGES> pp."
            # where we remove the tag and output it, or something like this
            # "pub_raw":"eprint arXiv:astro-ph/0003081"
            # that gets output as is
            pub_raw = self.REGEX_REMOVE_TAGS_PUB_RAW.sub('', pub_raw)
            ET.SubElement(parent, field).text = self.__format_line_wrapped(pub_raw)


    def __get_fields(self, xml_export_format):
        """
        from solr to each types' tags

        :param xml_export_format:
        :return:
        """
        if (xml_export_format == self.EXPORT_FORMAT_REF_XML):
            fields = [('bibcode', 'bibcode'), ('title', 'title'), ('author', 'author'),
                      ('pub_raw', 'journal'), ('pubdate', 'pubdate'), ('link', 'link'),
                      ('', 'score'), ('num_citations', 'citations'), ('doi', 'DOI'),
                      ('eprintid', 'eprintid')]
        elif (xml_export_format == self.EXPORT_FORMAT_REF_ABS_XML):
            fields = [('bibcode', 'bibcode'), ('title', 'title'), ('author', 'author'),
                      ('aff', 'affiliation'), ('pub_raw', 'journal'), ('volume', 'volume'),
                      ('pubdate', 'pubdate'), ('page', 'page'), ('page_range', 'lastpage'),
                      ('keyword', 'keywords'), ('', 'origin'), ('publisher', 'publisher'),
                      ('copyright', 'copyright'), ('link', 'link'), ('url', 'url'),
                      ('comment', 'comment'), ('', 'score'), ('num_citations', 'citations'),
                      ('abstract', 'abstract'), ('doi', 'DOI'), ('eprintid', 'eprintid')]
        elif (xml_export_format == self.EXPORT_FORMAT_DUBLIN_XML):
            fields = [('bibcode', 'dc:identifier'), ('title', 'dc:title'), ('author', 'dc:creator'),
                      ('pub_raw', 'dc:source'), ('pubdate', 'dc:date'), ('keyword', 'dc:subject'),
                      ('copyright', 'dc:rights'), ('url', 'dc:relation'), ('num_citations', 'dc:relation'),
                      ('abstract', 'dc:description'), ('doi', 'dc:identifier'), ('publisher', 'dc:publisher')]
        elif (xml_export_format == self.EXPORT_FORMAT_JATS_XML):
            # note that order matters here
            fields = [('front_tag', 'front'), # first top level tag, with two middle level tags (level 1)
                      ('journal-meta_tag', 'journal-meta'), # first sub element of `front` (level 1_i)
                      ('bibstem', 'journal-id'), ('issn', 'issn'), ('publisher', 'publisher'), # sub elements of `journal-meta` (level 1_i_, order of these do not matter)
                      ('article-meta_tag', 'article-meta'), # second sub element of `front` (level 1_ii)
                      ('bibcode', 'article-id'), ('doi', 'article-id'), ('title', 'title-group'), # the rest are sub elements of `article_meta` (level 1_ii_, order of these do not matter)
                      ('author', 'contrib-group'), ('date', 'date'), ('volume', 'volume'), ('issue', 'issue'),
                      ('page', 'fpage'), ('page_range', 'lpage'), ('abstract', 'abstract'),
                      ('body_tag', 'body'),  # second top level tag (level 2), optional -> ignore
                      ('back_tag', 'back')] # third top level tag (level 3), optional -> ignore
        else:
            fields = []
        return OrderedDict(fields)


    def __get_doi(self, doi):
        """

        :param doi:
        :return:
        """
        if len(doi) > 0:
            return 'doi:' + doi
        return ''


    def __get_citation(self, num_citations, xml_export_format):
        """

        :param num_citations:
        :return:
        """
        if num_citations != 0:
            if (xml_export_format == self.EXPORT_FORMAT_REF_XML) or (xml_export_format == self.EXPORT_FORMAT_REF_ABS_XML):
                return str(num_citations)
            if (xml_export_format == self.EXPORT_FORMAT_DUBLIN_XML):
                return 'citations:' + str(num_citations)
        return ''


    def __add_page(self, a_doc, parent, field):
        """

        :return:
        """
        if 'page_range' not in a_doc or 'page' not in a_doc:
            return
        page = ''.join(a_doc.get('page_range', ''))
        if len(page) > 0:
            if '-' in page:
                page,lastpage = page.split('-')
            else:
                lastpage = ''
        else:
            page = ''.join(a_doc.get('page', ''))
            lastpage = ''
        if (field == 'page') or (field == 'fpage'):
            self.__add_in(parent, field, page)
        elif (field == 'lastpage') or (field == 'lpage'):
            self.__add_in(parent, field, lastpage)


    def __add_in(self, parent, field, value):
        """
        add the value into the return structure, only if a value was defined in Solr

        :param parent:
        :param field:
        :param value:
        :return:
        """
        if (len(value) > 0):
            ET.SubElement(parent, field).text = value


    def __get_attrib(self, xml_export_format):
        """

        :param xml_export_format:
        :return:
        """
        if (xml_export_format == self.EXPORT_FORMAT_REF_XML):
            return OrderedDict(self.EXPORT_SERVICE_RECORDS_SET_XML_REF)
        if (xml_export_format == self.EXPORT_FORMAT_REF_ABS_XML):
            return OrderedDict(self.EXPORT_SERVICE_RECORDS_SET_XML_REF_ABS)
        if (xml_export_format == self.EXPORT_FORMAT_DUBLIN_XML):
            return OrderedDict(self.EXPORT_SERVICE_RECORDS_SET_XML_DUBLIN)
        if (xml_export_format == self.EXPORT_FORMAT_JATS_XML):
            return OrderedDict(self.EXPORT_SERVICE_RECORDS_SET_XML_JATS)
        return OrderedDict([])


    def __get_num_citations(self):
        """

        :return:
        """
        num_citations = 0
        for a_doc in self.from_solr['response'].get('docs'):
            num_citations += int(a_doc.get('num_citations', '0'))
        return num_citations


    def __get_doc_dublin_xml(self, index):
        """
        for each document from Solr, get the fields, and format them accordingly for Dublin format

        :param index:
        :return:
        """
        a_doc = self.from_solr['response'].get('docs')[index]
        fields = self.__get_fields(self.EXPORT_FORMAT_DUBLIN_XML)
        record = ET.Element("record")
        for field in fields:
            if field in ['bibcode', 'copyright']:
                self.__add_in(record, fields[field], a_doc.get(field, ''))
            elif (field == 'title'):
                self.__add_in(record, fields[field], ''.join(a_doc.get(field, '')))
            elif (field == 'author'):
                self.__add_author_list(a_doc, record, fields[field])
            elif (field == 'pub_raw'):
                self.__add_pub_raw(a_doc, record, fields[field], self.EXPORT_FORMAT_DUBLIN_XML)
            elif (field == 'pubdate'):
                self.__add_in(record, fields[field], self.__format_date(a_doc.get(field, ''), self.EXPORT_FORMAT_DUBLIN_XML))
            elif (field == 'keyword'):
                self.__add_keywords(a_doc, record, self.EXPORT_FORMAT_DUBLIN_XML)
            elif (field == 'url'):
                self.__add_in(record, fields[field], current_app.config.get('EXPORT_SERVICE_FROM_BBB_URL') + '/' + a_doc.get('bibcode', ''))
            elif (field == 'abstract'):
                self.__add_in(record, fields[field], self.__format_line_wrapped(a_doc.get(field, '')))
            elif (field == 'doi'):
                self.__add_in(record, fields[field], self.__get_doi('; '.join(a_doc.get(field, ''))))
            elif (field == 'num_citations'):
                self.__add_in(record, fields[field], self.__get_citation(int(a_doc.get(field, 0)), self.EXPORT_FORMAT_DUBLIN_XML))
            elif (field == 'publisher'):
                self.__add_in(record, fields[field], a_doc.get(field, ''))
        return record


    def __get_doc_reference_xml(self, index, xml_export_format):
        """
        for each document from Solr, get the fields, and format them accordingly for Reference format

        :param index
        :param xml_export_format:
        :return:
        """
        a_doc = self.from_solr['response'].get('docs')[index]
        fields = self.__get_fields(xml_export_format)
        record = ET.Element("record")
        if (xml_export_format == self.EXPORT_FORMAT_REF_ABS_XML):
            property = a_doc.get('property', [])
            if 'REFEREED' in property:
                record.set('refereed', 'true')
            if 'ARTICLE' in property:
                record.set('article', 'true')
            record.set('type', a_doc.get('doctype', ''))
        for field in fields:
            if field in ['bibcode', 'pub', 'volume', 'copyright']:
                self.__add_in(record, fields[field], a_doc.get(field, ''))
            elif field in ['title', 'doi']:
                self.__add_in(record, fields[field], ''.join(a_doc.get(field, '')))
            elif (field == 'author'):
                self.__add_author_list(a_doc, record, fields[field])
            elif (field == 'aff'):
                self.__add_affiliation_list(a_doc, record, fields[field])
            elif (field == 'pubdate'):
                self.__add_in(record, fields[field], self.__format_date(a_doc.get(field, ''), xml_export_format))
            elif (field == 'pub_raw'):
                self.__add_pub_raw(a_doc, record, fields[field], xml_export_format)
            elif field in ['page', 'page_range']:
                self.__add_page(a_doc, record, fields[field])
            elif (field == 'keyword'):
                self.__add_keywords(a_doc, record, xml_export_format)
            elif (field == 'url'):
                self.__add_in(record, fields[field], current_app.config.get('EXPORT_SERVICE_FROM_BBB_URL') + '/' + a_doc.get('bibcode', ''))
            elif (field == 'num_citations'):
                self.__add_in(record, fields[field], self.__get_citation(int(a_doc.get(field, 0)), xml_export_format))
            elif (field == 'abstract'):
                self.__add_in(record, fields[field], self.__format_line_wrapped(a_doc.get(field, '')))
            elif (field == 'link'):
                self.__add_doc_links(a_doc, record)
            elif (field == 'eprintid'):
                self.__add_in(record, fields[field], get_eprint(a_doc))
            elif (field == 'publisher'):
                self.__add_in(record, fields[field], a_doc.get(field, ''))
        return record


    def __add_author_list_jats_xml(self, doc, parent):
        """
        add authors for JATS xml format

        :param doc:
        :param parent:
        :return:
        """
        for author, affiliation, orcid in zip(doc.get('author', []), doc.get('aff', []), doc.get('orcid_pub', [])):
            # add contrib tag, parent to name, aff, and orcid
            contrib = ET.SubElement(parent, 'contrib', {"contrib-type": "author"})
            # add orcid id first, if available
            if orcid != '-':
                ET.SubElement(contrib, 'contrib-id', {"contrib-id-type": "orcid"}).text = orcid
            # add name tag, parent to surname and given-names
            name = ET.SubElement(contrib, 'name')
            try:
                surname, given_names = author.split(', ')
                ET.SubElement(name, 'surname').text = surname
                ET.SubElement(name, 'given-names').text = given_names
            except ValueError:
                ET.SubElement(name, 'surname').text = author
            if affiliation != '-':
                ET.SubElement(contrib, 'aff').text = affiliation


    def __add_date_jats_xml(self, doc, parent):
        """

        :param doc:
        :param parent:
        :return:
        """
        try:
            iso_date = doc.get('pubdate', '')
            year, month, day = iso_date.split('-')

            # electronic version or print version
            format = "electronic" if doc.get('eid', None) else "print"
            pub_date_attributes = {"publication-format": "%s" % format,
                                   "date-type": "pub",
                                   "iso-8601-date": "%s" % iso_date}

            pub_date = ET.SubElement(parent, "pub-date", attrib=pub_date_attributes)

            ET.SubElement(pub_date, "day").text = day
            ET.SubElement(pub_date, "month").text = month
            ET.SubElement(pub_date, "year").text = year
        except ValueError:
            current_app.logger.error(f"Invalid date format: {iso_date}")


    def __to_string(self, element, declaration=True):
        """

        :param element:
        :param declaration:
        :return:
        """
        str_element = ET.tostring(element, encoding='utf8', method='xml', xml_declaration=declaration).decode('utf-8')
        str_element = '>\n<'.join(str_element.split('><'))
        return str_element


    def __add_specific_header_jats_xml(self, format):
        """

        :param format:
        :return:
        """
        new_header_lines = [
            '<?xml version="1.0" encoding="UTF-8" ?>',
            '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.2 20190208//EN" "https://jats.nlm.nih.gov/publishing/1.2/JATS-journalpublishing1.dtd">'
        ]
        return self.re_xml_header.sub('\n'.join(new_header_lines), format)


    def __get_outer_structure(self, xml_export_format, num_docs):
        """

        :param xml_export_format:
        :param num_docs:
        :return:
        """
        records = ET.Element("records")
        attribs = self.__get_attrib(xml_export_format)
        for attrib in attribs:
            records.set(attrib, attribs[attrib])
        records.set('retrieved', str(num_docs))
        records.set('start', str(1))
        records.set('selected', str(num_docs))
        num_citations = self.__get_num_citations()
        if num_citations > 0 and xml_export_format != self.EXPORT_FORMAT_JATS_XML:
            records.set('citations', str(num_citations))

        # add placeholder to references
        self.add_xml_placeholder_references(records, "references")

        return self.__to_string(records)



    def __get_doc_jats_xml(self, index):
        """
        for each document from Solr, get the fields, and format them accordingly for JATS `Journal Publishing` format

        :param index:
        :return:
        """
        # source: https://jats.nlm.nih.gov/publishing/tag-library/1.3/attribute/article-type.html
        ads_to_jats_doctype_mapping = {
            'article': 'research-article', 'eprint': 'research-article', 'inbook': 'research-article',
            'inproceedings': 'research-article', 'proceedings': 'research-article',
            'abstract': 'abstract', 'pressrelease': 'announcement', 'bookreview': 'book-review',
            'erratum': 'correction', 'mastersthesis': 'dissertation', 'phdthesis': 'dissertation',
            'editorial': 'editorial', 'newsletter': 'news', 'obituary': 'obituary',
            'book': 'other', 'catalog': 'other', 'circular': 'other', 'misc': 'other',
            'proposal': 'other', 'software': 'other', 'talk': 'other', 'techreport': 'other', 'dataset': 'other',
        }
        a_doc = self.from_solr['response'].get('docs')[index]
        fields = self.__get_fields(self.EXPORT_FORMAT_JATS_XML)

        # add outter tag for this reference
        article_type = ads_to_jats_doctype_mapping[a_doc.get('doctype', '')]
        article_attributes = {"xmlns:xlink": "http://www.w3.org/1999/xlink",
                              "xmlns:mml": "http://www.w3.org/1998/Math/MathML",
                              "article-type": "%s"%article_type}
        article = ET.Element("article", article_attributes)

        front_section = journal_meta_section = article_meta_section = None
        for field in fields:
            if (field == 'front_tag'):
                front_section = ET.SubElement(article, fields[field])
            elif (field == 'journal-meta_tag'):
                journal_meta_section = ET.SubElement(front_section, fields[field])
            elif (field == 'bibstem'):
                ET.SubElement(journal_meta_section, fields[field], {"journal-id-type":"publisher"}).text = a_doc.get(field, '')[0]
            elif (field == 'issn'):
                self.__add_in(journal_meta_section, fields[field], '; '.join(a_doc.get(field, '')))
            elif (field == 'publisher'):
                publisher_name = a_doc.get(field, '')
                if publisher_name:
                    ET.SubElement(ET.SubElement(journal_meta_section, fields[field]), 'publisher-name').text = publisher_name
            elif (field == 'article-meta_tag'):
                article_meta_section = ET.SubElement(front_section, fields[field])
            elif (field == 'bibcode'):
                ET.SubElement(article_meta_section, fields[field], {"pub-id-type": "archive"}).text = a_doc.get(field, '')
            elif (field == 'doi'):
                if a_doc.get(field, ''):
                    ET.SubElement(article_meta_section, fields[field], {"pub-id-type": "doi"}).text = '; '.join(a_doc.get(field, ''))
            elif (field == 'title'):
                title = ET.SubElement(article_meta_section, fields[field])
                ET.SubElement(title, 'article-title').text = '; '.join(a_doc.get(field, ''))
            elif (field == 'author'):
                # add `contrib-group` tag and call the function to add list of authors to this tag
                self.__add_author_list_jats_xml(a_doc, ET.SubElement(article_meta_section, fields[field]))
            elif (field == 'date'):
                self.__add_date_jats_xml(a_doc, article_meta_section)
            elif field in ['volume', 'issue']:
                self.__add_in(article_meta_section, fields[field], a_doc.get(field, ''))
            elif (field == 'abstract'):
                # permissions tag is required and must appear before the abstract,
                # no copyright information is available in solr right now, so add an empty permission tag for now
                ET.SubElement(article_meta_section, "permissions").text = ""
                # add abstract tag, then paragraph tag around the abstract (required)
                abstract = ET.SubElement(article_meta_section, fields[field])
                self.__add_in(abstract, "p", a_doc.get(field, ''))
            elif field in ['page', 'page_range']:
                self.__add_page(a_doc, article_meta_section, fields[field])

        return article


    def __get_xml(self, xml_export_format, output_format):
        """
        setup the outer xml structure

        :param xml_export_format:
        :param output_format:
        :return:
        """
        num_docs = 0
        references = []
        bibcodes = []
        if (self.status == 0):
            num_docs = self.get_num_docs()
            # from Alberto:
            # we should drop the <records> wrapper when a single record is output, since this element is not part of the JATS DTD
            # when multiple records are output, we can keep the <records> element in there as the third line in the output
            if xml_export_format == self.EXPORT_FORMAT_JATS_XML and num_docs == 1:
                references.append(self.__add_specific_header_jats_xml(self.__to_string(self.__get_doc_jats_xml(0))))
                bibcodes.append(self.from_solr['response'].get('docs')[0]['bibcode'])
                return self.formatted_export(output_format, num_docs, references, bibcodes, '')
            else:
                outer_structure = self.__get_outer_structure(xml_export_format, num_docs)

                if (xml_export_format == self.EXPORT_FORMAT_REF_XML) or (xml_export_format == self.EXPORT_FORMAT_REF_ABS_XML):
                    for index in range(num_docs):
                        references.append(self.__to_string(self.__get_doc_reference_xml(index, xml_export_format), False) + '\n\n')
                        bibcodes.append(self.from_solr['response'].get('docs')[index]['bibcode'])
                elif (xml_export_format == self.EXPORT_FORMAT_DUBLIN_XML):
                    for index in range(num_docs):
                        references.append(self.__to_string(self.__get_doc_dublin_xml(index), False) + '\n\n')
                        bibcodes.append(self.from_solr['response'].get('docs')[index]['bibcode'])
                elif (xml_export_format == self.EXPORT_FORMAT_JATS_XML):
                    outer_structure = self.__add_specific_header_jats_xml(outer_structure)
                    for index in range(num_docs):
                        references.append(self.__to_string(self.__get_doc_jats_xml(index), False) + '\n')
                        bibcodes.append(self.from_solr['response'].get('docs')[index]['bibcode'])
                header, footer = self.get_top_and_bottom_xml_references(outer_structure)

        return self.formatted_export(output_format, num_docs, references, bibcodes, '', header, footer)




    def get_reference_xml(self, include_abs, output_format):
        """

        :param include_abs:
        :param output_format:
        :return: reference xml format with or without abstract
        """
        if include_abs:
            return self.__get_xml(self.EXPORT_FORMAT_REF_ABS_XML, output_format)
        return self.__get_xml(self.EXPORT_FORMAT_REF_XML, output_format)


    def get_dublincore_xml(self, output_format):
        """

        :param output_format:
        :return: dublin xml format
        """
        return self.__get_xml(self.EXPORT_FORMAT_DUBLIN_XML, output_format)


    def get_jats_xml(self, output_format):
        """

        :param output_format:
        :return: jats xml format
        """
        return self.__get_xml(self.EXPORT_FORMAT_JATS_XML, output_format)

