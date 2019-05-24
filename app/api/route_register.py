"""
    Route permettant de manipuler les données de UsersHub via une API
"""
from datetime import datetime, timedelta

import hashlib
import random
import re


from flask import (
    Blueprint, request
)
from app.env import db
from app.utils.utilssqlalchemy import json_resp
from app.models import (
    TRoles,
    CorRoleAppProfil,
    TProfils,
    CorRoles
)
from config import config

from pypnusershub import routes as fnauth

from pypnusershub.db.models_register import TempUser, CorRoleToken

route = Blueprint('api_register', __name__)

@route.route('/role/<id_role>', methods=['GET', 'POST'])
@fnauth.check_auth(1, False, '/api_register/role_check_auth_error')
@json_resp
def get_one_t_roles(id_role):
    '''
        Fonction qui retourne les données concernant un utilisateur
    '''
    role = TRoles.get_one(id_role)

    return role


@route.route("/test_connexion", methods=['GET', 'POST'])
@fnauth.check_auth(1)
@json_resp
def test_connexion():
    '''
        route pour tester la connexion
    '''
    return {'msg': "connexion ok"}


@route.route("/create_temp_user", methods=['POST'])
@fnauth.check_auth(5)
@json_resp
def create_temp_user():
    '''
        route pour creer un compte temporaire en attendait
        la confirmation de l'adresse mail
        les mots de passe seront stocké en crypté

        1. on stocke les variables qui seront
            utilisées par la création de compte
        2. on envoie un mail pour demander la confirmation du compte mail
    '''

    # recuperation des parametres
    data = request.get_json()

    # recuperation et verif de l'url de confirmation
    # @REM : Non necessaire si l'envoie de mail est géré par une autre application
    url_confirmation = data.get('url_confirmation', None)
    if url_confirmation is None:
        return {"msg": "Erreur server parameters url_confirmation is required"}, 500

    # filtre des données correspondant à un role

    role_data = {}
    for att in data:
        if hasattr(TempUser, att):
            role_data[att] = data[att]

    temp_user = TempUser(**role_data)

    # verification des parametres
    (is_temp_user_valid, msg) = temp_user.is_valid()

    if not is_temp_user_valid:

        return {'msg': msg}, 400

    # on efface les comptes doublons
    db.session.query(
        TempUser
    ).filter(
        TempUser.identifiant == temp_user.identifiant
        ).delete()
    db.session.commit()

    # on efface les compte de plus de 168h
    db.session.query(
        TempUser
    ).filter(
        TempUser.date_insert <= (datetime.now() - timedelta(days=7))
    ).delete()
    db.session.commit()

    # verification si on a un utilisateur
    # qui a le meme email et les memes droits

    user = db.session.query(
        TRoles
    ).filter(
        TRoles.identifiant == temp_user.identifiant
    ).first()

    if not user:

        # dans ce cas on cree un nouveau utilisateur
        temp_user.token_role = str(random.getrandbits(128))

        # encryption des mdp
        temp_user.encrypt_password(config.SECRET_KEY)

        # sauvegarde en base
        db.session.add(temp_user)
        db.session.commit()

        return {
            'token': temp_user.token_role
        }, 200

    return {'msg': "Un utilisateur avec l'identifiant existe déjà."}, 422


@route.route('valid_temp_user', methods=['POST'])
@fnauth.check_auth(5)
@json_resp
def valid_temp_user():
    '''
        route pour valider un compte temporaire
        et en faire un utilisateur (requete a usershub)
    '''

    data_in = request.get_json()

    token = data_in['token']
    id_application = data_in['id_application']

    # recherche de l'utilisateur temporaire correspondant au token
    temp_user = db.session.query(
        TempUser
    ).filter(
        token == TempUser.token_role
    ).first()

    if not temp_user:
        return {
            "msg": "pas d'utilisateur trouvé avec le token user demandé"
        }, 422

    temp_user.decrypt_password(config.SECRET_KEY)
    req_data = temp_user.as_dict()

    # Récupération du groupe par défaut
    id_grp = CorRoleAppProfil.get_default_for_app(id_application)
    if not id_grp:
        return {"msg": "pas de groupe par défaut pour l'application"}, 500

    role_data = {"active": True}
    for att in req_data:
        if hasattr(TRoles, att):
            #Patch pas beau pour corriger le db.Unicode de TRole pour id_organisme
            if att == 'id_organisme' and req_data[att] == 'None':
                role_data[att] = None
            else:
                role_data[att] = req_data[att]

    # Validation email
    if re.search("[@.]", req_data['email']) is None:
        return {"msg": "email not valid"}, 500

    role = TRoles(**role_data)

    if req_data['password']:
        role.fill_password(
            req_data['password'], req_data['password_confirmation']
        )

    db.session.add(role)
    db.session.commit()

    # Ajout du role au profil
    cor = CorRoles(
        id_role_groupe=id_grp.id_role,
        id_role_utilisateur=role.id_role
    )
    db.session.add(cor)

    db.session.delete(temp_user)
    db.session.commit()

    return role.as_dict(recursif=True)


