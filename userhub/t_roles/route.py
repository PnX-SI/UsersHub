from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from userhub import genericRepository
from userhub.t_roles import forms as t_rolesforms
from userhub.models import TRoles
from userhub.models import Bib_Organismes, CorRoles
from userhub.utils.utilssqlalchemy import json_resp
from userhub.env import db


route =  Blueprint('user',__name__)


@route.route('/login', methods=['GET','POST'])
def login():
    form = t_rolesforms.LogUser()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        if t_rolesrepository.admin_valide(form.username.data,form.password.data) :
            session['Pseudo']= (form.username.data, form.password.data)
            print(session.get('Pseudo')[0],session.get('Pseudo')[1])
            return redirect(url_for('user.accueil'))
    return render_template('login.html', form=form)


@route.route('/accueil',methods=['GET','POST'])
def accueil():   
    return render_template('accueil.html')


@route.route('/users',methods=['GET','POST'])
def users():
    entete = ['Id','Groupe','Identifiant', 'Nom','Prenom','Description','Email', 'ID organisme', 'Remarques']
    colonne = ['id_role','groupe','identifiant','nom_role','prenom_role','desc_role','email','id_organisme','remarques']
    filters = [{'col': 'groupe', 'filter': 'False'}]
    contenu = TRoles.get_all(colonne,filters)
    return render_template('affichebase.html', entete = entete ,ligne = colonne,  table = contenu,  cle = 'id_role', cheminM = '/t_roles/users/', cheminS = '/t_roles/user/delete/')    

    

@route.route('/user', methods=['GET','POST'])
def user():
    formu = t_rolesforms.Utilisateur()
    formu.id_organisme.choices = Bib_Organismes.choixOrg()
    if request.method == 'POST':
        if formu.validate_on_submit() and formu.validate():
            form_user = formu.data
            form_user['groupe'] = False 
            form_user.pop('mdpconf')
            form_user.pop('submit')
            form_user.pop('csrf_token')
            form_user.pop('id_role')
            if formu.pass_plus.data == formu.mdpconf.data:
                TRoles.post(form_user)
                return redirect(url_for('user.users'))
            else :
                flash("mot de passe non identiques")
        else :
            flash(formu.errors)
    return render_template('user_unique.html', form = formu)
    
@route.route('/users/<id_role>',  methods=['GET','POST'])
def user_unique(id_role):
    user = TRoles.get_one(id_role)
    formu = t_rolesforms.Utilisateur(request.form)
    formu.id_organisme.choices = Bib_Organismes.choixOrg()
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
            if formu.pass_plus.data == formu.mdpconf.data:
                form_user['id_role'] = user['id_role']
                TRoles.update(form_user)
                return redirect(url_for('user.users'))
            else :
                flash("mot de passe non identiques")
        else :
            flash(formu.errors)
    return render_template('user_unique.html',form = formu, nom_role = user['nom_role'], prenom_role = user['prenom_role'],  email= user['email'],desc_role = user['desc_role'], remarques = user['remarques'] )
    
@route.route('/user/delete/<id_role>', methods = ['GET','POST'])
def deluser(id_role):
    TRoles.delete(id_role)
    return redirect(url_for('user.users'))

@route.route('/test')
@json_resp
def test():
    filters = [{'col': 'id_role_utilisateur', 'filter':'5'}]
    return CorRoles.get_all(params = filters)