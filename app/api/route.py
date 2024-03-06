from flask import Blueprint, request


from app.env import db
from app.utils.utilssqlalchemy import json_resp
from app.models import TProfils, CorProfilForApp


route = Blueprint("api", __name__)


@route.route("/profils", methods=["GET"])
@json_resp
def get_profils():
    """
    Return the profils
    """
    params = request.args
    q = db.session.query(TProfils)
    if "id_application" in params:
        q = q.join(
            CorProfilForApp, CorProfilForApp.id_profil == TProfils.id_profil
        ).filter(CorProfilForApp.id_application == params["id_application"])
    data = [data.as_dict(columns=["id_profil", "nom_profil"]) for data in q.all()]
    return data
