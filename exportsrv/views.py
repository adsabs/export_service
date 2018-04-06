# -*- coding: utf-8 -*-

from flask import current_app, request, Blueprint, Response
from flask_discoverer import advertise

import json

from exportsrv.utils import get_solr_data
from exportsrv.formatter.ads import adsFormatter, adsCSLStyle
from exportsrv.formatter.cslJson import CSLJson
from exportsrv.formatter.csl import CSL
from exportsrv.formatter.xmlFormat import XMLFormat
from exportsrv.formatter.bibTexFormat import BibTexFormat
from exportsrv.formatter.fieldedFormat import FieldedFormat
from exportsrv.formatter.customFormat import CustomFormat
from exportsrv.formatter.convertCF import convert
from exportsrv.formatter.voTableFormat import VOTableFormat
from exportsrv.formatter.rssFormat import RSSFormat


bp = Blueprint('export_service', __name__)



def default_solr_fields():
    """

    :return: list of fields needed from solr
    """
    return 'author,title,year,date,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,' \
           'citation_count,read_count,bibcode,identifier,copyright,keyword,doctype,' \
           'reference,comment,property,esources,data,isbn,pubnote,eid'


def return_response(results, status, request_type=''):
    """

    :param results: results in a dict
    :param status: status code
    :return:
    """

    if status != 200:
        current_app.logger.error('sending response status={status}'.format(status=status))
        current_app.logger.error('sending response text={response}'.format(response=results))
        r = Response(response=json.dumps(results), status=status)
        r.headers['content-type'] = 'application/json'
        return r

    if request_type == 'POST':
        current_app.logger.info('sending response status={status}'.format(status=status))
        r = Response(response=json.dumps(results), status=status)
        r.headers['content-type'] = 'application/json'
        return r

    if request_type == 'GET':
        current_app.logger.info('sending response status={status}'.format(status=status))
        r = Response(response=results['export'], status=status)
        r.headers['content-type'] = 'text/plain'
        return r

    return None

def return_bibTex_format_export(solr_data, include_abs, request_type='POST'):
    """

    :param include_abs:
    :return:
    """
    if (solr_data is not None):
        if ('error' in solr_data):
            return return_response({'error': 'unable to query solr'}, 400)
        bibTex_export = BibTexFormat(solr_data)
        return return_response(bibTex_export.get(include_abs=include_abs), 200, request_type)
    return return_response({'error': 'no result from solr'}, 404)


def return_fielded_format_export(solr_data, fielded_style, request_type='POST'):
    """

    :param solr_data:
    :param fielded_style:
    :return:
    """
    if (solr_data is not None):
        if ('error' in solr_data):
            return return_response({'error': 'unable to query solr'}, 400)

        fielded_export = FieldedFormat(solr_data)
        if fielded_style == 'ADS':
            return return_response(fielded_export.get_ads_fielded(), 200, request_type)
        if fielded_style == 'EndNote':
            return return_response(fielded_export.get_endnote_fielded(), 200, request_type)
        if fielded_style == 'ProCite':
            return return_response(fielded_export.get_procite_fielded(), 200, request_type)
        if fielded_style == 'Refman':
            return return_response(fielded_export.get_refman_fielded(), 200, request_type)
        if fielded_style == 'RefWorks':
            return return_response(fielded_export.get_refworks_fielded(), 200, request_type)
        if fielded_style == 'MEDLARS':
            return return_response(fielded_export.get_medlars_fielded(), 200, request_type)

    return return_response({'error': 'no result from solr'}, 404)


def return_xml_format_export(solr_data, xml_style, request_type='POST'):
    """

    :param solr_data:
    :param xml_style:
    :param include_abs:
    :return:
    """
    if (solr_data is not None):
        if ('error' in solr_data):
            return return_response({'error': 'unable to query solr'}, 400)

        xml_export = XMLFormat(solr_data)
        if xml_style == 'DublinCore':
            return return_response(xml_export.get_dublincore_xml(), 200, request_type)
        if xml_style == 'Reference':
            return return_response(xml_export.get_reference_xml(include_abs=False), 200, request_type)
        if xml_style == 'ReferenceAbs':
            return return_response(xml_export.get_reference_xml(include_abs=True), 200, request_type)

    return return_response({'error': 'no result from solr'}, 404, request_type)


