# Proxy for ADS Classic Export Functions


### Make a request:
curl -H "Content-Type: application/json" -X POST -d '{"bibcodes":["1980ApJS...44..137K","1980ApJS...44..489B"], "export_format" : "bibText" }' http://localhost:5000/export


### Accepted Export Formats (parameter name):
 * AASTeX (AASTeX)
 * BIBText (BIBTEX)
 * EndNote (ENDNOTE)
