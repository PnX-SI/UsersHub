from flask import current_app, Response, request, redirect
from urllib.parse import urlencode


# Unauthorized means disconnected
# (logged but not allowed to perform an action = Forbidden)


def handle_unauthenticated_request():
    """
    To avoid returning the login page html indicated in `routes_with_no_redirect_login`
    this function override `LoginManager.unauthorized()` from `flask-login` .

    Returns
    -------
    flask.Response
        response
    """
    routes_with_no_redirect_login = [
        "create_cor_role_token",
        "test_connexion",
    ]
    in_request = [
        route
        for route in routes_with_no_redirect_login
        if route in request.url_rule.rule
    ]
    if len(in_request):
        return Response(response={}, status=401)
    else:
        url_redirect = current_app.config["URL_REDIRECT"]
        query_string = urlencode({"next": request.url})
        return redirect(f"{url_redirect}?{query_string}")
