[![Build Status](https://travis-ci.org/adsabs/export_service.svg?branch=master)](https://travis-ci.org/adsabs/export_service)

## Proxy for ADS Classic Export Functions


#### Make a request:

`curl -H "Content-Type: application/json" -X POST -d '{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"]}' http://localhost:5000/aastex`


#### Endpoints for different datatypes:

* /aastex
* /bibtex
* /endnote
