from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash,json
)
from app.utils.utilssqlalchemy import json_resp
from app.models import TTags,BibTagTypes
from app.env import db  
from werkzeug.wrappers import Response

route = Blueprint('api',__name__)

@route.route('/application')
@json_resp
def test():
    q = db.session.query(TTags).filter(TTags.id_tag_type == 3)
    data = [data.as_dict(columns = ['id_tag','tag_name']) for data in q.all() ]
    return data