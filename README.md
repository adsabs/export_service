[![Build Status](https://travis-ci.org/adsabs/export_service.svg?branch=master)](https://travis-ci.org/adsabs/export_service)

## Proxy for ADS Classic Export Functions


#### Make a request:

`curl -H "Content-Type: application/json" -X POST -d <payload> http://localhost:5000/<endpoint>`


#### where <payload> and <endpoint> are as follows:

#####1. For endpoint /bibtex
⋅⋅⋅⋅*for BibTex Reference List define payload as
⋅⋅⋅⋅⋅⋅⋅⋅'{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"BibTex"}'
⋅⋅⋅⋅*or for BibTex with abstracts
⋅⋅⋅⋅⋅⋅⋅⋅'{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"BibTexAbs"}'

#####2. For endpoint /fielded
⋅⋅⋅⋅*for generic fielded format or define payload as
⋅⋅⋅⋅⋅⋅⋅⋅'{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"ADS"}'
⋅⋅⋅⋅*for EndNote fielded format define payload as
⋅⋅⋅⋅⋅⋅⋅⋅'{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"EndNote"}'
⋅⋅⋅⋅*for ProCite fielded format define payload as
⋅⋅⋅⋅⋅⋅⋅⋅'{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"ProCite"}'
⋅⋅⋅⋅*for Refman fielded format define payload as
⋅⋅⋅⋅⋅⋅⋅⋅'{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"Refman"}'
⋅⋅⋅⋅*for RefWorks fielded format define payload as
⋅⋅⋅⋅⋅⋅⋅⋅'{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"RefWorks"}'
⋅⋅⋅⋅*or for MEDLARS fielded format define payload as
⋅⋅⋅⋅⋅⋅⋅⋅'{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"MEDLARS"}'

#####3. For endpoint /xml
⋅⋅⋅⋅*for Dublin XML define payload as
⋅⋅⋅⋅⋅⋅⋅⋅'{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"Dublin"}'
⋅⋅⋅⋅*for XML References define payload as
⋅⋅⋅⋅⋅⋅⋅⋅'{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"Reference"}'
⋅⋅⋅⋅*or for XML References with abstracts define payload as
⋅⋅⋅⋅⋅⋅⋅⋅'{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"ReferenceAbs"}'

#####4. For endpoint /csl definde payload as
⋅⋅⋅⋅*'{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"", "format":""}'
⋅⋅⋅⋅⋅⋅⋅⋅where style can be: aastex, icarus, mnras, soph, aspc, apj, rhrv
⋅⋅⋅⋅⋅⋅⋅⋅and export can be: unicode=1, html=2, latex=3

#####5. For endpoint /custom define payload as
⋅⋅⋅⋅*'{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"],
⋅⋅⋅⋅⋅⋅⋅⋅"format":"%ZEncoding:latex%ZLinelength:0\bibitem[%4m(%Y)]{%R} %5.3l\ %Y, %j, %V, %p.\n"}'
