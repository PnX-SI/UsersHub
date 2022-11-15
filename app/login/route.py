from flask import (
    Flask, redirect, url_for, render_template,
    Blueprint, current_app
)

from app.env import db
from app.models import TApplications
route = Blueprint('login', __name__)


@route.route('login', methods=['GET'])
def login():
    app = TApplications.query.filter_by(code_application=current_app.config["CODE_APPLICATION"]).one()
    return render_template('login.html', id_app=app.id_application)
