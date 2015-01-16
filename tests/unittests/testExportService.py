import sys, os
PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__),'../../'))
sys.path.append(PROJECT_HOME)
from flask.ext.testing import TestCase
from flask import url_for
import unittest
import requests
import json
from app import create_app
import httpretty

class TestExports(TestCase):
  '''Tests that each route as an http response'''
  
  def tearDown(self):
    httpretty.disable()
    httpretty.reset()

  def setUp(self):
    def request_callback(request, uri, headers):
      try:
        assert request.parsed_body['data_type']
      except AssertionError:
        return (200,headers,"This is a 200 response from classic, but actually no data_type was found")

      resp = {
        'BIBTEX':  "bibcode response",
        'AASTeX':   "aastex response",
        'ENDNOTE':  "endnote response",
      }
      data_type = request.parsed_body['data_type'][0]
      response = resp[data_type]
      return (200, headers, response)

    httpretty.enable()
    httpretty.register_uri(
      httpretty.POST, 
      self.app.config.get('CLASSIC_EXPORT_URL'),
      body=request_callback
    )


  def create_app(self):
    '''Start the wsgi application'''
    return create_app()

  def test_sanitization(self):
    for route in map(url_for,['export.bibtex','export.aastex','export.endnote']):
      r = self.client.get(route)
      self.assertStatus(r,400)
      self.assertEqual(r.json,{'msg': 'no information received'})


  def test_BibtexRoute(self):
    r = self.client.get('/bibtex?bibcode=123')
    self.assertStatus(r,400)
    self.assertEqual(r.json,{u'msg': u'No records returned from ADS-Classic'})


if __name__ == '__main__':
  unittest.main()