def set_cor_role_token(email):
    '''
        fonction pour la creation d'un token associé a un id_role
        parametres : email
    '''
    if not email:
        return {'msg': "Aucun email"}, 404

    role = db.session.query(TRoles).filter(email == TRoles.email).first()

    if not role:
        return {'msg': "Pas de role trouvé pour l'email : " + email}, 400

    id_role = role.id_role

    token = str(random.getrandbits(128))

    # on efface les jeton précédent concernant cet id_role
    db.session.query(CorRoleToken).filter(
        CorRoleToken.id_role == id_role
    ).delete()
    db.session.commit()

    # creation du jeton
    cor = CorRoleToken(**{'id_role': id_role, 'token': token})
    db.session.add(cor)
    db.session.commit()

    return {'token': token, 'id_role': id_role}

def check_token(token):
    '''
        fonction permettant de vérifier la présence
        d'un token et qui retourne l'id_role associé
    '''
    res = db.session.query(
        CorRoleToken.id_role
    ).filter(CorRoleToken.token == token).first()

    if not res:
        return False
    return res

@route.route("/create_cor_role_token", methods=['POST'])
@fnauth.check_auth(5)
@json_resp
def create_cor_role_token():
    '''
        route pour la creation d'un token associé a un id_role
        fait un appel de la fonction set_cor_role_token(email)
        parametres post : email
    '''

    data = request.get_json()

    email = data['email']

    return set_cor_role_token(email)


@route.route("/change_password", methods=['POST'])
@fnauth.check_auth(5)
@json_resp
def change_password():
    '''
        Route permettant à un utilisateur de renouveller
        son mot de passe
    '''
    data = request.get_json()

    token = data.get('token', None)

    if not token:

        return {"msg": "token non defini dans paramètre POST"}, 500

    password = data.get('password', None)
    password_confirmation = data.get('password_confirmation', None)

    if not password_confirmation or not password:

        return {"msg": "password non defini dans paramètres POST"}, 500

    if not password_confirmation == password:

        return {
            "msg": "password et password_confirmation sont différents"
        }, 500

    associated_id_role = check_token(token)
    if not associated_id_role:

        return {"msg": "pas d'id role associée au token"}, 500

    id_role = associated_id_role[0]

    role = db.session.query(TRoles).filter(TRoles.id_role == id_role).first()

    if not role:

        return {"msg": "pas d'utilisateur correspondant à id_role"}, 500

    role.fill_password(password, password)
    db.session.commit()

    # delete cors
    db.session.query(
        CorRoleToken.id_role
    ).filter(CorRoleToken.token == token).delete()
    db.session.commit()

    return role.as_dict()


@route.route('/change_application_right', methods=['POST'])
@fnauth.check_auth(5)
@json_resp
def change_application_right():
    '''
        Change les droits d'un utilisateur pour une application
    '''

    req_data = request.get_json()

    id_application = req_data.get('id_application', None)

    # Test assurant une rétrocompatibilité (à l'époque des niveaux de droits)
    if req_data.get('id_droit', None):
        code_profil = req_data.get('id_droit', None)
    else:
        code_profil = req_data.get('id_profil', None)

    # Récupération de l'identifiant du profil à partir de son code
    profil = TProfils.get_profil_in_app_with_code(
        id_application, str(code_profil)
    )
    if not profil:
        return {
            "msg": "pas de profil " + str(code_profil) + "corespondant pour l'application"  # noqa
        }, 500

    id_profil = profil.id_profil

    id_role = req_data.get('id_role', None)

    role = db.session.query(TRoles).filter(TRoles.id_role == id_role).first()

    if not id_application or not id_role or not code_profil:
        return {'msg': 'Problème de paramètres POST'}, 400

    cor = db.session.query(
        CorRoleAppProfil
    ).filter(
        id_role == CorRoleAppProfil.id_role
    ).filter(
        id_application == CorRoleAppProfil.id_application
    ).first()

    if not cor:
        cor = CorRoleAppProfil(**{
            "id_role": id_role,
            "id_application": id_application,
            "id_profil": id_profil
        })
    else:
        cor.id_profil = id_profil

    db.session.commit()

    return {
        'id_role': id_role,
        'id_profil': code_profil,
        'id_droit': code_profil,  # Retrocompatiblité pour l'OEASC
        'id_application': id_application,
        "role": role.as_dict()
    }


