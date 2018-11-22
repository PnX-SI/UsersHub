from flask import Blueprint


from app.env import db
from app.utils.utilssqlalchemy import json_resp
from app.models import (
    TProfils
)


route = Blueprint('api', __name__)


@route.route('/application')
@json_resp
def test():
    q = db.session.query(TProfils)
    data = [data.as_dict(columns=['id_profil', 'nom_profil']) for data in q.all()]
    return data
