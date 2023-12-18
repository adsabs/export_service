# -*- coding: utf-8 -*-

from flask_testing import TestCase
import unittest

import json

from collections import OrderedDict

import warnings

import exportsrv.app as app
import exportsrv.views as views

from exportsrv.tests.unittests.stubdata import solrdata, bibTexTest, fieldedTest, xmlTest, cslTest, customTest, voTableTest, rssTest
from exportsrv.formatter.ads import adsCSLStyle, adsJournalFormat
from exportsrv.formatter.format import Format
from exportsrv.formatter.bibTexFormat import BibTexFormat
from exportsrv.formatter.fieldedFormat import FieldedFormat
from exportsrv.formatter.xmlFormat import XMLFormat
from exportsrv.formatter.cslJson import CSLJson
from exportsrv.formatter.csl import CSL, adsFormatter
from exportsrv.formatter.customFormat import CustomFormat
from exportsrv.formatter.voTableFormat import VOTableFormat
from exportsrv.formatter.rssFormat import RSSFormat
from exportsrv.formatter.toLaTex import encode_laTex
from exportsrv.utils import get_eprint, replace_html_entity

class TestExports(TestCase):
    def create_app(self):
        app_ = app.create_app()
        return app_

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
        # format the stubdata using the code
        bibtex_export = BibTexFormat(solrdata.data, "%R").get(include_abs=False, maxauthor=10, authorcutoff=200, journalformat=1)
        # now compare it with an already formatted data that we know is correct
        assert (bibtex_export == bibTexTest.data)

    def test_bibtex_with_abs(self):
        # format the stubdata using the code
        bibtex_export = BibTexFormat(solrdata.data, "%R").get(include_abs=True, maxauthor=0, authorcutoff=200, journalformat=1)
        # now compare it with an already formatted data that we know is correct
        assert (bibtex_export == bibTexTest.data_with_abs)

    def test_ads(self):
        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_ads_fielded()
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_ads)

    def test_endnote(self):
        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_endnote_fielded()
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_endnote)

    def test_procite(self):
        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_procite_fielded()
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_procite)

    def test_refman(self):
        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_refman_fielded()
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_refman)

    def test_refworks(self):
        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_refworks_fielded()
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_refworks)

    def test_medlars(self):
        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_medlars_fielded()
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_medlars)

    def test_dublinxml(self):
        # format the stubdata using the code
        xml_export = XMLFormat(solrdata.data).get_dublincore_xml()
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_dublin_core)

    def test_refxml(self):
        # format the stubdata using the code
        xml_export = XMLFormat(solrdata.data).get_reference_xml(include_abs=False)
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_ref)

    def test_refxml_with_abs(self):
        # format the stubdata using the code
        xml_export = XMLFormat(solrdata.data).get_reference_xml(include_abs=True)
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_ref_with_abs)

    def test_jatsxml(self):
        # format the stubdata using the code
        xml_export = XMLFormat(solrdata.data).get_jats_xml()
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_jats)

    def test_jatsxml_one_record(self):
        # format the stubdata using the code
        xml_export = XMLFormat(solrdata.data_2).get_jats_xml()
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_jats_one_record)

    def test_aastex(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'aastex', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_AASTex)

    def test_icarus(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'icarus', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_Icarus)

    def test_mnras(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'mnras', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert(csl_export == cslTest.data_MNRAS)

    def test_soph(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'soph', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_SoPh)

    def test_aspc(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'aspc', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_ASPC)

    def test_apsj(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'apsj', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_APSJ)

    def test_aasj(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'aasj', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_AASJ)

    def test_ieee(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'ieee', adsFormatter.unicode).get()
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_ieee)

    def test_custom(self):
        # format the stubdata using the code
        custom_format = CustomFormat(custom_format=r'%ZEncoding:latex\\bibitem[%2.1m\\(%Y)]{%2H%Y}\ %5.3l\ %Y\,%j\,%V\,%p ')
        custom_format.set_json_from_solr(solrdata.data)
        # now compare it with an already formatted data that we know is correct
        assert (custom_format.get() == customTest.data)
        # verify correct solr fields are fetched
        assert (custom_format.get_solr_fields() == 'author,year,pub,volume,page,page_range,bibcode,bibstem')

    def test_ads_formatter(self):
        assert(adsFormatter().verify('1') == True)
        assert(adsFormatter().verify(1) == True)
        assert(adsFormatter().verify('10') == False)
        assert(adsFormatter().verify(10) == False)

    def test_default_solr_fields(self):
        default_fields = 'author,title,year,pubdate,pub,pub_raw,issue,volume,page,page_range,aff,aff_canonical,doi,abstract,' \
                         'read_count,bibcode,identifier,copyright,keyword,doctype,[citations],comment,pubnote,version,' \
                         'property,esources,data,isbn,eid,issn,arxiv_class,editor,series,publisher,bibstem,page_count,orcid_pub'
        assert (views.default_solr_fields() == default_fields)

    def test_bibtex_success(self):
        response = views.return_bibTex_format_export(solrdata.data, False, '%R', 10, 200, 1)
        assert(response._status_code == 200)

    def test_bibtex_no_data(self):
        response = views.return_bibTex_format_export(None, False, '', 0, 0, 1)
        assert(response._status_code == 404)

    def test_fielded_success(self):
        for fielded_style in ['ADS','EndNote','ProCite','Refman','RefWorks','MEDLARS']:
            response = views.return_fielded_format_export(solrdata.data, fielded_style)
            assert(response._status_code == 200)

    def test_fielded_no_data(self):
        for fielded_style in ['ADS','EndNote','ProCite','Refman','RefWorks','MEDLARS']:
            response = views.return_fielded_format_export(None, fielded_style)
            assert(response._status_code == 404)

    def test_xml_success(self):
        for xml_style in ['DublinCore','Reference','ReferenceAbs']:
            response = views.return_xml_format_export(solrdata.data, xml_style)
            assert(response._status_code == 200)

    def test_xml_no_data(self):
        for xml_style in ['DublinCore','Reference','ReferenceAbs']:
            response = views.return_xml_format_export(None, xml_style)
            assert(response._status_code == 404)

    def test_csl(self):
        export_format = 2
        journal_macro = 1
        for csl_style in ['aastex','icarus','mnras', 'soph', 'aspc', 'apsj', 'aasj', 'ieee']:
            response = views.return_csl_format_export(solrdata.data, csl_style, export_format, journal_macro)
            assert(response._status_code == 200)

    def test_csl_no_data(self):
        export_format = 2
        journal_macro = 1
        for csl_style in ['aastex','icarus','mnras', 'soph', 'aspc', 'apsj', 'aasj', 'ieee']:
            response = views.return_csl_format_export(None, csl_style, export_format, journal_macro)
            assert(response._status_code == 404)

    def test_eprint(self):
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
        solr_data = \
            {
                "responseHeader": {
                    "status": 0,
                    "QTime": 2,
                    "params": {
                        "q": "title:\"lt;\"",
                        "indent": "on",
                        "fl": "bibcode,title,abstract",
                        "wt": "json",
                        "_": "1592510843440"}},
                "response": {"numFound": 4, "start": 0, "docs": [
                    {
                        "bibcode": "2016JLwT...34.4926L",
                        "title": ["Study of SiO{}_{{{x}}} (1 &lt; x lt; 2) Thin-Film Optical Waveguides"]},
                    {
                        "abstract": "Using Hubble Space Telescope Cosmic Origins Spectrograph observations of 89 QSO sightlines through the Sloan Digital Sky Survey footprint, we study the relationships between C IV absorption systems and the properties of nearby galaxies, as well as the large-scale environment. To maintain sensitivity to very faint galaxies, we restrict our sample to 0.0015&lt; z&lt; 0.015, which defines a complete galaxy survey to L≳ 0.01 L\\ast or stellar mass {M}<SUB>* </SUB>≳ {10}<SUP>8</SUP> {M}<SUB>☉ </SUB>. We report two principal findings. First, for galaxies with impact parameter ρ &lt; 1 {r}<SUB>{vir</SUB>}, C IV detection strongly depends on the luminosity/stellar mass of the nearby galaxy. C IV is preferentially associated with galaxies with {M}<SUB>* </SUB>&gt; {10}<SUP>9.5</SUP> {M}<SUB>☉ </SUB>; lower-mass galaxies rarely exhibit significant C IV absorption (covering fraction {f}<SUB>C</SUB>={9}<SUB>-6</SUB><SUP>+12</SUP> % for 11 galaxies with {M}<SUB>* </SUB>&lt; {10}<SUP>9.5</SUP> {M}<SUB>☉ </SUB>). Second, C IV detection within the {M}<SUB>* </SUB>&gt; {10}<SUP>9.5</SUP> {M}<SUB>☉ </SUB> population depends on environment. Using a fixed-aperture environmental density metric for galaxies with ρ &lt; 160 kpc at z&lt; 0.055, we find that {57}<SUB>-13</SUB><SUP>+12</SUP> % (8/14) of galaxies in low-density regions (regions with fewer than seven L&gt; 0.15 L\\ast galaxies within 1.5 Mpc) have affiliated C IV absorption; however, none (0/7) of the galaxies in denser regions show C IV. Similarly, the C IV detection rate is lower for galaxies residing in groups with dark matter halo masses of {M}<SUB>{halo</SUB>}&gt; {10}<SUP>12.5</SUP> {M}<SUB>☉ </SUB>. In contrast to C IV, H I is pervasive in the circumgalactic medium without regard to mass or environment. These results indicate that C IV absorbers with {log} N({{C}} {{IV}})≳ 13.5 {{cm}}<SUP>-2</SUP> trace the halos of {M}<SUB>* </SUB>&gt; {10}<SUP>9.5</SUP> {M}<SUB>☉ </SUB> galaxies but also reflect larger-scale environmental conditions.",
                        "bibcode": "2016ApJ...832..124B"},
                    {
                        "bibcode": "2015hst..prop14424B",
                        "title": ["STIS CCD Amp A, C, &amp; D Gains"]},
                    {
                        "bibcode": "2016BaltA..25..310K",
                        "abstract": "We use the Apparent Motion Parameters (AMP) method for the determination of orbits of visual double stars (Kiselev &amp; Kiyaeva 1980). The quality of AMP orbits is completely dependent on the precision of parameters of relative positions and motions at the same instant. They are calculated on the basis of a short arc of observations. To determine these parameters, we use recent high precision observations obtained with the best modern techniques. New orbits of three stars are presented."},
                ]}
            }
        # note that if there is a entity error in the text it does not get replaced (ie, the first title lt; missing &)
        result = OrderedDict([
            ('1_title', [u'Study of SiO{}_{{{x}}} (1 < x lt; 2) Thin-Film Optical Waveguides']),
            ('2_abstract', u'Using Hubble Space Telescope Cosmic Origins Spectrograph observations of 89 QSO sightlines through the Sloan Digital Sky Survey footprint, we study the relationships between C IV absorption systems and the properties of nearby galaxies, as well as the large-scale environment. To maintain sensitivity to very faint galaxies, we restrict our sample to 0.0015< z< 0.015, which defines a complete galaxy survey to L≳ 0.01 L\\ast or stellar mass {M}<SUB>* </SUB>≳ {10}<SUP>8</SUP> {M}<SUB>☉ </SUB>. We report two principal findings. First, for galaxies with impact parameter ρ < 1 {r}<SUB>{vir</SUB>}, C IV detection strongly depends on the luminosity/stellar mass of the nearby galaxy. C IV is preferentially associated with galaxies with {M}<SUB>* </SUB>> {10}<SUP>9.5</SUP> {M}<SUB>☉ </SUB>; lower-mass galaxies rarely exhibit significant C IV absorption (covering fraction {f}<SUB>C</SUB>={9}<SUB>-6</SUB><SUP>+12</SUP> % for 11 galaxies with {M}<SUB>* </SUB>< {10}<SUP>9.5</SUP> {M}<SUB>☉ </SUB>). Second, C IV detection within the {M}<SUB>* </SUB>> {10}<SUP>9.5</SUP> {M}<SUB>☉ </SUB> population depends on environment. Using a fixed-aperture environmental density metric for galaxies with ρ < 160 kpc at z< 0.055, we find that {57}<SUB>-13</SUB><SUP>+12</SUP> % (8/14) of galaxies in low-density regions (regions with fewer than seven L> 0.15 L\\ast galaxies within 1.5 Mpc) have affiliated C IV absorption; however, none (0/7) of the galaxies in denser regions show C IV. Similarly, the C IV detection rate is lower for galaxies residing in groups with dark matter halo masses of {M}<SUB>{halo</SUB>}> {10}<SUP>12.5</SUP> {M}<SUB>☉ </SUB>. In contrast to C IV, H I is pervasive in the circumgalactic medium without regard to mass or environment. These results indicate that C IV absorbers with {log} N({{C}} {{IV}})≳ 13.5 {{cm}}<SUP>-2</SUP> trace the halos of {M}<SUB>* </SUB>> {10}<SUP>9.5</SUP> {M}<SUB>☉ </SUB> galaxies but also reflect larger-scale environmental conditions.'),
            ('3_title', [u'STIS CCD Amp A, C, & D Gains']),
            ('4_abstract', u'We use the Apparent Motion Parameters (AMP) method for the determination of orbits of visual double stars (Kiselev & Kiyaeva 1980). The quality of AMP orbits is completely dependent on the precision of parameters of relative positions and motions at the same instant. They are calculated on the basis of a short arc of observations. To determine these parameters, we use recent high precision observations obtained with the best modern techniques. New orbits of three stars are presented.'),
        ])
        for key, doc in zip(result.keys(), solr_data['response']['docs']):
            if isinstance(doc[key[2:]], list):
                assert(replace_html_entity(doc[key[2:]][0], encode_style=adsFormatter.unicode) == result[key][0])
            elif isinstance(doc[key[2:]], str):
                assert(replace_html_entity(doc[key[2:]], encode_style=adsFormatter.unicode) == result[key])

    def test_format_status(self):
        format_export = Format(solrdata.data)
        assert(format_export.get_status() == 0)

    def test_format_no_num_docs(self):
        solr_data = \
            {
               "responseHeader":{
                  "status":1,
                  "QTime":1,
                  "params":{
                     "sort":"date desc",
                     "fq":"{!bitset}",
                     "rows":"19",
                     "q":"*:*",
                     "start":"0",
                     "wt":"json",
                     "fl":"author,title,year,date,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,num_citations,read_count,bibcode,identification,copyright,keyword,doctype,num_references,comment,property,esources,data"
                  }
               }
            }
        format_export = Format(solr_data)
        assert(format_export.get_num_docs() == 0)

    def test_votable(self):
        # format the stubdata using the code
        votable_export = VOTableFormat(solrdata.data).get()
        # now compare it with an already formatted data that we know is correct
        assert (votable_export == voTableTest.data)

    def test_rss(self):
        # format the stubdata using the code
        rss_export = RSSFormat(solrdata.data).get()
        # now compare it with an already formatted data that we know is correct
        assert (rss_export == rssTest.data)

    def test_votable_success(self):
        response = views.return_votable_format_export(solrdata.data)
        assert(response._status_code == 200)

    def test_votable_no_data(self):
        response = views.return_votable_format_export(None)
        assert(response._status_code == 404)

    def test_rss_success(self):
        response = views.return_rss_format_export(solrdata.data, '')
        assert(response._status_code == 200)

    def test_rss_no_data(self):
        response = views.return_rss_format_export(None, '')
        assert(response._status_code == 404)

    def test_rss_authors(self):
        solr_data = \
            {
                "responseHeader": {
                    "status": 0,
                    "QTime": 1,
                    "params": {
                        "sort": "date desc",
                        "fq": "{!bitset}",
                        "rows": "19",
                        "q": "*:*",
                        "start": "0",
                        "wt": "json",
                        "fl": "author,title,year,date,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,num_citations,read_count,bibcode,identification,copyright,keyword,doctype,num_references,comment,property,esources,data"
                    }
                },
                "response": {
                    "start": 0,
                    "numFound": 4,
                    "docs": [
                        {
                            "title": [
                                "A Microwave Free-Space Method Using Artificial Lens with Anti-reflection Layer"
                            ],
                            "author": [
                                "Zhang, Yangjun",
                                "Aratani, Yuki",
                                "Nakazima, Hironari"
                            ],
                        },
                        {
                            "author": [
                                "Ryan, R. E.",
                                "McCullough, P. R."
                            ],
                        },
                        {
                            "title": [
                                "Resolving Gas-Phase Metallicity In Galaxies"
                            ],
                        },
                        {
                            "bibcode": "2017ascl.soft06009C",
                        },
                    ]
                }
            }
        rss_export = RSSFormat(solrdata.data)
        # both author and title exists
        assert(rss_export._RSSFormat__get_author_title(solr_data['response'].get('docs')[0]) ==
               'Zhang, Yangjun: A Microwave Free-Space Method Using Artificial Lens with Anti-reflection Layer')
        # only author
        assert(rss_export._RSSFormat__get_author_title(solr_data['response'].get('docs')[1]) == 'Ryan, R. E.')
        # only title
        assert(rss_export._RSSFormat__get_author_title(solr_data['response'].get('docs')[2]) ==
               'Resolving Gas-Phase Metallicity In Galaxies')
        # neither author nor title exists
        assert(rss_export._RSSFormat__get_author_title(solr_data['response'].get('docs')[3]) == '')


    def test_all_gets(self):
        function_names = [views.bibTex_format_export_get, views.bibTex_abs_format_export_get,
                          views.fielded_ads_format_export_get, views.fielded_endnote_format_export_get,
                          views.fielded_procite_format_export_get, views.fielded_refman_format_export_get,
                          views.fielded_refworks_format_export_get, views.fielded_medlars_format_export_get,
                          views.xml_dublincore_format_export_get, views.xml_ref_format_export_get,
                          views.xml_refabs_format_export_get, views.csl_aastex_format_export_get,
                          views.csl_icarus_format_export_get, views.csl_mnras_format_export_get,
                          views.csl_soph_format_export_get, views.votable_format_export_get,
                          views.rss_format_export_get, views.csl_ieee_format_export_get]
        bibcode = self.app.config['EXPORT_SERVICE_TEST_BIBCODE_GET']
        for f in function_names:
            if f == views.rss_format_export_get:
                response = f(bibcode, '')
            else:
                response = f(bibcode)
            assert (response._status_code == 200)


    def test_all_posts(self):
        endpoints = ['/bibtex', '/bibtexabs', '/ads', '/endnote', '/procite', '/ris', '/refworks', '/medlars',
                     '/dcxml', '/refxml', '/refabsxml', '/aastex', '/icarus', '/mnras', '/soph', 'votable',
                     'rss', '/ieee']
        payload = {'bibcode': self.app.config['EXPORT_SERVICE_TEST_BIBCODE_GET'],
                   'link': ''}
        for ep in endpoints:
            response = self.client.post(ep, data=json.dumps(payload))
            assert (response._status_code == 200)


    def test_bibtex_keyformat_endpoint(self):
        payload = {'bibcode': self.app.config['EXPORT_SERVICE_TEST_BIBCODE_GET'],
                   'link': '',
                   'keyformat': '%1H:%Y:%q',
                   'maxauthor': 2}
        response = self.client.post('/bibtex', data=json.dumps(payload))
        assert (response._status_code == 200)


    def test_bibtex_keyformat(self):
        solr_data = \
            {
                "responseHeader": {
                    "status": 0,
                    "QTime": 51,
                    "params": {
                        "q": "author:\"^accomazzi\" year:2019",
                        "indent": "on",
                        "fl": "bibcode,author,pub,year",
                        "wt": "json",
                        "_": "1560183872951"}},
                "response": {"numFound": 3, "start": 0, "docs": [
                    {
                        "year": "2019",
                        "bibcode": "2019AAS...23338108A",
                        "bibstem": ["AAS",
                                    "AAS...233"],
                        "author": ["Accomazzi, Alberto",
                                   "Kurtz, Michael J.",
                                   "Henneken, Edwin",
                                   "Grant, Carolyn S.",
                                   "Thompson, Donna M.",
                                   "Chyla, Roman",
                                   "McDonald, Stephen",
                                   "Blanco-Cuaresma, Sergi",
                                   "Shapurian, Golnaz",
                                   "Hostetler, Timothy",
                                   "Templeton, Matthew",
                                   "Lockhart, Kelly"],
                        "pub": "American Astronomical Society Meeting Abstracts #233"},
                    {
                        "year": "2019",
                        "bibcode": "2019AAS...23320704A",
                        "bibstem":["AAS",
                          "AAS...233"],
                        "author": ["Accomazzi, Alberto"],
                        "pub": "American Astronomical Society Meeting Abstracts #233"},
                    {
                        "year":"2019",
                        "bibcode":"2019hsax.conf..526G",
                        "author":["Garzón, F.",
                          "Patrick, L.",
                          "Hammersley, P.",
                          "Streblyanska, A.",
                          "Insausti, M.",
                          "Barreto, M.",
                          "Fernández, P.",
                          "Joven, E.",
                          "López, P.",
                          "Mato, A.",
                          "Moreno, H.",
                          "Núñez, M.",
                          "Patrón, J.",
                          "Pascual, S.",
                          "Cardiel, N."],
                        "pub":"Highlights on Spanish Astrophysics X",
                        "bibstem":["hsax",
                          "hsax.conf"]
                    }
                ]}
            }
        bibtex_export = BibTexFormat(solr_data, "%1H:%Y:%q")
        # both author and title exists
        assert(bibtex_export._BibTexFormat__format_key(solr_data['response'].get('docs')[0]) == 'Accomazzi:2019:AAS')
        # verify that key is ascii
        assert(bibtex_export._BibTexFormat__format_key(solr_data['response'].get('docs')[2]) == 'Garzon:2019:hsax')

        # if keyformat is eprintid and there is no eid in the record
        bibtex_export = BibTexFormat(solr_data, "%X")
        # must return the default bibcode
        assert(bibtex_export._BibTexFormat__format_key(solr_data['response'].get('docs')[0]) == '2019AAS...23338108A')

        solr_data = \
            {
                "responseHeader": {
                    "status": 0,
                    "QTime": 29,
                    "params": {
                        "q": "author:\"accomazzi\" AND doctype:eprint AND year:2021",
                        "fl": "bibcode,eid,eprint",
                        "sort": "bibcode desc",
                        "rows": "300",
                        "_": "1642527401469"}},
                "response": {"numFound": 2, "start": 0, "docs": [
                    {
                        "bibcode": "2021arXiv211200590G",
                        "eid": "arXiv:2112.00590"},
                    {
                        "bibcode": "2021arXiv210601477C",
                        "eid": "arXiv:2106.01477"}]
                }
            }
        # keyformat is eprintid
        bibtex_export = BibTexFormat(solrdata.data, "%X")
        assert(bibtex_export._BibTexFormat__format_key(solr_data['response'].get('docs')[0]) == 'arXiv:2112.00590')

    def test_no_journal_macro(self):
        # test by passing replacing journal macros for journal names

        # bibTex format
        # display full journal name
        bibtex_export = BibTexFormat(solrdata.data_5, "%R").get(include_abs=False, maxauthor=10, authorcutoff=200, journalformat=3).get('export', '')
        bibtex_full_journal_name = u'@ARTICLE{2018PhRvL.120b9901P,\n       author = {{Pustilnik}, M. and {van Heck}, B. and {Lutchyn}, R.~M. and {Glazman}, L.~I.},\n        title = "{Erratum: Quantum Criticality in Resonant Andreev Conduction [Phys. Rev. Lett. 119, 116802 (2017)]}",\n      journal = {Physical Review Letters},\n         year = 2018,\n        month = jan,\n       volume = {120},\n       number = {2},\n          eid = {029901},\n        pages = {029901},\n          doi = {10.1103/PhysRevLett.120.029901},\n       adsurl = {https://ui.adsabs.harvard.edu/abs/2018PhRvL.120b9901P},\n      adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n}\n\n'
        assert (bibtex_export == bibtex_full_journal_name)
        # display abbreviated journal name
        bibtex_export = BibTexFormat(solrdata.data_5, "%R").get(include_abs=False, maxauthor=10, authorcutoff=200, journalformat=2).get('export', '')
        bibtex_abbrev_journal_name = u'@ARTICLE{2018PhRvL.120b9901P,\n       author = {{Pustilnik}, M. and {van Heck}, B. and {Lutchyn}, R.~M. and {Glazman}, L.~I.},\n        title = "{Erratum: Quantum Criticality in Resonant Andreev Conduction [Phys. Rev. Lett. 119, 116802 (2017)]}",\n      journal = {PhRvL},\n         year = 2018,\n        month = jan,\n       volume = {120},\n       number = {2},\n          eid = {029901},\n        pages = {029901},\n          doi = {10.1103/PhysRevLett.120.029901},\n       adsurl = {https://ui.adsabs.harvard.edu/abs/2018PhRvL.120b9901P},\n      adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n}\n\n'
        assert (bibtex_export == bibtex_abbrev_journal_name)
        # macro (default)
        bibtex_export = BibTexFormat(solrdata.data_5, "%R").get(include_abs=False, maxauthor=10, authorcutoff=200, journalformat=0).get('export', '')
        bibtex_default_journal_name = u'@ARTICLE{2018PhRvL.120b9901P,\n       author = {{Pustilnik}, M. and {van Heck}, B. and {Lutchyn}, R.~M. and {Glazman}, L.~I.},\n        title = "{Erratum: Quantum Criticality in Resonant Andreev Conduction [Phys. Rev. Lett. 119, 116802 (2017)]}",\n      journal = {\\prl},\n         year = 2018,\n        month = jan,\n       volume = {120},\n       number = {2},\n          eid = {029901},\n        pages = {029901},\n          doi = {10.1103/PhysRevLett.120.029901},\n       adsurl = {https://ui.adsabs.harvard.edu/abs/2018PhRvL.120b9901P},\n      adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n}\n\n'
        assert (bibtex_export == bibtex_default_journal_name)

        # aastex format
        # display full journal name
        csl_export = CSL(CSLJson(solrdata.data_5).get(), 'aastex', adsFormatter.latex, adsJournalFormat.full).get().get('export', '')
        # now compare it with an already formatted data that we know is correct
        aastex_full_journal_name = u'\\bibitem[Pustilnik et al.(2018)]{2018PhRvL.120b9901P} Pustilnik, M., van Heck, B., Lutchyn, R.~M., et al.\\ 2018, Physical Review Letters, 120, 029901. doi:10.1103/PhysRevLett.120.029901\n'
        assert (csl_export == aastex_full_journal_name)
        # display abbreviated journal name
        csl_export = CSL(CSLJson(solrdata.data_5).get(), 'aastex', adsFormatter.latex, adsJournalFormat.abbreviated).get().get('export', '')
        # now compare it with an already formatted data that we know is correct
        aastex_abbrev_journal_name = u'\\bibitem[Pustilnik et al.(2018)]{2018PhRvL.120b9901P} Pustilnik, M., van Heck, B., Lutchyn, R.~M., et al.\\ 2018, PhRvL, 120, 029901. doi:10.1103/PhysRevLett.120.029901\n'
        assert (csl_export == aastex_abbrev_journal_name)
        # display default journal name, which is the macro option
        csl_export = CSL(CSLJson(solrdata.data_5).get(), 'aastex', adsFormatter.latex, adsJournalFormat.default).get().get('export', '')
        # now compare it with an already formatted data that we know is correct
        aastex_default_journal_name = u'\\bibitem[Pustilnik et al.(2018)]{2018PhRvL.120b9901P} Pustilnik, M., van Heck, B., Lutchyn, R.~M., et al.\\ 2018, \\prl, 120, 029901. doi:10.1103/PhysRevLett.120.029901\n'
        assert (csl_export == aastex_default_journal_name)
        # display abbreviated journal name that needs to be escaped
        csl_export = CSL(CSLJson(solrdata.data_9).get(), 'aastex', adsFormatter.latex, adsJournalFormat.abbreviated).get().get('export', '')
        # now compare it with an already formatted data that we know is correct
        aastex_abbrev_journal_name = u'\\bibitem[Ajani et al.(2021)]{2021A&A...645L..11A} Ajani, V., Starck, J.-L., \\& Pettorino, V.\\ 2021, A\\&A, 645, L11. doi:10.1051/0004-6361/202039988\n'
        assert (csl_export == aastex_abbrev_journal_name)


    def test_bibtex_enumeration(self):
        # test bibtex key_format enumeration
        bibtex_export = BibTexFormat(solrdata.data_6, "%1H%Y%zm")
        key_formats_enumerated = ['Accomazzi2020', 'Accomazzi2019a', 'Accomazzi2015', 'Accomazzi2019b', 'Accomazzi2019c',
                                  'Accomazzi2018a', 'Accomazzi2018b', 'Accomazzi2017', 'Accomazzi2018c', 'Accomazzi2018d']
        assert (bibtex_export._BibTexFormat__enumerate_keys() == key_formats_enumerated)


    def test_tmp_bibcode_format(self):
        # test bibcodes that have no volume and page but doi for all CSL formats
        csl_export_output = {
            'aastex': u'\\bibitem[Aharon(2005)]{2005GML...tmp....1A} Aharon, P.\\ 2005, Geo-Marine Letters. doi:10.1007/s00367-005-0006-y\n',
            'icarus': u'\\bibitem[Aharon(2005)]{2005GML...tmp....1A} Aharon, P.\\ 2005.\\ Catastrophic flood outbursts in mid-continent left imprints in the Gulf of Mexico.\\ Geo-Marine Letters. doi:10.1007/s00367-005-0006-y\n',
            'mnras': u'\\bibitem[\\protect\\citeauthoryear{Aharon}{2005}]{2005GML...tmp....1A} Aharon P., 2005, GML...tmp. doi:10.1007/s00367-005-0006-y\n',
            'soph': u'\\bibitem[Aharon(2005)]{2005GML...tmp....1A}Aharon, P.: 2005, {\\it Geo-Marine Letters}. doi:10.1007/s00367-005-0006-y.\n',
            'aspc': u'\\bibitem[Aharon(2005)]{2005GML...tmp....1A} Aharon, P.\\ 2005, Geo-Marine Letters. doi:10.1007/s00367-005-0006-y.\n',
            'apsj': u'P. Aharon, (2005). doi:10.1007/s00367-005-0006-y.\n',
            'aasj': u'\\bibitem[Aharon(2005)]{2005GML...tmp....1A} Aharon, P.\\ 2005, Geo-Marine Letters. doi:10.1007/s00367-005-0006-y.\n',
            'ieee': u'[1]Aharon, P., “Catastrophic flood outbursts in mid-continent left imprints in the Gulf of Mexico”, <i>Geo-Marine Letters</i>, 2005. doi:10.1007/s00367-005-0006-y.\n'
        }
        cls_default_formats = [adsFormatter.latex] * 6 + [adsFormatter.unicode] * 2

        for style, format in zip(adsCSLStyle.ads_CLS, cls_default_formats):
            csl_export = CSL(CSLJson(solrdata.data_7).get(), style, format).get().get('export', '')
            assert (csl_export == csl_export_output[style])


    def test_encode_doi(self):
        # test doi that is encoded properly
        csl_export_output = {
            'aastex': u'\\bibitem[Greisen(2003)]{2003ASSL..285..109G} Greisen, E.~W.\\ 2003, Information Handling in Astronomy - Historical Vistas, 109. doi:10.1007/0-306-48080-8\\_7\n',
            'icarus': u'\\bibitem[Greisen(2003)]{2003ASSL..285..109G} Greisen, E.~W.\\ 2003.\\ AIPS, the VLA, and the VLBA.\\ Information Handling in Astronomy - Historical Vistas 109. doi:10.1007/0-306-48080-8\\_7\n',
            'mnras': u'\\bibitem[\\protect\\citeauthoryear{Greisen}{2003}]{2003ASSL..285..109G} Greisen E.~W., 2003, ASSL, 109. doi:10.1007/0-306-48080-8\\_7\n',
            'soph': u'\\bibitem[Greisen(2003)]{2003ASSL..285..109G}Greisen, E.W.: 2003, {\\it Information Handling in Astronomy - Historical Vistas}, 109. doi:10.1007/0-306-48080-8\\_7.\n',
            'aspc': u'\\bibitem[Greisen(2003)]{2003ASSL..285..109G} Greisen, E.~W.\\ 2003, Information Handling in Astronomy - Historical Vistas, 109. doi:10.1007/0-306-48080-8\\_7.\n',
            'apsj': u'E.~W. Greisen, in {\\bf 285}, 109. doi:10.1007/0-306-48080-8_7.\n',
            'aasj': u'\\bibitem[Greisen(2003)]{2003ASSL..285..109G} Greisen, E. W.\\ 2003, Information Handling in Astronomy - Historical Vistas, 109. doi:10.1007/0-306-48080-8\\_7.\n',
            'ieee': u'[1]Greisen, E. W., “AIPS, the VLA, and the VLBA”, in <i>Information Handling in Astronomy - Historical Vistas</i>, vol. 285, 2003, p. 109. doi:10.1007/0-306-48080-8_7.\n'
        }
        cls_default_formats = [adsFormatter.latex] * 6 + [adsFormatter.unicode] * 2
        for style, format in zip(adsCSLStyle.ads_CLS, cls_default_formats):
            csl_export = CSL(CSLJson(solrdata.data_10).get(), style, format).get().get('export', '')
            assert (csl_export == csl_export_output[style])


    def test_encode_latex_greek_alphabet(self):
        # test mapping of greek letter macros
        title = 'Measurement of the \\Sigma\\ beam asymmetry for the \\omega\\ photo-production off the proton and the neutron at GRAAL'
        title_encoded = r'Measurement of the \textbackslash{}Sigma\textbackslash{} beam asymmetry for the \textbackslash{}omega\textbackslash{} photo-production off the proton and the neutron at GRAAL'
        assert(encode_laTex(title) == title_encoded)

    def test_misc_with_and_without_publiser(self):
        # test misc for BibTex with and without publisher
        # if publisher, display it, if not, format pub_raw in howpublished
        expected_bibtex_export = u'@MISC{2023zndo...8083529K,\n       author = {{Karras}, Oliver},\n        title = "{Analysis of the State and Evolution of Empirical Research in Requirements Engineering}",\n     keywords = {Python, Jupyter notebook, Analysis, Empirical research, Requirements engineering},\n         year = 2023,\n        month = jun,\n          eid = {10.5281/zenodo.8083529},\n          doi = {10.5281/zenodo.8083529},\n      version = {v1.0},\n    publisher = {Zenodo},\n       adsurl = {https://ui.adsabs.harvard.edu/abs/2023zndo...8083529K},\n      adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n}\n\n@MISC{2023BoSAB..34......,\n        title = "{Proceedings da XLV Reuni{\~a}o Anual da SAB}",\n howpublished = {Boletim da Sociedade Astr{\^o}nomica Brasileira. Proceedings da XLV Reuni{\~a}o Anual da SAB},\n         year = 2023,\n        month = jan,\n       adsurl = {https://ui.adsabs.harvard.edu/abs/2023BoSAB..34......},\n      adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n}\n\n'
        bibtex_export = BibTexFormat(solrdata.data_16, "%R").get(include_abs=False, maxauthor=10, authorcutoff=200, journalformat=3).get('export', '')
        assert(bibtex_export == expected_bibtex_export)

if __name__ == '__main__':
  unittest.main()
