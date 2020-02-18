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
        self.current_app = app.create_app()
        return self.current_app

    def test_get_solr_data(self):
        """
        Tests POST for readhist endpoint when no optional param passed in, so default is returned
        """
        # the mock is for solr call
        with mock.patch.object(self.current_app.client, 'get') as post_mock:
            post_mock.return_value = mock_response = mock.Mock()
            mock_response.json.return_value = solrdata.data_6
            mock_response.status_code = 200
            bibcodes = ["2020AAS...23528705A", "2019EPSC...13.1911A", "2019AAS...23338108A", "2019AAS...23320704A",
                        "2018EPJWC.18608001A", "2018AAS...23221409A", "2018AAS...23136217A", "2018AAS...23130709A",
                        "2017ASPC..512...45A", "2015scop.confE...3A"]
            solr_data = get_solr_data(user_token=None, bibcodes=bibcodes, fields='bibcode,author,year,pub,bibstem',
                                      sort=self.current_app.config['EXPORT_SERVICE_NO_SORT_SOLR'])
            matched = 0
            for i, doc in enumerate(solr_data['response']['docs']):
                if doc['bibcode'] == bibcodes[i]:
                    matched += 1
            self.assertEqual(matched, len(bibcodes))


if __name__ == "__main__":
    unittest.main()
