from flask import (
    Flask, redirect, url_for, render_template,
    Blueprint, current_app
)

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