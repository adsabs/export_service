# -*- coding: utf-8 -*-

from flask_testing import TestCase
import unittest

import json
import re

from collections import OrderedDict

import warnings

import exportsrv.app as app
import exportsrv.views as views

from exportsrv.tests.unittests.stubdata import solrdata, bibTexTest, fieldedTest, xmlTest, cslTest, customTest, voTableTest, rssTest
from exportsrv.formatter.ads import adsCSLStyle, adsJournalFormat, adsOrganizer, adsOutputFormat
from exportsrv.formatter.format import Format
from exportsrv.formatter.bibTexFormat import BibTexFormat
from exportsrv.formatter.fieldedFormat import FieldedFormat
from exportsrv.formatter.xmlFormat import XMLFormat
from exportsrv.formatter.cslJson import CSLJson
from exportsrv.formatter.cslFormat import CSLFormat, adsFormatter
from exportsrv.formatter.customFormat import CustomFormat
from exportsrv.formatter.voTableFormat import VOTableFormat
from exportsrv.formatter.rssFormat import RSSFormat
from exportsrv.formatter.toLaTex import encode_laTex
from exportsrv.formatter.latexencode import utf8tolatex
from exportsrv.utils import get_eprint, replace_html_entity
from exportsrv.views import get_export_format_for_journal_style

