from flask import current_app, Response, request, redirect, url_for
from urllib.parse import urlencode
from werkzeug.exceptions import Unauthorized


# Unauthorized means disconnected
# (logged but not allowed to perform an action = Forbidden)


def handle_unauthenticated_request():
    """
    To avoid returning the login page html when a route is used by geonature API
    this function overrides `LoginManager.unauthorized()` from `flask-login` .

    Returns
    -------
    flask.Response
        response
    """
    if "application/json" in request.headers.get("Content-Type", ""):
        raise Unauthorized
    else:
        return redirect(url_for("login.login", next=request.path))
