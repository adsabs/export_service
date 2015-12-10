EXPORT_SERVICE_CLASSIC_EXPORT_URL = 'http://adsabs.harvard.edu/cgi-bin/nph-abs_connect'


EXPORT_SERVICE_CLASSIC_SUCCESS_STRING = '''Query Results from the ADS Database


Retrieved \d+ abstracts, starting with number \d+\.  Total number selected: \d+\.

'''

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
