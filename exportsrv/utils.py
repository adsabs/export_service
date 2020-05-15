
from flask import current_app, request
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
    rows = min(current_app.config['EXPORT_SERVICE_MAX_RECORDS_SOLR_BIGQUERY'], len(bibcodes))
    user_token = request.headers.get('X-Forwarded-Authorization', request.headers.get('Authorization', ''))
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
                headers={'Authorization': user_token},
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
                headers={'Authorization': user_token,
                         'Content-Type': 'big-query/csv'}
            )
        
        response.raise_for_status()

        if (response.status_code == 200):
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



