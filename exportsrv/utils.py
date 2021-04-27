
# encoding=utf8
PYTHONIOENCODING="UTF-8"

from builtins import str

from flask import current_app, request
import requests
import re

from exportsrv.formatter.ads import adsFormatter

def get_solr_data(bibcodes, fields, sort, start=0, encode_style=None):
    """

    :param bibcodes:
    :param fields:
    :param start:
    :param sort:
    :return:
    """
    authorization = current_app.config.get('SERVICE_TOKEN', None) or \
                    request.headers.get('X-Forwarded-Authorization', request.headers.get('Authorization', ''))

    rows = min(current_app.config['EXPORT_SERVICE_MAX_RECORDS_SOLR_BIGQUERY'], len(bibcodes))

    try:
        # use query if rows <= allowed number of bibcodes for query
        if rows <= current_app.config['EXPORT_SERVICE_MAX_RECORDS_SOLR_QUERY']:
            params = {
                'q': 'identifier:("' + '" OR "'.join(bibcodes) + '")',
                'rows': rows,
                'start': start,
                'sort': sort if sort != current_app.config['EXPORT_SERVICE_NO_SORT_SOLR'] else '',
                'fl': fields,
            }
            response = current_app.client.get(
                url=current_app.config['EXPORT_SOLR_QUERY_URL'],
                params=params,
                headers={'Authorization': authorization},
            )
        # otherwise go with bigquery
        else:
            params = {
                'q': '*:*',
                'wt': 'json',
                'rows': rows,
                'start': start,
                'sort': sort if sort != current_app.config['EXPORT_SERVICE_NO_SORT_SOLR'] else '',
                'fl': fields,
                'fq': '{!bitset}'
            }
            response = current_app.client.post(
                url=current_app.config['EXPORT_SOLR_BIGQUERY_URL'],
                params=params,
                data='bibcode\n' + '\n'.join(bibcodes),
                headers={'Authorization': authorization, 'Content-Type': 'big-query/csv'}
            )

        response.raise_for_status()

        # make sure solr found the documents
        from_solr = response.json()
        if (from_solr.get('response')):
            num_docs = from_solr['response'].get('numFound', 0)
            if num_docs > 0:
                for doc in from_solr['response']['docs']:
                    # before proceeding remove the compunded field and assign it to individual count variables
                    citations = doc.pop('[citations]', None)
                    if citations is not None:
                        doc.update({u'num_references':citations['num_references']})
                        doc.update({u'num_citations':citations['num_citations']})
                    # replace any html entities in both title and abstract
                    for field in ['title', 'abstract']:
                        if field in doc:
                            field_str = doc.get(field)
                            if isinstance(field_str, list):
                                field_str[0] = replace_html_entity(field_str[0], encode_style)
                            elif isinstance(field_str, str):
                                field_str = replace_html_entity(field_str, encode_style)
                            doc[field] = field_str
                from_solr['response']['numFound'] = len(from_solr['response']['docs'])
                # reorder the list based on the list of bibcodes provided
                if sort == current_app.config['EXPORT_SERVICE_NO_SORT_SOLR']:
                    new_docs = []
                    for bibcode in bibcodes:
                        for i, doc in enumerate(from_solr['response']['docs']):
                            if bibcode in doc['identifier']:
                                new_docs.append(doc)
                                from_solr['response']['docs'].pop(i)
                                break
                    from_solr['response']['docs'] = new_docs
                    from_solr['response']['numFound'] = len(new_docs)
                return from_solr

        current_app.logger.error('Solr returned {response}.'.format(response=response))
        return None
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        current_app.logger.error('Solr exception. Terminated request.')
        current_app.logger.error(str(e))
        return None

def get_eprint(solr_doc):
    """

    :param solr_doc:
    :return:
    """
    if 'eid' in solr_doc:
        eid = solr_doc.get('eid')
        if eid.startswith('arXiv') or eid.startswith('ascl'):
            return eid
    if 'identifier' in solr_doc:
        identifier = solr_doc.get('identifier')
        arxiv_category = ('astro-ph', 'cond-mat', 'gr-qc', 'hep-ex', 'hep-lat', 'hep-ph', 'hep-th', 'math-ph', 'nucl-ex',
                          'nucl-th', 'econ', 'eess', 'physics', 'quant-ph', 'math', 'nlin', 'cs', 'q-bio', 'q-fin', 'stat')
        for i in identifier:
            if ('arXiv:' in i) or ('ascl:' in i):
                return i
            if i.startswith(arxiv_category):
                return 'arXiv:' + i
    return ''

def replace_html_entity(text, encode_style):
    """

    :param text:
    :param encode_style:
    :return:
    """
    # note that some of these character apprently encoded in html, and some in latex
    if encode_style in [adsFormatter.default, adsFormatter.unicode]:
        html_entity_to_encode = {'&lt;': '<', '\\\\lt': '<',
                                 '&gt;': '>', '\\\\gt': '>',
                                 '&amp;': '&', '\\\\&': '&'}
    elif encode_style == adsFormatter.xml:
        html_entity_to_encode = {'&lt;': '&#60;', '\\\\lt': '&#60;',
                                 '&gt;': '&#62;', '\\\\gt': '&#62;',
                                 '&amp;': '&#38;', '\\\\&': '&#38;'}
    else:
        # make sure all the entities are in html (ie, replace all that are latex)
        html_entity_to_encode = {'\\\\lt': '&lt;',
                                 '\\\\gt': '&gt;',
                                 '\\\\&': '&amp;'}

    re_html_entity = re.compile(r'(%s)'%(r'|'.join(list(html_entity_to_encode.keys()))))

    for entity in re_html_entity.findall(text):
        # make sure text from solr was properly escapted
        entity_encode = r'\{}'.format(entity) if entity.count('\\') == 1 else entity
        text = re.sub(entity_encode, html_entity_to_encode.get(entity_encode, ''), text)

    return text
