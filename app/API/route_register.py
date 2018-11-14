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

import random

from config import config

from pypnusershub.db.models_register import TempUser, CorRoleToken

from datetime import datetime, timedelta

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

    return "authentification error", 401


@route.route("/test_connexion", methods=['GET'])
@fnauth.check_auth(5, False, '/api_register/role_check_auth_error')
def test_connexion():

    return "connexion ok"


@route.route("/create_temp_user", methods=['POST'])
@fnauth.check_auth(5, False, '/api_register/role_check_auth_error')
@json_resp
def create_temp_user():
    '''
        route pour creer un compte temporaire en attendait la confirmation de l'adresse mail
        les mot de passe seront stocké en crypté
        1. on stocke les variables qui seront utilisées par la création de compte
        2. on envoie un mail pour demander la confirmation du compte mail
    '''

    # recuperation des parametres
    data = request.get_json()

    temp_user = TempUser(**data)

    # verification des parametres
    (is_temp_user_valid, msg) = temp_user.is_valid()

    if not is_temp_user_valid:

        return msg, 412

    # on efface les comptes doublons
    db.session.query(TempUser).filter(TempUser.identifiant == temp_user.identifiant).delete()
    db.session.commit()

    # on efface les compte de plus de 24h
    db.session.query(TempUser).filter(TempUser.date_insert <= (datetime.now() - timedelta(days=1))).delete()
    db.session.commit()

    # verification si on a un utilisateur qui a le meme email et les memes droits

    user = db.session.query(TRoles).filter(TRoles.identifiant == temp_user.identifiant).first()

    if not user:

        # dans ce cas on cree un nouveau utilisateur
        temp_user.token_role = str(random.getrandbits(128))

        # encryption des mdp
        temp_user.encrypt_password(config.SECRET_KEY)

        # sauvegarde en base
        db.session.add(temp_user)
        db.session.commit()

        # envoie du mail de confirmation

        return {'token': temp_user.token_role}

    else:

        user_dict = user.as_dict(recursif=True)
        is_app_right = sum([user_app['id_application'] == config.ID_APP for user_app in user_dict.get('app_users', None)])

        if is_app_right:

            return "l'utilisateur l'identifiant " + user_dict['identifiant'] + "existe déjà", 422

        else:

            return "Un utilisateur avec l'identifiant existe déjà pour une autre application.", 422


@route.route('valid_temp_user', methods=['POST'])
@fnauth.check_auth(5, False, '/api_register/role_check_auth_error')
@json_resp
def valid_temp_user():
    '''
        route pour valider un compte temporire et en faire un utilisateur (requete a userbub)
    '''

    data_in = request.get_json()

    token = data_in['token']

    id_application = data_in['id_application']

    id_droit = data_in.get('id_droit', 1)

    # recherche de l'utilsateur temporaire correspondant au token
    temp_user = db.session.query(TempUser).filter(token == TempUser.token_role).first()

    if not temp_user:

        return "pas d'utilisateur avec le token user demandé", 422

    temp_user.decrypt_password(config.SECRET_KEY)

    req_data = temp_user.as_dict()

    # ici on ajoute le droit 1 par default (a voir si on fait passer ça en parametre)
    id_droit = 1

    req_data["applications"] = [
        {
            "id_app": id_application,
            "id_droit": id_droit
        }
    ]

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

    db.session.delete(temp_user)
    db.session.commit()

    return role.as_dict(recursif=True)


@route.route("/create_cor_role_token", methods=['POST'])
@fnauth.check_auth(5, False, '/api_register/role_check_auth_error')
@json_resp
def create_cor_role_token():

    data = request.get_json()

    id_role = data['id_role']

    token = str(random.getrandbits(128))

    # on efface les jeton précédent concernant cet id_role
    db.session.query(CorRoleToken).filter(CorRoleToken.id_role == id_role).delete()
    db.session.commit()

    # creation du jeton
    cor = CorRoleToken(**{'id_role': id_role, 'token': token})
    db.session.add(cor)
    db.session.commit()

    return {'token': token}


@route.route("/change_password", methods=['POST'])
@fnauth.check_auth(5, False, '/api_register/role_check_auth_error')
@json_resp
def change_password():

    data = request.get_json()

    token = data.get('token', None)

    if not token:

        return "token non defini dans paramètre POST", 500

    password = data.get('password', None)
    password_confirmation = data.get('password_confirmation', None)

    if not password_confirmation or not password:

        return "password non defini dans paramètres POST", 500

    if not password_confirmation == password:

        return "password et password_confirmation sont différents", 500

    res = db.session.query(CorRoleToken.id_role).filter(CorRoleToken.token == token).first()

    if not res:

        return "pas d'id role associée au token", 500

    id_role = res[0]

    role = db.session.query(TRoles).filter(TRoles.id_role == id_role).first()

    if not role:

        return "pas d'utilisateur correspondant à id_role", 500

    role.fill_password(password, password)
    db.session.commit()

    # delete cors
    db.session.query(CorRoleToken.id_role).filter(CorRoleToken.token == token).delete()
    db.session.commit()

    return role.as_dict()


@route.route('/add_application_right_to_role', methods=['POST'])
@fnauth.check_auth(5, False, '/api_register/role_check_auth_error')
@json_resp
def add_application_right_to_role():
    '''
        Route permettant de d'ajouter des droits pour une application a un utilisateur
    '''

    req_data = request.get_json()

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

        cor.id_droit = id_droit

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
