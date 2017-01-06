from flask import Flask
from views import Aastex, Bibtex, Endnote, Ris, Icarus, Mnras, SoPh, DCXML, VOTables
import logging.config
from flask.ext.restful import Api
from flask.ext.discoverer import Discoverer


def create_app():
    """
    Create the application and return it to the user

    :return: flask.Flask application
    """

    app = Flask(__name__, static_folder=None)
    app.url_map.strict_slashes = False

    # Load config and logging
    load_config(app)
    logging.config.dictConfig(
        app.config['EXPORT_SERVICE_LOGGING']
    )

    # Register extensions
    api = Api(app)
    Discoverer(app)

    api.add_resource(Aastex, '/aastex')
    api.add_resource(Bibtex, '/bibtex')
    api.add_resource(Endnote, '/endnote')
    api.add_resource(Ris, '/ris')
    api.add_resource(Icarus, '/icarus')
    api.add_resource(Mnras, '/mnras')
    api.add_resource(SoPh, '/soph')
    api.add_resource(DCXML, '/dcxml')
    api.add_resource(VOTables, '/votables')

    return app


def load_config(app):
    """
    Loads configuration in the following order:
        1. config.py
        2. local_config.py (ignore failures)
    :param app: flask.Flask application instance
    :return: None
    """

    app.config.from_pyfile('config.py')

    try:
        app.config.from_pyfile('local_config.py')
    except IOError:
        app.logger.warning("Could not load local_config.py")

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, use_reloader=False)
