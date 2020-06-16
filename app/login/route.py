from flask import (
    Flask, redirect, url_for, render_template,
    Blueprint, current_app
)

from app.env import db
from app.models import TApplications
route = Blueprint('login', __name__)


@route.route('login', methods=['GET'])
def login():
    t_app = TApplications.get_all(
        columns=["id_application"],
        params=[{'col': 'code_application', 'filter': 'UH'}],
        recursif=False
    )
    ID_APP = t_app[0]['id_application']
    return render_template('login.html', id_app=ID_APP)
