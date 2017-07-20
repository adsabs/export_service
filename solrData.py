#!/usr/bin/env python

from flask import current_app
import requests
from client import client
import json

def getSolrData(bibcodes,
                fields,
                start=0,
                sort='date desc'
                ):
    data = 'bibcode\n' + '\n'.join(bibcodes)

    # todo: there should be a top limit on number of bibcodes
    rows = len(bibcodes)

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
            url=current_app.config['EXPORT_SERVICE_BIGQUERY_PATH'],
            params=params,
            data=data,
            headers=headers
        )
        #print(response.ok)  # => True
        #print(response.status_code)  # => 200
        #print response.headers
        return response.json()
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print("\nbailing")
        print e
