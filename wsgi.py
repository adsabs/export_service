# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~

    entrypoint wsgi script
"""

import os
from werkzeug.serving import run_simple
from exportsrv import app

os.environ["EXPORT_SOLRQUERY_URL"] = "http://api.adsabs.harvard.edu/v1/search/bigquery"

application = app.create_app()

if __name__ == "__main__":
    run_simple('0.0.0.0', 4000, application, use_reloader=True, use_debugger=True)
