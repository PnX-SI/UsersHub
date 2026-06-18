import json
import logging
import re
import time
import uuid
from time import perf_counter

from flask import g, has_request_context, request
from flask_login import current_user
from sqlalchemy import event


log = logging.getLogger("usershub.observability")
slow_sql_log = logging.getLogger("usershub.sql.slow")
slow_request_log = logging.getLogger("usershub.request.slow")
error_request_log = logging.getLogger("usershub.request.error")

_SPACE_RE = re.compile(r"\s+")
_REQUEST_OBSERVABILITY_FIELDS = (
    "rendered_object_count",
    "rendered_object_label",
    "list_fetch_duration_ms",
    "list_prepare_duration_ms",
    "list_total_count",
    "list_filtered_count",
    "users_list_fetch_duration_ms",
    "users_list_prepare_duration_ms",
    "users_list_total_count",
    "users_list_filtered_count",
    "users_list_status_filter",
)


def _normalize_sql(statement):
    return _SPACE_RE.sub(" ", statement).strip()


def _get_user_id():
    if not has_request_context():
        return None
    try:
        if current_user and current_user.is_authenticated:
            return getattr(current_user, "id_role", None)
    except Exception:
        return None
    return None


def get_request_log_context():
    if not has_request_context():
        return {}
    return {
        "request_id": getattr(g, "request_id", None),
        "method": request.method,
        "path": request.path,
        "endpoint": request.endpoint,
        "route": getattr(request.url_rule, "rule", None),
        "user_id": _get_user_id(),
        "query_args": request.args.to_dict(flat=False),
    }


def get_request_duration_ms():
    if not has_request_context():
        return None
    started_at = getattr(g, "request_started_at", None)
    if started_at is None:
        return None
    return int((perf_counter() - started_at) * 1000)


def set_request_observability_fields(**fields):
    if not has_request_context():
        return
    for key, value in fields.items():
        setattr(g, key, value)


def _get_request_metrics_payload():
    if not has_request_context():
        return {}
    return {field: getattr(g, field, None) for field in _REQUEST_OBSERVABILITY_FIELDS}


def register_request_logging(app):
    app.config.setdefault("ENABLE_REQUEST_LOGGING", False)
    app.config.setdefault("ENABLE_SLOW_REQUEST_LOGGING", False)
    app.config.setdefault("SLOW_REQUEST_THRESHOLDS_MS", (500, 1000, 3000))
    app.config.setdefault("ENABLE_REQUEST_ERROR_LOGGING", False)

    @app.before_request
    def _before_request():
        g.request_started_at = perf_counter()
        g.request_started_epoch = time.time()
        g.request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex

    @app.after_request
    def _after_request(response):
        duration_ms = get_request_duration_ms()
        if duration_ms is None:
            duration_ms = 0
        response.headers["X-Request-ID"] = g.request_id

        if app.config["ENABLE_REQUEST_LOGGING"]:
            payload = get_request_log_context()
            payload.update(
                {
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                    "content_length": response.calculate_content_length(),
                }
            )
            payload.update(_get_request_metrics_payload())
            log.info("request_completed %s", json.dumps(payload, default=str, ensure_ascii=True))

        if app.config["ENABLE_SLOW_REQUEST_LOGGING"]:
            thresholds = sorted(app.config["SLOW_REQUEST_THRESHOLDS_MS"])
            slow_threshold = max(
                (threshold for threshold in thresholds if duration_ms >= threshold),
                default=None,
            )
            if slow_threshold is not None:
                payload = get_request_log_context()
                payload.update(
                    {
                        "status_code": response.status_code,
                        "duration_ms": duration_ms,
                        "content_length": response.calculate_content_length(),
                        "slow_threshold_ms": slow_threshold,
                    }
                )
                payload.update(_get_request_metrics_payload())
                slow_request_log.warning(
                    "slow_request %s", json.dumps(payload, default=str, ensure_ascii=True)
                )

        return response

    @app.teardown_request
    def _teardown_request(exc):
        if exc is None or not app.config["ENABLE_REQUEST_ERROR_LOGGING"]:
            return

        duration_ms = get_request_duration_ms()
        payload = get_request_log_context()
        payload.update({"duration_ms": duration_ms})
        error_request_log.exception(
            "request_failed %s",
            json.dumps(payload, default=str, ensure_ascii=True),
            exc_info=exc,
        )


def register_slow_sql_logging(app, engine):
    app.config.setdefault("ENABLE_SLOW_SQL_LOGGING", False)
    app.config.setdefault("SLOW_SQL_THRESHOLD_MS", 200)
    app.config.setdefault("SLOW_SQL_MAX_LENGTH", 1200)

    if not app.config["ENABLE_SLOW_SQL_LOGGING"]:
        return

    if getattr(engine, "_usershub_slow_sql_registered", False):
        return

    @event.listens_for(engine, "before_cursor_execute")
    def _before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault("query_start_time", []).append(perf_counter())

    @event.listens_for(engine, "after_cursor_execute")
    def _after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        start_times = conn.info.get("query_start_time", None)
        if not start_times:
            return
        duration_ms = int((perf_counter() - start_times.pop()) * 1000)
        if duration_ms < app.config["SLOW_SQL_THRESHOLD_MS"]:
            return

        normalized_sql = _normalize_sql(statement)
        max_length = app.config["SLOW_SQL_MAX_LENGTH"]
        if len(normalized_sql) > max_length:
            normalized_sql = normalized_sql[: max_length - 3] + "..."

        payload = {
            "duration_ms": duration_ms,
            "rowcount": cursor.rowcount,
            "statement": normalized_sql,
            "executemany": executemany,
        }
        if has_request_context():
            payload.update(get_request_log_context())

        slow_sql_log.warning(
            "slow_sql %s", json.dumps(payload, default=str, ensure_ascii=True)
        )

    engine._usershub_slow_sql_registered = True
