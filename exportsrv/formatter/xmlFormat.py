# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from collections import OrderedDict
from datetime import datetime
from flask import current_app
from textwrap import fill
import re
from geotext import GeoText
from csv import reader

from exportsrv.formatter.format import Format
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

    EXPORT_SERVICE_RECORDS_SET_XML_REF = [('xmlns', 'http://ads.harvard.edu/schema/abs/1.1/references'),
                                          ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
                                          ('xsi:schemaLocation', 'http://ads.harvard.edu/schema/abs/1.1/references http://ads.harvard.edu/schema/abs/1.1/references.xsd')]

    EXPORT_SERVICE_RECORDS_SET_XML_REF_ABS = [('xmlns', 'http://ads.harvard.edu/schema/abs/1.1/abstracts'),
                                              ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
                                              ('xsi:schemaLocation', 'http://ads.harvard.edu/schema/abs/1.1/abstracts http://ads.harvard.edu/schema/abs/1.1/abstracts.xsd')]

    EXPORT_SERVICE_RECORDS_SET_XML_DUBLIN = [('xmlns', 'http://ads.harvard.edu/schema/abs/1.1/dc'),
                                             ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
                                             ('xmlns:dc', 'http://purl.org/dc/elements/1.1/'),
                                             ('xsi:schemaLocation', 'http://ads.harvard.edu/schema/abs/1.1/dc http://ads.harvard.edu/schema/abs/1.1/dc.xsd')]

    EXPORT_SERVICE_RECORDS_SET_XML_JATS = [('xmlns', 'http://ads.harvard.edu/schema/abs/1.1/dc'),
                                           ('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
                                           ('xmlns:dc', 'http://purl.org/dc/elements/1.1/'),
                                           ('xsi:schemaLocation', 'http://ads.harvard.edu/schema/abs/1.0/jats http://ads.harvard.edu/schema/abs/1.0/jats.xsd')]

    re_year = re.compile(r'([12]+[09]\d\d)')

    # partial list of known publishers,
    # once this field is populated in solr, rely on solr,
    # for now this is only used for JATS format
    re_publisher_names = re.compile(r"([A-Z]+[A-Za-z\s\-:]+ University Press|[A-Z]+[A-Za-z\s\-:,']+ Press|Springer- .*|Elsevier|University of [A-Z]+[A-Za-z\s-]+ Press|University of [A-Z]+[A-Za-z\s-]+|[\w-]+,\s*\w+\s*:[\s\w]+|Springer\s+([A-Z]+[A-Za-z\s-]+)+|Springer Nature|Springer, Cham|Springer Fachmedien Wiesbaden GmbH, DE|Springer-Verlag GmbH Deutschland|Springer-Verlag Berlin Heidelberg|Springer-Verlag|Springer|Cambridge, J. Wilson and son, University press|Cambridge, The University press|Oxford university press|Loyola university press|Cambridge, University press|Harvard university press|Cambridge, Eng., The University press|Louisiana state university press|Des Moines, Iowa, University press|Cambridge [Eng.] The University press|Edinburgh University Press|Cambridge University Press|Yale University Press|Brigham Young University Press|University Press of Virginia|Erevan University Press|Artemis Press|Laval University Press|Columbia University Press|Rutgers University Press|University Press of America|Johns Hopkins University Press|Sydney University Press|Yerevan University press|McGill-Queen's University Press|Innsbruck University Press|University of Arizona Press|Atlantis Press|Ilia State University Press|Ziti press|The University of Chicago Press|Princeton University Press|eXamen.press|T rculo Press|Duke University Press|Kyoto University Press|Imperial College Press|Heron Press Ltd|Kyiv University Press|Sole Logistics Press|BrownWalker Press|Joseph Henry Press|National Radio Astronomy Press|SPIE Press|Kyriakidis Press|St. Martin's Press|Huntington Library and University of Washington Press|Microcosm Press|Free Press \(Simon and Schuster\)|Cambridge Univ. Press|Templeton Foundation Press|IEEE Press|Heron Press|AIP Press|Pergamon Press|Boydell Press|Baltic Astronomy 6 and L. Davis Press|West Virginia University Press|ACM Press Books|State University of New York \(SUNY\) Press|Clarendon Press|Universal Academic Press Inc|SPIE Optical Engineering Press|Presses universitaires de France|Ginn Press|ABELexpress|SPC Press|CRC Press|Plenum Press|Pedagogical Univ. Press|The MIT \(Massachusetts Institute of Technology\) Press|Yourdon Press Computing Series|L. Davis Press|Ivy Press Books|Moscow Univ. Press|Cambridge Univ.  Press|Presses du CNRS|Presses de l'Ecole nationale des ponts et chaussees|Academic Press Inc|Cambridge UniversityPress|Vantage Press Inc|Massachusettes Institute of Technology \(MIT\) Press|IAP Press|Academic Press and OHM|IEEE Comput. Soc. Press|The Weizmann Science Press of Israel|MIT Press|Process Press|Blandford Press|Science Press|University of Tasmania Press|Vantage Press|Arno Press|Academic Press|University of Massachusetts Press|Delacorte Press/E. Friede|The Macmillan Press Ltd|Peebles Press|Anchor Press/Doubleday|Smithsonian Institution Press|Anchor Press / Doubleday|FAN Press|Univ. Calif. Press|Presses de la Cite|Ballena Press|Pica Press|University of Texas Press|Optosonic Press|University of Missouri Press|University of Alabama Press|Nauka Press|Exposition Press|Presses universitaire de France|Viking Press|Priory Press|Chemical Rubber Co. Press|Books for Libraries Press|Pragopress|Fundamental Research Press|University of California Press|University of Michigan Press|University of New Mexico Press|University of London Press|Natural History Press|Lenin Belorussian State University Press|Crowell-Collier Press|Greenwood Press|NEO Press|M.I.T. Press|Univ. Wisconsin Press|University of Chicago Press|University of Colorado Press|Brockhampton Press|Golden Press|Lutterworth Press|Trident Press Book|Beacon Press|St Martin's Press|Pageant Press|M. I. T. Press|Orion Press|The Univesrity of Chicago Press|Museum Press|Citadel Press|Pegasus Press|Childrens Press|Ronald Press Co|Majestic Press|Westernlore Press|The Science press printing company|The Technical press ltd|The Florida Bible institute press|The Sheldon press|Pacific Science Press|The Theosophical press|The Clarendon press|The Pilgrim press|The Hispanic Society of America and The De Vinne Press|Press of E. W. Stephen|The Nichols press|Press of T. P. Nichols|Press of J. Wilson and son|Roy. Acad. press)")

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
        # 3/2 for now do not wrap text, it is way too slow
        return text
        return fill(text, width=72, break_on_hyphens=False)


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
                      ('url', 'url'), ('', 'score'), ('num_citations', 'citations'),
                      ('doi', 'DOI'), ('eprintid', 'eprintid')]
        elif (export_format == self.EXPORT_FORMAT_REF_ABS_XML):
            fields = [('bibcode', 'bibcode'), ('title', 'title'), ('author', 'author'),
                      ('aff', 'affiliation'), ('pub_raw', 'journal'), ('volume', 'volume'),
                      ('pubdate', 'pubdate'), ('page', 'page'), ('page_range', 'lastpage'),
                      ('keyword', 'keywords'), ('', 'origin'), ('copyright', 'copyright'),
                      ('link', 'link'), ('url', 'url'), ('comment', 'comment'),
                      ('', 'score'), ('num_citations', 'citations'), ('abstract', 'abstract'),
                      ('doi', 'DOI'), ('eprintid', 'eprintid')]
        elif (export_format == self.EXPORT_FORMAT_DUBLIN_XML):
            fields = [('bibcode', 'dc:identifier'), ('title', 'dc:title'), ('author', 'dc:creator'),
                      ('pub_raw', 'dc:source'), ('pubdate', 'dc:date'), ('keyword', 'dc:subject'),
                      ('copyright', 'dc:rights'), ('url', 'dc:relation'), ('num_citations', 'dc:relation'),
                      ('abstract', 'dc:description'), ('doi', 'dc:identifier')]
        elif (export_format == self.EXPORT_FORMAT_JATS_XML):
            fields = [('doctype', ''), ('author', ''), ('year', ''), ('title', ''),
                      ('pub', ''), ('pub_raw', ''), ('volume', 'volume'), ('issue', 'issue'),
                      ('editor', ''), ('publisher', ''), ('page', ''), ('page_range', ''), ('doi', '')]
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


    def __get_citation(self, num_citations, export_format):
        """

        :param num_citations:
        :return:
        """
        if num_citations != 0:
            if (export_format == self.EXPORT_FORMAT_REF_XML) or (export_format == self.EXPORT_FORMAT_REF_ABS_XML):
                return str(num_citations)
            if (export_format == self.EXPORT_FORMAT_DUBLIN_XML):
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


    def __get_num_citations(self):
        """

        :return:
        """
        num_citations = 0
        for a_doc in self.from_solr['response'].get('docs'):
            num_citations += int(a_doc.get('num_citations', '0'))
        return num_citations


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
            elif (field == 'num_citations'):
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
            elif (field == 'aff'):
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
            elif (field == 'num_citations'):
                self.__add_in(record, fields[field], self.__get_citation(int(a_doc.get(field, 0)), export_format))
            elif (field == 'abstract'):
                self.__add_in(record, fields[field], self.__format_line_wrapped(a_doc.get(field, '')))
            elif (field == 'link'):
                self.__add_doc_links(a_doc, record)
            elif (field == 'eprintid'):
                self.__add_in(record, fields[field], get_eprint(a_doc))


    def __add_person_group_jats_xml(self, person_list, record, person_group_type):
        """
        add author or editors for JATS xml format

        :param record:
        :param person_group_type:
        :return:
        """
        if person_list:
            # add outter tag
            person_group_record = ET.SubElement(record, 'person-group')
            person_group_record.set('person-group-type', person_group_type)
            # now add inner tag
            for person in person_list:
                separate = person.split(',')
                # author might not have first name
                if len(separate) >= 1:
                    person_record = ET.SubElement(person_group_record, 'string-name')
                    ET.SubElement(person_record, 'surname').text = separate[0].strip()
                if len(separate) == 2:
                    ET.SubElement(person_record, 'given-names').text = '%s.'%separate[1].strip()[0]
            # add role tag if this is editor type
            if (person_group_type == 'editor'):
                ET.SubElement(record, 'role').text = 'Eds.'


    def __add_title_jats_xml(self, title, record, publication_type, lookahead):
        """
        format title basded on JATS publication type

        :param title:
        :param record:
        :param publication_type:
        :param lookahead:
        :return:
        """
        title = ';'.join(title)

        # <article-title>title</article-title>.
        if publication_type in ['journal', 'report']:
            title_record = ET.SubElement(record, 'article-title')
            title_record.text = title
            title_record.tail = '.\n'
        # <article-title>title</article-title>,
        elif publication_type == 'confproc':
            title_record = ET.SubElement(record, 'article-title')
            title_record.text = title
            title_record.tail = ',\n'
        # book: <source><italic>title</italic></source>
        # book with editor: <source><italic>title</italic></source>;
        elif publication_type == 'book':
            title_record = ET.SubElement(record, 'title')
            ET.SubElement(title_record, 'italic').text = title
            # is set to true if the record has editor and needs to have semicolon at the end
            if lookahead:
                title_record.tail = ';\n'
        # <source>Ph.D. thesis</source>
        elif publication_type == 'thesis':
            ET.SubElement(record, 'source').text = 'Ph.D. thesis'
        # <source>title</source>.
        elif publication_type in ['software', 'review', 'other']:
            ET.SubElement(record, 'source').text = title


    def __add_conf_proc_info_jats_xml(self, pub_raw, record):
        """
        for confproc publication type, jats format the following four tags are needed to be filled
        <conf-name>usually the first or second substring</conf-name>,
        <conf-loc>city/country usually appears following conference name</conf-loc>,
        <month>most records do not have the month of conference so for now ignore</month>
        <year>year of the conference usually appears in pub_raw</year>.

        :param pub_raw:
        :param record:
        :return:
        """
        # see if the year appears in pub_raw
        year = None
        match = self.re_year.search(pub_raw)
        if match:
            year = match.group(1)

        # see if the location is in pub_raw
        location = ''
        places = GeoText(pub_raw)
        if places.cities:
            location = places.cities
        if places.countries:
            if location:
                location += ', '
            location += places.countries

        # now split the pub_raw and try to see if conference name can be inferred
        conference = [s for s in list(reader([pub_raw]))[0] if 'conference' in s.lower()]
        if conference:
            ET.SubElement(record, 'conf-name').text = conference[0]
            if location:
                ET.SubElement(record, 'conf-loc').text = location
            if year:
                ET.SubElement(record, 'year').text = location


    def __add_book_publisher_info_jats_xml(self, pub_raw, record):
        """
        for book publication type, jats format the following four tags are needed to be filled
        <publisher-loc>in pub_raw</publisher-loc>:
        <publisher-name>in pub_raw</publisher-name>.

        :param pub_raw:
        :param record:
        :return:
        """
        # see if the location is in pub_raw
        location = ''
        places = GeoText(pub_raw)
        if places.cities:
            location = places.cities
        if places.countries:
            if location:
                location += ', '
            location += places.countries

        publisher = ''
        match = self.re_publisher_names.search(pub_raw, re.IGNORECASE)
        if match:
            publisher = match.group(1)

        if publisher:
            if location:
                location_record = ET.SubElement(record, 'publisher-loc')
                location_record.text = location
                location_record.tail = ': '
            ET.SubElement(record, 'publisher-name').text = publisher

    def __get_doc_jats_xml(self, index, parent):
        """
        for each document from Solr, get the fields, and format them accordingly for JATS format

        :param index:
        :param parent:
        :return:
        """
        ads_to_jats_doctype_mapping = {
            'book': 'book', 'inproceedings': 'book', 'inbook': 'book',
            'proceedings':'confproc',
            'article': 'journal', 'abstract': 'journal', 'eprint': 'journal',
            'phdthesis': 'thesis', 'mastersthesis': 'thesis',
            'software': 'software',
            'techreport': 'report',
            'bookreview': 'review',
            'circular': 'other', 'editorial': 'other', 'erratum': 'other', 'misc': 'other', 'catalog': 'other',
            'newsletter': 'other', 'obituary': 'other', 'pressrelease': 'other', 'proposal': 'other', 'talk': 'other',
        }
        a_doc = self.from_solr['response'].get('docs')[index]
        fields = self.__get_fields(self.EXPORT_FORMAT_JATS_XML)

        # add outter tag and label for this reference
        ref = ET.SubElement(parent, 'ref', id='CIT%03d'%(index+1))
        ET.SubElement(ref, 'label').text = '%d.'%(index+1)

        publication_type = ''
        for field in fields:
            if not a_doc.get(field, None):
                continue

            if (field == 'doctype'):
                publication_type = ads_to_jats_doctype_mapping[a_doc.get(field, '')]
                record = ET.SubElement(ref, 'mixed-citation')
                record.set('publication-type', publication_type)
            elif (field == 'author') or (field == 'editor'):
                self.__add_person_group_jats_xml(a_doc.get(field, []), record, field)
            elif (field == 'year'):
                # year appears in parenthesis, so need to find the last element and add open parenthesis
                if record:
                    record[-1].tail = '\n('
                else:
                    record.text = '\n('
                year = ET.SubElement(record, 'year')
                year.text = a_doc.get(field, '')
                # now add the close parenthesis
                year.tail = ')\n'
            elif (field == 'title'):
                self.__add_title_jats_xml(a_doc.get(field, ''), record, publication_type, a_doc.get('editor', None))
            elif (field == 'pub'):
                if (publication_type == 'journal'):
                    source_record = ET.SubElement(record, 'source')
                    ET.SubElement(source_record, 'italic').text = a_doc.get(field, '')
            elif (field == 'pub_raw'):
                if (publication_type == 'confproc'):
                    self.__add_conf_proc_info_jats_xml(a_doc.get(field, ''), record)
                # TODO: once solr contains publisher info need to remove extracting publisher from pub_raw
                elif (publication_type == 'book') or (publication_type == 'report'):
                    self.__add_book_publisher_info_jats_xml(a_doc.get(field, ''), record)
            elif (field == 'volume'):
                ET.SubElement(record, 'volume').text = a_doc.get(field, '')
            elif (field == 'issue'):
                # issue appears in parenthesis, so need to find the last element and add open parenthesis
                record[-1].tail = '(\n'
                issue = ET.SubElement(record, 'issue')
                issue.text = a_doc.get(field, '')
                # now add the close parenthesis followed by colon
                issue.tail = '):'
            elif (field == 'page'):
                ET.SubElement(record, 'fpage').text = ''.join(a_doc.get(field, ''))
            elif (field == 'page_range'):
                pages = ''.join(a_doc.get('page_range', '')).split('-')
                if len(pages) == 2:
                    # need to insert a dash before lastpage
                    record[-1].tail = ' #x2013;'
                    ET.SubElement(record, 'lpage').text = pages[1]
                # insert a dot after page info
                record[-1].tail = '.\n'
            elif (field == 'doi'):
                # need to add `doi:` before tag
                record[-1].tail = ' doi:'
                doi = ET.SubElement(record, 'pub-id')
                doi.set('pub-id-type', 'doi')
                doi.text = ''.join(a_doc.get(field, ''))


    def __get_xml(self, export_format):
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
            records.set('start', str(1))
            records.set('selected', str(num_docs))
            num_citations = self.__get_num_citations()
            if num_citations > 0:
                records.set('citations', str(num_citations))
            if (export_format == self.EXPORT_FORMAT_REF_XML) or (export_format == self.EXPORT_FORMAT_REF_ABS_XML):
                for index in range(num_docs):
                    self.__get_doc_reference_xml(index, records, export_format)
            elif (export_format == self.EXPORT_FORMAT_DUBLIN_XML):
                for index in range(num_docs):
                    self.__get_doc_dublin_xml(index, records)
            elif (export_format == self.EXPORT_FORMAT_JATS_XML):
                for index in range(num_docs):
                    self.__get_doc_jats_xml(index, records)
            format_xml = ET.tostring(records, encoding='utf8', method='xml')
            format_xml = (b'>\n<'.join(format_xml.split(b'><')))
            format_xml = format_xml.replace(b'</record>', b'</record>\n')
        result_dict = {}
        result_dict['msg'] = 'Retrieved {} abstracts, starting with number 1.'.format(num_docs)
        result_dict['export'] = format_xml.decode('utf8')
        return result_dict


    def get_reference_xml(self, include_abs=False):
        """

        :param include_abs:
        :return: reference xml format with or without abstract
        """
        if include_abs:
            return self.__get_xml(self.EXPORT_FORMAT_REF_ABS_XML)
        return self.__get_xml(self.EXPORT_FORMAT_REF_XML)


    def get_dublincore_xml(self):
        """

        :return: dublin xml format
        """
        return self.__get_xml(self.EXPORT_FORMAT_DUBLIN_XML)


    def get_jats_xml(self):
        """

        :return: jats xml format
        """
        return self.__get_xml(self.EXPORT_FORMAT_JATS_XML)

