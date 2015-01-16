SECRET_KEY = 'this should be changed'

#This section configures this application to act as a client, for example to query solr via adsws
CLIENT = {
  'TOKEN': 'we will provide an api key token for this application'
}

CLASSIC_EXPORT_URL = 'http://adsabs.harvard.edu/cgi-bin/nph-abs_connect'

CLASSIC_EXPORT_SUCCESS_STRINGS = {
  'BIBTEX':'''Query Results from the ADS Database


Retrieved \d+ abstracts, starting with number \d+\.  Total number selected: \d+\.

''',
  'AASTeX':'',
  'ENDNOTE':'',

}