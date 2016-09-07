# This is the URL to communicate with ADS Classic
EXPORT_SERVICE_CLASSIC_EXPORT_URL = 'http://adsabs.harvard.edu/cgi-bin/nph-abs_connect'
# The string in the results sent back from Classic indicating success
EXPORT_SERVICE_CLASSIC_SUCCESS_STRING = '''Query Results from the ADS Database


Retrieved \d+ abstracts, starting with number \d+\.  Total number selected: \d+\.

'''
# Configure logging
EXPORT_SERVICE_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s\t%(process)d '
                      '[%(asctime)s]:\t%(message)s',
            'datefmt': '%m/%d/%Y %H:%M:%S',
        }
    },
    'handlers': {
        'file': {
            'formatter': 'default',
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/tmp/export_service_app.log',
        },
        'console': {
            'formatter': 'default',
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
        # 'syslog': {
        #     'formatter': 'default',
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.SysLogHandler',
        #     'address': '/dev/log'
        # }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
