from flask import current_app, request
import requests
from flask.ext.restful import Resource
from flask.ext.discoverer import advertise
import re


class Export(Resource):
    """Returns export data for a list of bibcodes"""
    decorators = [advertise('scopes', 'rate_limit')]

    def get(self):
        payload = dict(request.args)
        return self.get_data_from_classic(payload)

    def post(self):
        try:
            payload = request.get_json(force=True)  # post data in json
        except:
            payload = dict(request.form)  # post data in form encoding
        return self.get_data_from_classic(payload)

    def get_data_from_classic(self, payload):
        if not payload:
            return {'error': 'no information received'}, 400
        elif 'bibcode' not in payload:
            return {'error': 'no bibcodes found in payload (parameter '
                             'name is "bibcode")'}, 400

        headers = {'User-Agent': 'ADS Script Request Agent'}

        # assign data type based on endpoint
        payload["data_type"] = self.data_type

        # actual request
        r = requests.post(
            current_app.config.get("EXPORT_SERVICE_CLASSIC_EXPORT_URL"),
            data=payload,
            headers=headers
        )
        r.raise_for_status()

        hdr = re.match(
            current_app.config['EXPORT_SERVICE_CLASSIC_SUCCESS_STRING'],
            r.text
        )
        if not hdr:
            return {"error": "No records returned from ADS-Classic"}, 400

        result = r.text.replace(hdr.group(), '')

        if 'callback' in payload:  # for jsonp
            result = payload['callback'][0] + u'(' + result + u');'
        return result, 200


class Aastex(Export):
    """Return AASTeX"""
    scopes = []
    rate_limit = [200, 60*60*24]
    data_type = 'AASTeX'


class Endnote(Export):
    """Return Endnote"""
    scopes = []
    rate_limit = [200, 60*60*24]
    data_type = 'ENDNOTE'


class Bibtex(Export):
    """Return Bibtex"""
    scopes = []
    rate_limit = [200, 60*60*24]
    data_type = 'BIBTEX'


