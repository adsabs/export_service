# -*- coding: utf-8 -*-

from flask_testing import TestCase
import unittest

import json
import mock

import exportsrv.app as app
from exportsrv.utils import get_solr_data
from stubdata import solrdata

class TestSolrData(TestCase):
    def create_app(self):
        self.current_app = app.create_app(**{'EXPORT_SERVICE_MAX_RECORDS_SOLR_QUERY': 10})
        return self.current_app

    def test_get_solr_data(self):
        """
        Tests query and bigquery requests from solr depending on the number of bibcodes
        """
        # the mock is for solr call query, with 10 bibcodes
        with mock.patch.object(self.current_app.client, 'get') as post_mock:
            post_mock.return_value = mock_response = mock.Mock()
            mock_response.json.return_value = solrdata.data_6
            mock_response.status_code = 200
            bibcodes = ["2020AAS...23528705A", "2019EPSC...13.1911A", "2019AAS...23338108A", "2019AAS...23320704A",
                        "2018EPJWC.18608001A", "2018AAS...23221409A", "2018AAS...23136217A", "2018AAS...23130709A",
                        "2017ASPC..512...45A", "2015scop.confE...3A"]
            solr_data = get_solr_data(bibcodes=bibcodes, fields='bibcode,author,year,pub,bibstem',
                                      sort=self.current_app.config['EXPORT_SERVICE_NO_SORT_SOLR'])
            matched = 0
            for i, doc in enumerate(solr_data['response']['docs']):
                if doc['bibcode'] == bibcodes[i]:
                    matched += 1
            self.assertEqual(matched, len(bibcodes))

        # the mock is for solr call bigquery, with 22 bibcodes
        with mock.patch.object(self.current_app.client, 'post') as post_mock:
            post_mock.return_value = mock_response = mock.Mock()
            mock_response.json.return_value = solrdata.data
            mock_response.status_code = 200
            bibcodes = ["2018Wthr...73Q..35.", "2018TDM.....5a0201F", "2018Spin....877001P", "2018SAAS...38.....D",
                        "2018PhRvL.120b9901P", "2017PhDT........14C", "2017nova.pres.2388K", "2017CBET.4403....2G",
                        "2017ascl.soft06009C", "2017yCat.113380453S", "2017AAVSN.429....1W", "2017sptz.prop13168Y",
                        "2017MsT..........2A", "2016emo6.rept.....R", "2016iac..talk..872V", "2009bcet.book...65L",
                        "2007AAS...210.2104M", "2007RJPh....1...35.", "1995ans..agar..390M", "1995anda.book.....N",
                        "1991hep.th....8028G", "1983aiaa.meetY....K"]
            solr_data = get_solr_data(bibcodes=bibcodes, fields='bibcode,author,year,pub,bibstem',
                                      sort='')
            matched = 0
            for i, doc in enumerate(solr_data['response']['docs']):
                if doc['bibcode'] == bibcodes[i]:
                    matched += 1
            self.assertEqual(matched, len(bibcodes))


if __name__ == "__main__":
    unittest.main()
