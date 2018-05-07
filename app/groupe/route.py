from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from app import genericRepository
from app.t_roles import forms as t_rolesforms
from app.groupe import forms as groupeforms
from app.models import TRoles
from app.models import Bib_Organismes, CorRoles
from app.utils.utilssqlalchemy import json_resp
from app.env import db

route = Blueprint('groupe', __name__)

@route.route('groupes/add', methods=['GET','POST'])
def groupes():
    entete = ['ID groupe', 'nom', 'description' ]
    colonne = ['id_role', 'nom_role', 'desc_role']
    filters = [{'col': 'groupe', 'filter': 'True'}]
    contenu = TRoles.get_all(colonne,filters)
    # test
    form = groupeforms.Groupe()
    form.groupe.process_data(True)
    if request.method == 'POST':
        if form.validate_on_submit() and form.validate():
            form_group = form.data
            form_group.pop('id_role')
            form_group.pop('csrf_token')
            form_group.pop('submit')            
            TRoles.post(form_group)
            return redirect(url_for('groupe.groupes'))
        else:
            flash(form.errors)
    return render_template('affichebase.html', entete = entete , ligne = colonne, table = contenu ,  cle = "id_role", cheminM = "/groupes/update/", cheminS = "/groupes/delete/", test = 'groupe.html', form = form )




@route.route('groupes/update/<id_groupe>', methods=['GET','POST'])
def groupe_unique(id_groupe):
    entete = ['ID groupe', 'nom', 'description' ]
    colonne = ['id_role', 'nom_role', 'desc_role']
    filters = [{'col': 'groupe', 'filter': 'True'}]
    contenu = TRoles.get_all(colonne,filters)
    #test
    groupe = TRoles.get_one(id_groupe)
    form = groupeforms.Groupe()
    form.groupe.process_data(True)
    if request.method == 'POST':
        if form.validate_on_submit() and form.validate():
            form_group = form.data
            form_group['id_role'] = groupe['id_role']
            form_group.pop('csrf_token')
            form_group.pop('submit')
            TRoles.update(form_group)
            return redirect(url_for('groupe.groupes'))
        else:
            flash(form.errors)
    return render_template('affichebase.html', entete = entete , ligne = colonne, table = contenu ,  cle = "id_role", cheminM = "/groupes/update/", cheminS = "/groupes/delete/", test ='groupe.html',form = form, nom_role = groupe['nom_role'], desc_role = groupe['desc_role'])



@route.route('groupes/delete/<id_groupe>', methods=['GET','POST'])
def delete(id_groupe):
    TRoles.delete(id_groupe)
    return redirect(url_for('groupe.groupes'))


#  NON UTILISE
@route.route('/groupe', methods=['GET','POST'])
def groupe():
    form = groupeforms.Groupe()
    form.groupe.process_data(True)
    if request.method == 'POST':
        if form.validate_on_submit() and form.validate():
            form_group = form.data
            form_group.pop('id_role')
            form_group.pop('csrf_token')
            form_group.pop('submit')            
            TRoles.post(form_group)
            return redirect(url_for('groupe.groupes'))
        else:
            flash(form.errors)
    return render_template('groupe.html', form = form)





@route.route('/mbgroupe/<id_groupe>', methods=['GET','POST'])
def mbgroupe(id_groupe):
    entete = ['identifiant', 'id role', 'prenom role', 'nom role']
    colonne = ['identifiant','id_role','prenom_role', 'nom_role']
    q = db.session.query(TRoles)
    q = q.join(CorRoles)
    q = q.filter(id_groupe == CorRoles.id_role_groupe  )
    [data.as_dict(True) for data in q.all()]
    return render_template('affichebase.html', entete = entete , ligne = colonne, table = [data.as_dict(True) for data in q.all()] , cle = "", cheminM = "", cheminS = "" )
    
    
    
    # contenu = CorRoles.get_all(colonne,filters)
    # print(contenu)
    # print(contenu[0]["t_roles"]['identifiant'])
    