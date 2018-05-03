from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from userhub import genericRepository
from userhub.auth import forms as authforms
from userhub.models import TRoles
from userhub.utils.utilssqlalchemy import json_resp
from userhub.env import db
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
            print(login)
            print(password)
            q = db.session.query(TRoles)
            q =q.filter(TRoles.prenom_role == login)
            data = q.all()
            for user in data:
                print('cc')
                print(login)
                mdp = user.pass_plus.encode('utf-8')
                print(mdp)
                if check_password_hash(mdp,password):
                    print('yes')
                    return redirect(url_for('user.accueil'))

    return render_template('login.html', form = form)
