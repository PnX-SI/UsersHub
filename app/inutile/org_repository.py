from flask import current_app,Blueprint, jsonify
from app.env import db
from app.models import TRoles
from app.models import Bib_Organismes



def getAll():
    q = db.session.query(Bib_Organismes)
    return [organisme.as_dict() for organisme in q.all()]


# def choixOrgquery():
#     q = Bib_Organismes.query
#     print (q)
#     return q
    
    

def choixOrg():
        org = getAll()
        choices = []
        for o in org :
            choices.append((o['id_organisme'], o['nom_organisme']))
        return choices