class TestExports(TestCase):

    def create_app(self):
        """ create app """

        self.current_app = app.create_app()
        return self.current_app


    def setUp(self):
        """ executed before each test """

        # prevent display of the following warning from citeproc
        #  /Users/gshapurian/code/export_service/python/lib/python3.8/site-packages/citeproc/source/__init__.py:31: UserWarning: The following arguments for Reference are unsupported: bibstem
        #    warn('The following arguments for {} are '.format(cls_name) +
        warnings.filterwarnings(action='ignore', category=UserWarning, module='citeproc')


    def tearDown(self):
        """ executed after each test """

        pass


    def test_bibtex(self):
        """ test Bibtex format """

        # format the stubdata using the code
        bibtex_export = BibTexFormat(solrdata.data, "%R").get(include_abs=False, max_author=10, author_cutoff=200, journal_format=1, output_format=1)
        # now compare it with an already formatted data that we know is correct
        assert (bibtex_export == bibTexTest.data)


    def test_bibtex_with_abs(self):
        """ test BibTex with abstract format """

        # format the stubdata using the code
        bibtex_export = BibTexFormat(solrdata.data, "%R").get(include_abs=True, max_author=0, author_cutoff=200, journal_format=1, output_format=1)
        # now compare it with an already formatted data that we know is correct
        assert (bibtex_export == bibTexTest.data_with_abs)


    def test_ads(self):
        """ test fielded format ADS """

        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_ads_fielded(output_format=1)
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_ads)


    def test_endnote(self):
        """ test fielded format endnote """

        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_endnote_fielded(output_format=1)
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_endnote)


    def test_procite(self):
        """ test fielded format procite """

        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_procite_fielded(output_format=1)
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_procite)


    def test_refman(self):
        """ test fielded format refman """

        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_refman_fielded(output_format=1)
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_refman)


    def test_refworks(self):
        """ test fielded format refworks """

        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_refworks_fielded(output_format=1)
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_refworks)


    def test_medlars(self):
        """ test fielded format medlars """

        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_medlars_fielded(output_format=1)
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_medlars)


    def test_dublinxml(self):
        """ test xml format Dublin """

        # format the stubdata using the code
        xml_export = XMLFormat(solrdata.data).get_dublincore_xml(output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_dublin_core)


    def test_refxml(self):
        """ test xml format Reference """

        # format the stubdata using the code
        xml_export = XMLFormat(solrdata.data).get_reference_xml(include_abs=False, output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_ref)


    def test_refxml_with_abs(self):
        """ test xml format Reference with abstract"""

        # format the stubdata using the code
        xml_export = XMLFormat(solrdata.data).get_reference_xml(include_abs=True, output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_ref_with_abs)


    def test_jatsxml(self):
        """ test xml format Jats """

        # format the stubdata using the code
        xml_export = XMLFormat(solrdata.data).get_jats_xml(output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_jats)


    def test_jatsxml_one_record(self):
        """ test xml format Jats when there is only one record """

        # format the stubdata using the code
        xml_export = XMLFormat(solrdata.data_2).get_jats_xml(output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_jats_one_record)


    def test_aastex(self):
        """ test csl format aastex """

        # format the stubdata using the code
        csl_export = CSLFormat(CSLJson(solrdata.data).get(), 'aastex', adsFormatter.latex).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_AASTex)


    def test_icarus(self):
        """ test csl format icarus """

        # format the stubdata using the code
        csl_export = CSLFormat(CSLJson(solrdata.data).get(), 'icarus', adsFormatter.latex).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_Icarus)


    def test_mnras(self):
        """ test csl format mnras """

        # format the stubdata using the code
        csl_export = CSLFormat(CSLJson(solrdata.data).get(), 'mnras', adsFormatter.latex).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert(csl_export == cslTest.data_MNRAS)


    def test_soph(self):
        """ test csl format soph """

        # format the stubdata using the code
        csl_export = CSLFormat(CSLJson(solrdata.data).get(), 'soph', adsFormatter.latex).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_SoPh)


    def test_aspc(self):
        """ test csl format aspc """

        # format the stubdata using the code
        csl_export = CSLFormat(CSLJson(solrdata.data).get(), 'aspc', adsFormatter.latex).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_ASPC)


    def test_apsj(self):
        """ test csl format apsj """

        # format the stubdata using the code
        csl_export = CSLFormat(CSLJson(solrdata.data).get(), 'apsj', adsFormatter.latex).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_APSJ)


    def test_aasj(self):
        """ test csl format aasj """

        # format the stubdata using the code
        csl_export = CSLFormat(CSLJson(solrdata.data).get(), 'aasj', adsFormatter.latex).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_AASJ)


    def test_ieee(self):
        """ test csl format ieee """

        # format the stubdata using the code
        csl_export = CSLFormat(CSLJson(solrdata.data).get(), 'ieee', adsFormatter.unicode).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_ieee)


    def test_agu(self):
        """ test csl format agu """

        # format the stubdata using the code
        csl_export = CSLFormat(CSLJson(solrdata.data).get(), 'agu', adsFormatter.unicode).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_agu)


    def test_gsa(self):
        """ test csl format gsa """

        # format the stubdata using the code
        csl_export = CSLFormat(CSLJson(solrdata.data).get(), 'gsa', adsFormatter.unicode).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_gsa)


    def test_ams(self):
        """ test csl format ams """

        # format the stubdata using the code
        csl_export = CSLFormat(CSLJson(solrdata.data).get(), 'ams', adsFormatter.unicode).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_ams)


    def test_custom(self):
        """ test custom format """

        # format the stubdata using the code
        custom_format = CustomFormat(custom_format=r'%ZEncoding:latex\\bibitem[%2.1m\\(%Y)]{%2H%Y}\ %5.3l\ %Y\,%j\,%V\,%p ')
        custom_format.set_json_from_solr(solrdata.data)
        # now compare it with an already formatted data that we know is correct
        assert (custom_format.get(adsOutputFormat.classic) == customTest.data)
        # verify correct solr fields are fetched
        assert (custom_format.get_solr_fields() == 'author,year,pub,volume,page,page_range,bibcode,bibstem')


    def test_ads_formatter(self):
        """ test adsFormatter class's verify method """

        assert(adsFormatter().verify('1') == True)
        assert(adsFormatter().verify(1) == True)
        assert(adsFormatter().verify('10') == False)
        assert(adsFormatter().verify(10) == False)


    def test_default_solr_fields(self):
        """ test default list of solr fields """

        default_fields = 'author,title,year,pubdate,pub,pub_raw,issue,volume,page,page_range,aff,aff_canonical,doi,abstract,' \
                         'read_count,bibcode,identifier,copyright,keyword,doctype,[citations],comment,pubnote,version,' \
                         'property,esources,data,isbn,eid,issn,arxiv_class,editor,series,publisher,bibstem,page_count,orcid_pub'
        assert (views.default_solr_fields() == default_fields)

        # test when there a limit is defined for authors and affilations
        author_limit = 3
        default_fields_limited = default_fields + f',[fields author={author_limit} aff={author_limit} aff_canonical={author_limit}]'
        assert (views.default_solr_fields(author_limit) == default_fields_limited)


    def test_bibtex_success(self):
        """ test views return_bibTex_format_export when succeed """

        response = views.return_bibTex_format_export(solrdata.data, False, '%R', 10, 200, 1, 1)
        assert(response._status_code == 200)


    def test_bibtex_no_data(self):
        """ test views return_bibTex_format_export when error """

        response = views.return_bibTex_format_export(None, False, '', 0, 0, 1, 1)
        assert(response._status_code == 404)


    def test_fielded_success(self):
        """ test views return_fielded_format_export when succeed for each fielded format """

        for fielded_style in ['ADS','EndNote','ProCite','Refman','RefWorks','MEDLARS']:
            response = views.return_fielded_format_export(solrdata.data, fielded_style, adsOutputFormat.classic)
            assert(response._status_code == 200)


    def test_fielded_no_data(self):
        """ test views return_fielded_format_export when error for each fielded format """

        for fielded_style in ['ADS','EndNote','ProCite','Refman','RefWorks','MEDLARS']:
            response = views.return_fielded_format_export(None, fielded_style, adsOutputFormat.classic)
            assert(response._status_code == 404)


    def test_xml_success(self):
        """ test views return_xml_format_export when succeed for each format """

        for xml_style in ['DublinCore','Reference','ReferenceAbs']:
            response = views.return_xml_format_export(solrdata.data, xml_style, adsOutputFormat.classic)
            assert(response._status_code == 200)


    def test_xml_no_data(self):
        """ test views return_xml_format_export when error for each format """

        for xml_style in ['DublinCore','Reference','ReferenceAbs']:
            response = views.return_xml_format_export(None, xml_style, adsOutputFormat.classic)
            assert(response._status_code == 404)


    def test_csl(self):
        """ test views return_csl_format_export when succeed for each format """

        export_format = 2
        journal_macro = 1
        for csl_style in ['aastex','icarus','mnras', 'soph', 'aspc', 'apsj', 'aasj', 'ieee', 'agu', 'gsa', 'ams']:
            response = views.return_csl_format_export(solrdata.data, csl_style, export_format, journal_macro, adsOutputFormat.classic)
            assert(response._status_code == 200)


    def test_csl_no_data(self):
        """ test views return_csl_format_export when error for each format """

        export_format = 2
        journal_macro = 1
        for csl_style in ['aastex','icarus','mnras', 'soph', 'aspc', 'apsj', 'aasj', 'ieee', 'agu', 'gsa', 'ams']:
            response = views.return_csl_format_export(None, csl_style, export_format, journal_macro, adsOutputFormat.classic)
            assert(response._status_code == 404)


    def test_eprintid(self):
        """ test extracting eprint id """

        a_doc_no_eprint = solrdata.data['response'].get('docs')[0]
        assert (get_eprint(a_doc_no_eprint) == '')

        a_doc_arxiv = \
            {
                "bibcode": "2018arXiv180303598K",
                "eid": "arXiv:1803.03598"
            }
        assert (get_eprint(a_doc_arxiv) == 'arXiv:1803.03598')

        a_doc_ascl = \
            {
                "bibcode": "2013ascl.soft08009C",
                "eid": "ascl:1308.009"
            }
        assert (get_eprint(a_doc_ascl) == 'ascl:1308.009')


    def test_replace_html_entity(self):
        """ test to verify html entities are replace correctly in the title and abstract """

        # note that if there is a entity error in the text it does not get replaced (ie, the first title lt; missing &)
        result = OrderedDict([
            ('1_title', [u'Study of SiO{}_{{{x}}} (1 < x lt; 2) Thin-Film Optical Waveguides']),
            ('2_abstract', u'Using Hubble Space Telescope Cosmic Origins Spectrograph observations of 89 QSO sightlines through the Sloan Digital Sky Survey footprint, we study the relationships between C IV absorption systems and the properties of nearby galaxies, as well as the large-scale environment. To maintain sensitivity to very faint galaxies, we restrict our sample to 0.0015< z< 0.015, which defines a complete galaxy survey to L≳ 0.01 L\\ast or stellar mass {M}<SUB>* </SUB>≳ {10}<SUP>8</SUP> {M}<SUB>☉ </SUB>. We report two principal findings. First, for galaxies with impact parameter ρ < 1 {r}<SUB>{vir</SUB>}, C IV detection strongly depends on the luminosity/stellar mass of the nearby galaxy. C IV is preferentially associated with galaxies with {M}<SUB>* </SUB>> {10}<SUP>9.5</SUP> {M}<SUB>☉ </SUB>; lower-mass galaxies rarely exhibit significant C IV absorption (covering fraction {f}<SUB>C</SUB>={9}<SUB>-6</SUB><SUP>+12</SUP> % for 11 galaxies with {M}<SUB>* </SUB>< {10}<SUP>9.5</SUP> {M}<SUB>☉ </SUB>). Second, C IV detection within the {M}<SUB>* </SUB>> {10}<SUP>9.5</SUP> {M}<SUB>☉ </SUB> population depends on environment. Using a fixed-aperture environmental density metric for galaxies with ρ < 160 kpc at z< 0.055, we find that {57}<SUB>-13</SUB><SUP>+12</SUP> % (8/14) of galaxies in low-density regions (regions with fewer than seven L> 0.15 L\\ast galaxies within 1.5 Mpc) have affiliated C IV absorption; however, none (0/7) of the galaxies in denser regions show C IV. Similarly, the C IV detection rate is lower for galaxies residing in groups with dark matter halo masses of {M}<SUB>{halo</SUB>}> {10}<SUP>12.5</SUP> {M}<SUB>☉ </SUB>. In contrast to C IV, H I is pervasive in the circumgalactic medium without regard to mass or environment. These results indicate that C IV absorbers with {log} N({{C}} {{IV}})≳ 13.5 {{cm}}<SUP>-2</SUP> trace the halos of {M}<SUB>* </SUB>> {10}<SUP>9.5</SUP> {M}<SUB>☉ </SUB> galaxies but also reflect larger-scale environmental conditions.'),
            ('3_title', [u'STIS CCD Amp A, C, & D Gains']),
            ('4_abstract', u'We use the Apparent Motion Parameters (AMP) method for the determination of orbits of visual double stars (Kiselev & Kiyaeva 1980). The quality of AMP orbits is completely dependent on the precision of parameters of relative positions and motions at the same instant. They are calculated on the basis of a short arc of observations. To determine these parameters, we use recent high precision observations obtained with the best modern techniques. New orbits of three stars are presented.'),
        ])
        for key, doc in zip(result.keys(), solrdata.data_24['response']['docs']):
            if isinstance(doc[key[2:]], list):
                assert(replace_html_entity(doc[key[2:]][0], encode_style=adsFormatter.unicode) == result[key][0])
            elif isinstance(doc[key[2:]], str):
                assert(replace_html_entity(doc[key[2:]], encode_style=adsFormatter.unicode) == result[key])


    def test_format_status(self):
        """ test to verify the Format class's get_status method """

        format_export = Format(solrdata.data)
        assert(format_export.get_status() == 0)


    def test_format_no_num_docs(self):
        """ test to verify that Format class can handle when there are no docs """

        format_export = Format(solrdata.data_25)
        assert(format_export.get_num_docs() == 0)


    def test_votable(self):
        """ test votable export format """

        # format the stubdata using the code
        votable_export = VOTableFormat(solrdata.data).get(output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (votable_export == voTableTest.data)


    def test_rss(self):
        """ test rss export format """

        # format the stubdata using the code
        rss_export = RSSFormat(solrdata.data).get(link='', output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (rss_export == rssTest.data)


    def test_views_return_votable_format_export_success(self):
        """ test views module return_votable_format_export method when successed"""

        response = views.return_votable_format_export(solrdata.data, adsOutputFormat.classic)
        assert(response._status_code == 200)


    def test_views_return_votable_format_export_no_data(self):
        """ test views module return_votable_format_export method when errors """

        response = views.return_votable_format_export(None, adsOutputFormat.classic)
        assert(response._status_code == 404)


    def test_views_return_rss_format_export_success(self):
        """ test views module return_rss_format_export method when successed"""

        response = views.return_rss_format_export(solrdata.data, '', adsOutputFormat.classic)
        assert(response._status_code == 200)


    def test_views_return_rss_format_export_no_data(self):
        """ test views module return_rss_format_export method when errors """

        response = views.return_rss_format_export(None, '', adsOutputFormat.classic)
        assert(response._status_code == 404)


    def test_rss_authors(self):
        """ test rss format for various types of available metadata """

        rss_export = RSSFormat(solrdata.data)
        # both author and title exists
        assert(rss_export._RSSFormat__get_author_title(solrdata.data_23['response'].get('docs', adsOutputFormat.classic)[0]) ==
               'Zhang, Yangjun: A Microwave Free-Space Method Using Artificial Lens with Anti-reflection Layer')
        # only author
        assert(rss_export._RSSFormat__get_author_title(solrdata.data_23['response'].get('docs', adsOutputFormat.classic)[1]) == 'Ryan, R. E.')
        # only title
        assert(rss_export._RSSFormat__get_author_title(solrdata.data_23['response'].get('docs', adsOutputFormat.classic)[2]) ==
               'Resolving Gas-Phase Metallicity In Galaxies')
        # neither author nor title exists
        assert(rss_export._RSSFormat__get_author_title(solrdata.data_23['response'].get('docs', adsOutputFormat.classic)[3]) == '')


    def test_all_gets(self):
        """ test all the get endpoints """

        function_names = [views.bibTex_format_export_get, views.bibTex_abs_format_export_get,
                          views.fielded_ads_format_export_get, views.fielded_endnote_format_export_get,
                          views.fielded_procite_format_export_get, views.fielded_refman_format_export_get,
                          views.fielded_refworks_format_export_get, views.fielded_medlars_format_export_get,
                          views.xml_dublincore_format_export_get, views.xml_ref_format_export_get,
                          views.xml_refabs_format_export_get, views.xml_jats_format_export_get,
                          views.csl_aastex_format_export_get, views.csl_icarus_format_export_get,
                          views.csl_mnras_format_export_get, views.csl_soph_format_export_get,
                          views.votable_format_export_get, views.rss_format_export_get,
                          views.csl_ieee_format_export_get, views.csl_aspc_format_export_get,
                          views.csl_aasj_format_export_get, views.csl_apsj_format_export_get,
                          views.csl_agu_format_export_get, views.csl_gsa_format_export_get, views.csl_ams_format_export_get]
        bibcode = self.app.config['EXPORT_SERVICE_TEST_BIBCODE_GET']
        for f in function_names:
            if f == views.rss_format_export_get:
                response = f(bibcode, '')
            else:
                response = f(bibcode)
            assert (response._status_code == 200)


    def test_all_posts(self):
        """ test all the post endpoints """

        endpoints = ['/bibtex', '/bibtexabs', '/ads', '/endnote', '/procite', '/ris', '/refworks', '/medlars',
                     '/dcxml', '/refxml', '/refabsxml', '/jatsxml', '/aastex', '/icarus', '/mnras', '/soph',
                     '/aspc', '/apsj', '/aasj', '/ieee', '/agu', '/gsa', '/ams',
                     '/custom', '/csl', '/votable', '/rss']

        payload_base = {'bibcode': self.app.config['EXPORT_SERVICE_TEST_BIBCODE_GET']}
        payload_specific = {
            '/bibtex': {'maxauthor': 0, 'authorcutoff': 0},
            '/rss': {'link': ''},
            '/custom': {'format': '%R'},
            '/csl': {'style': 'aastex', 'format': '1', 'journalformat': '2', 'outputformat': '1', 'sort': 'date desc', 'authorlimit': 10}
        }

        for ep in endpoints:
            payload = {**payload_base, **payload_specific.get(ep, {})}
            response = self.client.post(ep, data=json.dumps(payload))
            assert (response._status_code == 200)


    def test_posts_endpoint_payload_except(self):
        """ test the post endpoints when there is no payload """

        endpoints = ['/bibtex', '/bibtexabs', '/ads', '/endnote', '/procite', '/ris', '/refworks', '/medlars',
                     '/dcxml', '/refxml', '/refabsxml', '/jatsxml', '/aastex', '/icarus', '/mnras', '/soph',
                     '/aspc', '/apsj', '/aasj', '/ieee', '/agu', '/gsa', '/ams',
                     '/custom', '/csl', '/votable', '/rss']

        for ep in endpoints:
            response = self.client.post(ep, data=None)
            assert (response._status_code == 400)
            assert (response.data == b'{"error": "no information received"}')


    def test_bibtex_keyformat_endpoint(self):
        """ test the BibTeX endpoint with a specific key format and author limit """

        payload = {'bibcode': self.app.config['EXPORT_SERVICE_TEST_BIBCODE_GET'],
                   'keyformat': '%1H:%Y:%q',
                   'maxauthor': 2}
        response = self.client.post('/bibtex', data=json.dumps(payload))
        assert (response._status_code == 200)


    def test_bibtex_keyformat(self):
        """ test BibTex class to generate key format, including when eprint is specified """

        bibtex_export = BibTexFormat(solrdata.data_20, "%1H:%Y:%q")
        # both author and title exists
        assert(bibtex_export._BibTexFormat__format_key(solrdata.data_21['response'].get('docs')[0]) == 'Accomazzi:2019:AAS')
        # verify that key is ascii
        assert(bibtex_export._BibTexFormat__format_key(solrdata.data_21['response'].get('docs')[2]) == 'Garzon:2019:hsax')

        # if keyformat is eprintid and there is no eid in the record
        bibtex_export = BibTexFormat(solrdata.data_20, "%X")
        # must return the default bibcode
        assert(bibtex_export._BibTexFormat__format_key(solrdata.data_21['response'].get('docs')[0]) == '2019AAS...23338108A')

        # keyformat is eprintid
        bibtex_export = BibTexFormat(solrdata.data_22, "%X")
        assert(bibtex_export._BibTexFormat__format_key(solrdata.data_22['response'].get('docs')[0]) == 'arXiv:2112.00590')


    def test_no_journal_macro(self):
        """ test by passing replacing journal macros for journal names """

        # bibTex format
        # display full journal name
        bibtex_export = BibTexFormat(solrdata.data_5, "%R").get(include_abs=False, max_author=10, author_cutoff=200, journal_format=3, output_format=1).get('export', '')
        bibtex_full_journal_name = u'@ARTICLE{2018PhRvL.120b9901P,\n       author = {{Pustilnik}, M. and {van Heck}, B. and {Lutchyn}, R.~M. and {Glazman}, L.~I.},\n        title = "{Erratum: Quantum Criticality in Resonant Andreev Conduction [Phys. Rev. Lett. 119, 116802 (2017)]}",\n      journal = {Physical Review Letters},\n         year = 2018,\n        month = jan,\n       volume = {120},\n       number = {2},\n          eid = {029901},\n        pages = {029901},\n          doi = {10.1103/PhysRevLett.120.029901},\n       adsurl = {https://ui.adsabs.harvard.edu/abs/2018PhRvL.120b9901P},\n      adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n}\n\n'
        assert (bibtex_export == bibtex_full_journal_name)
        # display abbreviated journal name
        bibtex_export = BibTexFormat(solrdata.data_5, "%R").get(include_abs=False, max_author=10, author_cutoff=200, journal_format=2, output_format=1).get('export', '')
        bibtex_abbrev_journal_name = u'@ARTICLE{2018PhRvL.120b9901P,\n       author = {{Pustilnik}, M. and {van Heck}, B. and {Lutchyn}, R.~M. and {Glazman}, L.~I.},\n        title = "{Erratum: Quantum Criticality in Resonant Andreev Conduction [Phys. Rev. Lett. 119, 116802 (2017)]}",\n      journal = {PhRvL},\n         year = 2018,\n        month = jan,\n       volume = {120},\n       number = {2},\n          eid = {029901},\n        pages = {029901},\n          doi = {10.1103/PhysRevLett.120.029901},\n       adsurl = {https://ui.adsabs.harvard.edu/abs/2018PhRvL.120b9901P},\n      adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n}\n\n'
        assert (bibtex_export == bibtex_abbrev_journal_name)
        # macro (default)
        bibtex_export = BibTexFormat(solrdata.data_5, "%R").get(include_abs=False, max_author=10, author_cutoff=200, journal_format=0, output_format=1).get('export', '')
        bibtex_default_journal_name = u'@ARTICLE{2018PhRvL.120b9901P,\n       author = {{Pustilnik}, M. and {van Heck}, B. and {Lutchyn}, R.~M. and {Glazman}, L.~I.},\n        title = "{Erratum: Quantum Criticality in Resonant Andreev Conduction [Phys. Rev. Lett. 119, 116802 (2017)]}",\n      journal = {\\prl},\n         year = 2018,\n        month = jan,\n       volume = {120},\n       number = {2},\n          eid = {029901},\n        pages = {029901},\n          doi = {10.1103/PhysRevLett.120.029901},\n       adsurl = {https://ui.adsabs.harvard.edu/abs/2018PhRvL.120b9901P},\n      adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n}\n\n'
        assert (bibtex_export == bibtex_default_journal_name)

        # aastex format
        # display full journal name
        csl_export = CSLFormat(CSLJson(solrdata.data_5).get(), 'aastex', adsFormatter.latex, adsJournalFormat.full).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic).get('export', '')
        # now compare it with an already formatted data that we know is correct
        aastex_full_journal_name = u'\\bibitem[Pustilnik et al.(2018)]{2018PhRvL.120b9901P} Pustilnik, M., van Heck, B., Lutchyn, R.~M., et al.\\ 2018, Physical Review Letters, Erratum: Quantum Criticality in Resonant Andreev Conduction [Phys. Rev. Lett. 119, 116802 (2017)], 120, 2, 029901. doi:10.1103/PhysRevLett.120.029901\n'
        assert (csl_export == aastex_full_journal_name)
        # display abbreviated journal name
        csl_export = CSLFormat(CSLJson(solrdata.data_5).get(), 'aastex', adsFormatter.latex, adsJournalFormat.abbreviated).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic).get('export', '')
        # now compare it with an already formatted data that we know is correct
        aastex_abbrev_journal_name = u'\\bibitem[Pustilnik et al.(2018)]{2018PhRvL.120b9901P} Pustilnik, M., van Heck, B., Lutchyn, R.~M., et al.\\ 2018, PhRvL, Erratum: Quantum Criticality in Resonant Andreev Conduction [Phys. Rev. Lett. 119, 116802 (2017)], 120, 2, 029901. doi:10.1103/PhysRevLett.120.029901\n'
        assert (csl_export == aastex_abbrev_journal_name)
        # display default journal name, which is the macro option
        csl_export = CSLFormat(CSLJson(solrdata.data_5).get(), 'aastex', adsFormatter.latex, adsJournalFormat.default).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic).get('export', '')
        # now compare it with an already formatted data that we know is correct
        aastex_default_journal_name = u'\\bibitem[Pustilnik et al.(2018)]{2018PhRvL.120b9901P} Pustilnik, M., van Heck, B., Lutchyn, R.~M., et al.\\ 2018, \\prl, Erratum: Quantum Criticality in Resonant Andreev Conduction [Phys. Rev. Lett. 119, 116802 (2017)], 120, 2, 029901. doi:10.1103/PhysRevLett.120.029901\n'
        assert (csl_export == aastex_default_journal_name)
        # display abbreviated journal name that needs to be escaped
        csl_export = CSLFormat(CSLJson(solrdata.data_9).get(), 'aastex', adsFormatter.latex, adsJournalFormat.abbreviated).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic).get('export', '')
        # now compare it with an already formatted data that we know is correct
        aastex_abbrev_journal_name = u'\\bibitem[Ajani et al.(2021)]{2021A&A...645L..11A} Ajani, V., Starck, J.-L., \\& Pettorino, V.\\ 2021, A\\&A, Starlet {\ensuremath{\ell}}$_{1}$-norm for weak lensing cosmology, 645, L11. doi:10.1051/0004-6361/202039988\n'
        assert (csl_export == aastex_abbrev_journal_name)


    def test_bibtex_enumeration(self):
        """ test bibtex key_format enumeration """

        bibtex_export = BibTexFormat(solrdata.data_6, "%1H%Y%zm")
        key_formats_enumerated = ['Accomazzi2020', 'Accomazzi2019a', 'Accomazzi2015', 'Accomazzi2019b', 'Accomazzi2019c',
                                  'Accomazzi2018a', 'Accomazzi2018b', 'Accomazzi2017', 'Accomazzi2018c', 'Accomazzi2018d']
        assert (bibtex_export._BibTexFormat__enumerate_keys() == key_formats_enumerated)


    def test_tmp_bibcode_format(self):
        """ test bibcodes that have no volume and page but doi for all CSLFormat formats """

        csl_export_output = {
            'aastex': u'\\bibitem[Aharon(2005)]{2005GML...tmp....1A} Aharon, P.\\ 2005, Geo-Marine Letters, Catastrophic flood outbursts in mid-continent left imprints in the Gulf of Mexico. doi:10.1007/s00367-005-0006-y\n',
            'icarus': u'\\bibitem[Aharon(2005)]{2005GML...tmp....1A} Aharon, P.\\ 2005.\\ Catastrophic flood outbursts in mid-continent left imprints in the Gulf of Mexico.\\ Geo-Marine Letters. doi:10.1007/s00367-005-0006-y\n',
            'mnras': u'\\bibitem[\\protect\\citeauthoryear{Aharon}{2005}]{2005GML...tmp....1A} Aharon P., 2005, GML...tmp. doi:10.1007/s00367-005-0006-y\n',
            'soph': u'\\bibitem[Aharon(2005)]{2005GML...tmp....1A}Aharon, P.: 2005, {\\it Geo-Marine Letters}. doi:10.1007/s00367-005-0006-y.\n',
            'aspc': u'\\bibitem[Aharon(2005)]{2005GML...tmp....1A} Aharon, P.\\ 2005, Geo-Marine Letters. doi:10.1007/s00367-005-0006-y.\n',
            'apsj': u'P. Aharon, (2005). doi:10.1007/s00367-005-0006-y.\n',
            'aasj': u'\\bibitem[Aharon(2005)]{2005GML...tmp....1A} Aharon, P.\\ 2005, Geo-Marine Letters. doi:10.1007/s00367-005-0006-y.\n',
            'ieee': u'[1]Aharon, P., “Catastrophic flood outbursts in mid-continent left imprints in the Gulf of Mexico”, <i>Geo-Marine Letters</i>, 2005. doi:10.1007/s00367-005-0006-y.\n',
            'agu': u'Aharon, P. (2005) Catastrophic flood outbursts in mid-continent left imprints in the Gulf of Mexico <i>Geo-marine Letters</i>. https://doi.org/10.1007/s00367-005-0006-y\n',
            'gsa': u'Aharon, P., 2005, Catastrophic flood outbursts in mid-continent left imprints in the Gulf of Mexico: Geo-Marine Letters,, doi:10.1007/s00367-005-0006-y.\n',
            'ams': u'Aharon, P., 2005: Catastrophic flood outbursts in mid-continent left imprints in the Gulf of Mexico https://doi.org/10.1007/s00367-005-0006-y.\n',
        }
        cls_default_formats = [adsFormatter.latex] * 6 + [adsFormatter.unicode] * 5

        for style, format in zip(adsCSLStyle.ads_CLS, cls_default_formats):
            csl_export = CSLFormat(CSLJson(solrdata.data_7).get(), style, format).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic).get('export', '')
            assert (csl_export == csl_export_output[style])


    def test_encode_doi(self):
        """ test doi that is encoded properly """

        csl_export_output = {
            'aastex': u'\\bibitem[Greisen(2003)]{2003ASSL..285..109G} Greisen, E.~W.\\ 2003, Information Handling in Astronomy - Historical Vistas, AIPS, the VLA, and the VLBA, 285, 109. doi:10.1007/0-306-48080-8\_7\n',
            'icarus': u'\\bibitem[Greisen(2003)]{2003ASSL..285..109G} Greisen, E.~W.\\ 2003.\\ AIPS, the VLA, and the VLBA.\\ Information Handling in Astronomy - Historical Vistas 109. doi:10.1007/0-306-48080-8\\_7\n',
            'mnras': u'\\bibitem[\\protect\\citeauthoryear{Greisen}{2003}]{2003ASSL..285..109G} Greisen E.~W., 2003, ASSL, 285, 109. doi:10.1007/0-306-48080-8\\_7\n',
            'soph': u'\\bibitem[Greisen(2003)]{2003ASSL..285..109G}Greisen, E.W.: 2003, {\\it Information Handling in Astronomy - Historical Vistas}, 109. doi:10.1007/0-306-48080-8\\_7.\n',
            'aspc': u'\\bibitem[Greisen(2003)]{2003ASSL..285..109G} Greisen, E.~W.\\ 2003, Information Handling in Astronomy - Historical Vistas, 109. doi:10.1007/0-306-48080-8\\_7.\n',
            'apsj': u'E.~W. Greisen, in {\\bf 285}, 109. doi:10.1007/0-306-48080-8_7.\n',
            'aasj': u'\\bibitem[Greisen(2003)]{2003ASSL..285..109G} Greisen, E. W.\\ 2003, Information Handling in Astronomy - Historical Vistas, 109. doi:10.1007/0-306-48080-8\\_7.\n',
            'ieee': u'[1]Greisen, E. W., “AIPS, the VLA, and the VLBA”, in <i>Information Handling in Astronomy - Historical Vistas</i>, vol. 285, A. Heck, Ed. 2003, p. 109. doi:10.1007/0-306-48080-8_7.\n',
            'agu': u'Greisen, E. W. (2003) AIPS, the VLA, and the VLBA In A. Heck (Ed.), <i>Information Handling in Astronomy - Historical Vistas</i> (Vol. 285, p. 109). https://doi.org/10.1007/0-306-48080-8_7\n',
            'gsa': u'Greisen, E.W., 2003, AIPS, the VLA, and the VLBA, <i>in</i> Heck, A. ed., Information Handling in Astronomy - Historical Vistas, doi:10.1007/0-306-48080-8_7.\n',
            'ams': u'Greisen, E. W., 2003: AIPS, the VLA, and the VLBA. <i>Information Handling in Astronomy - Historical Vistas</i>, A. Heck, Ed., Vol. 285 of, p. 109, https://doi.org/10.1007/0-306-48080-8_7.\n',
        }
        cls_default_formats = [adsFormatter.latex] * 6 + [adsFormatter.unicode] * 5
        for style, format in zip(adsCSLStyle.ads_CLS, cls_default_formats):
            csl_export = CSLFormat(CSLJson(solrdata.data_10).get(), style, format).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic).get('export', '')
            assert (csl_export == csl_export_output[style])


    def test_encode_latex_greek_alphabet(self):
        """ test mapping of greek letter macros """

        title = 'Measurement of the \\Sigma\\ beam asymmetry for the \\omega\\ photo-production off the proton and the neutron at GRAAL'
        title_encoded = r'Measurement of the \textbackslash{}Sigma\textbackslash{} beam asymmetry for the \textbackslash{}omega\textbackslash{} photo-production off the proton and the neutron at GRAAL'
        assert(encode_laTex(title) == title_encoded)


    def test_misc_with_and_without_publiser(self):
        """ test misc for BibTex with and without publisher """

        # if publisher, display it, if not, format pub_raw in howpublished
        expected_bibtex_export = u'@software{2023zndo...8083529K,\n       author = {{Karras}, Oliver},\n        title = "{Analysis of the State and Evolution of Empirical Research in Requirements Engineering}",\n         year = 2023,\n        month = jun,\n          eid = {10.5281/zenodo.8083529},\n          doi = {10.5281/zenodo.8083529},\n      version = {v1.0},\n    publisher = {Zenodo},\n       adsurl = {https://ui.adsabs.harvard.edu/abs/2023zndo...8083529K},\n      adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n}\n\n@MISC{2023BoSAB..34......,\n        title = "{Proceedings da XLV Reuni{\\~a}o Anual da SAB}",\n howpublished = {Boletim da Sociedade Astr{\\^o}nomica Brasileira. Proceedings da XLV Reuni{\\~a}o Anual da SAB},\n         year = 2023,\n        month = jan,\n       adsurl = {https://ui.adsabs.harvard.edu/abs/2023BoSAB..34......},\n      adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n}\n\n@dataset{2012ddsw.rept.....T,\n       author = {{Thornton}, P.~E. and {Thornton}, M.~M. and {Mayer}, B.~W. and {Wilhelmi}, N. and {Wei}, Y. and {Devarakonda}, R. and {Cook}, R.},\n        title = "{Daymet: Daily surface weather on a 1 km grid for North America, 1980-2008}",\n howpublished = {Oak Ridge National Laboratory (ORNL) Distributed Active Archive Center for Biogeochemical Dynamics (DAAC)},\n         year = 2012,\n        month = apr,\n          doi = {10.3334/ORNLDAAC/1219},\n       adsurl = {https://ui.adsabs.harvard.edu/abs/2012ddsw.rept.....T},\n      adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n}\n\n'
        bibtex_export = BibTexFormat(solrdata.data_16, "%R").get(include_abs=False, max_author=10, author_cutoff=200, journal_format=3, output_format=1).get('export', '')
        assert(bibtex_export == expected_bibtex_export)


    def test_bibtex_publisher(self):
        """ format the publisher stubdata using the code """

        bibtex_export = BibTexFormat(solrdata.data_17, "%R").get(include_abs=False, max_author=10, author_cutoff=200, journal_format=1, output_format=1)
        # now compare it with an already formatted data that we know is correct
        assert (bibtex_export == bibTexTest.data_publisher)


    def test_bibtex_with_abs_publisher(self):
        """ format the publisher stubdata using the code """

        bibtex_export = BibTexFormat(solrdata.data_17, "%R").get(include_abs=True, max_author=0, author_cutoff=200, journal_format=1, output_format=1)
        # now compare it with an already formatted data that we know is correct
        assert (bibtex_export == bibTexTest.data_with_abs_publisher)


    def test_custom_publisher(self):
        """ format the publisher stubdata using the code """

        custom_format = CustomFormat(custom_format=r'%ZEncoding:latex\\bibitem[%2.1m\\(%Y)]{%2H%Y}\ %5.3l\ %Y\,%j\,%V\,%p\,Publisher:%pb ')
        custom_format.set_json_from_solr(solrdata.data_17)
        # now compare it with an already formatted data that we know is correct
        assert (custom_format.get(adsOutputFormat.classic) == customTest.data_publisher)
        # verify correct solr fields are fetched
        assert (custom_format.get_solr_fields() == 'author,year,pub,volume,publisher,page,page_range,bibcode,bibstem')


    def test_ads_publisher(self):
        """ format the publisher stubdata using the code """

        fielded_export = FieldedFormat(solrdata.data_17).get_ads_fielded(output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_ads_publisher)


    def test_endnote_publisher(self):
        """ format the publisher stubdata using the code """

        fielded_export = FieldedFormat(solrdata.data_17).get_endnote_fielded(output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_endnote_publisher)


    def test_procite_publisher(self):
        """ format the publisher stubdata using the code """

        fielded_export = FieldedFormat(solrdata.data_17).get_procite_fielded(output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_procite_publisher)


    def test_refman_publisher(self):
        """ format the publisher stubdata using the code """

        fielded_export = FieldedFormat(solrdata.data_17).get_refman_fielded(output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_refman_publisher)


    def test_refworks_publisher(self):
        """ format the publisher stubdata using the code """

        fielded_export = FieldedFormat(solrdata.data_17).get_refworks_fielded(output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_refworks_publisher)


    def test_dublinxml_publisher(self):
        """ format the publisher stubdata using the code """

        xml_export = XMLFormat(solrdata.data_17).get_dublincore_xml(output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_dublin_core_publisher)


    def test_refxml_with_abs_publisher(self):
        """ format the publisher stubdata using the code """

        xml_export = XMLFormat(solrdata.data_17).get_reference_xml(include_abs=True, output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert (xml_export == xmlTest.data_ref_with_abs_publisher)


    def test_jatsxml_publisher(self):
        """ format the publisher stubdata using the code """

        xml_export = XMLFormat(solrdata.data_17).get_jats_xml(output_format=adsOutputFormat.classic)
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_jats_publisher)


    def test_endnote_conf_loc(self):
        """ test extracting conference location from pub_raw """

        fielded_export = FieldedFormat({})
        fielded_export._FieldedFormat__setup_conf_loc()

        pub_raws = [
            "Solar Wind 4, Proceedings of the Conferene held in August 18-September 1, 1978 in Burghausen, FDR. Edited by H. Rosenbauer. MPAE-W-100-81-31. Garching, FDR: Max-Planck-Institute f√ºr Aeronomie",
            "AIAA, Aerospace Sciences Meeting, 28th, Reno, NV, Jan. 8-11, 1990. 16 p",
            "The Sun.  Part 1 of Solar-Terrestrial Physics/1970. Comprising the Proceedings fo the International Symposium on Solar-Terrestrial Physics Held in Leningrad, USSR, 12-19 May 1970.  Edited by C. de Jager and E. R. Dyer.  Dordrecht-Holland: D. Reidel Publishing Company.  Astrophysics and Space Science Library, Vol. 29",
            "Evolutionary Phenomena in Galaxies. Contributed papers, contributed at the Summer School, held July 4-15, 1988 in Puerto de la Cruz, Tenerife. Editors, J.E. Beckman, B.E.J. Pagel; Publisher, Cambridge University Press, Cambridge, England, New York, NY, 1989. LC # QB857.5.E96 E86 1989. ISBN: 0-521-37193-7. P. 1, 1989",
            "Presented at the Wind Workshop 6, Minneapolis, 1-3 Jun. 1983; sponsored by American Solar Energy Society",
            "Presented at the Symp. on Fluid Mech. of Combustion Systems, Boulder, Colo., 22 Jun. 1981",
        ]
        conference_locations = [
            "Burghausen",
            "Reno, NV",
            "Leningrad, USSR",
            "Puerto de la Cruz",
            "Minneapolis",
            "Boulder, Colo.",
        ]
        for pub_raw, conference_location in zip(pub_raws, conference_locations):
            assert(fielded_export._FieldedFormat__get_conf_loc(pub_raw) == conference_location)


    def test_encode_laTex(self):
        """ test for various scenarios in the encode_laTex function """

        # text with one $ sign, escape it
        text1 = "This is a test with one $ sign."
        expected1 = "This is a test with one \$ sign."
        self.assertEqual(encode_laTex(text1), expected1)

        # text with math mode chunks (even count of $), no substitution in the math mode
        text2 = "This is a $ math mode $ example."
        expected2 = "This is a $ math mode $ example."
        self.assertEqual(encode_laTex(text2), expected2)


    def test_utf8tolatex(self):
        """ test the main loop of utf8tolatex function to ensure correct processing of ASCII and non-ASCII characters """

        text = "Consider these characters: #, &, α, Θ, ☃, ♞."

        expected1 = r"Consider these characters: {\#}, {\&}, {\ensuremath{\alpha}}, {\ensuremath{\Theta}}, ☃, ♞."
        self.assertEqual(utf8tolatex(text, non_ascii_only=False, brackets=True, substitute_bad_chars=False, ascii_no_brackets=False), expected1)

        expected2 = r"Consider these characters: #, &, \ensuremath{\alpha}, \ensuremath{\Theta}, {\bfseries ?}, {\bfseries ?}."
        self.assertEqual(utf8tolatex(text, non_ascii_only=True, brackets=False, substitute_bad_chars=True, ascii_no_brackets=False), expected2)


    def test_generate_counter_id(self):
        """ test when the generated id string is longer that needs to be three characters long """
        length = (26**2) + 2
        counter_ids = Format(from_solr={}).generate_counter_id(length)
        self.assertEqual(len(counter_ids), 678)
        self.assertEqual(counter_ids[0], 'AA')
        self.assertEqual(counter_ids[-1], 'AAB')


    def test_adsOrganizer_citation_bibliography(self):
        """ test adsOrganizer's citation_bibliography option """

        csl_export = CSLFormat(CSLJson(solrdata.data_16).get(), 'ieee', adsFormatter.latex).get(export_organizer=adsOrganizer.citation_bibliography, output_format=adsOutputFormat.classic)
        expected_results = [
            '2023zndo...8083529K', '', '[1]Karras, O., “Analysis of the State and Evolution of Empirical Research in Requirements Engineering”, <i>Zenodo</i>, Art. no. 10.5281/zenodo.8083529, Zenodo, 2023. doi:10.5281/zenodo.8083529.',
            '2023BoSAB..34......', '', '[2]No author, “Proceedings da XLV Reunião Anual da SAB”, BoSAB..34, 2023.',
            '2012ddsw.rept.....T', '', '[3]Thornton, P. E., “Daymet: Daily surface weather on a 1 km grid for North America, 1980-2008”, <i>Oak Ridge National Laboratory (ORNL) Distributed Active Archive Center for Biogeochemical Dynamics (DAAC</i>, 2012. doi:10.3334/ORNLDAAC/1219.',
            ''
        ]
        self.assertEqual(csl_export.split('\n'), expected_results)

        # send it an unrecognizable export_organizer id
        self.assertEqual(CSLFormat(CSLJson(solrdata.data_16).get(), 'ieee', adsFormatter.latex).get(export_organizer=10, output_format=adsOutputFormat.classic), [])


    def test_adsFormatter_is_number(self):
        """ test adsFormatter's is_number method """

        # U+2162 Roman numeral three
        self.assertTrue(adsFormatter()._adsFormatter__is_number("Ⅲ"))
        # not a number
        self.assertFalse(adsFormatter()._adsFormatter__is_number("ABC"))


    def test_adsFormatter_native_encoding(self):
        """ test adsFormatter's native_encoding function to ensure the correct encoding is determined """

        instance = adsFormatter()

        # where native_format is in native_latex
        self.assertEqual(instance.native_encoding('BibTex'), adsFormatter.latex)

        # where native_format is in native_xml
        self.assertEqual(instance.native_encoding('DublinCore'), adsFormatter.xml)

        # where native_format is not in either list
        self.assertEqual(instance.native_encoding('UnknownFormat'), adsFormatter.unicode)


    def test_adsJournalFormat_verify(self):
        """ test adsJournalFormat's verify function """

        self.assertTrue(adsJournalFormat().verify(style=adsJournalFormat.full))
        # give it an undefined style
        self.assertFalse(adsJournalFormat().verify(style=10))


    def test_bibtex_authors_w_suffix(self):
        """ test bibtex format, formatting authors with suffix """

        bibtex_export = BibTexFormat(solrdata.data_18, "%R")
        expected_results = [
            '{Smith}, Jr, Frank D.',
            '{Thompson}, A. Richard and {Moran}, James M. and {Swenson}, Jr., George W.',
            '{Wang}, Y. -M. and {Sheeley}, Jr., N.~R.',
            '{Spilker}, Jr., J.~J.',
            '{Anderson}, D.~G. and {Goodyear}, A.~C. and {Stafford}, Jr., T.~W. and {Kennett}, J. and {West}, A.',
            '{Wang}, Y. -M. and {Sheeley}, Jr., N.~R.',
            '{Spitzer}, Jr., Lyman and {Hart}, Michael H.',
            '{Merow}, Cory and {Smith}, Matthew J. and {Silander}, Jr., John A.',
        ]

        for a_doc, expected_result in zip(bibtex_export.from_solr['response'].get('docs'), expected_results):
            self.assertEqual(bibtex_export._BibTexFormat__get_author_list(a_doc, 'author', max_author=0, author_cutoff=25), expected_result)


    def test_bibtex_authors_w_suffix_et_al(self):
        """ test bibtex format, formatting authors with suffix, shorten the list """

        bibtex_export = BibTexFormat(solrdata.data_18, "%R")
        expected_results = [
            '{Smith}, Jr, Frank D.',
            '{Thompson}, A. Richard and et al.',
            '{Wang}, Y. -M. and {Sheeley}, Jr., N.~R.',
            '{Spilker}, Jr., J.~J.',
            '{Anderson}, D.~G. and et al.',
            '{Wang}, Y. -M. and {Sheeley}, Jr., N.~R.',
            '{Spitzer}, Jr., Lyman and {Hart}, Michael H.',
            '{Merow}, Cory and et al.',
        ]

        for a_doc, expected_result in zip(bibtex_export.from_solr['response'].get('docs'), expected_results):
            # show one author is more than 2
            self.assertEqual(bibtex_export._BibTexFormat__get_author_list(a_doc, 'author', max_author=1, author_cutoff=2), expected_result)


    def test_get_author_lastname_list(self):
        """ test Bibtex format's get_author_lastname_list method """

        bibtex_export = BibTexFormat(solrdata.data_18, "%R")

        expected_results = [
            'Smith',
            'ThompsonMoranSwenson',
            'WangSheeley',
            'Spilker',
            'AndersonGoodyearStaffordKennettWest',
            'WangSheeley',
            'SpitzerHart',
            'MerowSmithSilander',
        ]

        for a_doc, expected_result in zip(bibtex_export.from_solr['response'].get('docs'), expected_results):
            self.assertEqual(bibtex_export._BibTexFormat__get_author_lastname_list(a_doc, max_author=10), expected_result)


    def test_get_affiliation_list(self):
        """ test Bibtex format's get_affiliation_list method """

        # when there is no aff in a doc
        bibtex_export = BibTexFormat(solrdata.data_8, "%R")

        for a_doc in bibtex_export.from_solr['response'].get('docs'):
            self.assertEqual(bibtex_export._BibTexFormat__get_affiliation_list(a_doc, max_author=0, author_cutoff=25), '')

        bibtex_export = BibTexFormat(solrdata.data_9, "%R")

        # when there are aff and doctype is not thesis
        expected_results = [
            r'AA(AIM, CEA, CNRS, Universit{\'e} Paris-Saclay, Universit{\'e} de Paris, Sorbonne Paris Cit{\'e}, 91191, Gif-sur-Yvette, France), AB(AIM, CEA, CNRS, Universit{\'e} Paris-Saclay, Universit{\'e} de Paris, Sorbonne Paris Cit{\'e}, 91191, Gif-sur-Yvette, France), AC(AIM, CEA, CNRS, Universit{\'e} Paris-Saclay, Universit{\'e} de Paris, Sorbonne Paris Cit{\'e}, 91191, Gif-sur-Yvette, France)'
        ]

        for a_doc, expected_result in zip(bibtex_export.from_solr['response'].get('docs'), expected_results):
            self.assertEqual(bibtex_export._BibTexFormat__get_affiliation_list(a_doc, max_author=0, author_cutoff=25), expected_result)

        # now returned just one author
        expected_results = [
            r'AA(AIM, CEA, CNRS, Universit{\'e} Paris-Saclay, Universit{\'e} de Paris, Sorbonne Paris Cit{\'e}, 91191, Gif-sur-Yvette, France)'
        ]

        for a_doc, expected_result in zip(bibtex_export.from_solr['response'].get('docs'), expected_results):
            self.assertEqual(bibtex_export._BibTexFormat__get_affiliation_list(a_doc, max_author=1, author_cutoff=2), expected_result)


    def test_bibtex_add_clean_pub_raw(self):
        """ test bibtex format's add_clean_pub_raw method """

        bibtex_export = BibTexFormat(solrdata.data_9, "%R")

        expected_result = 'Astronomy \& Astrophysics, Volume 645, id.L11, 8 pp.'

        result = bibtex_export._BibTexFormat__add_clean_pub_raw(bibtex_export.from_solr['response'].get('docs')[0])

        self.assertEqual(result, expected_result)


    def test_bibtex_add_in_eprint(self):
        """ Test Bibtex format's add_in_eprint method """

        bibtex_export = BibTexFormat(solrdata.data_9, "%R")

        a_doc = bibtex_export.from_solr['response'].get('docs')[0]

        self.assertEqual(bibtex_export._BibTexFormat__add_in_eprint('archivePrefix|eprint', get_eprint(a_doc), u'{0:>13} = {{{1}}}'), 'archivePrefix = {arXiv},\n       eprint = {2101.01542},\n')

        # now send input that are not correct
        self.assertEqual(bibtex_export._BibTexFormat__add_in_eprint('eprint', 'can be empty too', u'{0:>13} = {{{1}}}'), '')


    def test_bibtex_keyformat_enumeration(self):
        """ text Bibtex format's get method check for keyformat enumeration """

        bibtex_export = BibTexFormat(solrdata.data_19, "%zm%H").get(include_abs=False, max_author=10, author_cutoff=200, journal_format=1, output_format=1)

        assert (bibtex_export == {'msg': 'Retrieved 3 abstracts, starting with number 1.', 'export': '{Shapuriana\n}\n\n{Shapurianb\n}\n\n{Koch\n}\n\n'})


    def test_bibtex_keyformat_ascii(self):
        """ text Bibtex format's get method check for keyformat being ascii """

        bibtex_export = BibTexFormat(solrdata.data_20, "%H").get(include_abs=False, max_author=10, author_cutoff=200, journal_format=1, output_format=1)

        assert (bibtex_export == {'msg': 'Retrieved 1 abstracts, starting with number 1.', 'export': '{Andre\n}\n\n'})


    def test_bibtex_field_wrapped(self):
        """ text Bibtex format's field_wrapped method when no value is passed in to return empty string """

        assert (BibTexFormat(solrdata.data_20, "%H")._BibTexFormat__field_wrapped('', '', ''), '')


    def test_bibtex_get_journal(self):
        """ text Bibtex format's get_journal method when doctype is software to return empty string """

        bibtex_export = BibTexFormat(solrdata.data_16, "%R")
        a_doc = bibtex_export.from_solr['response'].get('docs')[0]

        assert (BibTexFormat(solrdata.data_10, "%R")._BibTexFormat__get_journal(a_doc, ''), None)


    def test_bibtex_format_line_wrapped(self):
        """ text Bibtex format's format_line_wrapped """

        assert (BibTexFormat(solrdata.data_20, "%H")._BibTexFormat__format_line_wrapped('author', 'Di Francesco, J.', u'{0:>13} = {{{1}}}'), 'author = {Di Francesco, J.}')


    def test_views_get_export_format_for_journal_style(self):
        """ test views module's get_export_format_for_journal_style method """

        # if payload is not valid, knowing the style aastex is useless
        assert (get_export_format_for_journal_style(payload={}, style='aastex') == -1)

        # if style is one of these, ['icarus', 'mnras', 'soph', 'apsj'], return value is 3
        assert (get_export_format_for_journal_style(payload={}, style='icarus') == 3)

        # when style is unknown
        assert (get_export_format_for_journal_style(payload={}, style='') == -1)


    def test_doi_cls(self):
        """ test that all doctypes for thecsl format display doi"""
        re_doi = re.compile(r"(doi:10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)")

        formats = ['aastex']
        for format in formats:
            # format the stubdata using the code
            csl_export = CSLFormat(CSLJson(solrdata.data_26).get(), format, adsFormatter.latex).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.classic)
            for doc in csl_export['export'][:-1].split('\n'):
                # now verify that it found it
                assert (re_doi.search(doc))


    def test_output_format_individual(self):
        """ test the new output format that displays bibcodes and references individually """

        # custom format csv when there is a header only
        custom_format = CustomFormat(custom_format=r'%ZEncoding:csv %R,%H')
        custom_format.set_json_from_solr(solrdata.data_17)
        expected = {
            'num_docs': 5,
            'docs': [
                {'bibcode': '2024zndo..10908474S', 'reference': '"2024zndo..10908474S","Schade"'},
                {'bibcode': '2024wsp..conf...20V', 'reference': '"2024wsp..conf...20V","Vidmachenko"'},
                {'bibcode': '2024asal.book..204V', 'reference': '"2024asal.book..204V","Vidmachenko"'},
                {'bibcode': '2018scrp.conf.....K', 'reference': '"2018scrp.conf.....K","Kent"'},
                {'bibcode': '2023uwff.book.....R', 'reference': '"2023uwff.book.....R","Renwick"'}
            ],
            'header': '"bibcode","author"'
        }
        assert (custom_format.get(adsOutputFormat.individual) == expected)

        # ieee format when there is no header or footer
        exported = CSLFormat(CSLJson(solrdata.data_17).get(), 'ieee', adsFormatter.unicode).get(export_organizer=adsOrganizer.plain, output_format=adsOutputFormat.individual)
        expected = {
            'num_docs': 5,
            'docs': [
                {'bibcode': '2024zndo..10908474S', 'reference': '[1]Schade, R., “pc2/pqdts: v2024.2”, <i>Zenodo</i>, Art. no. 10.5281/zenodo.10908474, Zenodo, 2024. doi:10.5281/zenodo.10908474.'},
                {'bibcode': '2024wsp..conf...20V', 'reference': '[2]Vidmachenko, A., “A modern view of former rivers on Mars.”, in <i>Proceedings of the VIII International Scientific and Practical Conference. World science priorities (February 08 – 09</i>, 2024, pp. 20–25.'},
                {'bibcode': '2024asal.book..204V', 'reference': '[3]Vidmachenko, A., “New generation telescopes for the astronomy of the future.”, in <i>In book: Astronomical almanac</i>, Kyiv, 2024, pp. 204–209.'},
                {'bibcode': '2018scrp.conf.....K', 'reference': '[4]Kent, B. R., “Science and Computing with Raspberry Pi”, in <i>Science and Computing with Raspberry Pi</i>, 2018.'},
                {'bibcode': '2023uwff.book.....R', 'reference': '[5]Renwick, J. A., <i>Under the weather: a future forecast for New Zealand</i>. HarperCollins, 2023.'}]
        }
        assert (exported == expected)

        # dublin xml when there is both header and footer
        exported = XMLFormat(solrdata.data).get_dublincore_xml(output_format=adsOutputFormat.individual)
        assert (exported == xmlTest.data_dublin_core_individual)


if __name__ == '__main__':
  unittest.main()
