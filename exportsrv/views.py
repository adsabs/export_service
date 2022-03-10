# -*- coding: utf-8 -*-

from flask import current_app, request, Blueprint, Response
from flask_discoverer import advertise

import json

from exportsrv.utils import get_solr_data
from exportsrv.formatter.ads import adsFormatter, adsCSLStyle, adsJournalFormat
from exportsrv.formatter.cslJson import CSLJson
from exportsrv.formatter.csl import CSL
from exportsrv.formatter.xmlFormat import XMLFormat
from exportsrv.formatter.bibTexFormat import BibTexFormat
from exportsrv.formatter.fieldedFormat import FieldedFormat
from exportsrv.formatter.customFormat import CustomFormat
from exportsrv.formatter.voTableFormat import VOTableFormat
from exportsrv.formatter.rssFormat import RSSFormat
from exportsrv.tests.unittests.stubdata import solrdata

bp = Blueprint('export_service', __name__)



def default_solr_fields():
    """

    :return: list of fields needed from solr
    """
    return 'author,title,year,pubdate,pub,pub_raw,issue,volume,page,page_range,aff,aff_canonical,doi,abstract,' \
           'read_count,bibcode,identifier,copyright,keyword,doctype,[citations],comment,version,' \
           'property,esources,data,isbn,eid,issn,arxiv_class,editor,series,publisher,bibstem,page_count'


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


def return_bibTex_format_export(solr_data, include_abs, keyformat, maxauthor, authorcutoff, journalformat, request_type='POST'):
    """

    :param include_abs:
    :return:
    """
    if (solr_data is not None):
        bibTex_export = BibTexFormat(solr_data, keyformat=keyformat)
        return return_response(bibTex_export.get(include_abs=include_abs, maxauthor=maxauthor, authorcutoff=authorcutoff, journalformat=journalformat),
                               200, request_type)
    return return_response({'error': 'no result from solr'}, 404)


def return_fielded_format_export(solr_data, fielded_style, request_type='POST'):
    """

    :param solr_data:
    :param fielded_style:
    :return:
    """
    if (solr_data is not None):
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
        xml_export = XMLFormat(solr_data)
        if xml_style == 'DublinCore':
            return return_response(xml_export.get_dublincore_xml(), 200, request_type)
        if xml_style == 'Reference':
            return return_response(xml_export.get_reference_xml(include_abs=False), 200, request_type)
        if xml_style == 'ReferenceAbs':
            return return_response(xml_export.get_reference_xml(include_abs=True), 200, request_type)

    return return_response({'error': 'no result from solr'}, 404)


def return_csl_format_export(solr_data, csl_style, export_format, journal_format, request_type='POST'):
    """

    :param solr_data:
    :param csl_style:
    :param export_format:
    :param request_type:
    :return:
    """
    if (solr_data is not None):
        csl_export = CSL(CSLJson(solr_data).get(), csl_style, export_format, journal_format)
        return return_response(csl_export.get(), 200, request_type)
    return return_response({'error': 'no result from solr'}, 404)


def return_votable_format_export(solr_data, request_type='POST'):
    """

    :param solr_data:
    :param request_type:
    :return:
    """
    if (solr_data is not None):
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
        rss_export = RSSFormat(solr_data)
        return return_response(rss_export.get(link), 200, request_type)
    return return_response({'error': 'no result from solr'}, 404)


def read_value_list_or_not(payload, field):
    """

    :param payload:
    :param field:
    :return:
    """
    if type(payload[field]) is list:
        return payload[field][0]
    return payload[field]


def export_post(request, style, format=-1):
    """

    :param request:
    :param style:
    :param format:
    :return:
    """
    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if not payload:
        return {'error': 'no information received'}, 400
    if 'bibcode' not in payload:
        return {'error': 'no bibcode found in payload (parameter name is `bibcode`)'}, 400
    if 'sort' in payload:
        sort = read_value_list_or_not(payload, 'sort')
    else:
        sort = 'date desc, bibcode desc'

    bibcodes = payload['bibcode']

    if format == -1:
        current_app.logger.info('received request with bibcodes={bibcodes} to export in {style} style using sort order={sort}'.
                    format(bibcodes=','.join(bibcodes), style=style, sort=sort))
    else:
        current_app.logger.info('received request with bibcodes={bibcodes} to export in {style} style with output format {format} using sort order={sort}'.
                    format(bibcodes=','.join(bibcodes), style=style, format=format, sort=sort))

    # if in the test mode, return test solr data
    if current_app.config['EXPORT_SERVICE_TEST_BIBCODE_GET'] == bibcodes:
        return solrdata.data, 200

    return get_solr_data(bibcodes=bibcodes, fields=default_solr_fields(), sort=sort, encode_style=adsFormatter().native_encoding(format)), 200

