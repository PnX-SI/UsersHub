from flask import Blueprint


from app.env import db
from app.utils.utilssqlalchemy import json_resp
from app.models import (
    TTags
)


route = Blueprint('api', __name__)


@route.route('/application')
@json_resp
def test():
    q = db.session.query(TTags).filter(TTags.id_tag_type == 3)
    data = [data.as_dict(columns=['id_tag', 'tag_name']) for data in q.all()]
    return data
