from flask import (
    Flask, redirect, url_for, render_template,
    Blueprint, request, session, flash, current_app
)
from app import genericRepository
from app.auth import forms as authforms
from app.models import TRoles
from app.utils.utilssqlalchemy import json_resp
from app.env import db
from flask_bcrypt import (Bcrypt,
                          check_password_hash,
                          generate_password_hash)
import bcrypt

route = Blueprint('login', __name__)


@route.route('/', methods=['GET'])
def auth():
    return render_template('login.html', id_app=current_app.config['ID_APP'])
