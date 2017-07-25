#!/usr/bin/env python

import sys
import os
PROJECT_HOME = os.path.abspath(
    os.path.join(os.path.dirname(__file__)))
sys.path.append(PROJECT_HOME)

from flask import current_app, request, Blueprint, Response
from flask_discoverer import advertise
from flask_restful import Resource

import json

from solrData import getSolrData
from .formatter.ads import adsFormatter, adsCSLStyle
from .formatter.cslJson import CSLJson
from .formatter.csl import CSL
from .formatter.xmlFormat import XMLFormat
from .formatter.bibTexFormat import BibTexFormat
from .formatter.fieldedFormat import FieldedFormat
from .formatter.customFormat import CustomFormat

bp = Blueprint('export_service', __name__)

def __defaultFields():
    return current_app.config['EXPORT_SERVICE_QUERY_DEFAULT_FIELDS']

def __returnResponse(response, status):
    r = Response(response=response, status=status)
    r.headers['content-type'] = 'application/json'
    return r

@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/bibtex', methods=['POST'])
def bibTexFormatExport():
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return __returnResponse('error: no information received', 400)
    elif 'bibcode' not in payload:
        return __returnResponse('error: no bibcodes found in payload (parameter name is "bibcode")', 400)
    elif 'style' not in payload:
        return __returnResponse('error: no style found in payload (parameter name is "style")', 400)

    bibcodes = payload['bibcode']
    bibTexStyle = payload['style']

    if (len(bibcodes) == 0) or (len(bibTexStyle) == 0):
        return __returnResponse('error: not all the needed information received', 400)

    if (bibTexStyle == 'BibTex'):
        bibTexExport = BibTexFormat(getSolrData(bibcodes=bibcodes, fields=__defaultFields()))
        return __returnResponse(bibTexExport.get(includeAbs=False), 200)
    if (bibTexStyle == 'BibTexAbs'):
        bibTexExport = BibTexFormat(getSolrData(bibcodes=bibcodes, fields=__defaultFields()))
        return __returnResponse(bibTexExport.get(includeAbs=True), 200)
    return __returnResponse('error: unrecognizable style (supprted styles are: BibTex, BibTexAbs)', 503)

@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/fielded', methods=['POST'])
def fieldedFormatExport():
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return __returnResponse('error: no information received', 400)
    elif 'bibcode' not in payload:
        return __returnResponse('error: no bibcodes found in payload (parameter name is "bibcode")', 400)
    elif 'style' not in payload:
        return __returnResponse('error: no style found in payload (parameter name is "style")', 400)

    bibcodes = payload['bibcode']
    fieldedStyle = payload['style']

    if (len(bibcodes) == 0) or (len(fieldedStyle) == 0):
        return __returnResponse('error: not all the needed information received', 400)

    if (fieldedStyle == 'ADS'):
        fieldedExport = FieldedFormat(getSolrData(bibcodes=bibcodes, fields=__defaultFields()))
        return __returnResponse(fieldedExport.getADSFielded(), 200)
    if (fieldedStyle == 'EndNote'):
        fieldedExport = FieldedFormat(getSolrData(bibcodes=bibcodes, fields=__defaultFields()))
        return __returnResponse(fieldedExport.getEndNoteFielded(), 200)
    if (fieldedStyle == 'ProCite'):
        fieldedExport = FieldedFormat(getSolrData(bibcodes=bibcodes, fields=__defaultFields()))
        return __returnResponse(fieldedExport.getProCiteFielded(), 200)
    if (fieldedStyle == 'Refman'):
        fieldedExport = FieldedFormat(getSolrData(bibcodes=bibcodes, fields=__defaultFields()))
        return __returnResponse(fieldedExport.getRefmanFielded(), 200)
    if (fieldedStyle == 'RefWorks'):
        fieldedExport = FieldedFormat(getSolrData(bibcodes=bibcodes, fields=__defaultFields()))
        return __returnResponse(fieldedExport.getRefWorksFielded(), 200)
    if (fieldedStyle == 'MEDLARS'):
        fieldedExport = FieldedFormat(getSolrData(bibcodes=bibcodes, fields=__defaultFields()))
        return __returnResponse(fieldedExport.getMEDLARSFielded(), 200)
    return __returnResponse('error: unrecognizable style (supprted styles are: ADS, EndNote, ProCite, Refman, RefWorks, MEDLARS)', 503)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/xml', methods=['POST'])