def export_post_extras(request, style):
    """

    :param request:
    :param style:
    :return:
    """

    def read_journal_format_param(payload):
        """
        local method to read journal format parameter
            1: Use AASTeX macros (default)
            2: Use Journal Abbreviations
            3: Use Full Journal Name
        :param payload:
        :return:
        """
        if 'journalformat' in payload:
            journalformat = read_value_list_or_not(payload, 'journalformat')
            if not adsJournalFormat().verify(journalformat):
                journalformat = adsJournalFormat.default
        else:
            journalformat = adsJournalFormat.default
        return journalformat


    try:
        payload = request.get_json(force=True)  # post data in json
    except:
        payload = dict(request.form)  # post data in form encoding

    if style in ['BibTex', 'BibTex Abs']:
        if payload:
            if 'maxauthor' in payload:
                maxauthor = read_value_list_or_not(payload, 'maxauthor')
                if maxauthor < 0:
                    maxauthor = 0
            elif style == 'BibTex':
                maxauthor = 10
            else:
                # for BibTex Abs default is to display all authors and hence 0
                maxauthor = 0
            if 'keyformat' in payload:
                keyformat = read_value_list_or_not(payload, 'keyformat')
            else:
                keyformat = '%R'
            if 'authorcutoff' in payload:
                authorcutoff = read_value_list_or_not(payload, 'authorcutoff')
                if authorcutoff <= 0:
                    authorcutoff = 200
            else:
                authorcutoff = 200
            journalformat = read_journal_format_param(payload)
            return maxauthor, keyformat, authorcutoff, journalformat
        return None, None, None

    # for /cls formats default for the following 3 is to turn into macro
    if style in ['aastex', 'aspc', 'aasj']:
        if payload:
            return read_journal_format_param(payload)
        return None
    # default for the following four is to keep the full journal name, and hence 3
    if style in ['icarus', 'mnras', 'soph', 'apsj']:
        return 3

    return -1


def export_get(bibcode, style, format=-1):
    """

    :param bibcode:
    :param style:
    :param format:
    :return:
    """
    if format == -1:
        current_app.logger.debug('received request with bibcode={bibcode} to export in {style} style'.
                    format(bibcode=bibcode, style=style))
    else:
        current_app.logger.debug('received request with bibcode={bibcode} to export in {style} style with output format {format}'.
                    format(bibcode=bibcode, style=style, format=format))

    sort = 'date desc, bibcode desc'

    # if in the test mode, return test solr data
    if current_app.config['EXPORT_SERVICE_TEST_BIBCODE_GET'] == bibcode:
        return solrdata.data_2

    return get_solr_data(bibcodes=[bibcode], fields=default_solr_fields(), sort=sort, encode_style=adsFormatter().native_encoding(format))

