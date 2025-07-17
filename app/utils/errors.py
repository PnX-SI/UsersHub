import re
import logging
from flask import current_app, flash, Response, request, json, redirect, url_for
from urllib.parse import urlencode
from werkzeug.exceptions import Unauthorized, HTTPException
from sqlalchemy.exc import IntegrityError

# Unauthorized means disconnected
# (logged but not allowed to perform an action = Forbidden)
log = logging.getLogger(__name__)


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


def handle_integrity_error(e):
    db = current_app.config.get("DB")
    if db:
        db.session.rollback()
    action = {
        "GET": "l'affichage",
        "POST": "la création",
        "PUT": "la mise à jour",
        "PATCH": "la mise à jour",
        "DELETE": "la suppression",
    }.get(request.method, "le traitement")
    if "delete" in (request.url_rule.rule or "") or request.endpoint.endswith("delete"):
        action = "la suppression"
    msg = str(e.orig)
    m = re.search(r"DETAIL:\s*(.*)", msg, re.IGNORECASE)
    if m:
        detail = m.group(1)
        flash(
            f"Cet élément ne peut pas être modifié lors de {action} : {detail}", "error"
        )
    else:
        flash(f"Une erreur est survenue lors de {action} de cet élément.", "error")

    log.error(f"IntegrityError pendant {action} : {msg}", exc_info=True)
    target = request.referrer or url_for("user.users")

    return redirect(target)


def handle_general_exception(e):
    if isinstance(e, HTTPException):
        return e
    flash("Une erreur inattendue est survenue.", "error")
    log.error(f"Exception inattendue : {e}", exc_info=True)
    target = request.referrer or url_for("user.users")

    return redirect(target)
