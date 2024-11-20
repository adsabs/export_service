# -*- coding: utf-8 -*-

from flask_testing import TestCase
import unittest
import json
from datetime import datetime

import xml.etree.ElementTree as ET

import exportsrv.app as app
from exportsrv.formatter.rssFormat import RSSFormat
from exportsrv.formatter.strftime import strftime
from exportsrv.formatter.latexencode import utf8tolatex

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
            self.assertEqual(response, b'{"error": "no information received"}')


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
            self.assertEqual(response, b'{"error": "no bibcode found in payload (parameter name is `bibcode`)"}')


    def test_missing_payload_param(self):
        """
        Ensure that all of the payload params were passed in, otherwise returns 400
        """
        payload = {'bibcode': '', 'style': '', 'format': ''}
        for route in ['/csl', '/custom']:
            r = self.client.post(route, data=json.dumps(payload))
            status = r.status_code
            response = r.data
            self.assertEqual(status, 400)
            self.assertEqual(response, b'{"error": "not all the needed information received"}')


    def test_non_exist_style(self):
        """
        Ensure that if payload contains the supported styles for each endpoints otherwise returns 400
        """
        payload = {'bibcode': '1989ApJ...342L..71R', 'style': 'nonExsistingStyle', 'format': 'nonEsistingFormat'}
        end_point = {'/csl':b'{"error": "unrecognizable style (supprted formats are: aastex, icarus, mnras, soph, aspc, apsj, aasj, ieee, agu, gsa, ams)"}'}
        for key in end_point:
            r = self.client.post(key, data=json.dumps(payload))
            status = r.status_code
            response = r.data
            self.assertEqual(status, 400)
            self.assertEqual(response, end_point[key])


    def test_non_exist_format(self):
        """
        Ensure that if payload contains the supported styles for each endpoints otherwise returns 400
        """
        payload = {'bibcode': '1989ApJ...342L..71R', 'style': 'aastex', 'format': 'nonEsistingFormat'}
        end_point = {'/csl':b'{"error": "unrecognizable format (supprted formats are: unicode=1, html=2, latex=3)"}'}
        for key in end_point:
            r = self.client.post(key, data=json.dumps(payload))
            status = r.status_code
            response = r.data
            self.assertEqual(status, 400)
            self.assertEqual(response, end_point[key])


    def test_rss_add_in_with_empty_value(self):
        """
        Test rss format add_in for when the element is not availabe
        """
        parent = ET.Element('parent')
        instance = RSSFormat(from_solr={})

        # call the __add_in method with an empty value
        instance._RSSFormat__add_in(parent, 'testField', '')

        # check that the element was added and the text is 'Not Available'
        added_element = parent.find('testField')
        self.assertIsNotNone(added_element, "The element was not added.")
        self.assertEqual(added_element.text, 'Not Available', "The text is not 'Not Available'.")


    def test_strftime_when_illegal_format_raises_type_error(self):
        """
        test strftime function in the strftime module
        """
        dt = datetime(2022, 2, 2)
        # triggers the _illegal_s search condition
        illegal_format = "%s"

        with self.assertRaises(TypeError):
            strftime(dt, illegal_format)

    def test_utf8tolatex_when_empty_string(self):
        """
        send empty string to latexencode's utf8tolatex function
        """
        self.assertTrue(utf8tolatex("") == "")


if __name__ == "__main__":
    unittest.main()
