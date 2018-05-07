from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from app import genericRepository
from app.t_roles import forms as t_rolesforms
from app.models import TRoles
from app.models import Bib_Organismes, CorRoles
from app.utils.utilssqlalchemy import json_resp
from app.env import db
from flask_bcrypt import (Bcrypt,
                          check_password_hash,
                          generate_password_hash)

import bcrypt


route =  Blueprint('user',__name__)


# @route.route('/login', methods=['GET','POST'])
# def login():
#     form = t_rolesforms.LogUser()
#     print(form.validate_on_submit())
#     if form.validate_on_submit():
#         if t_rolesrepository.admin_valide(form.username.data,form.password.data) :
#             session['Pseudo']= (form.username.data, form.password.data)
#             print(session.get('Pseudo')[0],session.get('Pseudo')[1])
#             return redirect(url_for('user.accueil'))
#     return render_template('login.html', form=form)




@route.route('users/add',methods=['GET','POST'])
def users():
    entete = ['Id','Groupe','Identifiant', 'Nom','Prenom','Description','Email', 'ID organisme', 'Remarques']
    colonne = ['id_role','groupe','identifiant','nom_role','prenom_role','desc_role','email','id_organisme','remarques']
    filters = [{'col': 'groupe', 'filter': 'False'}]
    contenu = TRoles.get_all(colonne,filters)
    # test
    formu = t_rolesforms.Utilisateur()
    formu.id_organisme.choices = Bib_Organismes.choixSelect('id_organisme','nom_organisme')
    # print(TRoles.choixGroupe('id_role','nom_role',1))
    formu.a_groupe.choices = TRoles.choixGroupe('id_role','nom_role',1)
    if request.method == 'POST':
        if formu.validate_on_submit() and formu.validate():
            form_user = formu.data
            form_user['groupe'] = False
            print(form_user['a_groupe'])
            form_user.pop('mdpconf')
            form_user.pop('submit')
            form_user.pop('csrf_token')
            form_user.pop('id_role')
            form_user.pop('a_groupe')           
            if formu.pass_plus.data == formu.mdpconf.data:
                form_user['pass_plus'] = generate_password_hash(form_user['pass_plus'].encode('utf-8'))
                form_user['pass_plus'] = form_user['pass_plus'].decode('utf-8')
                TRoles.post(form_user)
                return redirect(url_for('user.users'))
            else :
                flash("mot de passe non identiques")
        else :
            flash(formu.errors)
    return render_template('affichebase.html', entete = entete ,ligne = colonne,  table = contenu,  cle = 'id_role', cheminM = '/users/update/', cheminS = '/users/delete/', test = 'user_unique.html', form = formu)    

    


    
@route.route('users/update/<id_role>',  methods=['GET','POST'])
def user_unique(id_role):
    entete = ['Id','Groupe','Identifiant', 'Nom','Prenom','Description','Email', 'ID organisme', 'Remarques']
    colonne = ['id_role','groupe','identifiant','nom_role','prenom_role','desc_role','email','id_organisme','remarques']
    filters = [{'col': 'groupe', 'filter': 'False'}]
    contenu = TRoles.get_all(colonne,filters)
    # test
    user = TRoles.get_one(id_role)
    formu = t_rolesforms.Utilisateur(request.form)
    formu.id_organisme.choices = Bib_Organismes.choixSelect('id_organisme','nom_organisme')
    if request.method == 'GET':
        formu.id_organisme.process_data(user['id_organisme'])
        print(formu.id_organisme.data)
        print('coucou')
    if request.method == 'POST':
        if formu.validate_on_submit() and formu.validate():  
            print('coucou2')             
            form_user = formu.data
            form_user['groupe'] = False      
            form_user.pop('mdpconf')
            form_user.pop('submit')
            form_user.pop('csrf_token')
            form_user.pop('a_groupe')           
            if formu.pass_plus.data == formu.mdpconf.data:
                form_user['id_role'] = user['id_role']
                form_user['pass_plus'] = generate_password_hash(form_user['pass_plus'].encode('utf-8'))
                form_user['pass_plus'] = form_user['pass_plus'].decode('utf-8')
                TRoles.update(form_user)
                return redirect(url_for('user.users'))
            else :
                flash("mot de passe non identiques")
        else :
            flash(formu.errors)
    return render_template('affichebase.html', entete = entete ,ligne = colonne,  table = contenu,  cle = 'id_role', cheminM = '/users/update/', cheminS = '/user/delete/', test ='user_unique.html',form = formu, nom_role = user['nom_role'], prenom_role = user['prenom_role'],  email= user['email'],desc_role = user['desc_role'], remarques = user['remarques'], identifiant= user['identifiant'] )
    
@route.route('users/delete/<id_role>', methods = ['GET','POST'])
def deluser(id_role):
    TRoles.delete(id_role)
    return redirect(url_for('user.users'))

#  NON UTILISE

@route.route('/user', methods=['GET','POST'])
def user():
    formu = t_rolesforms.Utilisateur()
    formu.id_organisme.choices = Bib_Organismes.choixSelect('id_organisme','nom_organisme')
    if request.method == 'POST':
        if formu.validate_on_submit() and formu.validate():
            form_user = formu.data
            form_user['groupe'] = False           
            form_user.pop('mdpconf')
            form_user.pop('submit')
            form_user.pop('csrf_token')
            form_user.pop('id_role')
            if formu.pass_plus.data == formu.mdpconf.data:
                form_user['pass_plus'] = generate_password_hash(form_user['pass_plus'].decode('utf-8'))
                form_user['pass_plus'] = form_user['pass_plus'].decode('utf-8')
                TRoles.post(form_user)
                return redirect(url_for('user.users'))
            else :
                flash("mot de passe non identiques")
        else :
            flash(formu.errors)
    return render_template('user_unique.html', form = formu)


@route.route('/accueil',methods=['GET','POST'])
def accueil():   
    return render_template('accueil.html')
# @route.route('/test')
# @json_resp
# def test():
#     filters = [{'col': 'id_role_utilisateur', 'filter':'5'}]
#     return CorRoles.get_all(params = filters)