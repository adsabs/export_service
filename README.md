[![Build Status](https://travis-ci.org/adsabs/export_service.svg?branch=master)](https://travis-ci.org/adsabs/export_service)

# ADS Export Service


#### Make a request:

`curl -H "Content-Type: application/json" -X POST -d <payload> http://localhost:5000/<endpoint>`


#### where `<payload>` and `<endpoint>` are as follows:


##### 1. For endpoint /bibtex
    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"BibTex"}

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"BibTexAbs"}


##### 2. For endpoint /fielded
    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"ADS"}

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"EndNote"}

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"ProCite"}

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"Refman"}

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"RefWorks"}

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"MEDLARS"}


##### 3. For endpoint /xml

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"Dublin"}

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"Reference"}

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"ReferenceAbs"}


##### 4. For endpoint /csl

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"", "format":""}

    where style can be: aastex, icarus, mnras, soph, aspc, apj, rhrv and export can be: unicode=1, html=2, latex=3


##### 5. For endpoint /custom

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "format":"%ZEncoding:latex%ZLinelength:0\bibitem[%4m(%Y)]{%R} %5.3l\ %Y, %j, %V, %p.\n"}

