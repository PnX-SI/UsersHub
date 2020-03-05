"""
    Serveur de l'application UsersHub
"""

import os
import sys

# # Test si dossier vendor exists alors on l'ajoute au sys path
# if os.path.isdir('app/vendor'):
#     abs_p = os.path.abspath('app/vendor')
#     sys.path.append(abs_p)
# # Sinon activation du virtual env


import json
import toml

from flask import (
    Flask, redirect, url_for,
    request, session, render_template,
    g
)
from toml import TomlDecodeError

from app.env import db

class ReverseProxied(object):
    def __init__(self, app, script_name=None, scheme=None, server=None):
        self.app = app
        self.script_name = script_name
        self.scheme = scheme
        self.server = server

    def __call__(self, environ, start_response):
        script_name = environ.get("HTTP_X_SCRIPT_NAME", "") or self.script_name
        if script_name:
            environ["SCRIPT_NAME"] = script_name
            path_info = environ["PATH_INFO"]
            if path_info.startswith(script_name):
                environ["PATH_INFO"] = path_info[len(script_name) :]
        scheme = environ.get("HTTP_X_SCHEME", "") or self.scheme
        if scheme:
            environ["wsgi.url_scheme"] = scheme
        server = environ.get("HTTP_X_FORWARDED_SERVER", "") or self.server
        if server:
            environ["HTTP_HOST"] = server
        return self.app(environ, start_response)


def load_toml(file_path):
    """
        Chargement des fichier de type toml
    """
    try:
        return toml.load(file_path)
    except (TypeError, TomlDecodeError) as exp:
        sys.exit(
            "Unable to parse config file '{}' : {}".format(
                    file_path, exp
                )
            )


def loadConfig():
    """
        Chargement de la configuration
            si prod = fichiers
                - /etc/usershub.conf
                - /etc/geonature-db.conf
            si dev = fichier config/config.py

            Les fichiers sont chargés
                les uns après les autres et se surchagent
    """
    config = {}
    config_files = [
        "config/usershub.conf.default",
        "/etc/geonature/usershub.conf",
        "/etc/geonature/geonature-db.conf",
        "config/config.conf"
    ]
    for f in config_files:
        if os.path.isfile(f):
            config.update(load_toml(f))

    # Generation SQLALCHEMY_DATABASE_URI
    if 'SQLALCHEMY_DATABASE_URI' not in config:
        db_uri = "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}".format(  # noqa E501
            **config
        )
        config['SQLALCHEMY_DATABASE_URI'] = db_uri

    config['URL_REDIRECT'] = "{}/{}".format(config['URL_APPLICATION'], "login")

    return config

# Chargement de la config
CONF = loadConfig()

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

app.wsgi_app = ReverseProxied(app.wsgi_app, script_name=CONF['URL_APPLICATION'])

app.config.update(CONF)



app.secret_key = CONF['SECRET_KEY']

db.init_app(app)
# pass parameters to the usershub authenfication sub-module, DONT CHANGE THIS
app.config["DB"] = db

with app.app_context():
    app.jinja_env.globals["url_application"] = app.config["URL_APPLICATION"]

    if CONF['ACTIVATE_APP']:

        @app.route("/")
        def index():
            """ Route par défaut de l'application """
            return redirect(url_for("user.users"))

        @app.route("/constants.js")
        def constants_js():
            """ Route des constantes javascript """
            return render_template("constants.js")

        @app.after_request
        def after_login_method(response):
            """
                Fonction s'exécutant après chaque requete
                permet de gérer l'authentification
            """
            if not request.cookies.get("token"):
                session["current_user"] = None

            if request.endpoint == "auth.login" and response.status_code == 200:  # noqa
                current_user = json.loads(response.get_data().decode("utf-8"))
                session["current_user"] = current_user["user"]
            return response

        @app.context_processor
        def inject_user():
            return dict(user=getattr(g, "user", None))

        from pypnusershub import routes

        app.register_blueprint(routes.routes, url_prefix="/pypn/auth")

        from app.t_roles import route

        app.register_blueprint(route.route, url_prefix="/")

        from app.bib_organismes import route

        app.register_blueprint(route.route, url_prefix="/")

        from app.groupe import route

        app.register_blueprint(route.route, url_prefix="/")

        from app.liste import route

        app.register_blueprint(route.route, url_prefix="/")

        from app.t_applications import route

        app.register_blueprint(route.route, url_prefix="/")

        from app.t_profils import route

        app.register_blueprint(route.route, url_prefix="/")

        from app.login import route

        app.register_blueprint(route.route, url_prefix="/")

        from app.temp_users import routes

        app.register_blueprint(routes.routes, url_prefix="/temp_users")

        from app.api import route

        app.register_blueprint(route.route, url_prefix="/api")

    if CONF['ACTIVATE_API']:
        from app.api import route_register

        app.register_blueprint(route_register.route, url_prefix="/api_register")  # noqa


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=CONF['DEBUG'], port=CONF['PORT'])
