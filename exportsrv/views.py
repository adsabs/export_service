#!/usr/bin/python
# -*- coding: utf-8 -*-


from flask import current_app, request, Blueprint, Response
from flask_discoverer import advertise

from adsmutils import setup_logging

from exportsrv.models import get_solr_data
from exportsrv.formatter.ads import adsFormatter, adsCSLStyle
from exportsrv.formatter.cslJson import CSLJson
from exportsrv.formatter.csl import CSL
from exportsrv.formatter.xmlFormat import XMLFormat
from exportsrv.formatter.bibTexFormat import BibTexFormat
from exportsrv.formatter.fieldedFormat import FieldedFormat
from exportsrv.formatter.customFormat import CustomFormat


bp = Blueprint('export_service', __name__)

global logger
logger = None


def __setup_logging():
    global logger
    logger = setup_logging('export_service', current_app.config.get('LOG_LEVEL', 'INFO'))


def __default_fields():
    return 'author,title,year,date,pub,pub_raw,issue,volume,page,aff,doi,abstract,eid,' \
           'citation_count,read_count,bibcode,identification,copyright,keyword,doctype,' \
           'links_data,reference,comment'


def __return_response(response, status):
    __setup_logging()

    r = Response(response=response, status=status)

    if status == 200:
        r.headers['content-type'] = 'application/json'
        logger.debug('returning results with status code 200')
    else:
        r.headers['content-type'] = 'text/plain'
        logger.error('{} status code = {}'.format(response, status))

    return r


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/bibtex', methods=['POST'])
def bibTexFormatExport():
    __setup_logging()

    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return __return_response('error: no information received', 400)
    elif 'bibcode' not in payload:
        return __return_response('error: no bibcodes found in payload (parameter name is "bibcode")', 400)
    elif 'style' not in payload:
        return __return_response('error: no style found in payload (parameter name is "style")', 400)

    bibcodes = payload['bibcode']
    bibTex_style = payload['style']

    logger.debug('received request with bibcodes={bibcodes} to export in {bibTex_style} style format'.
                 format(bibcodes=''.join(bibcodes), bibTex_style=bibTex_style))

    if (len(bibcodes) == 0) or (len(bibTex_style) == 0):
        return __return_response('error: not all the needed information received', 400)

    if (bibTex_style == 'BibTex'):
        bibTexExport = BibTexFormat(get_solr_data(bibcodes=bibcodes, fields=__default_fields()))
        return __return_response(bibTexExport.get(includeAbs=False), 200)
    if (bibTex_style == 'BibTexAbs'):
        bibTexExport = BibTexFormat(get_solr_data(bibcodes=bibcodes, fields=__default_fields()))
        return __return_response(bibTexExport.get(includeAbs=True), 200)
    return __return_response('error: unrecognizable style (supprted styles are: BibTex, BibTexAbs)', 503)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/fielded', methods=['POST'])
def fieldedFormatExport():
    __setup_logging()

    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return __return_response('error: no information received', 400)
    elif 'bibcode' not in payload:
        return __return_response('error: no bibcodes found in payload (parameter name is "bibcode")', 400)
    elif 'style' not in payload:
        return __return_response('error: no style found in payload (parameter name is "style")', 400)

    bibcodes = payload['bibcode']
    fielded_style = payload['style']

    logger.debug('received request with bibcodes={bibcodes} to export in {fielded_style} style format'.
                 format(bibcodes=''.join(bibcodes), fielded_style=fielded_style))
    
    if (len(bibcodes) == 0) or (len(fielded_style) == 0):
        return __return_response('error: not all the needed information received', 400)

    if (fielded_style == 'ADS'):
        fieldedExport = FieldedFormat(get_solr_data(bibcodes=bibcodes, fields=__default_fields()))
        return __return_response(fieldedExport.get_ads_fielded(), 200)
    if (fielded_style == 'EndNote'):
        fieldedExport = FieldedFormat(get_solr_data(bibcodes=bibcodes, fields=__default_fields()))
        return __return_response(fieldedExport.get_endnote_fielded(), 200)
    if (fielded_style == 'ProCite'):
        fieldedExport = FieldedFormat(get_solr_data(bibcodes=bibcodes, fields=__default_fields()))
        return __return_response(fieldedExport.get_procite_fielded(), 200)
    if (fielded_style == 'Refman'):
        fieldedExport = FieldedFormat(get_solr_data(bibcodes=bibcodes, fields=__default_fields()))
        return __return_response(fieldedExport.get_refman_fielded(), 200)
    if (fielded_style == 'RefWorks'):
        fieldedExport = FieldedFormat(get_solr_data(bibcodes=bibcodes, fields=__default_fields()))
        return __return_response(fieldedExport.get_refworks_fielded(), 200)
    if (fielded_style == 'MEDLARS'):
        fieldedExport = FieldedFormat(get_solr_data(bibcodes=bibcodes, fields=__default_fields()))
        return __return_response(fieldedExport.get_medlars_fielded(), 200)
    return __return_response('error: unrecognizable style (supprted styles are: ADS, EndNote, ProCite, Refman, RefWorks, MEDLARS)', 503)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/xml', methods=['POST'])
