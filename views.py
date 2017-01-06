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
        # to tell Classic not to return the default of 200 records
        payload["nr_to_return"] = '3000'
        # log what we are about to do
        current_app.logger.info('Sending a request to Classic to retrieve %s for %s records'%(self.data_type, len(payload["bibcode"])))
        # actual request
        r = requests.post(
            current_app.config.get("EXPORT_SERVICE_CLASSIC_EXPORT_URL"),
            data=payload,
            headers=headers
        )
        r.raise_for_status()

        if self.data_type in ['DUBLINCORE','VOTABLE']:
            if self.data_type == 'DUBLINCORE':
                nrecs = r.text.count('<record>')
            else:
                nrecs = r.text.count('<TR>')
            if nrecs == 0:
                current_app.logger.warning('No records were returned from Classic')
                return {"error": "No records returned from ADS-Classic"}, 400
            msg = "Exported %s records in %s format" % (nrecs, self.data_type)
            current_app.logger.info('Export from Classic was successful: %s'%msg)
            return {
                "export": r.text.strip(),
                "msg": msg
            }

        hdr = re.match(
            current_app.config['EXPORT_SERVICE_CLASSIC_SUCCESS_STRING'],
            r.text
        )
        if not hdr:
            current_app.logger.warning('No records were returned from Classic')
            return {"error": "No records returned from ADS-Classic"}, 400

        msg = hdr.group().strip().split("\n")[::-1][0]
        current_app.logger.info('Export from Classic was successful: %s'%msg)
        return {
            "export": r.text.replace(hdr.group(), ''),
            "msg": msg
        }


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

class Ris(Export):
    """Return RIS (REFMAN)"""
    scopes = []
    rate_limit = [200, 60*60*24]
    data_type = 'REFMAN'

class Icarus(Export):
    """Return Icarus"""
    scopes = []
    rate_limit = [200, 60*60*24]
    data_type = 'Icarus'

class Mnras(Export):
    """Return MNRAS"""
    scopes = []
    rate_limit = [200, 60*60*24]
    data_type = 'MNRAS'

class SoPh(Export):
    """Return SoPh"""
    scopes = []
    rate_limit = [200, 60*60*24]
    data_type = 'SoPh'

class DCXML(Export):
    """Return Dublin Core XML"""
    scopes = []
    rate_limit = [200, 60*60*24]
    data_type = 'DUBLINCORE'

class VOTables(Export):
    """Return VOTables"""
    scopes = []
    rate_limit = [200, 60*60*24]
    data_type = 'VOTABLE'
