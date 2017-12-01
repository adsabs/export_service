#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_testing import TestCase
import unittest
import json

import exportsrv.app as app

class TestExportsError(TestCase):
    def create_app(self):
        app_ = app.create_app()
        return app_


    def test_no_payload_post(self):
        """
        Ensure that if no payload is passed in, returns 400
        """
        for route in ['/csl', '/custom',
                      '/bibtex','/bibtexabs',
                      '/ads','/endnote','/procite','/ris','/refworks','/medlars',
                      '/dcxml','/refxml','/refabsxml',
                      '/aastex','/icarus','/mnras','/soph']:
            r = self.client.post(route)
            status = r.status_code
            response = r.data
            self.assertEqual(status, 400)
            self.assertEqual(response, '{"msg": "error: no information received", "export": ""}')


    def test_no_payload_get(self):
        """
        Ensure that if no param is passed in, returns 405
        """
        for route in ['/bibtex','/bibtexabs',
                      '/ads','/endnote','/procite','/ris','/refworks','/medlars',
                      '/dcxml','/refxml','/refabsxml',
                      '/aastex','/icarus','/mnras','/soph']:
            r = self.client.get(route)
            status = r.status_code
            response = r.data
            self.assertEqual(status, 405)


    def test_no_payload_param(self):
        """
        Ensure that if payload without all the needed params is passed in, returns 400
        """
        for route in ['/csl', '/custom',
                      '/bibtex','/bibtexabs',
                      '/ads','/endnote','/procite','/ris','/refworks','/medlars',
                      '/dcxml','/refxml','/refabsxml',
                      '/aastex','/icarus','/mnras','/soph']:
            r = self.client.post(route, data=json.dumps({'missingParamsPayload':''}))
            status = r.status_code
            response = r.data
            self.assertEqual(status, 400)
            self.assertEqual(response, '{"msg": "error: no bibcodes found in payload (parameter name is `bibcodes`)", "export": ""}')


    def test_missing_payload_param(self):
        """
        Ensure that all of the payload params were passed in, otherwise returns 400
        """
        payload = {'bibcodes': '', 'style': '', 'format': ''}
        for route in ['/csl', '/custom']:
            r = self.client.post(route, data=json.dumps(payload))
            status = r.status_code
            response = r.data
            self.assertEqual(status, 400)
            print '>>>>>response', response
            self.assertEqual(response, '{"msg": "error: not all the needed information received", "export": ""}')


    def test_non_exist_style(self):
        """
        Ensure that if payload contains the supported styles for each endpoints otherwise returns 503
        """
        payload = {'bibcodes': '1989ApJ...342L..71R', 'style': 'nonExsistingStyle', 'format': 'nonEsistingFormat'}
        end_point = {'/csl':'{"msg": "error: unrecognizable style (supprted formats are: aastex, icarus, mnras, soph, aspc, apsj, aasj)", "export": ""}'}
        for key in end_point:
            r = self.client.post(key, data=json.dumps(payload))
            status = r.status_code
            response = r.data
            self.assertEqual(status, 503)
            self.assertEqual(response, end_point[key])


    def test_non_exist_format(self):
        """
        Ensure that if payload contains the supported styles for each endpoints otherwise returns 503
        """
        payload = {'bibcodes': '1989ApJ...342L..71R', 'style': 'aastex', 'format': 'nonEsistingFormat'}
        end_point = {'/csl':'{"msg": "error: unrecognizable format (supprted formats are: unicode=1, html=2, latex=3)", "export": ""}'}
        for key in end_point:
            r = self.client.post(key, data=json.dumps(payload))
            status = r.status_code
            response = r.data
            self.assertEqual(status, 503)
            self.assertEqual(response, end_point[key])


if __name__ == "__main__":
    unittest.main()