def return_csl_format_export(solr_data, csl_style, export_format, request_type='POST'):
    """

    :param solr_data:
    :param csl_style:
    :param export_format:
    :param request_type:
    :return:
    """
    if (solr_data is not None):
        if ('error' in solr_data):
            return return_response({'error': 'unable to query solr'}, 400)
        csl_export = CSL(CSLJson(solr_data).get(), csl_style, export_format)
        return return_response(csl_export.get(), 200, request_type)
    return return_response({'error': 'no result from solr'}, 404)


def return_votable_format_export(solr_data, request_type='POST'):
    """

    :param solr_data:
    :param request_type:
    :return:
    """
    if (solr_data is not None):
        if ('error' in solr_data):
            return return_response({'error': 'unable to query solr'}, 400)
        votable_export = VOTableFormat(solr_data)
        return return_response(votable_export.get(), 200, request_type)
    return return_response({'error': 'no result from solr'}, 404)


def return_rss_format_export(solr_data, link, request_type='POST'):
    """

    :param solr_data:
    :param link:
    :param request_type:
    :return:
    """
    if (solr_data is not None):
        if ('error' in solr_data):
            return return_response({'error': 'unable to query solr'}, 400)
        rss_export = RSSFormat(solr_data)
        return return_response(rss_export.get(link), 200, request_type)
    return return_response({'error': 'no result from solr'}, 404)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/bibtex', methods=['POST'])
def bibTex_format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']
    bibTex_style = 'BibTex'

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in {bibTex_style} style format'.
                 format(bibcodes=''.join(bibcodes), bibTex_style=bibTex_style))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_bibTex_format_export(solr_data=solr_data, include_abs=False)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/bibtex/<bibcode>', methods=['GET'])
def bibTex_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    bibTex_style = 'BibTex'

    current_app.logger.debug('received request with bibcode={bibcode} to export in {bibTex_style} style format'.
                 format(bibcode=bibcode, bibTex_style=bibTex_style))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_bibTex_format_export(solr_data=solr_data, include_abs=False, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/bibtexabs', methods=['POST'])
def bibTex_abs_format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']
    bibTex_style = 'BibTex Abs'

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in {bibTex_style} style format'.
                 format(bibcodes=''.join(bibcodes), bibTex_style=bibTex_style))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_bibTex_format_export(solr_data=solr_data, include_abs=True)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/bibtexabs/<bibcode>', methods=['GET'])
def bibTex_abs_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    bibTex_style = 'BibTex Abs'

    current_app.logger.debug('received request with bibcode={bibcode} to export in {bibTex_style} style format'.
                 format(bibcode=bibcode, bibTex_style=bibTex_style))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_bibTex_format_export(solr_data=solr_data, include_abs=True, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/ads', methods=['POST'])
def fielded_ads_format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']
    fielded_style = 'ADS'

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in {fielded_style} style format'.
                 format(bibcodes=''.join(bibcodes), fielded_style=fielded_style))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_fielded_format_export(solr_data, fielded_style)

@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/ads/<bibcode>', methods=['GET'])
def fielded_ads_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    fielded_style = 'ADS'

    current_app.logger.debug('received request with bibcode={bibcode} to export in {fielded_style} style format'.
                 format(bibcode=bibcode, fielded_style=fielded_style))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_fielded_format_export(solr_data, fielded_style, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/endnote', methods=['POST'])
def fielded_endnote_format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']
    fielded_style = 'EndNote'

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in {fielded_style} style format'.
                 format(bibcodes=''.join(bibcodes), fielded_style=fielded_style))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_fielded_format_export(solr_data, fielded_style)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/endnote/<bibcode>', methods=['GET'])
