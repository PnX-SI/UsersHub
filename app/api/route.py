from flask import Blueprint, request

from app.env import db
from app.utils.utilssqlalchemy import json_resp
from app.models import TProfils, CorProfilForApp, Bib_Organismes


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


@route.route("/organisms/autocomplete", methods=["GET"])
@json_resp
def autocomplete_organisms():
    """
    Return organism suggestions for form autocomplete.
    """
    search_value = request.args.get("q", "").strip()
    limit = min(max(request.args.get("limit", default=10, type=int), 1), 25)

    q = db.session.query(
        Bib_Organismes.id_organisme,
        Bib_Organismes.nom_organisme,
        Bib_Organismes.ville_organisme,
    )
    if search_value:
        pattern = f"%{search_value}%"
        q = q.filter(Bib_Organismes.nom_organisme.ilike(pattern))

    q = q.order_by(Bib_Organismes.nom_organisme.asc(), Bib_Organismes.id_organisme.asc())

    data = []
    for organism in q.limit(limit).all():
        label = organism.nom_organisme or f"Organisme #{organism.id_organisme}"
        if organism.ville_organisme:
            label = f"{label} ({organism.ville_organisme})"
        data.append(
            {
                "id_organisme": organism.id_organisme,
                "nom_organisme": organism.nom_organisme or "",
                "label": label,
            }
        )
    return data
