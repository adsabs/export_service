
from werkzeug.serving import run_simple

from flask_discoverer import Discoverer

from adsmutils import ADSFlask

from exportsrv.views import bp, endpoint_registry

def attach_routes_to_registry(app):
    for rule in app.url_map.iter_rules():
        if rule.endpoint == 'static':
            continue
        view_func = app.view_functions[rule.endpoint]
        for name, entry in endpoint_registry.items():
            if view_func in entry["handlers"]:
                if rule.rule not in entry["routes"]:
                    entry["routes"].append(rule.rule)

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

    Discoverer(app)

    app.register_blueprint(bp)

    attach_routes_to_registry(app)
    return app

if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, create_app(), use_reloader=False, use_debugger=False)