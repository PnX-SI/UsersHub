import requests as req_lib

from flask import (
    Blueprint,
    request,
    render_template,
    current_app,
    redirect,
    url_for,
    flash,
)
from pypnusershub.db.models_register import TempUser
from pypnusershub import routes as fnauth

from app.env import db, URL_REDIRECT
from app.utils.utilssqlalchemy import json_resp
from app.models import TApplications


routes = Blueprint("temp_users", __name__)


@routes.route("/list", methods=["GET"])
@fnauth.check_auth(6, False, URL_REDIRECT)
def temp_users_list():
    """
    Get all temp_users
    """
    data = db.session.query(TempUser).all()
    temp_users = []
    for d in data:
        temp_user = d.as_dict()
        temp_user["full_name"] = temp_user["nom_role"] + " " + temp_user["prenom_role"]
        app = db.session.query(TApplications).get(temp_user["id_application"])
        temp_user["app_name"] = None
        if app:
            temp_user["app_name"] = app.nom_application
        temp_users.append(temp_user)
    columns = [
        {"key": "identifiant", "label": "Login"},
        {"key": "full_name", "label": "Nom - Prénom"},
        {"key": "email", "label": "Email"},
        {"key": "app_name", "label": "Application"},
        {"key": "champs_addi", "label": "Autres"},
    ]
    return render_template("temp_users.html", data=temp_users, columns=columns)


@routes.route("/validate", methods=["POST"])
@fnauth.check_auth(6, False, URL_REDIRECT)
@json_resp
def validate():
    """
    Call the API to validate a temp user
    return an URL to redirect, managed by frontend
    """
    data_posted = request.get_json()
    url_validate = (
        current_app.config["URL_APPLICATION"] + "/api_register/valid_temp_user"
    )
    r = req_lib.post(url=url_validate, json=data_posted, cookies=request.cookies)
    if r.status_code == 200:
        flash("L'utilisateur a bien été validé")
        return {"url_redirect": url_for("temp_users.temp_users_list")}, 200
    else:
        flash("Une erreur s'est produite", "error")
        return {"url_redirect": url_for("temp_users.temp_users_list")}, 500
