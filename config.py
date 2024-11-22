
# must be here for adsmutils to override it using env vars
# but if left empty (resolving to False) it won't be used
SERVICE_TOKEN = None

# configuration for accessing solr db
# these values can be overwritten by local_config values
# maximum number of records that can be fetched by bigquery is for now 2000
# this can be overwritten to become smaller but it cannot become larger
# cutoff to use query vs bigquery is 100, anything equal and lower calls query, otherwise bigquery is called
EXPORT_SOLR_BIGQUERY_URL = "https://api.adsabs.harvard.edu/v1/search/bigquery"
EXPORT_SERVICE_MAX_RECORDS_SOLR_BIGQUERY = 2000
EXPORT_SOLR_QUERY_URL = "https://api.adsabs.harvard.edu/v1/search/query"
EXPORT_SERVICE_MAX_RECORDS_SOLR_QUERY = 100

# these are used for linkout links
EXPORT_SERVICE_FROM_BBB_URL = 'https://ui.adsabs.harvard.edu/abs'
EXPORT_SERVICE_RESOLVE_URL = "https://ui.adsabs.harvard.edu/link_gateway"

# added to the end of bibTex
EXPORT_SERVICE_ADS_NOTES = 'Provided by the SAO/NASA Astrophysics Data System'

# sort specified by user when they want the service to keep the same order they have specified
# going to be useful when used through the API
# not giong to be implemented from the UI
EXPORT_SERVICE_NO_SORT_SOLR = 'no sort'

# Journal Abbreviations used in the ADS BibTeX entries
# From http://adsabs.harvard.edu/abs_doc/aas_macros.html
# Journal name   TeX macro
EXPORT_SERVICE_AASTEX_JOURNAL_MACRO = [
    ['AJ', r'\aj'],
    ['ApJ', r'\apj'],
    ['AcA', r'\actaa'],
    ['ARA&A', r'\araa'],
    ['ApJL', r'\apjl'],
    ['ApJS', r'\apjs'],
    ['ApOpt', r'\ao'],
    ['Ap&SS', r'\apss'],
    ['A&A', r'\aap'],
    ['A&ARv', r'\aapr'],
    ['A&AS', r'\aaps'],
    ['AZh', r'\azh'],
    ['BAAS', r'\baas'],
    ['ChA&A', r'\caa'],
    ['ChJAA', r'\cjaa'],
    ['Icar', r'\icarus'],
    ['JCAP', r'\jcap'],
    ['JRASC', r'\jrasc'],
    ['MmRAS', r'\memras'],
    ['MNRAS', r'\mnras'],
    ['NewA', r'\na'],
    ['NewAR', r'\nar'],
    ['PhRvA', r'\pra'],
    ['PhRvB', r'\prb'],
    ['PhRvC', r'\prc'],
    ['PhRvD', r'\prd'],
    ['PhRvE', r'\pre'],
    ['PhRvL', r'\prl'],
    ['PASA', r'\pasa'],
    ['PASP', r'\pasp'],
    ['PASJ', r'\pasj'],
    ['RMxAA', r'\rmxaa'],
    ['QJRAS', r'\qjras'],
    ['S&T', r'\skytel'],
    ['SoPh', r'\solphys'],
    ['SvA', r'\sovast'],
    ['SSRv', r'\ssr'],
    ['ZA', r'\zap'],
    ['Natur', r'\nat'],
    ['IAUC', r'\iaucirc'],
    ['ApL', r'\aplett'],
    ['ASPRv', r'\apspr'],
    ['BAN', r'\bain'],
    ['FCPh', r'\fcp'],
    ['GeCoA', r'\gca'],
    ['GeoRL', r'\grl'],
    ['JChPh', r'\jcp'],
    ['JGR', r'\jgr'],
    ['JQSRT', r'\jqsrt'],
    ['MmSAI', r'\memsai'],
    ['NuPhA', r'\nphysa'],
    ['PhR', r'\physrep'],
    ['PhyS', r'\physscr'],
    ['P&SS', r'\planss'],
    ['SPIE', r'\procspie'],
    ['JAVSO', r'\jaavso'],
    ['PSJ', r'\psj'],
    ['M&PS', r'\maps'],
    ['AAS', r'\aas'],
    ['DPS', r'\dps'],
]

# For SoPh format:
# First element is the journal abbreviation to be output,
# second one is the bibstem to which it applies.
EXPORT_SERVICE_SOPH_JOURNAL_ABBREVIATION = {
    'A&A..': 'Astron. Astroph.',
    'ApJ..': 'Astrophys. J.',
    'SoPh.': 'Solar Phys.',
    'GeoRL': 'Geophys. Res. Lett.',
    'JGRA.': 'J.Geophys. Res. A',
    'JGRB.': 'J.Geophys. Res. B',
    'JGRC.': 'J.Geophys. Res. C',
    'JGRD.': 'J.Geophys. Res. D',
    'JGRE.': 'J.Geophys. Res. E',
}


# Testing Bibcode for GET
EXPORT_SERVICE_TEST_BIBCODE_GET = ['TEST..BIBCODE..GET.']
