from flask import (
    Flask, redirect, url_for, render_template,
    Blueprint, current_app
)

from app.env import db
from app.models import TApplications
route = Blueprint('login', __name__)


@route.route('login', methods=['GET'])
def login():
    return render_template('login.html', id_app=current_app.config['ID_APP'])
