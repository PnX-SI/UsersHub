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

@route.route('groups/list', methods=['GET','POST'])
def groups():
    fLine = ['ID groupe', 'nom', 'description' ]
    columns = ['id_role', 'nom_role', 'desc_role']
    filters = [{'col': 'groupe', 'filter': 'True'}]
    contents = TRoles.get_all(columns,filters)
    return render_template('table_database.html', fLine = fLine , line = columns, table = contents ,  key = "id_role", pathU = "/group/update/", pathD = "/groups/delete/", pathA = '/group/add/new', pathP = '/groups/members/',name = "un groupe", name_list = "Liste des Groupes", otherCol = 'True', Members = "Membres",)


@route.route('group/add/new',defaults={'id_role': None}, methods=['GET','POST'])
@route.route('group/update/<id_role>', methods=['GET','POST'])
def addorupdate(id_role):
    form = groupeforms.Group()
    form.groupe.process_data(True)
    if id_role == None:
        if request.method == 'POST':
            if form.validate_on_submit() and form.validate():
                form_group = pops(form.data)
                form_group.pop('id_role')
                TRoles.post(form_group)
                return redirect(url_for('groupe.groups'))
            else:
                flash(form.errors)
        return render_template('group.html', form = form)
    else :
        group = TRoles.get_one(id_role)
        if request.method =='GET':
            form = process(form,group)
        if request.method == 'POST':
            if form.validate_on_submit() and form.validate():
                form_group = pops(form.data)
                form_group['id_role'] = group['id_role']
                TRoles.update(form_group)
                return redirect(url_for('groupe.groups'))
            else:
                flash(form.errors)
        return render_template('group.html', form = form)



  
@route.route('groups/members/<id_groupe>', methods=['GET','POST'])
def membres(id_groupe):
    # liste utilisateurs
    fLine = ['ID groupe', 'nom', 'description' ]
    columns = ['id_role', 'nom_role', 'desc_role']
    filters = [{'col': 'groupe', 'filter': 'False'}]
    contents = TRoles.get_all(columns,filters)
    # liste des utilisateurs du groupe
    fLine2 = ['id role','identifiant',  'prenom role', 'nom role']
    columns2 = ['id_role','identifiant','prenom_role', 'nom_role']
    q = db.session.query(TRoles)
    q = q.join(CorRoles)
    q = q.filter(id_groupe == CorRoles.id_role_groupe  )
    return render_template("tobelong.html", fLine = fLine , line = columns, table = contents, fLine2 = fLine2, line2 = columns2, table2 = [data.as_dict(True) for data in q.all()]  )




@route.route('groups/delete/<id_groupe>', methods=['GET','POST'])
def delete(id_groupe):
    TRoles.delete(id_groupe)
    return redirect(url_for('groupe.groups'))


def pops(form):
    form.pop('submit')
    form.pop('csrf_token')
    return form


def process(form,group):
    form.nom_role.process_data(group['nom_role'])
    form.desc_role.process_data(group['desc_role'])
    return form


#  NON UTILISE
# @route.route('/groupe', methods=['GET','POST'])
# def groupe():
#     form = groupeforms.Groupe()
#     form.groupe.process_data(True)
#     if request.method == 'POST':
#         if form.validate_on_submit() and form.validate():
#             form_group = form.data
#             form_group.pop('id_role')
#             form_group.pop('csrf_token')
#             form_group.pop('submit')            
#             TRoles.post(form_group)
#             return redirect(url_for('groupe.groupes'))
#         else:
#             flash(form.errors)
#     return render_template('groupe.html', form = form)




# @route.route('groups/update/<id_groupe>', methods=['GET','POST'])
# def groupe_unique(id_groupe):
#     entete = ['ID groupe', 'nom', 'description' ]
#     colonne = ['id_role', 'nom_role', 'desc_role']
#     filters = [{'col': 'groupe', 'filter': 'True'}]
#     contenu = TRoles.get_all(colonne,filters)
#     #test
#     groupe = TRoles.get_one(id_groupe)
#     form = groupeforms.Groupe()
#     form.groupe.process_data(True)
#     if request.method == 'POST':
#         if form.validate_on_submit() and form.validate():
#             form_group = form.data
#             form_group['id_role'] = groupe['id_role']
#             form_group.pop('csrf_token')
#             form_group.pop('submit')
#             TRoles.update(form_group)
#             return redirect(url_for('groupe.groupes'))
#         else:
#             flash(form.errors)
#     return render_template('affichebase.html', entete = entete , ligne = colonne, table = contenu ,  cle = "id_role", cheminM = "/groups/update/", cheminS = "/groups/delete/", test ='groupe.html',form = form, nom_role = groupe['nom_role'], desc_role = groupe['desc_role'])



   
    
    # contenu = CorRoles.get_all(colonne,filters)
    # print(contenu)
    # print(contenu[0]["t_roles"]['identifiant'])


# @route.route('/mbgroupe/<id_groupe>', methods=['GET','POST'])
# def mbgroupe(id_groupe):
#     entete = ['identifiant', 'id role', 'prenom role', 'nom role']
#     colonne = ['identifiant','id_role','prenom_role', 'nom_role']
#     q = db.session.query(TRoles)
#     q = q.join(CorRoles)
#     q = q.filter(id_groupe == CorRoles.id_role_groupe  )
#     [data.as_dict(True) for data in q.all()]
#     return render_template('affichebase.html', entete = entete , ligne = colonne, table = [data.as_dict(True) for data in q.all()] , cle = "", cheminM = "", cheminS = "" )
      