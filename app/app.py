"""
Serveur de l'application UsersHub
"""

import os
import sys
import json
import logging
from pkg_resources import iter_entry_points
from urllib.parse import urlsplit, urlencode
from pathlib import Path

from flask import (
    Flask,
    Response,
    redirect,
    url_for,
    request,
    session,
    render_template,
    g,
)
from werkzeug.middleware.proxy_fix import ProxyFix
from sqlalchemy.exc import ProgrammingError
from flask_migrate import Migrate

from app.env import db

from pypnusershub.db.models import Application
from app.utils.errors import handle_unauthenticated_request
from pypnusershub.auth import auth_manager
from pathlib import Path
import importlib.metadata

migrate = Migrate()


@migrate.configure
def configure_alembic(alembic_config):
    """
    This function add to the 'version_locations' parameter of the alembic config the
    'migrations' entry point value of the 'gn_module' group for all modules having such entry point.
    Thus, alembic will find migrations of all installed geonature modules.
    """
    version_locations = alembic_config.get_main_option(
        "version_locations", default=""
    ).split()
    for entry_point in iter_entry_points("alembic", "migrations"):
        _, migrations = str(entry_point).split("=", 1)
        version_locations += [migrations.strip()]
    alembic_config.set_main_option("version_locations", " ".join(version_locations))
    return alembic_config


def create_app():
    app = Flask(
        __name__, static_folder=os.environ.get("USERSHUB_STATIC_FOLDER", "static")
    )
    app.config.from_pyfile(os.environ.get("USERSHUB_SETTINGS", "../config/config.py"))
    app.config.from_prefixed_env(prefix="USERSHUB")
    app.config["APPLICATION_ROOT"] = urlsplit(app.config["URL_APPLICATION"]).path or "/"
    if "SCRIPT_NAME" not in os.environ and app.config["APPLICATION_ROOT"] != "/":
        os.environ["SCRIPT_NAME"] = app.config["APPLICATION_ROOT"]
    app.config["URL_REDIRECT"] = "{}/{}".format(app.config["URL_APPLICATION"], "login")
    app.secret_key = app.config["SECRET_KEY"]
    app.config["VERSION"] = importlib.metadata.version("usershub")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_host=1)
    db.init_app(app)
    app.config["DB"] = db
    providers_config = [
        {
            "module": "pypnusershub.auth.providers.default.LocalProvider",
            "id_provider": "local_provider",
        },
    ]
    auth_manager.init_app(
        app, prefix="/pypn/auth/", providers_declaration=providers_config
    )
    auth_manager.home_page = app.config["URL_APPLICATION"]

    migrate.init_app(app, db, directory=Path(__file__).absolute().parent / "migrations")

    if "CODE_APPLICATION" not in app.config:
        app.config["CODE_APPLICATION"] = "UH"

    with app.app_context():
        app.jinja_env.globals["url_application"] = app.config["URL_APPLICATION"]

        if app.config["ACTIVATE_APP"]:

            @app.route("/")
            def index():
                """Route par défaut de l'application"""
                return redirect(url_for("user.users"))

            @app.route("/constants.js")
            def constants_js():
                """Route des constantes javascript"""
                return render_template("constants.js")

            @app.context_processor
            def inject_user():
                return dict(user=getattr(g, "user", None))

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

        if app.config["ACTIVATE_API"]:
            from app.api import route_register

            app.register_blueprint(
                route_register.route, url_prefix="/api_register"
            )  # noqa

        app.login_manager.unauthorized_handler(handle_unauthenticated_request)

    return app
