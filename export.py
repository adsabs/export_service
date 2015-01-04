from flask import Flask
from flask import Blueprint, request
from flask import current_app

from urllib import urlencode
import requests
import json

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/', methods=['POST', 'GET'])
def export():
    headers = request.headers
    
    payload = dict(request.args) #get data
    payload.update(request.form) #post data
    #print payload
    headers = dict(headers.items())
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    r = requests.post(current_app.config.get('CLASSIC_EXPORT_URL'), 
                      data=urlencode(payload, doseq=True), headers=headers)
    
    val = r.text
    if ('Retrieved' in val and '@' in val):
        msg = val[0:val.index('@')]
        val = val[val.index('@'):]
        ret = json.dumps({'msg': msg.strip(), 'export': val.strip()})
        status = 200
    else:
        ret = json.dumps({'msg': r.text})
        status = r.status_code
    
    if ('callback' in payload): # for jsonp
        ret = payload['callback'][0] + u'('+ ret + u');'
        
    return ret, status

if __name__ == '__main__':
    app.run()