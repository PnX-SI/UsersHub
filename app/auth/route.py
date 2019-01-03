from flask import (
    Flask, redirect, url_for, render_template,
    Blueprint, request, session, flash, current_app
)

import bcrypt

from app import genericRepository
from app.auth import forms as authforms
from app.models import TRoles
from app.utils.utilssqlalchemy import json_resp
from app.env import db
from flask_bcrypt import (Bcrypt,
                          check_password_hash,
                          generate_password_hash)

from config import config

route = Blueprint('login', __name__)


@route.route('/', methods=['GET'])
def auth():
    return render_template('login.html', id_app=current_app.config['ID_APP'])

@route.route('/logout', methods=['GET'])
def logout():
    resp = redirect(url_for('login.auth'), code=302)
    resp.delete_cookie('token')
    resp.delete_cookie('session')
    return resp