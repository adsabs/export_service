#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_testing import TestCase
import unittest

import exportsrv.app as app

from stubdata import solrdata, bibTexTest, fieldedTest, xmlTest, cslTest, customTest
from exportsrv.formatter.bibTexFormat import BibTexFormat
from exportsrv.formatter.fieldedFormat import FieldedFormat
from exportsrv.formatter.xmlFormat import XMLFormat
from exportsrv.formatter.cslJson import CSLJson
from exportsrv.formatter.csl import CSL, adsFormatter
from exportsrv.formatter.customFormat import CustomFormat

class TestExports(TestCase):
    def create_app(self):
        app_ = app.create_app()
        return app_

    def test_bibtex(self):
        # format the stubdata using the code
        bibtex_export = BibTexFormat(solrdata.data).get(includeAbs=False)
        # now compare it with an already formatted data that we know is correct
        assert(bibtex_export == bibTexTest.data)

    def test_bibtex_with_abs(self):
        # format the stubdata using the code
        bibtex_export = BibTexFormat(solrdata.data).get(includeAbs=True)
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
        xml_export = XMLFormat(solrdata.data).get_dublin_xml()
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_dublin)

    def test_refxml(self):
        # format the stubdata using the code
        xml_export = XMLFormat(solrdata.data).get_reference_xml(includeAsb=False)
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_ref)

    def test_refxml_with_abs(self):
        # format the stubdata using the code
        xml_export = XMLFormat(solrdata.data).get_reference_xml(includeAsb=True)
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_ref_with_abs)

    def test_aastex(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'aastex', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_AASTex)

    def test_icarus(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'Icarus', adsFormatter.latex).get()
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

    def test_custom(self):
        # format the stubdata using the code
        custom_format = CustomFormat(custom_format=r'\\bibitem[%m\(%Y)]{%2H%Y}\ %5.3l\ %Y\,%j\,%V\,%p \n')
        custom_format.set_json_from_solr(solrdata.data)
        # now compare it with an already formatted data that we know is correct
        assert (custom_format.get() == customTest.data)

if __name__ == '__main__':
  unittest.main()
