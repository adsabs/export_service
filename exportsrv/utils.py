
from flask import current_app
import requests
import re

from exportsrv.client import client

def get_solr_data(bibcodes, fields, sort, start=0):
    """

    :param bibcodes:
    :param fields:
    :param start:
    :param sort:
    :return:
    """
    data = 'bibcode\n' + '\n'.join(bibcodes)

    rows = min(current_app.config['EXPORT_SERVICE_MAX_RECORDS_SOLR'], len(bibcodes))

    params = {
        'q': '*:*',
        'wt': 'json',
        'rows': rows,
        'start': start,
        'sort': sort,
        'fl': fields,
        'fq': '{!bitset}'
    }

    headers = {
        'Authorization': 'Bearer '+current_app.config['EXPORT_SERVICE_ADSWS_API_TOKEN'],
        'Content-Type': 'big-query/csv',
    }

    try:
        response = client().post(
            url=current_app.config['EXPORT_SOLRQUERY_URL'],
            params=params,
            data=data,
            headers=headers
        )
        if (response.status_code == 200):
            # make sure solr found the documents
            from_solr = response.json()
            if (from_solr.get('response')):
                num_docs = from_solr['response'].get('numFound', 0)
                if num_docs > 0:
                    return from_solr
        current_app.logger.error('Solr returned {response}.'.format(response=response))
        return None
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        current_app.logger.error('Solr exception. Terminated request.')
        current_app.logger.error(e)
        return None


def get_eprint(solr_doc):
    """

    :param a_doc:
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



