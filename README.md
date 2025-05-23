[![Build Status](https://travis-ci.org/adsabs/export_service.svg)](https://travis-ci.org/adsabs/export_service)
[![Coverage Status](https://coveralls.io/repos/github/adsabs/export_service/badge.svg?branch=master)](https://coveralls.io/github/adsabs/export_service?branch=master)

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
    
Note that there is an optional parameter `sort` for sorting the records from solr. The default sort option (if omitted) is by `date desc, bibcode desc`. For example

    curl -H "Authorization: Bearer <your API token>" -H "Content-Type: application/json" -X POST -d '{"bibcode":["2015ApJS..219...21Z", "2018AAS...23221409A"], "sort":"bibcode desc"}' https://api.adsabs.harvard.edu/v1/export/bibtex

To return the records in the exact order of input bibcode list, set `sort` to `no sort`.


###### 1. For the following endpoints output is in tagged format:
* **/bibtex** *BibTeX reference list*
* **/bibtexabs** *BibTeX with abstracts*
* **/ads** *Generic tagged abstracts*
* **/endnote** *EndNote format*
* **/procite** *ProCite format*
* **/ris** *Refman format*
* **/refworks** *RefWorks format*
* **/medlars** *MEDLARS format*


Note that for endpoints `/bibtex` and `/bibtexabs` optional parameters `maxauthor`, `authorcutoff`, `keyformat` and `journalformat` can be passed in. 
* `maxauthor` is maxinum number of authors displayed. The default values for `maxauthor` for `/bibtex` and `/bibtexabs` respectivley are 10 and 0, where 0 means all.
* `authorcutoff` is the threshold for truncating number of authors. If the number of authors is larger than `authorcutoff`, author list is truncated and `maxauthor` number of authors will be returned followed by `et al.`. If `authorcutoff` is not specified, the default of 200 is used.
* `keyformat` allows user to customize bibtex key and could contain some combination of authors' last name(s), publication year, journal, and bibcode. User is now able to pick the key generation algorithm by specifying a custom format for it. To provide a specific example, this is our default format for 2019AAS...23338108A:

        @INPROCEEDINGS{2019AAS...23338108A,
           author = {{Accomazzi}, Alberto and {Kurtz}, Michael J. and {Henneken}, Edwin and
        ...

   In addition `keyformat` accepts specifier `%zm` to enumerate keys (one character alphabet) should duplicate keys get created. Note that if enumeration specifier is not included, even if duplicate key are found, service does not enumerate the keys.

   Now user can define one of the following:

        Accomazzi:2019              -- %1H:%Y
        Accomazzi:2019:AAS          -- %1H:%Y:%q
        Accomazzi2019               -- %1H%Y
        Accomazzi2019AAS            -- %1H%Y%q
        AccomazziKurtz2019          -- %2H%Y


###### 2. For the following endpoints output is in xml format:
* **/dcxml** *Dublin Core XML*
* **/refxml** *XML references*
* **/refabsxml** *XML with abstracts*
* **/votable** *VOTables*
* **/rss** *RSS*
* **/jatsxml** *JATS Journal Publishing XML*


Note that for endpoint `/rss` an optional parameter `link` can be passed in. `link` is the query url that generated the bibcodes. 

For example querying ADS Bumblebee for

    author:"accomazzi" and year:2018

at the end of March 2018, returns the following 4 bibcodes, and generates the url as specified below: 

    {"bibcode":["2018arXiv180303598K","2018arXiv180101021FB","2018AAS...23136217A","2018AAS...23130709A"], "link":"https://ui.adsabs.harvard.edu/#search/q=author%3A%22accomazzi%22%20and%20year%3A2018&sort=date%20desc%2C%20bibcode%20desc"}

which can be passed as payload to `/rss` endpoint.


###### 3. For the following Citation Style Language Format endpoints output is in latex format:
* **/aastex** *AASTeX format* (excludes record title)
* **/aastex-psj** *AASTeX format for PSJ* (exact same as `/aastex` but includes record title)
* **/icarus** *Icarus format*
* **/mnras** *MNRAS format*
* **/soph** *SoPh format*
* **/aspc** *ASP Conference Series format*
* **/aasj** *AAS Journals format*


Note that for the endpoints `/aastex` there is an optional parameter `journalformat` which allows user to decide on the format of journal name. `1` indicates to use AASTeX macros if there are any (default), otherwise full journal name is exported. `2` means use journal abbreviations and `3` means use full journal name.


###### 4. For the following Citation Style Language Format endpoints output is in text format:
* **/apsj** *APS Journals format*
* **/ieee** *IEEE format*
* **/agu** *AGU Journals format*
* **/gsa** *GSA format*
* **/ams** *AMS (Meteorological) format*


###### 5. Using the /csl endpoint for Citation Style Language Formats:

The /csl endpoint allows various citation style language (CSL) and output formats to be defined in the payload as follows:

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "style":"", "format":"", "sort":"date desc, bibcode, desc"}

The style parameter can be any of the CSL formats listed in sections 3 and 4 (e.g., aastex, icarus, mnras, soph, aspc, apsj, ieee, agu, gsa, ams). The format specifies the output type: 1 (Unicode), 2 (HTML), or 3 (LaTeX). Additionally, there is an optional journalformat parameter for certain styles (aastex, aspc, and aasj) to specify the journal name format, with values 1 (AASTeX macros, default), 2 (journal abbreviations), or 3 (full journal name).

Note that, as mentioned above, all the CSL formats can also be accessed through their dedicated endpoints, as listed earlier, using a payload like:

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "sort":"date desc, bibcode, desc"}


###### 6. For endpoint /custom define payload as:

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


### Optional parameter for all export formats :

A new parameter, `authorlimit`, has been introduced to limit the number of authors and their affiliations returned in exported records. This addresses the growing issue of excessively large author lists, with some papers featuring thousands of authors.

At the request of stakeholders, the `authorlimit` parameter has been set to a default value of 200 in the service. While this default is hardcoded, it remains configurable through both the ADS UI and the API, ensuring flexibility in controlling the number of authors and affiliations displayed based on user needs.

If the `authorlimit` parameter is omitted when using the API, the default value of 200 will apply. However, as mentioned, users can override this limit by explicitly specifying their desired value in the API request.

    {"bibcode": ["1980ApJS...44..137K", "1980ApJS...44..489B"], "authorlimit": 500}
    
To retrieve all records without this limit using the API, you can use the provided script: https://github.com/adsabs/export_service/blob/master/export_with_api.py.


Another optional parameter added in 2024 is `outputformat`, which determines the structure and content of exported bibliographic records. Two formats are currently supported: `classic` and `individual`.

The classic format includes two fields:

    msg: A message summarizing the number of retrieved records.
    export: A single string containing all references, formatted for copy-pasting.

Example Response:

    {
        "msg": "Retrieved 2 abstracts, starting with number 1.",
        "export": "Reference 1\nReference 2\n..."
    }

The individual format separates records into distinct entries, allowing for more structured data handling.

The individual format includes six fields:

    num_docs: The number of documents retrieved.
    docs: A list of dictionaries, each containing:
        bibcode: ADS identifier for the record
        reference: The formatted reference for the record
    header: Content that appears before the data records. For XML formats, this includes metadata or structure before the data records tag (ie, <records>). For custom formats like CSV, this includes the header line, and any user-specified header.
    footer: Content that appears after the data records. For XML formats, this includes closing XML tags. For custom formats, this includes any user-specified footer.

Example Response:

    {
        "num_docs": 2,
        "docs": [
            {"bibcode": "1980ApJS...44..137K", "reference": "Formatted Reference 1"},
            {"bibcode": "1980ApJS...44..489B", "reference": "Formatted Reference 2"}
        ],
        "header": "Custom header or XML top content",
        "footer": "Custom footer or XML bottom content"
    }

To specify this parameters:

    {"bibcode":["1980ApJS...44..137K","1980ApJS...44..489B"], "sort":"date desc, bibcode, desc", "outputformat": ""}

The `outputformat` field accepts the values `1` for `classic` and `2` for `individual`.

By default, if `outputformat` is not specified, the service will use the classic format.


## Maintainers

Golnaz, Edwin
