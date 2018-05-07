from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
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

route =  Blueprint('auth',__name__)

@route.route('/auth',methods=['GET','POST'])
def auth():
    form = authforms.Admin()
    if request.method == 'POST':
        if form.validate_on_submit() and form.validate():
            data = form.data
            login = data['username']
            password = data['password'].encode('utf-8')
            q = db.session.query(TRoles)
            q =q.filter(TRoles.identifiant == login)
            data = q.all()
            for user in data:
                mdp = user.pass_plus.encode('utf-8')
                if check_password_hash(mdp,password):
                    Session['user'] = data['password']
                    return redirect(url_for('user.accueil'))

    return render_template('login.html', form = form)