def xmlFormatExport():
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return __returnResponse('error: no information received', 400)
    elif 'bibcode' not in payload:
        return __returnResponse('error: no bibcodes found in payload (parameter name is "bibcode")', 400)
    elif 'style' not in payload:
        return __returnResponse('error: no style found in payload (parameter name is "style")', 400)

    bibcodes = payload['bibcode']
    xmlStyle = payload['style']

    if (len(bibcodes) == 0) or (len(xmlStyle) == 0):
        return __returnResponse('error: not all the needed information received', 400)

    if (xmlStyle == 'Dublin'):
        xmlExport = XMLFormat(getSolrData(bibcodes=bibcodes, fields=__defaultFields()))
        return __returnResponse(xmlExport.getDublinXML(), 200)
    if (xmlStyle == 'Reference'):
        xmlExport = XMLFormat(getSolrData(bibcodes=bibcodes, fields=__defaultFields()))
        return __returnResponse(xmlExport.getReferenceXML(includeAsb=False), 200)
    if (xmlStyle == 'ReferenceAbs'):
        xmlExport = XMLFormat(getSolrData(bibcodes=bibcodes, fields=__defaultFields()))
        return __returnResponse(xmlExport.getReferenceXML(includeAsb=True), 200)
    return __returnResponse('error: unrecognizable style (supprted styles are: Dublin, Reference, ReferenceAbs)', 503)

@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/csl', methods=['POST'])
def cslFormatExport():
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return __returnResponse('error: no information received', 400)
    elif 'bibcode' not in payload:
        return __returnResponse('error: no bibcodes found in payload (parameter name is "bibcode")', 400)
    elif 'style' not in payload:
        return __returnResponse('error: no style found in payload (parameter name is "style")', 400)
    elif 'format' not in payload:
        return __returnResponse('error: no output format found in payload (parameter name is "format")', 400)

    bibcodes = payload['bibcode']
    cslStyle = payload['style']
    exportFormat = payload['format']

    if (len(bibcodes) == 0) or (len(cslStyle) == 0)  or (len(exportFormat) == 0):
        return __returnResponse('error: not all the needed information received', 400)

    if (not adsCSLStyle().verify(cslStyle)):
        return __returnResponse('error: unrecognizable style (supprted formats are: ' + adsCSLStyle().get() + ')', 503)
    if (not adsFormatter().verify(exportFormat)):
        return __returnResponse('error: unrecognizable format (supprted formats are: unicode=1, html=2, latex=3)', 503)

    fromSolr = getSolrData(bibcodes=bibcodes, fields=__defaultFields())
    return __returnResponse(CSL(CSLJson(fromSolr).get(), cslStyle, exportFormat).get(), 200)

@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/custom', methods=['POST'])
def customFormatExport():
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return __returnResponse('error: no information received', 400)
    elif 'bibcode' not in payload:
        return __returnResponse('error: no bibcodes found in payload (parameter name is "bibcode")', 400)
    elif 'format' not in payload:
        return __returnResponse('error: no custom format found in payload (parameter name is "format")', 400)

    bibcodes = payload['bibcode']
    customformatStr = payload['format']

    if (len(bibcodes) == 0) or (len(customformatStr) == 0):
        return __returnResponse('error: not all the needed information received', 400)

    # pass the user defined format to CustomFormat to parse and we would be able to get which fields
    # in Solr we need to query on
    customExport = CustomFormat(customFormat=customformatStr)
    fields = customExport.getSolrFields()
    # now get the required data from Solr and send it to customFormat for formatting
    fromSolr = getSolrData(bibcodes=bibcodes, fields=fields)
    customExport.setJSONFromSolr(fromSolr)

    return __returnResponse(customExport.get(), 200)

@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/', methods=['POST'])
def home():
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return __returnResponse('error: no information received', 400)
    elif 'bibcode' not in payload:
        return __returnResponse('error: no bibcodes found in payload (parameter name is "bibcode")', 400)

    bibcodes = payload['bibcode']

    if (len(bibcodes) == 0):
        return __returnResponse('error: not all the needed information received', 400)

    fromSolr = getSolrData(bibcodes=bibcodes, fields=__defaultFields())
    return __returnResponse(fromSolr['response'], 200)
