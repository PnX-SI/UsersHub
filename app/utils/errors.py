import logging
import json
import re

from flask import current_app, jsonify, request, redirect, url_for, flash, g
from werkzeug.exceptions import Unauthorized, HTTPException

from app.observability import get_request_duration_ms, get_request_log_context

# Unauthorized means disconnected
# (logged but not allowed to perform an action = Forbidden)

log = logging.getLogger(__name__)
JSON_API_PATH_PREFIXES = ("/api/", "/api_register/", "/pypn/auth/")
ACTION_LABELS = {
    "GET": "l'affichage",
    "POST": "la creation",
    "PUT": "la mise a jour",
    "PATCH": "la mise a jour",
    "DELETE": "la suppression",
}


def wants_json_response():
    content_type = request.headers.get("Content-Type", "")
    accept = request.headers.get("Accept", "")
    return (
        "application/json" in content_type
        or "application/json" in accept
        or request.path.startswith(JSON_API_PATH_PREFIXES)
    )


def _rollback_session():
    db = current_app.config.get("DB")
    if db:
        db.session.rollback()


def _get_request_id():
    return getattr(g, "request_id", None)


def _build_action_label():
    action = ACTION_LABELS.get(request.method, "le traitement")
    rule = getattr(request.url_rule, "rule", "") or ""
    endpoint = request.endpoint or ""
    if "delete" in rule or endpoint.endswith("delete") or endpoint.endswith("deluser"):
        action = "la suppression"
    return action


def _extract_integrity_detail(exc):
    msg = str(getattr(exc, "orig", exc))
    detail_match = re.search(r"DETAIL:\s*(.*)", msg, re.IGNORECASE)
    if detail_match:
        return detail_match.group(1)
    return msg


def _html_error_redirect(message):
    flash(message, "error")
    return redirect(request.referrer or url_for("user.users"))


def _json_error_response(message, status_code):
    return jsonify({"message": message}), status_code


def _append_request_id(message, request_id):
    if not request_id:
        return message
    return f"{message} Request ID: {request_id}"


def _log_error(event_name, exc, detail=None):
    payload = get_request_log_context()
    payload.update(
        {
            "duration_ms": get_request_duration_ms(),
        }
    )
    if detail:
        payload["detail"] = detail
    log.error(
        "%s %s",
        event_name,
        json.dumps(payload, default=str, ensure_ascii=True),
        exc_info=exc,
    )


def _build_error_response(event_name, exc, message, status_code=500, detail=None):
    request_id = _get_request_id()
    _log_error(event_name, exc, detail=detail)
    if wants_json_response():
        return _json_error_response(message, status_code)
    return _html_error_redirect(_append_request_id(message, request_id))


def handle_unauthenticated_request():
    """
    To avoid returning the login page html when a route is used by geonature API
    this function overrides `LoginManager.unauthorized()` from `flask-login` .

    Returns
    -------
    flask.Response
        response
    """
    if wants_json_response():
        raise Unauthorized
    return redirect(url_for("login.login", next=request.path))


def handle_integrity_error(exc):
    _rollback_session()
    action = _build_action_label()
    detail = _extract_integrity_detail(exc)
    message = f"Operation impossible lors de {action}."
    if detail:
        message = f"{message} {detail}"
    return _build_error_response("integrity_error", exc, message, detail=detail)


def handle_sqlalchemy_error(exc):
    _rollback_session()
    action = _build_action_label()
    message = f"Erreur base de donnees lors de {action}."
    return _build_error_response("sqlalchemy_error", exc, message)


def handle_general_exception(exc):
    if isinstance(exc, HTTPException):
        return exc

    _rollback_session()
    action = _build_action_label()
    message = f"Une erreur inattendue est survenue lors de {action}."
    return _build_error_response("unexpected_error", exc, message)
