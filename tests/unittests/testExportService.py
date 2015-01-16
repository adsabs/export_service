import sys, os
PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__),'../../'))
sys.path.append(PROJECT_HOME)
from flask.ext.testing import TestCase
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
      

    httpretty.enable()
    for method in [httpretty.GET,httpretty.POST]:
      httpretty.register_uri(
        method, 
        self.app.config.get('CLASSIC_EXPORT_URL'),
        body=request_callback
      )


  def create_app(self):
    '''Start the wsgi application'''
    return create_app()

  def test_ExportsRoute(self):
    '''Tests for the existence of a /resources route, and that it returns properly formatted JSON data'''
    r = self.client.get('/')

if __name__ == '__main__':
  unittest.main()