"""
    Route permettant de manipuler les données de UsersHub via une API
"""
import hashlib

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

from config import config


route = Blueprint('api_register', __name__)


@route.route('/role/<id_role>', methods=['GET'])
@fnauth.check_auth(1, False, '/api_register/role_check_auth_error')
@json_resp
def get_one_t_roles(id_role):
    '''
        Fonction qui retourne les données concernant un utilisateur
    '''
    role = TRoles.get_one(id_role)
    return 1
    return role


@route.route('/role_check_auth_error')
def role_check_auth_error():

    return "authentification error"


@route.route("/change_password", methods=['POST'])
@fnauth.check_auth(5, False, '/api_register/role_check_auth_error')
@json_resp
def change_password():



    data = request.get_json()

    id_role = data.get('id_role', None)

    password = data.get('password', None)

    if not id_role:

        return 'id_role non renseigné', 500

    if not password:

        return 'password non renseigné', 500

    role = db.session.query(TRoles).filter(TRoles.id_role == id_role).first()

    if not role:

        return "pas d'utilisateur correspondant à id_role", 500

    role.fill_password(password, password)

    db.session.commit()

    return id_role


@route.route('/add_application_right_to_role', methods=['POST'])
@fnauth.check_auth(5, False, '/api_register/role_check_auth_error')
@json_resp
def add_application_right_to_role():
    '''
        Route permettant de d'ajouter des droits pour une application a un utilisateur
    '''

    req_data = request.get_json()

    print(req_data)

    identifiant = req_data.get('login', None)
    pwd = req_data.get('password', None)

    id_application = req_data.get('id_application', None)
    id_droit = req_data.get('id_droit', 1)

    if not identifiant or not pwd or not id_application or not id_droit:

        return "les parametres sont mal renseignés", 500

    role = db.session.query(TRoles).filter(TRoles.identifiant == identifiant).first()

    if not role:

        return "pas d'user pour l'identifiant " + str(identifiant), 500

    id_role = role.id_role

    # check pwd

    pwd_hash = hashlib.md5(pwd.encode('utf-8')).hexdigest()

    if not role.pass_md5 == pwd_hash:

        return "password false", 500

    # on regarder les droits que possede cet utilisateur
    cor = db.session.query(CorRoleDroitApplication).filter(
        id_role == CorRoleDroitApplication.id_role).filter(
        id_application == CorRoleDroitApplication.id_application).first()

    # si pas de droit pour cette application on ajoute
    if not cor:

        cor = CorRoleDroitApplication(
            id_role=role.id_role,
            id_droit=id_droit,
            id_application=id_application
        )
        db.session.add(cor)
        db.session.commit()

    # sinon on update avec les nouveaux droits

    else:

        cor.id_droit=id_droit

        db.session.commit()


    return role.as_dict(recursif=True)



@route.route('/role', methods=['POST'])
@fnauth.check_auth(5, False, '/api_register/role_check_auth_error')
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
