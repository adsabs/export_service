import requests
import json


def query_solr(query, start=1, rows=2000, fl='bibcode'):
    """
    to get the list of bibcodes, note that 2000 is the maximum numbero rows that can be extracted with a request

    :param query:
    :param start:
    :param rows:
    :param fl:
    :return:
    """
    params = {
        'q': query,
        'start': start,
        'rows': rows,
        'sort': 'bibcode desc',
        'fl': fl,
    }

    try:
        response = requests.get(
            url='https://api.adsabs.harvard.edu/v1/search/query',
            params=params,
            headers={'Authorization': 'Bearer %s' % api_token},
            timeout=60
        )
        if response.status_code == 200:
            # make sure solr found the documents
            from_solr = response.json()
            if (from_solr.get('response')):
                docs = from_solr['response']['docs']
                return docs, 200
        return None, response.status_code
    except requests.exceptions.RequestException as e:
        return None, e

def get_records_export(data, endpoint):
    """
    call export service with data to format it using the endpoint format

    :param data
    :param endpoint:
    :return:
    """
    response = requests.post(
        url='https://api.adsabs.harvard.edu/v1/export' + endpoint,
        headers={'Authorization': 'Bearer %s' % api_token},
        data=json.dumps(data)
    )

    if response.status_code == 200:
        return json.loads(response.text).get('export', None)
    return 'status_code=%d'%(response.status_code)




# note that the list of formats' endpoints, and optional/required parameters for each is in readme of the service
# (https://github.com/adsabs/export_service/blob/master/README.md)

# 0- create an API token if you have not created it yet (https://ui.adsabs.harvard.edu/user/settings/token) and put it here
api_token = 'your token here'

if __name__ == "__main__":

    # 1- get list of bibcodes from ADS for your query, format them into a list and init the data with them
    docs, status_code = query_solr(query='author:"shapurian, g" year:2024', fl='bibcode')
    if status_code == 200:
        identifiers = [doc['bibcode'] for doc in docs]
        data = {"bibcode": identifiers}

        # 2- include optional parameters (the same for all the formats), skip otherwise
        data.update({"sort": "date desc, bibcode desc", "authorlimit": 500})

        # 3- optional/required parameters for some of the export formats (ie, BibTex has an optional parameter keyformat)
        # check the readme for the parameter(s) of your selected format
        data.update({"keyformat": "%H%Y"})

        # 4- specify the format you want the records to be exported to
        endpoint = '/bibtex'

        # 5- send the request to ADS API
        results = get_records_export(data=data, endpoint=endpoint)
        print(results)
    else:
        print('Error:', status_code)