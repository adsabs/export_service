[![Build Status](https://travis-ci.org/adsabs/export_service.svg?branch=master)](https://travis-ci.org/adsabs/export_service)

# ADS Export Service


#### Make a request:

`curl -H "Content-Type: application/json" -X POST -d <payload> http://localhost:5000/<endpoint>`


#### where `<payload>` and `<endpoint>` are as follows:


##### 1. For endpoint /bibtex
    * define payload for BibTex style

    `{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"BibTex"}`
    
    
    * define payload for BibTex with abstracts style

    `{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"BibTexAbs"}`


##### 2. For endpoint /fielded
    * define payload for generic fielded format

    `{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"ADS"}`


    * define payload for EndNote fielded format

    `{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"EndNote"}`


    * define payload for ProCite fielded format

    `{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"ProCite"}`


    * define payload for Refman fielded format

    `{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"Refman"}`


    * define payload for RefWorks fielded format

    `{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"RefWorks"}`


    * define payload for MEDLARS fielded format

    `{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"MEDLARS"}`


##### 3. For endpoint /xml

    * define payload for Dublin XML format

    `{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"Dublin"}`


    * define payload for XML References format

    `{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"Reference"}`


    * define payload for XML References with abstracts as

    `{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"ReferenceAbs"}`


##### 4. For endpoint /csl define payload as

    `{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"", "format":""}`
    
    where style can be: aastex, icarus, mnras, soph, aspc, apj, rhrv and export can be: unicode=1, html=2, latex=3


##### 5. For endpoint /custom define payload as

    `{"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "format":"%ZEncoding:latex%ZLinelength:0\bibitem[%4m(%Y)]{%R} %5.3l\ %Y, %j, %V, %p.\n"}`
