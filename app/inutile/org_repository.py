from flask import current_app,Blueprint, jsonify
from app.env import db
from app.models import TRoles, Bib_Organismes


def getAll():
    q = db.session.query(Bib_Organismes)
    return [organisme.as_dict() for organisme in q.all()]


def choixOrg():
        
    return [o['id_organisme'], o['nom_organisme'] for o in getAll()]