@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/bibtex', methods=['POST'])
def bibTex_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'BibTex')
    if status == 200:
        maxauthor, keyformat, authorcutoff, journalformat = export_post_extras(request, 'BibTex')
        return return_bibTex_format_export(solr_data=results, include_abs=False,
                                           keyformat=keyformat, maxauthor=maxauthor, authorcutoff=authorcutoff,
                                           journalformat=journalformat)
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/bibtex/<bibcode>', methods=['GET'])
def bibTex_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_bibTex_format_export(solr_data=export_get(bibcode, 'BibTex'), include_abs=False,
                                       keyformat='%R', maxauthor=10, authorcutoff=200, journalformat=1, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/bibtexabs', methods=['POST'])
def bibTex_abs_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'BibTex Abs')
    if status == 200:
        maxauthor, keyformat, authorcutoff, journalformat = export_post_extras(request, 'BibTex Abs')
        return return_bibTex_format_export(solr_data=results, include_abs=True,
                                           keyformat=keyformat, maxauthor=maxauthor, authorcutoff=authorcutoff,
                                           journalformat=journalformat)
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/bibtexabs/<bibcode>', methods=['GET'])
def bibTex_abs_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_bibTex_format_export(solr_data=export_get(bibcode, 'BibTex Abs'), include_abs=True,
                                       keyformat='%R', maxauthor=0, authorcutoff=200, journalformat=1, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/ads', methods=['POST'])
def fielded_ads_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'ADS')
    if status == 200:
        return return_fielded_format_export(solr_data=results, fielded_style='ADS', request_type='POST')
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/ads/<bibcode>', methods=['GET'])
def fielded_ads_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_fielded_format_export(solr_data=export_get(bibcode, 'ADS'), fielded_style='ADS', request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/endnote', methods=['POST'])
def fielded_endnote_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'EndNote')
    if status == 200:
        return return_fielded_format_export(solr_data=results, fielded_style='EndNote', request_type='POST')
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/endnote/<bibcode>', methods=['GET'])
def fielded_endnote_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_fielded_format_export(solr_data=export_get(bibcode, 'EndNote'), fielded_style='EndNote', request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/procite', methods=['POST'])
def fielded_procite_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'ProCite')
    if status == 200:
        return return_fielded_format_export(solr_data=results, fielded_style='ProCite', request_type='POST')
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/procite/<bibcode>', methods=['GET'])
def fielded_procite_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_fielded_format_export(solr_data=export_get(bibcode, 'ProCite'), fielded_style='ProCite', request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/ris', methods=['POST'])
def fielded_refman_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'Refman')
    if status == 200:
        return return_fielded_format_export(solr_data=results, fielded_style='Refman', request_type='POST')
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/ris/<bibcode>', methods=['GET'])
def fielded_refman_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_fielded_format_export(solr_data=export_get(bibcode, 'Refman'), fielded_style='Refman', request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/refworks', methods=['POST'])
def fielded_refworks_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'RefWorks')
    if status == 200:
        return return_fielded_format_export(solr_data=results, fielded_style='RefWorks', request_type='POST')
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/refworks/<bibcode>', methods=['GET'])
def fielded_refworks_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_fielded_format_export(solr_data=export_get(bibcode, 'RefWorks'), fielded_style='RefWorks', request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/medlars', methods=['POST'])
def fielded_medlars_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'MEDLARS')
    if status == 200:
        return return_fielded_format_export(solr_data=results, fielded_style='MEDLARS', request_type='POST')
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/medlars/<bibcode>', methods=['GET'])
def fielded_medlars_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_fielded_format_export(solr_data=export_get(bibcode, 'MEDLARS'), fielded_style='MEDLARS', request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/dcxml', methods=['POST'])
def xml_dublincore_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'DublinCore')
    if status == 200:
        return return_xml_format_export(solr_data=results, xml_style='DublinCore')
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/dcxml/<bibcode>', methods=['GET'])
def xml_dublincore_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_xml_format_export(solr_data=export_get(bibcode, 'DublinCore'), xml_style='DublinCore', request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/refxml', methods=['POST'])
def xml_ref_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'Reference')
    if status == 200:
        return return_xml_format_export(solr_data=results, xml_style='Reference')
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/refxml/<bibcode>', methods=['GET'])
def xml_ref_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_xml_format_export(solr_data=export_get(bibcode, 'Reference'), xml_style='Reference', request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/refabsxml', methods=['POST'])
def xml_refabs_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'ReferenceAbs')
    if status == 200:
        return return_xml_format_export(solr_data=results, xml_style='ReferenceAbs')
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/refabsxml/<bibcode>', methods=['GET'])
def xml_refabs_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_xml_format_export(solr_data=export_get(bibcode, 'ReferenceAbs'), xml_style='ReferenceAbs', request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/aastex', methods=['POST'])
def csl_aastex_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'aastex', 2)
    if status == 200:
        journal_format = export_post_extras(request, 'aastex')
        return return_csl_format_export(solr_data=results,
                                        csl_style='aastex', export_format=adsFormatter.latex, journal_format=journal_format,
                                        request_type='POST')
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/aastex/<bibcode>', methods=['GET'])
def csl_aastex_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_csl_format_export(solr_data=export_get(bibcode, 'aastex', 2),
                                    csl_style='aastex', export_format=adsFormatter.latex, journal_format=adsJournalFormat.macro, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/icarus', methods=['POST'])
def csl_icarus_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'icarus', 2)
    if status == 200:
        return return_csl_format_export(solr_data=results,
                                        csl_style='icarus', export_format=adsFormatter.latex, journal_format=adsJournalFormat.full, request_type='POST')
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/icarus/<bibcode>', methods=['GET'])
def csl_icarus_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_csl_format_export(solr_data=export_get(bibcode, 'icarus', 2),
                                    csl_style='icarus', export_format=adsFormatter.latex, journal_format=adsJournalFormat.full, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/mnras', methods=['POST'])
def csl_mnras_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'mnras', 2)
    if status == 200:
        return return_csl_format_export(solr_data=results,
                                        csl_style='mnras', export_format=adsFormatter.latex, journal_format=adsJournalFormat.full, request_type='POST')
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/mnras/<bibcode>', methods=['GET'])
def csl_mnras_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_csl_format_export(solr_data=export_get(bibcode, 'mnras', 2),
                                    csl_style='mnras', export_format=adsFormatter.latex, journal_format=adsJournalFormat.full, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/soph', methods=['POST'])
def csl_soph_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'soph', 2)
    if status == 200:
        return return_csl_format_export(solr_data=results,
                                        csl_style='soph', export_format=adsFormatter.latex, journal_format=adsJournalFormat.full, request_type='POST')
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/soph/<bibcode>', methods=['GET'])
def csl_soph_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_csl_format_export(solr_data=export_get(bibcode, 'soph', 2),
                                    csl_style='soph', export_format=adsFormatter.latex, journal_format=3, request_type='GET')


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
    if 'sort' in payload:
        sort = read_value_list_or_not(payload, 'sort')
    else:
        sort = 'date desc, bibcode desc'

    bibcodes = payload['bibcode']
    csl_style = payload['style']
    export_format = payload['format']

    if (len(bibcodes) == 0) or (len(csl_style) == 0)  or (export_format == None):
        return return_response({'error': 'not all the needed information received'}, 400)

    if (not adsCSLStyle().verify(csl_style)):
        return return_response({'error': 'unrecognizable style (supprted formats are: ' + adsCSLStyle().get() + ')'}, 400)
    if (not adsFormatter().verify(export_format)):
        return return_response({'error': 'unrecognizable format (supprted formats are: unicode=1, html=2, latex=3)'}, 400)

    current_app.logger.info('received request with bibcodes={bibcodes} to export in {csl_style} style with output format {export_format}  style using sort order={sort}'.
                 format(bibcodes=','.join(bibcodes), csl_style=csl_style, export_format=export_format, sort=sort))

    solr_data = get_solr_data(bibcodes=bibcodes, fields=default_solr_fields(), sort=sort, encode_style=export_format)
    journal_format = export_post_extras(request, csl_style)
    return return_csl_format_export(solr_data, csl_style, export_format, journal_format)


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
    if 'sort' in payload:
        sort = read_value_list_or_not(payload, 'sort')
    else:
        sort = 'date desc, bibcode desc'

    bibcodes = payload['bibcode']
    try:
        custom_format_str = read_value_list_or_not(payload, 'format')
    except Exception as e:
        return return_response({'error': 'unable to read custom format'}, 400)

    current_app.logger.info('received request with bibcodes={bibcodes} to export in a custom format: {custom_format_str}  style using sort order={sort}'.
                 format(bibcodes=','.join(bibcodes), custom_format_str=custom_format_str.encode('utf8'), sort=sort))

    if (len(bibcodes) == 0) or (len(custom_format_str) == 0):
        return return_response({'error': 'not all the needed information received'}, 400)

    # pass the user defined format to CustomFormat to parse and we would be able to get which fields
    # in Solr we need to query on
    custom_export = CustomFormat(custom_format=custom_format_str)
    fields = custom_export.get_solr_fields()

    # now get the required data from Solr and send it to customFormat for formatting
    solr_data = get_solr_data(bibcodes=bibcodes, fields=fields, sort=sort)
    if (solr_data is not None):
        if ('error' in solr_data):
            return return_response({'error': 'unable to query solr'}, 400)
        custom_export.set_json_from_solr(solr_data)
        return return_response(custom_export.get(), 200, 'POST')
    return return_response({'error': 'no result from solr'}, 404)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/votable', methods=['POST'])
