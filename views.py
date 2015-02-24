import json
from flask import current_app, request
import requests
from flask.ext.restful import Resource
import inspect
import re
import sys

#This resource must be available for every adsabs webservice.
class Resources(Resource):
  '''Overview of available resources'''
  scopes = []
  rate_limit = [1000,60*60*24]
  def get(self):
    func_list = {}
    clsmembers = [i[1] for i in inspect.getmembers(sys.modules[__name__], inspect.isclass)]
    for rule in current_app.url_map.iter_rules():
      f = current_app.view_functions[rule.endpoint]
      #If we load this webservice as a module, we can't guarantee that current_app only has these views
      if not hasattr(f,'view_class') or f.view_class not in clsmembers:
        continue
      methods = f.view_class.methods
      scopes = f.view_class.scopes
      rate_limit = f.view_class.rate_limit
      description = f.view_class.__doc__
      func_list[rule.rule] = {'methods':methods,'scopes': scopes,'description': description,'rate_limit':rate_limit}
    return func_list, 200

class Export(Resource):
  '''Returns export data for a list of bibcodes'''
  def get(self):
    payload = dict(request.args)
    return self.get_data_from_classic(payload)

  def post(self):
    try:
      payload =request.get_json(force=True) #post data in json
    except:
      payload = dict(request.form) #post data in form encoding
    return self.get_data_from_classic(payload)

  def get_data_from_classic(self, payload):
    if not payload:
      return {'msg': 'no information received'}, 400
    elif not 'bibcode' in payload:
      return {'msg': 'no bibcodes found in payload (parameter name is "bibcode")'}, 400

    headers = {'User-Agent':'ADS Script Request Agent'}
    #assign data type based on endpoint
    payload["data_type"] = self.data_type

    #actual request
    r = requests.post(current_app.config.get("CLASSIC_EXPORT_URL"),  data=payload, headers=headers)
    r.raise_for_status()

    hdr = re.match(current_app.config['CLASSIC_EXPORT_SUCCESS_STRING'],r.text)
    if not hdr:
      return {"msg":"No records returned from ADS-Classic"}, 400

    result = {"export" : r.text.replace(hdr.group(),''),
              "msg" : hdr.group().strip().split("\n")[::-1][0]
            }

    if ('callback' in payload): # for jsonp
        result = payload['callback'][0] + u'('+ unicode(result) + u');'    
    return result, 200

class Aastex(Export):
  '''Return AASTeX'''
  scopes = []
  rate_limit = [100,60*60*24]
  data_type = 'AASTeX'

class Endnote(Export):
  '''Return Endnote'''
  scopes = []
  rate_limit = [100,60*60*24]
  data_type = 'ENDNOTE'

class Bibtex(Export):
  '''Return Bibtex'''
  scopes = []
  rate_limit = [100,60*60*24]
  data_type = 'BIBTEX'


