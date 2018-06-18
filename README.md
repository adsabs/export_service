[![Build Status](https://travis-ci.org/adsabs/export_service.svg)](https://travis-ci.org/adsabs/export_service)
[![Coverage Status](https://coveralls.io/repos/adsabs/export_service/badge.svg)](https://coveralls.io/r/adsabs/export_service?branch=master)


# ADS Export Service

## Short Summary

This microservice exports ADS records with various formats including BibTex, AASTex, and multiple fielded and xml options.


## Setup (recommended)

    $ virtualenv python
    $ source python/bin/activate
    $ pip install -r requirements.txt
    $ pip install -r dev-requirements.txt
    $ vim local_config.py # edit, edit

    
## Testing

On your desktop run:

    $ py.test
    

## API

### POST a request:

To get e.g. BibTeX for a set of records you do a POST request to the endpoint

    https://api.adsabs.harvard.edu/v1/export/bibtex

within the POST header payload is defined as

    {"bibcode":["<bibcode1>","<bibcode2>", ...]}
    
For example to get the BibTeX for the record with bibcode 2015ApJS..219...21Z, you would do

    curl -H "Authorization: Bearer <your API token>" -H "Content-Type: application/json" -X POST -d '{"bibcode":["2015ApJS..219...21Z"]}' https://api.adsabs.harvard.edu/v1/export/bibtex


and the API then responds in JSON with 

    {u'msg': u'Retrieved 1 abstracts, starting with number 1.  Total number selected: 1.', u'export': u'@ARTICLE{2015ApJS..219...21Z,\n   author = {{Zhang}, M. and {Fang}, M. and {Wang}, H. and {Sun}, J. and \n\t{Wang}, M. and {Jiang}, Z. and {Anathipindika}, S.},\n    title = "{A Deep Near-infrared Survey toward the Aquila Molecular Cloud. I. Molecular Hydrogen Outflows}",\n  journal = {\\apjs},\narchivePrefix = "arXiv",\n   eprint = {1506.08372},\n primaryClass = "astro-ph.SR",\n keywords = {infrared: ISM, ISM: jets and outflows, shock waves, stars: formation, stars: winds, outflows},\n     year = 2015,\n    month = aug,\n   volume = 219,\n      eid = {21},\n    pages = {21},\n      doi = {10.1088/0067-0049/219/2/21},\n   adsurl = {http://adsabs.harvard.edu/abs/2015ApJS..219...21Z},\n  adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n}\n\n'}
    
Note that there is an optional parameter `sort` for sorting the records from solr. The default is sort option (if omitted) is by `date desc, bibcode desc`. For example

    curl -H "Authorization: Bearer <your API token>" -H "Content-Type: application/json" -X POST -d '{"bibcode":["2015ApJS..219...21Z", "2018AAS...23221409A"], "sort":"bibcode desc"}' https://api.adsabs.harvard.edu/v1/export/bibtex

###### 1. For the following endpoints output is in tagged format:
* **/bibtex** *BibTeX reference list*
* **/bibtexabs** *BibTeX with abstracts*
* **/ads** *Generic tagged abstracts*
* **/endnote** *EndNote format*
* **/procite** *ProCite format*
* **/ris** *Refman format*
* **/refworks** *RefWorks format*
* **/medlars** *MEDLARS format*

###### 2. For the following endpoints output is in latex format:
* **/aastex** *AASTeX format*
* **/icarus** *Icarus format*
* **/mnras** *MNRAS format*
* **/soph** *SoPh format*

###### 3. For the following endpoints output is in xml format:
* **/dcxml** *Dublin Core XML*
* **/refxml** *XML references*
* **/refabsxml** *XML with abstracts*
* **/votable** *VOTables*
* **/rss** *RSS*

Note that for endpoint `/rss` an optional parameter `link` can be passed in. `link` is the query url that generated the bibcodes. 

For example querying ADS Bumblebee for

    author:"accomazzi" and year:2018

at the end of March 2018, returns the following 4 bibcodes, and generates the url as specified below: 

    {"bibcode":["2018arXiv180303598K","2018arXiv180101021FB","2018AAS...23136217A","2018AAS...23130709A"], "link":"https://ui.adsabs.harvard.edu/#search/q=author%3A%22accomazzi%22%20and%20year%3A2018&sort=date%20desc%2C%20bibcode%20desc"}

which can be passed as payload to `/rss` endpoint.


###### 4. Using endpoint /csl allows various styles and output formats to be defined in payload as follows:

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"", "format":""}

    where style can be: aastex, icarus, mnras, soph, aspc, apj, rhrv and format can be: 1, 2 or 3, for output formats Unicode, HTML or LaTeX respectively.


###### 5. For endpoint /custom define payload as:

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "format":"%ZEncoding:latex%ZLinelength:0\bibitem[%4m(%Y)]{%R} %5.3l\ %Y, %j, %V, %p.\n"}


### GET a request:

GET endpoints are similar to the POSTS endpoints. The `curl` command has the following syntax:

    curl -H "Authorization: Bearer <your API token>" <endpoint>/<bibcode>`


### To Convert a Classic Custom Format to the Current Custom Format:

    curl -H "Authorization: Bearer <your API token>" -H "Content-Type: application/json" -X POST -d <payload> <endpoint>

where `<endpoint>` is `/convert` and `<payload>` is formatted as: 
    {"format":<classic custom format string>}

For example:

    curl -H "Authorization: Bearer <your API token>" -H "Content-Type: application/json" -X POST -d '{"format":"\\\\bibitem[%\\2m%(y)]\\{%za1%y} %\\8l %\\Y,%\\j,%\\V,%\\p"}' https://api.adsabs.harvard.edu/v1/export/convert


## Maintainers

Golnaz, Edwin