@route.route('/add_application_right_to_role', methods=['POST'])
@fnauth.check_auth(5)
@json_resp
def add_application_right_to_role():
    '''
        Route permettant de d'ajouter des droits
        pour une application a un utilisateur
        soit en l'associant à un groupe
        soit en lui affectant le profil "1"
    '''

    req_data = request.get_json()

    identifiant = req_data.get('login', None)
    pwd = req_data.get('password', None)

    id_application = req_data.get('id_application', None)

    if not identifiant or not pwd or not id_application:
        return {"msg": "les parametres sont mal renseignés"}, 500

    # Récupération du groupe par défaut
    id_grp = CorRoleAppProfil.get_default_for_app(id_application)
    if not id_grp:
        return {"msg": "pas de groupe par défaut pour l'application"}, 500

    role = db.session.query(TRoles).filter(
        TRoles.identifiant == identifiant
    ).first()

    if not role:
        return {
            "msg": "pas d'user pour l'identifiant " + str(identifiant)
        }, 500

    id_role = role.id_role

    # check pwd
    pwd_hash = hashlib.md5(pwd.encode('utf-8')).hexdigest()

    if not role.pass_md5 == pwd_hash:

        return {"msg": "password false"}, 500

    # Test si l'utilisateur n'est pas déjà associé au groupe
    # par défaut
    if not CorRoles.test_role_in_grp(id_role, id_grp.id_role):
        cor = CorRoles(
            id_role_groupe=id_grp.id_role,
            id_role_utilisateur=role.id_role
        )
        db.session.add(cor)
        db.session.commit()

    return role.as_dict(recursif=True)


@route.route('/login_recovery', methods=['POST'])
@fnauth.check_auth(5)
@json_resp
def login_recovery():
    '''
        route pour changer des paramètres d'utilisateur
        FIXME : Route qui ne modifie rien du tout
            devrait peut être transformée pour être plus générique
            et retourner les informations d'un utilisateur donné
    '''
    req_data = request.get_json()

    email = req_data.get('email', None)

    if not email:
        return {'msg': "Pas d'email"}, 400

    count = db.session.query(TRoles).filter_by(email=email).count()

    if count == 0:
        return {"msg": "Adresse mail inconnue"}, 404
    if count > 1:
        return {"msg": "Plusieurs identifiants correspondent à cette adresse, veuillez contacter l'administrateur"}, 404 # noqa

    user = db.session.query(TRoles).filter_by(email=email).one()

    # FIXME changer le retour de la fonction
    return {"msg": "Un mail avec votre identifiant vient d'être envoyé sur l'adresse %s" % email}, 200


@route.route('/password_recovery', methods=['POST'])
@fnauth.check_auth(5)
@json_resp
def password_recovery():
    '''
        route pour changer des paramètres d'utilisateur
        FIXME route une fois vidée de sa fonctionnalité d'envoie de mail
            est en doublon avec create_cor_role_token (pour qui
            il manque des tests)
    '''
    req_data = request.get_json()

    email = req_data.get('email', None)
    #recuperation et verif de l'url de confirmation
    url_confirmation = req_data.get('url_confirmation', None)

    if not email:
        return {'msg': "Pas d'email"}, 400

    if url_confirmation is None:
        return {"msg": "Erreur server"}, 500

    count = db.session.query(TRoles).filter_by(email=email).count()

    if count == 0:
        return {"msg": "Adresse mail inconnue"}, 404
    if count > 1:
        return {"msg": "Plusieur identifiants correspondent à cette adresse, veuillez contacter l'administrateur"}, 404

    token = set_cor_role_token(email)
    user = db.session.query(TRoles).filter_by(email=email).one()

    # TODO : change return msg
    return {"msg": "Un mail avec pour modifier votre mot de passe vient d'être envoyé sur l'adresse %s" % email}, 200


@route.route('/update_user', methods=['POST'])
@fnauth.check_auth(5)
@json_resp
def update_user():
    '''
        route pour changer des paramètres d'utilisateur
    '''
    req_data = request.get_json()

    id_role = req_data.get('id_role', None)

    if not id_role:

        return {'msg': "Pas d'id_role"}, 400

    role_data = {}
    for att in req_data:
        if hasattr(TRoles, att):
            role_data[att] = req_data[att]

    role = TRoles(**role_data)
    db.session.merge(role)
    db.session.commit()
    role = db.session.query(TRoles).get(id_role)
    return role.as_dict(recursif=True)


@route.route("/check_token", methods=['POST'])
@json_resp
def check_token_validity():
    '''
        route permettant de savoir si un token est toujours valide
        parametres post : token
    '''

    data = request.get_json()

    token_exists = check_token(data.get('token', None))
    if token_exists:
        return {"msg":"valid token"}, 200

    return {"msg":"invalid token"}, 500