def votable_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'VOTable')
    if status == 200:
        return return_votable_format_export(solr_data=results, request_type='POST')
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/votable/<bibcode>', methods=['GET'])
def votable_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_votable_format_export(solr_data=export_get(bibcode, 'VOTable'), request_type='GET')


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

    if 'link' in payload:
        link = read_value_list_or_not(payload, 'link')
    else:
        link = ''

    results, status = export_post(request, 'RSS')
    if status == 200:
        return return_rss_format_export(solr_data=results, link=link)
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/rss/<bibcode>/', defaults={'link': ''}, methods=['GET'])
@bp.route('/rss/<bibcode>/<path:link>', methods=['GET'])
def rss_format_export_get(bibcode, link):
    """

    :param bibcode:
    :param link:
    :return:
    """
    return return_rss_format_export(solr_data=export_get(bibcode, 'RSS'), link=link, request_type='GET')


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/ieee', methods=['POST'])
def csl_ieee_format_export_post():
    """

    :return:
    """
    results, status = export_post(request, 'ieee', 2)
    if status == 200:
        return return_csl_format_export(solr_data=results,
                                        csl_style='ieee', export_format=adsFormatter.unicode, journal_format=adsJournalFormat.full, request_type='POST')
    return return_response(results, status)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/ieee/<bibcode>', methods=['GET'])
def csl_ieee_format_export_get(bibcode):
    """

    :param bibcode:
    :return:
    """
    return return_csl_format_export(solr_data=export_get(bibcode, 'ieee', 2),
                                    csl_style='ieee', export_format=adsFormatter.unicode, journal_format=adsJournalFormat.full, request_type='GET')
