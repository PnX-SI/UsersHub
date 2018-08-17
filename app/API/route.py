from flask import (
    Blueprint, request
)

from flask_bcrypt import (
    generate_password_hash
)

from app.env import db
from app.utils.utilssqlalchemy import json_resp
from app.models import (
    TTags,
    TRoles,
    CorRoleDroitApplication
)


route = Blueprint('api', __name__)


@route.route('/application')
@json_resp
def test():
    q = db.session.query(TTags).filter(TTags.id_tag_type == 3)
    data = [data.as_dict(columns=['id_tag', 'tag_name']) for data in q.all()]
    return data


@route.route('/role/<id_role>', methods=['GET'])
@json_resp
def get_one_t_roles(id_role):
    '''
        Fonction qui retourne les données concernant un utilisateur
    '''
    role = TRoles.get_one(id_role)
    return role


@route.route('/role', methods=['POST'])
@json_resp
def insert_one_t_role():
    '''
        Route permettant de créer un utilisateur

        curl --header "Content-Type: application/json" \
        --request POST \
        --data '{"email": null, "groupe": false, "pn": true, "remarques": "utilisateur test api", "desc_role": null, "prenom_role": "test", "identifiant": "test_api", "id_unite": -1, "id_organisme": -1, "uuid_role": "c8f63c2d-e606-49c5-8865-edb0953c496f", "nom_role": "API", "pass_plus": "123456", "pass_plus_confirmation": "123456", "applications":[{"id_app":2, "id_droit":1}]}' \
        http://localhost:5001/api/role
    '''
    req_data = request.get_json()

    role_data = {}
    for att in req_data:
        if hasattr(TRoles, att):
            role_data[att] = req_data[att]

    # Traitement du mot de passe
    if req_data['pass_plus'] == req_data['pass_plus_confirmation'] and req_data['pass_plus'] != "": # noqa E501
        req_data['pass_plus'] = generate_password_hash(req_data['pass_plus'].encode('utf-8')) # noqa E501
    else:
        return "mot de passe non identiques", 500
    role = TRoles(**role_data)
    db.session.add(role)
    db.session.commit()

    for app in req_data['applications']:
        c = CorRoleDroitApplication(
            id_role=role.id_role,
            id_droit=app['id_droit'],
            id_application=app['id_app']
        )
        db.session.add(c)
        db.session.commit()

    return role.as_dict(recursif=True)