def xmlFormatExport():
    __setup_logging()

    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return __return_response('error: no information received', 400)
    elif 'bibcode' not in payload:
        return __return_response('error: no bibcodes found in payload (parameter name is "bibcode")', 400)
    elif 'style' not in payload:
        return __return_response('error: no style found in payload (parameter name is "style")', 400)

    bibcodes = payload['bibcode']
    xml_style = payload['style']

    logger.debug('received request with bibcodes={bibcodes} to export in {xml_style} style format'.
                 format(bibcodes=''.join(bibcodes), xml_style=xml_style))

    if (len(bibcodes) == 0) or (len(xml_style) == 0):
        return __return_response('error: not all the needed information received', 400)

    if (xml_style == 'Dublin'):
        xmlExport = XMLFormat(get_solr_data(bibcodes=bibcodes, fields=__default_fields()))
        return __return_response(xmlExport.get_dublin_xml(), 200)
    if (xml_style == 'Reference'):
        xmlExport = XMLFormat(get_solr_data(bibcodes=bibcodes, fields=__default_fields()))
        return __return_response(xmlExport.get_reference_xml(includeAsb=False), 200)
    if (xml_style == 'ReferenceAbs'):
        xmlExport = XMLFormat(get_solr_data(bibcodes=bibcodes, fields=__default_fields()))
        return __return_response(xmlExport.get_reference_xml(includeAsb=True), 200)
    return __return_response('error: unrecognizable style (supprted styles are: Dublin, Reference, ReferenceAbs)', 503)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/csl', methods=['POST'])
def csl_format_export():
    __setup_logging()

    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return __return_response('error: no information received', 400)
    elif 'bibcode' not in payload:
        return __return_response('error: no bibcodes found in payload (parameter name is "bibcode")', 400)
    elif 'style' not in payload:
        return __return_response('error: no style found in payload (parameter name is "style")', 400)
    elif 'format' not in payload:
        return __return_response('error: no output format found in payload (parameter name is "format")', 400)

    bibcodes = payload['bibcode']
    csl_style = payload['style']
    export_format = payload['format']

    logger.debug('received request with bibcodes={bibcodes} to export in {csl_style} style with output format {export_format}'.
                 format(bibcodes=''.join(bibcodes), csl_style=csl_style, export_format=export_format))

    if (len(bibcodes) == 0) or (len(csl_style) == 0)  or (export_format == None):
        return __return_response('error: not all the needed information received', 400)

    if (not adsCSLStyle().verify(csl_style)):
        return __return_response('error: unrecognizable style (supprted formats are: ' + adsCSLStyle().get() + ')', 503)
    if (not adsFormatter().verify(export_format)):
        return __return_response('error: unrecognizable format (supprted formats are: unicode=1, html=2, latex=3)', 503)

    from_solr = get_solr_data(bibcodes=bibcodes, fields=__default_fields())
    return __return_response(CSL(CSLJson(from_solr).get(), csl_style, export_format).get(), 200)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/custom', methods=['POST'])
def custom_format_export():
    __setup_logging()

    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return __return_response('error: no information received', 400)
    elif 'bibcode' not in payload:
        return __return_response('error: no bibcodes found in payload (parameter name is "bibcode")', 400)
    elif 'format' not in payload:
        return __return_response('error: no custom format found in payload (parameter name is "format")', 400)

    bibcodes = payload['bibcode']
    custom_format_str = payload['format']

    logger.debug('received request with bibcodes={bibcodes} to export in a custom format: {custom_format_str}'.
                 format(bibcodes=''.join(bibcodes), custom_format_str=custom_format_str))

    if (len(bibcodes) == 0) or (len(custom_format_str) == 0):
        return __return_response('error: not all the needed information received', 400)

    # pass the user defined format to CustomFormat to parse and we would be able to get which fields
    # in Solr we need to query on
    custom_export = CustomFormat(customFormat=custom_format_str)
    fields = custom_export.getSolrFields()
    # now get the required data from Solr and send it to customFormat for formatting
    from_solr = get_solr_data(bibcodes=bibcodes, fields=fields)
    custom_export.setJSONFromSolr(from_solr)

    return __return_response(custom_export.get(), 200)
