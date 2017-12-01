#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import inspect

from flask_restful import Api
from flask_discoverer import Discoverer

from adsmutils import ADSFlask

from exportsrv.views import bp

def create_app(**config):
    """
    Create the application and return it to the user
    :return: flask.Flask application
    """

    if config:
        app = ADSFlask(__name__, static_folder=None, local_config=config)
    else:
        app = ADSFlask(__name__, static_folder=None)

    app.url_map.strict_slashes = False

    # Register extensions
    api = Api(app)
    Discoverer(app)

    app.register_blueprint(bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, use_reloader=False)