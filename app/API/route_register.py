"""
    Route permettant de manipuler les données de UsersHub via une API
"""

import re

from flask import (
    Blueprint, request
)

from app.env import db
from app.utils.utilssqlalchemy import json_resp
from app.models import (
    TRoles,
    CorRoleDroitApplication
)

from pypnusershub import routes as fnauth

from flask_cors import cross_origin

from config import config


route = Blueprint('api_register', __name__)


@route.route('/role/<id_role>', methods=['GET'])
@json_resp
def get_one_t_roles(id_role):
    '''
        Fonction qui retourne les données concernant un utilisateur
    '''
    role = TRoles.get_one(id_role)
    return role


# @route.route('/role_check_auth_error')
# def role_check_auth_error():

#     return "authentification error"


# @fnauth.check_auth(4, False, '/role_check_auth_error')

@route.route('/role', methods=['POST'])
@cross_origin(config.URLS_COR)
@json_resp
def insert_one_t_role():
    '''
        Route permettant de créer un utilisateur

        curl --header "Content-Type: application/json" \
        --request POST \
        --data '{"email": "a@test.fr", "groupe": false, "pn": true, "remarques": "utilisateur test api", "desc_role": null, "prenom_role": "test", "identifiant": "test_api", "id_unite": -1, "id_organisme": -1, "uuid_role": "c8f63c2d-e606-49c5-8865-edb0953c496f", "nom_role": "API", "password": "123456", "password_confirmation": "123456", "applications":[{"id_app":2, "id_droit":1}]}' \
        http://localhost:5001/api_register/role
    '''
    req_data = request.get_json()

    role_data = {}
    for att in req_data:
        if hasattr(TRoles, att):
            role_data[att] = req_data[att]

    # Validation email
    if re.search("[@.]", req_data['email']) is None:
        return "email not valid", 500

    role = TRoles(**role_data)

    if req_data['password']:
        role.fill_password(
            req_data['password'], req_data['password_confirmation']
        )

    db.session.add(role)
    db.session.commit()

    for app in req_data['applications']:
        cor = CorRoleDroitApplication(
            id_role=role.id_role,
            id_droit=app['id_droit'],
            id_application=app['id_app']
        )
        db.session.add(cor)
        db.session.commit()

    return role.as_dict(recursif=True)