def fielded_endnote_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    fielded_style = 'EndNote'

    current_app.logger.debug('received request with bibcode={bibcode} to export in {fielded_style} style format'.
                 format(bibcode=bibcode, fielded_style=fielded_style))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_fielded_format_export(solr_data, fielded_style, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/procite', methods=['POST'])
def fielded_procite_format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']
    fielded_style = 'ProCite'

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in {fielded_style} style format'.
                 format(bibcodes=''.join(bibcodes), fielded_style=fielded_style))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_fielded_format_export(solr_data, fielded_style)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/procite/<bibcode>', methods=['GET'])
def fielded_procite_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    fielded_style = 'ProCite'

    current_app.logger.debug('received request with bibcode={bibcode} to export in {fielded_style} style format'.
                 format(bibcode=bibcode, fielded_style=fielded_style))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_fielded_format_export(solr_data, fielded_style, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/ris', methods=['POST'])
def fielded_refman_format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']
    fielded_style = 'Refman'

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in {fielded_style} style format'.
                 format(bibcodes=''.join(bibcodes), fielded_style=fielded_style))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_fielded_format_export(solr_data, fielded_style)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/ris/<bibcode>', methods=['GET'])
def fielded_refman_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    fielded_style = 'Refman'

    current_app.logger.debug('received request with bibcode={bibcode} to export in {fielded_style} style format'.
                 format(bibcode=bibcode, fielded_style=fielded_style))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_fielded_format_export(solr_data, fielded_style, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/refworks', methods=['POST'])
def fielded_refworks_format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']
    fielded_style = 'RefWorks'

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in {fielded_style} style format'.
                 format(bibcodes=''.join(bibcodes), fielded_style=fielded_style))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_fielded_format_export(solr_data, fielded_style)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/refworks/<bibcode>', methods=['GET'])
def fielded_refworks_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    fielded_style = 'RefWorks'

    current_app.logger.debug('received request with bibcode={bibcode} to export in {fielded_style} style format'.
                 format(bibcode=bibcode, fielded_style=fielded_style))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_fielded_format_export(solr_data, fielded_style, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/medlars', methods=['POST'])
def fielded_medlars__format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']
    fielded_style = 'MEDLARS'

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in {fielded_style} style format'.
                 format(bibcodes=''.join(bibcodes), fielded_style=fielded_style))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_fielded_format_export(solr_data, fielded_style)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/medlars/<bibcode>', methods=['GET'])
def fielded_medlars__format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    fielded_style = 'MEDLARS'

    current_app.logger.debug('received request with bibcode={bibcode} to export in {fielded_style} style format'.
                 format(bibcode=bibcode, fielded_style=fielded_style))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_fielded_format_export(solr_data, fielded_style, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/dcxml', methods=['POST'])
def xml_dublincore_format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']
    xml_style = 'DublinCore'

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in {xml_style} style format'.
                 format(bibcodes=''.join(bibcodes), xml_style=xml_style))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_xml_format_export(solr_data, xml_style)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/dcxml/<bibcode>', methods=['GET'])
def xml_dublincore_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    xml_style = 'DublinCore'

    current_app.logger.debug('received request with bibcode={bibcode} to export in {xml_style} style format'.
                 format(bibcode=bibcode, xml_style=xml_style))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_xml_format_export(solr_data, xml_style, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/refxml', methods=['POST'])
def xml_ref_format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']
    xml_style = 'Reference'

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in {xml_style} style format'.
                 format(bibcodes=''.join(bibcodes), xml_style=xml_style))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_xml_format_export(solr_data, xml_style)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/refxml/<bibcode>', methods=['GET'])
