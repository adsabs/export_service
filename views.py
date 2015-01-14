import json
from flask import current_app, Blueprint, jsonify, request
from flask.ext.restful import Resource, reqparse
import inspect
import sys


blueprint = Blueprint(
    'export',
    __name__,
    static_folder=None,
)

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
  scopes = ['api:search'] 
  rate_limit = [1000,60*60*24]

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
      return {'msg': 'no bibcodes found in POST body (parameter name is "bibcode")'}, 400

    headers = {'User-Agent':'ADS Script Request Agent'}
    #assign data type based on endpoint
    payload["data_type"] = self.data_type

    #check for errors
    try:
        #actual request
        r = current_app.client.session.post(current_app.config.get("CLASSIC_EXPORT_URL"),  data=payload, headers=headers)
        r.raise_for_status()
    except Exception, e:
        exc_info = sys.exc_info()
        return "Classic export http request error: %s" % (exc_info[1]), 503
            
    #get all the lines of the response
    result = r.text.split('\n')
    
    #if there are enough rows, remove the header of the page
    if len(result) > 5:
        result = result[5:]
    
    if ('callback' in payload): # for jsonp
        ret = payload['callback'][0] + u'('+ ret + u');'
    
    return '\n'.join(result), 200

class Aastex(Export):
  '''Return AASTeX'''
  scopes = ['ads:default']
  rate_limit = [100,60*60*24]
  data_type = 'AASTeX'

class Endnote(Export):
  '''Return Endnote'''
  scopes = ['ads:default']
  rate_limit = [100,60*60*24]
  data_type = 'ENDNOTE'

class Bibtex(Export):
  '''Return Bibtex'''
  scopes = ['ads:default']
  rate_limit = [100,60*60*24]
  data_type = 'BIBTEX'


