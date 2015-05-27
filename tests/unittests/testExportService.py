import sys, os
PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__),'../../'))
sys.path.append(PROJECT_HOME)
from flask.ext.testing import TestCase
from flask import url_for
import unittest
from app import create_app
import httpretty

class TestExports(TestCase):
  
  def tearDown(self):
    httpretty.disable()
    httpretty.reset()

  def setUp(self):
    def request_callback(request, uri, headers):
      if 'data_type' not in request.parsed_body or not request.parsed_body['data_type']:
        return (200,headers,"This is a 200 response from classic, but actually no data_type was found")

      resp = {
        'BIBTEX':  "bibtex response",
        'AASTeX':   "aastex response",
        'ENDNOTE':  "endnote response",
      }
      data_type = request.parsed_body['data_type'][0]
      response = resp[data_type]

      #Set up the proper "success" header
      if "real" in request.parsed_body['bibcode']:
        hdr = self.app.config['EXPORT_SERVICE_CLASSIC_SUCCESS_STRING']
        hdr = hdr.replace('\d+',str(len(request.parsed_body['bibcode'])))
        hdr = hdr.replace('\.','.')
        response = '%s%s' % (hdr,response)
      return (200, headers, response)

    httpretty.enable()
    httpretty.register_uri(
      httpretty.POST, 
      self.app.config.get('EXPORT_SERVICE_CLASSIC_EXPORT_URL'),
      body=request_callback
    )

  def create_app(self):
    return create_app()

  def test_emptypayload(self):
    for route in map(url_for,['bibtex', 'aastex', 'endnote']):
      for f in [self.client.get,self.client.post]:
        r = f(route)
        self.assertStatus(r,400)
        self.assertEqual(r.json,{'error': 'no information received'})

  def test_BibtexRoute(self):
    u = url_for('bibtex')
    r = self.client.get(u+'?bibcode=fake')
    self.assertStatus(r,400)
    self.assertEqual(r.json,{u'error': u'No records returned from ADS-Classic'})

    r = self.client.get(u+'?bibcode=real')
    self.assertStatus(r,200)
    self.assertEqual(r.json,{u'msg': u'Retrieved 1 abstracts, starting with number 1.  Total number selected: 1.', u'export': u'bibtex response'})

    r = self.client.post(u,data={'bibcode':'fake'})
    self.assertStatus(r,400)
    self.assertEqual(r.json,{u'error': u'No records returned from ADS-Classic'})

    r = self.client.post(u,data={'bibcode':'real'})
    self.assertStatus(r,200)
    self.assertEqual(r.json, {u'msg': u'Retrieved 1 abstracts, starting with number 1.  Total number selected: 1.', u'export': u'bibtex response'})

  def test_EndnoteRoute(self):
    u = url_for('endnote')
    r = self.client.get(u+'?bibcode=fake')
    self.assertStatus(r,400)
    self.assertEqual(r.json,{u'error': u'No records returned from ADS-Classic'})

    r = self.client.get(u+'?bibcode=real')
    self.assertStatus(r,200)
    self.assertEqual(r.json,{u'msg': u'Retrieved 1 abstracts, starting with number 1.  Total number selected: 1.', u'export': u'endnote response'})

    r = self.client.post(u,data={'bibcode':'fake'})
    self.assertStatus(r,400)
    self.assertEqual(r.json,{u'error': u'No records returned from ADS-Classic'})

    r = self.client.post(u,data={'bibcode':'real'})
    self.assertStatus(r,200)
    self.assertEqual(r.json, {u'msg': u'Retrieved 1 abstracts, starting with number 1.  Total number selected: 1.', u'export': u'endnote response'})

  def test_AastextRoute(self):
    u = url_for('aastex')
    r = self.client.get(u+'?bibcode=fake')
    self.assertStatus(r,400)
    self.assertEqual(r.json,{u'error': u'No records returned from ADS-Classic'})

    r = self.client.get(u+'?bibcode=real')
    self.assertStatus(r,200)
    self.assertEqual(r.json, {u'msg': u'Retrieved 1 abstracts, starting with number 1.  Total number selected: 1.', u'export': u'aastex response'})

    r = self.client.post(u,data={'bibcode':'fake'})
    self.assertStatus(r,400)
    self.assertEqual(r.json,{u'error': u'No records returned from ADS-Classic'})

    r = self.client.post(u,data={'bibcode':'real'})
    self.assertStatus(r,200)
    self.assertEqual(r.json,{u'msg': u'Retrieved 1 abstracts, starting with number 1.  Total number selected: 1.', u'export': u'aastex response'})

  def test_jsonp(self):
    u = url_for('aastex')
    r = self.client.get(u+'?bibcode=real&callback=JSONP_CALLBACK')
    self.assertEqual(r.json, u"JSONP_CALLBACK({'msg': u'Retrieved 1 abstracts, starting with number 1.  Total number selected: 1.', 'export': u'aastex response'});")

    r = self.client.post(u,data={'bibcode':'real','callback':'JSONP_CALLBACK'})
    self.assertEqual(r.json, u"JSONP_CALLBACK({'msg': u'Retrieved 1 abstracts, starting with number 1.  Total number selected: 1.', 'export': u'aastex response'});")

if __name__ == '__main__':
  unittest.main()