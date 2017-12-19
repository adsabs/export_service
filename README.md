[![Build Status](https://travis-ci.org/adsabs/export_service.svg?branch=master)](https://travis-ci.org/adsabs/export_service)
[![Coverage Status](https://coveralls.io/repos/adsabs/export_service/badge.svg?branch=master)](https://coveralls.io/r/adsabs/export_service?branch=master)


# ADS Export Service


#### Make a POST request:

`curl -H "Content-Type: application/json" -X POST -d <payload> <endpoint>`


##### where `<payload>` and `<endpoint>` are as follows:


###### 1. For endpoints `/bibtex` and `/bibtexabs` payload is defined as
    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"]}


###### 2. For the fielded export format we have the following endpoints
* /ads
* /endnote
* /procite
* /ris
* /refworks
* /medlars

similarly to #1, payload should be defined as a comma separated list of bibcodes


###### 3. For endpoint xml export format we have teh following endpoints
* /dcxml
* /refxml
* /refabsxml


###### 4. For the following endpoints output is in latex format
* /aastex
* /icarus
* /mnras
* /soph


###### 5. For endpoint /csl inlcude style and output format in the payload as defined below

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"", "format":""}

    where style can be: aastex, icarus, mnras, soph, aspc, apj, rhrv and format can be: 1, 2 or 3, for output format Unicode, HTML or LaTeX respectively.


###### 6. For endpoint /custom

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "format":"%ZEncoding:latex%ZLinelength:0\bibitem[%4m(%Y)]{%R} %5.3l\ %Y, %j, %V, %p.\n"}



#### Make a GET request:

`curl -H "Content-Type: application/json" -X GET -d <endpoint>/<bibcode>`


##### where `<endpoint>` are as follows:
* /bibtex
* /bibtexabs
* /ads
* /endnote
* /procite
* /ris
* /refworks
* /medlars
* /dcxml
* /refxml
* /refabsxml
* /aastex
* /icarus
* /mnras
* /soph


#### Convert a Classic Custom Format to the Current Custom Format:

`curl -H "Content-Type: application/json" -X POST -d <payload> <endpoint>`

##### where `<endpoint>` is `/convert` and `<payload>` is formatted as: 
    {"format":<classic custom format string>}

##### For example:

`curl -H "Content-Type: application/json" -X POST -d '{"format":"\\\\bibitem[%\\2m%(y)]\\{%za1%y} %\\8l %\\Y,%\\j,%\\V,%\\p"}' http://localhost:4000/convert`