def xml_ref_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    xml_style = 'Reference'

    current_app.logger.debug('received request with bibcode={bibcode} to export in {xml_style} style format'.
                 format(bibcode=bibcode, xml_style=xml_style))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_xml_format_export(solr_data, xml_style, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/refabsxml', methods=['POST'])
def xml_refabs_format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']
    xml_style = 'ReferenceAbs'

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in {xml_style} style format'.
                 format(bibcodes=''.join(bibcodes), xml_style=xml_style))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_xml_format_export(solr_data, xml_style)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/refabsxml/<bibcode>', methods=['GET'])
def xml_refabs_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    xml_style = 'ReferenceAbs'

    current_app.logger.debug('received request with bibcode={bibcode} to export in {xml_style} style format'.
                 format(bibcode=bibcode, xml_style=xml_style))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_xml_format_export(solr_data, xml_style, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/aastex', methods=['POST'])
def csl_aastex_format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']
    csl_style = 'aastex'
    export_format = 2

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in {csl_style} style with output format {export_format}'.
                 format(bibcodes=''.join(bibcodes), csl_style=csl_style, export_format=export_format))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_csl_format_export(solr_data, csl_style, export_format)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/aastex/<bibcode>', methods=['GET'])
def csl_aastex_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    csl_style = 'aastex'
    export_format = 2

    current_app.logger.debug('received request with bibcode={bibcode} to export in {csl_style} style with output format {export_format}'.
                 format(bibcode=bibcode, csl_style=csl_style, export_format=export_format))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_csl_format_export(solr_data, csl_style, export_format, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/icarus', methods=['POST'])
def csl_icarus_format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']
    csl_style = 'icarus'
    export_format = 2

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in {csl_style} style with output format {export_format}'.
                 format(bibcodes=''.join(bibcodes), csl_style=csl_style, export_format=export_format))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_csl_format_export(solr_data, csl_style, export_format)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/icarus/<bibcode>', methods=['GET'])
def csl_icarus_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    csl_style = 'icarus'
    export_format = 2

    current_app.logger.debug('received request with bibcode={bibcode} to export in {csl_style} style with output format {export_format}'.
                 format(bibcode=bibcode, csl_style=csl_style, export_format=export_format))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_csl_format_export(solr_data, csl_style, export_format, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/mnras', methods=['POST'])
def csl_mnras_format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']
    csl_style = 'mnras'
    export_format = 2

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in {csl_style} style with output format {export_format}'.
                 format(bibcodes=''.join(bibcodes), csl_style=csl_style, export_format=export_format))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_csl_format_export(solr_data, csl_style, export_format)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/mnras/<bibcode>', methods=['GET'])
def csl_mnras_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    csl_style = 'mnras'
    export_format = 2

    current_app.logger.debug('received request with bibcode={bibcode} to export in {csl_style} style with output format {export_format}'.
                 format(bibcode=bibcode, csl_style=csl_style, export_format=export_format))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_csl_format_export(solr_data, csl_style, export_format, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/soph', methods=['POST'])
def csl_soph_format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']
    csl_style = 'soph'
    export_format = 2

    current_app.logger.info('received request with bibcodes={bibcodes} to export in {csl_style} style with output format {export_format}'.
                 format(bibcodes=''.join(bibcodes), csl_style=csl_style, export_format=export_format))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_csl_format_export(solr_data, csl_style, export_format)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/soph/<bibcode>', methods=['GET'])
def csl_soph_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    csl_style = 'soph'
    export_format = 2

    current_app.logger.info('received request with bibcode={bibcode} to export in {csl_style} style with output format {export_format}'.
                 format(bibcode=bibcode, csl_style=csl_style, export_format=export_format))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_csl_format_export(solr_data, csl_style, export_format, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/csl', methods=['POST'])
def csl_format_export():
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)
    if 'style' not in payload:
        return return_response({'error': 'no style found in payload (parameter name is `style`)'}, 400)
    if 'format' not in payload:
        return return_response({'error': 'no output format found in payload (parameter name is `format`)'}, 400)

    bibcodes = payload['bibcode']
    csl_style = payload['style']
    export_format = payload['format']

    if (len(bibcodes) == 0) or (len(csl_style) == 0)  or (export_format == None):
        return return_response({'error': 'not all the needed information received'}, 400)

    if (not adsCSLStyle().verify(csl_style)):
        return return_response({'error': 'unrecognizable style (supprted formats are: ' + adsCSLStyle().get() + ')'}, 400)
    if (not adsFormatter().verify(export_format)):
        return return_response({'error': 'unrecognizable format (supprted formats are: unicode=1, html=2, latex=3)'}, 400)

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in {csl_style} style with output format {export_format}'.
                 format(bibcodes=''.join(bibcodes), csl_style=csl_style, export_format=export_format))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_csl_format_export(solr_data, csl_style, export_format)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/custom', methods=['POST'])
