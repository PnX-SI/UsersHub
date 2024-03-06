import requests as req_lib
import logging

from flask import (
    Blueprint,
    request,
    render_template,
    current_app,
    redirect,
    url_for,
    flash,
    current_app,
)
from pypnusershub.db.models_register import TempUser
from pypnusershub import routes as fnauth

from app.env import db
from app.utils.utilssqlalchemy import json_resp
from app.models import TApplications


routes = Blueprint("temp_users", __name__)
log = logging.getLogger()


@routes.route("/list", methods=["GET"])
@fnauth.check_auth(6)
def temp_users_list():
    """
    Get all temp_users
    """
    data = db.session.query(TempUser).order_by("identifiant").all()
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


@routes.route("/validate/<token>/<int:id_application>", methods=["GET"])
@fnauth.check_auth(6)
def validate(token, id_application):
    """
    Call the API to validate a temp user
    """
    data_to_post = {"token": token, "id_application": id_application}

    # Get temp user infos
    temp_user = (
        db.session.query(TempUser.confirmation_url)
        .filter(token == TempUser.token_role)
        .first()
    )
    if not temp_user:
        return {"msg": "Aucun utilisateur trouvé avec le token user demandé"}, 404
    url_after_validation = temp_user[0]

    # Call temp user validation URL
    url_validate = (
        current_app.config["URL_APPLICATION"] + "/api_register/valid_temp_user"
    )
    r = req_lib.post(url=url_validate, json=data_to_post, cookies=request.cookies)
    if r.status_code != 200:
        flash("Erreur durant la validation de l'utilisateur temporaire", "error")
        return redirect(url_for("temp_users.temp_users_list"))
    elif not url_after_validation:
        flash("L'utilisateur a bien été validé")
        return redirect(url_for("temp_users.temp_users_list"))

    user_data = r.json()

    # Call post UsersHub actions URL
    if url_after_validation:
        r = req_lib.post(
            url=url_after_validation, json=user_data, cookies=request.cookies
        )
    if r.status_code == 200:
        flash("L'utilisateur a bien été validé")
        return redirect(url_for("temp_users.temp_users_list"))
    else:
        flash("Erreur durant l'appel des actions de l'application", "error")
        log.error("Error HTTP {} for {}".format(r.status_code, url_after_validation))
        return redirect(url_for("temp_users.temp_users_list"))


@routes.route("/delete/<token>", methods=["GET"])
@fnauth.check_auth(6)
def delete(token):
    """
    DELETE a temp_user
    """

    temp_user = db.session.query(TempUser).filter(TempUser.token_role == token).first()
    if temp_user:
        db.session.delete(temp_user)
        db.session.commit()
        flash("L'utilisateur a bien été supprimé")
        return redirect(url_for("temp_users.temp_users_list"))
    else:
        flash("Une erreur s'est produite", "error")
        return redirect(url_for("temp_users.temp_users_list"))
