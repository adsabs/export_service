# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from collections import OrderedDict
from datetime import datetime
from flask import current_app
from textwrap import fill

from exportsrv.formatter.format import Format
from exportsrv.utils import get_eprint
from exportsrv.formatter.strftime import strftime

# This class accepts JSON object created by Solr and can reformats it
# for the XML Export formats we are supporting.
# 1- To get Dublin Core XML use
#    dublinXML = XMLFormat(jsonFromSolr).get_dublincore_xml()
# 2- To get Reference XML without Abstract use
#    referenceXML = XMLFormat(jsonFromSolr).get_reference_xml()
# 3- To get Reference XML with Abstract use
#    referenceXML = XMLFormat(jsonFromSolr).get_reference_xml(True)

class XMLFormat(Format):

    EXPORT_FORMAT_REF_XML = 'ReferenceXML'
    EXPORT_FORMAT_REF_ABS_XML = 'ReferenceAbsXML'
    EXPORT_FORMAT_DUBLIN_XML = 'DublinXML'

    EXPORT_SERVICE_RECORDS_SET_XML_REF = [('xmlns', 'http://ads.harvard.edu/schema/abs/1.1/references'),
                                          ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
                                          ('xsi:schemaLocation', 'http://ads.harvard.edu/schema/abs/1.1/references http://ads.harvard.edu/schema/abs/1.1/references.xsd')]

    EXPORT_SERVICE_RECORDS_SET_XML_REF_ABS = [('xmlns', 'http://ads.harvard.edu/schema/abs/1.1/abstract'),
                                              ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
                                              ('xsi:schemaLocation', 'http://ads.harvard.edu/schema/abs/1.1/abstract http://ads.harvard.edu/schema/abs/1.1/abstract.xsd')]

    EXPORT_SERVICE_RECORDS_SET_XML_DUBLIN = [('xmlns', 'http://ads.harvard.edu/schema/abs/1.1/dc'),
                                             ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
                                             ('xmlns:dc', 'http://purl.org/dc/elements/1.1/'),
                                             ('xsi:schemaLocation', 'http://ads.harvard.edu/schema/abs/1.1/dc http://ads.harvard.edu/schema/abs/1.1/dc.xsd')]

    def __format_date(self, solr_date, export_format):
        """

        :param solr_date:
        :param export_format:
        :return:
        """
        # solr_date has the format 2017-12-01
        dateTime = datetime.strptime(solr_date.replace('-00', '-01'), '%Y-%m-%d')
        formats = {self.EXPORT_FORMAT_DUBLIN_XML: '%Y-%m-%d', self.EXPORT_FORMAT_REF_XML: '%b %Y', self.EXPORT_FORMAT_REF_ABS_XML: '%b %Y'}
        return strftime(dateTime, formats[export_format])


    def __format_line_wrapped(self, text):
        """

        :param text:
        :return:
        """
        return fill(text, width=72)


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
        if ('aff_raw') not in a_doc:
            return ''
        counter = self.generate_counter_id(len(a_doc['aff_raw']))
        separator = ', '
        affiliation_list = ''
        for affiliation, i in zip(a_doc['aff_raw'], range(len(a_doc['aff_raw']))):
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
                        ('citations', [a_doc.get('citation_count', 0), 'Citations to the Article', 'citations', True]),
                        ('reference', [a_doc.get('reference', 0), 'References in the Article', 'references', True]),
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


    def __add_keywords(self, a_doc, parent, export_format):
        """
        format keyword

        :param a_doc:
        :param parent:
        :param export_format:
        :return:
        """
        if 'keyword' not in a_doc:
            return
        if (export_format == self.EXPORT_FORMAT_REF_ABS_XML):
            record = ET.SubElement(parent, "keywords")
            for keyword in a_doc['keyword']:
                ET.SubElement(record, 'keyword').text = keyword
        elif (export_format == self.EXPORT_FORMAT_DUBLIN_XML):
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


    def __add_pub_raw(self, a_doc, parent, field, export_format):
        """
        format pub_raw

        :param a_doc:
        :param parent:
        :param field:
        :param export_format:
        :return:
        """
        if 'pub_raw' not in a_doc:
            return
        pub_raw = self.__add_clean_pub_raw(a_doc)
        if (export_format == self.EXPORT_FORMAT_REF_XML) or (export_format == self.EXPORT_FORMAT_REF_ABS_XML):
            ET.SubElement(parent, field).text = pub_raw

        elif (export_format == self.EXPORT_FORMAT_DUBLIN_XML):
            # for dublin both types of pub_raw are exported
            # we could have something like this is Solr
            # "pub_raw":"Sensing and Imaging, Volume 18, Issue 1, article id. #17, <NUMPAGES>12</NUMPAGES> pp."
            # where we remove the tag and output it, or something like this
            # "pub_raw":"eprint arXiv:astro-ph/0003081"
            # that gets output as is
            pub_raw = self.REGEX_REMOVE_TAGS_PUB_RAW.sub('', pub_raw)
            ET.SubElement(parent, field).text = self.__format_line_wrapped(pub_raw)


    def __get_fields(self, export_format):
        """
        from solr to each types' tags

        :param export_format:
        :return:
        """
        if (export_format == self.EXPORT_FORMAT_REF_XML):
            fields = [('bibcode', 'bibcode'), ('title', 'title'), ('author', 'author'),
                      ('pub_raw', 'journal'), ('pubdate', 'pubdate'), ('link', 'link'),
                      ('url', 'url'), ('', 'score'), ('citation_count', 'citations'),
                      ('doi', 'DOI'), ('eprintid', 'eprintid')]
        elif (export_format == self.EXPORT_FORMAT_REF_ABS_XML):
            fields = [('bibcode', 'bibcode'), ('title', 'title'), ('author', 'author'),
                      ('aff_raw', 'affiliation'), ('pub_raw', 'journal'), ('volume', 'volume'),
                      ('pubdate', 'pubdate'), ('page', 'page'), ('page_range', 'lastpage'),
                      ('keyword', 'keywords'), ('', 'origin'), ('copyright', 'copyright'),
                      ('link', 'link'), ('url', 'url'), ('comment', 'comment'),
                      ('', 'score'), ('citation_count', 'citations'), ('abstract', 'abstract'),
                      ('doi', 'DOI'), ('eprintid', 'eprintid')]
        elif (export_format == self.EXPORT_FORMAT_DUBLIN_XML):
            fields = [('bibcode', 'dc:identifier'), ('title', 'dc:title'), ('author', 'dc:creator'),
                      ('pub_raw', 'dc:source'), ('pubdate', 'dc:date'), ('keyword', 'dc:subject'),
                      ('copyright', 'dc:rights'), ('url', 'dc:relation'), ('citation_count', 'dc:relation'),
                      ('abstract', 'dc:description'), ('doi', 'dc:identifier')]
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


    def __get_citation(self, citation_count, export_format):
        """

        :param citation_count:
        :return:
        """
        if citation_count != 0:
            if (export_format == self.EXPORT_FORMAT_REF_XML) or (export_format == self.EXPORT_FORMAT_REF_ABS_XML):
                return str(citation_count)
            if (export_format == self.EXPORT_FORMAT_DUBLIN_XML):
                return 'citations:' + str(citation_count)
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
        if (field == 'page'):
            self.__add_in(parent, field, page)
        elif (field == 'lastpage'):
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


    def __get_attrib(self, export_format):
        """

        :param export_format:
        :return:
        """
        if (export_format == self.EXPORT_FORMAT_REF_XML):
            return OrderedDict(self.EXPORT_SERVICE_RECORDS_SET_XML_REF)
        if (export_format == self.EXPORT_FORMAT_REF_ABS_XML):
            return OrderedDict(self.EXPORT_SERVICE_RECORDS_SET_XML_REF_ABS)
        if (export_format == self.EXPORT_FORMAT_DUBLIN_XML):
            return OrderedDict(self.EXPORT_SERVICE_RECORDS_SET_XML_DUBLIN)
        return OrderedDict([])


    def __get_doc_dublin_xml(self, index, parent):
        """
        for each document from Solr, get the fields, and format them accordingly for Dublin format

        :param index:
        :param parent:
        :return:
        """
        a_doc = self.from_solr['response'].get('docs')[index]
        fields = self.__get_fields(self.EXPORT_FORMAT_DUBLIN_XML)
        record = ET.SubElement(parent, "record")
        for field in fields:
            if (field == 'bibcode') or (field == 'copyright'):
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
                self.__add_in(record, fields[field], self.__get_doi(''.join(a_doc.get(field, ''))))
            elif (field == 'citation_count'):
                self.__add_in(record, fields[field], self.__get_citation(int(a_doc.get(field, 0)), self.EXPORT_FORMAT_DUBLIN_XML))


    def __get_doc_reference_xml(self, index, parent, export_format):
        """
        for each document from Solr, get the fields, and format them accordingly for Reference format

        :param index:
        :param parent:
        :param export_format:
        :return:
        """
        a_doc = self.from_solr['response'].get('docs')[index]
        fields = self.__get_fields(export_format)
        record = ET.SubElement(parent, "record")
        if (export_format == self.EXPORT_FORMAT_REF_ABS_XML):
            property = a_doc.get('property', [])
            if 'REFEREED' in property:
                record.set('refereed', 'true')
            if 'ARTICLE' in property:
                record.set('article', 'true')
            record.set('type', a_doc.get('doctype', ''))
        for field in fields:
            if (field == 'bibcode') or (field == 'pub') or (field == 'volume') or \
               (field == 'copyright'):
                self.__add_in(record, fields[field], a_doc.get(field, ''))
            elif (field == 'title') or (field == 'doi'):
                self.__add_in(record, fields[field], ''.join(a_doc.get(field, '')))
            elif (field == 'author'):
                self.__add_author_list(a_doc, record, fields[field])
            elif (field == 'aff_raw'):
                self.__add_affiliation_list(a_doc, record, fields[field])
            elif (field == 'pubdate'):
                self.__add_in(record, fields[field], self.__format_date(a_doc.get(field, ''), export_format))
            elif (field == 'pub_raw'):
                self.__add_pub_raw(a_doc, record, fields[field], export_format)
            elif (field == 'page') or (field == 'page_range'):
                self.__add_page(a_doc, record, fields[field])
            elif (field == 'keyword'):
                self.__add_keywords(a_doc, record, export_format)
            elif (field == 'url'):
                self.__add_in(record, fields[field], current_app.config.get('EXPORT_SERVICE_FROM_BBB_URL') + '/' + a_doc.get('bibcode', ''))
            elif (field == 'citation_count'):
                self.__add_in(record, fields[field], self.__get_citation(int(a_doc.get(field, 0)), export_format))
            elif (field == 'abstract'):
                self.__add_in(record, fields[field], self.__format_line_wrapped(a_doc.get(field, '')))
            elif (field == 'link'):
                self.__add_doc_links(a_doc, record)
            elif (field == 'eprintid'):
                self.__add_in(record, fields[field], get_eprint(a_doc))


    def __get_xml(self, export_format, start):
        """
        setup the outer xml structure

        :param export_format:
        :return:
        """
        num_docs = 0
        format_xml = ''
        if (self.status == 0):
            num_docs = self.get_num_docs()
            records = ET.Element("records")
            attribs = self.__get_attrib(export_format)
            for attrib in attribs:
                records.set(attrib, attribs[attrib])
            records.set('retrieved', str(num_docs))
            records.set('start', str(start))
            records.set('selected', str(num_docs))
            if (export_format == self.EXPORT_FORMAT_REF_XML) or (export_format == self.EXPORT_FORMAT_REF_ABS_XML):
                for index in range(num_docs):
                    self.__get_doc_reference_xml(index, records, export_format)
            elif (export_format == self.EXPORT_FORMAT_DUBLIN_XML):
                for index in range(num_docs):
                    self.__get_doc_dublin_xml(index, records)
            format_xml = ET.tostring(records, encoding='utf8', method='xml')
            format_xml = ('>\n<'.join(format_xml.split('><')))
            format_xml = format_xml.replace('</record>', '</record>\n')
        result_dict = {}
        result_dict['msg'] = 'Retrieved {} abstracts, starting with number 1.'.format(num_docs)
        result_dict['export'] = format_xml
        return result_dict


    def get_reference_xml(self, start, include_abs=False):
        """

        :param include_abs:
        :return: reference xml format with or without abstract
        """
        if include_abs:
            return self.__get_xml(self.EXPORT_FORMAT_REF_ABS_XML, start)
        return self.__get_xml(self.EXPORT_FORMAT_REF_XML, start)


    def get_dublincore_xml(self, start=1):
        """

        :return: dublin xml format
        """
        return self.__get_xml(self.EXPORT_FORMAT_DUBLIN_XML, start)

