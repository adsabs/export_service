from flask import Flask
import logging.config
from views import bp
from flask_restful import Api
from flask_discoverer import Discoverer

def create_app(config=None):
    """
    Create the application and return it to the user

    :return: flask.Flask application
    """

    app = Flask(__name__, static_folder=None)
    app.url_map.strict_slashes = False

    # Load config and logging
    load_config(app, config)
    logging.config.dictConfig(
        app.config['EXPORT_SERVICE_LOGGING']
    )

    # Register extensions
    api = Api(app)
    Discoverer(app)

    app.register_blueprint(bp)
    return app


def load_config(app, config=None):
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
