[![Build Status](https://travis-ci.org/adsabs/export_service.svg?branch=master)](https://travis-ci.org/adsabs/export_service)

## Proxy for ADS Classic Export Functions


#### Make a request:

`curl -H "Content-Type: application/json" -X POST -d <payload> http://localhost:5000/<endpoint>`


#### where <payload> and <endpoint> are as follows:

1- For endpoint /bibtex define payload as
    '{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"BibTex"}'       for BibTex Reference List or
    '{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"BibTexAbs"}'    for BibTex with abstracts

2- For endpoint /fielded define payload as
    '{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"ADS"}'          for generic fielded format or
    '{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"EndNote"}'      for EndNote fielded format or
    '{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"ProCite"}'      for ProCite fielded format or
    '{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"Refman"}'       for Refman fielded format or
    '{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"RefWorks"}'     for RefWorks fielded format or
    '{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"MEDLARS"}'      for MEDLARS fielded format

3- For endpoint /xml define payload as
    '{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"Dublin"}'       for Dublin XML or
    '{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"Reference"}'    for XML References
    '{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"ReferenceAbs"}' for XML References with abstracts

4- For endpoint /csl definde payload as
    '{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"", "format":""}'
    where style can be: aastex, icarus, mnras, soph, aspc, apj, rhrv
    and export can be: unicode=1, html=2, latex=3

5- For endpoint /custom define payload as
    '{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "format":"%ZEncoding:latex%ZLinelength:0\bibitem[%4m(%Y)]{%R} %5.3l\ %Y, %j, %V, %p.\n"}'
