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

  def post(self):

    #"force=True" means it will attempt to retrieve json even if contentType is something different
    request_json = request.get_json(force=True)

    if not request_json or not 'bibcodes' in request_json:
      return {'msg': 'no bibcodes found in POST body'}, 400

    bibcodes = map(str, request_json['bibcodes'])

    export_format = request_json.get("export_format")

    if not export_format:
      return {'msg': 'no export format specified'}, 400

    parameters = {'bibcode' : ';'.join(bibcodes),
                  'data_type' : export_format,
                  'sort' : 'NONE'
                  }
    headers = {'User-Agent':'ADS Script Request Agent'}

    #check for errors
    try:
        #actual request
        r = current_app.client.session.post(current_app.config.get("CLASSIC_EXPORT_URL"), data=parameters, headers=headers)
        r.raise_for_status()
    except Exception, e:
        exc_info = sys.exc_info()
        return "Classic export http request error: %s" % (exc_info[1]), 503
            
    #get all the lines of the response
    result = r.text.split('\n')
    
    #if there are enough rows, remove the header of the page
    if len(result) > 5:
        result = result[5:]
    
    return '\n'.join(result), 200
