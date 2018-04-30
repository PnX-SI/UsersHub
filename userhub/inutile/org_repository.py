from flask import current_app,Blueprint, jsonify
from userhub.env import db
from userhub.models import TRoles
from userhub.models import Bib_Organismes



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