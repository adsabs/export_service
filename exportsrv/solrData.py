#!/usr/bin/env python

import os

from flask import current_app
import requests
from client import client

from adsmutils import setup_logging

global logger
logger = None

def get_solr_data(bibcodes, fields, start=0, sort='date desc'):
    global logger
    logger = setup_logging('export_service', current_app.config.get('LOG_LEVEL', 'INFO'))

    data = 'bibcode\n' + '\n'.join(bibcodes)

    rows = max(6000, len(bibcodes))

    params = {
        'q': '*:*',
        'wt': 'json',
        'rows': rows,
        'start': start,
        'sort': sort,
        'fl': fields,
        'fq': '{!bitset}'
    }

    headers = {'Authorization':current_app.config['EXPORT_SERVICE_ADSWS_API_TOKEN']}

    try:
        response = client().post(
            url=os.environ.get('EXPORT_SOLRQUERY_URL'),
            params=params,
            data=data,
            headers=headers
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        logger.error('\nbailing')
        logger.error(e)