def custom_format_export():
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)
    if 'format' not in payload:
        return return_response({'error': 'no custom format found in payload (parameter name is `format`)'}, 400)

    bibcodes = payload['bibcode']
    custom_format_str = payload['format']

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in a custom format: {custom_format_str}'.
                 format(bibcodes=''.join(bibcodes), custom_format_str=custom_format_str))

    if (len(bibcodes) == 0) or (len(custom_format_str) == 0):
        return return_response({'error': 'not all the needed information received'}, 400)

    # pass the user defined format to CustomFormat to parse and we would be able to get which fields
    # in Solr we need to query on
    custom_export = CustomFormat(custom_format=custom_format_str)
    fields = custom_export.get_solr_fields()
    # now get the required data from Solr and send it to customFormat for formatting
    solr_data = get_solr_data(bibcodes=bibcodes, fields=fields)
    if (solr_data is not None):
        if ('error' in solr_data):
            return return_response({'error': 'unable to query solr'}, 400)
        custom_export.set_json_from_solr(solr_data)
        return return_response(custom_export.get(), 200)
    return return_response({'error': 'no result from solr'}, 404)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/convert', methods=['POST'])
def custom_format_convert():
    """
    
    :return: converted custom format to the new specification
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'format' not in payload:
        return return_response({'error': 'no classic custom format found in payload (parameter name is `format`)'}, 400)

    classic_custom_format = payload['format']

    current_app.logger.info('received request to convert the classic custom format "' + classic_custom_format + '".')
    return return_response(convert(classic_custom_format), 200)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/votable', methods=['POST'])
def votable_format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in VOTable format'.
                 format(bibcodes=''.join(bibcodes)))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_votable_format_export(solr_data=solr_data)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/votable/<bibcode>', methods=['GET'])
def votable_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    current_app.logger.debug('received request with bibcode={bibcode} to export in VOTable format'.
                 format(bibcode=bibcode))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_votable_format_export(solr_data=solr_data, request_type='GET')

@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/rss', methods=['POST'])
def rss_format_export_post():
    """

    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return return_response({'error': 'no information received'}, 400)
    if 'bibcode' not in payload:
        return return_response({'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400)

    bibcodes = payload['bibcode']
    if 'link' in payload:
        link = payload['link']
    else:
        link = ''

    current_app.logger.debug('received request with bibcodes={bibcodes} to export in RSS format'.
                 format(bibcodes=''.join(bibcodes)))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields())
    return return_rss_format_export(solr_data=solr_data, link=link)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/rss/<bibcode>/', defaults={'link': ''}, methods=['GET'])
@bp.route('/rss/<bibcode>/<path:link>', methods=['GET'])
def rss_format_export_get(bibcode, link):
    """

    :param bibcode:
    :param link:
    :return:
    """
    current_app.logger.debug('received request with bibcode={bibcode} to export in RSS format'.
                 format(bibcode=bibcode))

    solr_data = get_solr_data(bibcodes=[bibcode], fields=default_solr_fields())
    return return_rss_format_export(solr_data=solr_data, link=link, request_type='GET')

