from flask_testing import TestCase
import unittest
from app import create_app
import json
from stubdata import solrdata, bibTexTest, fieldedTest, xmlTest, cslTest, customTest
from formatter.bibTexFormat import BibTexFormat
from formatter.fieldedFormat import FieldedFormat
from formatter.xmlFormat import XMLFormat
from formatter.cslJson import CSLJson
from formatter.csl import CSL, adsFormatter
from formatter.customFormat import CustomFormat

class TestExports(TestCase):
    def create_app(self):
        app_ = create_app()
        return app_

    def test_bibtex(self):
        # format the stubdata using the code
        bibTexExport = BibTexFormat(solrdata.data).get(includeAbs=False)
        # now compare it with an already formatted data that we know is correct
        assert(bibTexExport == bibTexTest.data)

    def test_bibtex_with_abs(self):
        # format the stubdata using the code
        bibTexExport = BibTexFormat(solrdata.data).get(includeAbs=True)
        # now compare it with an already formatted data that we know is correct
        assert (bibTexExport == bibTexTest.dataWithAbs)

    def test_ads(self):
        # format the stubdata using the code
        fieldedExport = FieldedFormat(solrdata.data).getADSFielded()
        # now compare it with an already formatted data that we know is correct
        assert (fieldedExport == fieldedTest.dataADS)

    def test_endnote(self):
        # format the stubdata using the code
        fieldedExport = FieldedFormat(solrdata.data).getEndNoteFielded()
        # now compare it with an already formatted data that we know is correct
        assert (fieldedExport == fieldedTest.dataEndNote)

    def test_procite(self):
        # format the stubdata using the code
        fieldedExport = FieldedFormat(solrdata.data).getProCiteFielded()
        # now compare it with an already formatted data that we know is correct
        assert (fieldedExport == fieldedTest.dataProCite)

    def test_refman(self):
        # format the stubdata using the code
        fieldedExport = FieldedFormat(solrdata.data).getRefmanFielded()
        # now compare it with an already formatted data that we know is correct
        assert (fieldedExport == fieldedTest.dataRefman)

    def test_refworks(self):
        # format the stubdata using the code
        fieldedExport = FieldedFormat(solrdata.data).getRefWorksFielded()
        # now compare it with an already formatted data that we know is correct
        assert (fieldedExport == fieldedTest.dataRefWorks)

    def test_medlars(self):
        # format the stubdata using the code
        fieldedExport = FieldedFormat(solrdata.data).getMEDLARSFielded()
        # now compare it with an already formatted data that we know is correct
        assert (fieldedExport == fieldedTest.dataMEDLARS)

    def test_dublinxml(self):
        # format the stubdata using the code
        xmlExport = XMLFormat(solrdata.data).getDublinXML()
        # now compare it with an already formatted data that we know is correct
        assert(xmlExport == xmlTest.dataDublin)

    def test_refxml(self):
        # format the stubdata using the code
        xmlExport = XMLFormat(solrdata.data).getReferenceXML(includeAsb=False)
        # now compare it with an already formatted data that we know is correct
        assert(xmlExport == xmlTest.dataRef)

    def test_refxml_with_abs(self):
        # format the stubdata using the code
        xmlExport = XMLFormat(solrdata.data).getReferenceXML(includeAsb=True)
        # now compare it with an already formatted data that we know is correct
        assert(xmlExport == xmlTest.dataRefWithAbs)

    def test_aastex(self):
        # format the stubdata using the code
        cslExport = CSL(CSLJson(solrdata.data).get(), 'aastex', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (cslExport == cslTest.dataAASTex)

    def test_icarus(self):
        # format the stubdata using the code
        cslExport = CSL(CSLJson(solrdata.data).get(), 'Icarus', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (cslExport == cslTest.dataIcarus)

    def test_mnras(self):
        # format the stubdata using the code
        cslExport = CSL(CSLJson(solrdata.data).get(), 'mnras', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert(cslExport == cslTest.dataMNRAS)

    def test_soph(self):
        # format the stubdata using the code
        cslExport = CSL(CSLJson(solrdata.data).get(), 'soph', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (cslExport == cslTest.dataSoPh)

    def test_aspc(self):
        # format the stubdata using the code
        cslExport = CSL(CSLJson(solrdata.data).get(), 'aspc', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (cslExport == cslTest.dataASPC)

    def test_apsj(self):
        # format the stubdata using the code
        cslExport = CSL(CSLJson(solrdata.data).get(), 'apsj', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (cslExport == cslTest.dataAPSJ)

    def test_aasj(self):
        # format the stubdata using the code
        cslExport = CSL(CSLJson(solrdata.data).get(), 'aasj', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (cslExport == cslTest.dataAASJ)

    def test_custom(self):
        # format the stubdata using the code
        customFormat = CustomFormat(customFormat=r'\\bibitem[%m\(%Y)]{%2H%Y}\ %5.3l\ %Y\,%j\,%V\,%p\n')
        customFormat.setJSONFromSolr(solrdata.data)
        # now compare it with an already formatted data that we know is correct
        assert (customFormat.get() == customTest.data)

if __name__ == '__main__':
  unittest.main()
