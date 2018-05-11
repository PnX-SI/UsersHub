from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from app import genericRepository
from app.t_tags import forms as t_tagsforms
from app.models import TTags,BibTagTypes, TApplications, CorRoleTag, TRoles
from app.utils.utilssqlalchemy import json_resp
from app.env import db

route =  Blueprint('tags',__name__)

@route.route('tags/list', methods=['GET','POST'])
def tags():
    entete =['ID','ID_type', 'CODE', 'Nom', 'Label', 'Description']
    colonne = ['id_tag','id_tag_type','tag_code','tag_name','tag_label','tag_desc']
    contenu = TTags.get_all(colonne)
    return render_template('affichebase.html' ,entete = entete ,ligne = colonne,  table = contenu,  cle = 'id_tag', cheminM = '/tag/update/', cheminS = '/tags/delete/', cheminA = '/tag/add/new', cheminP = "/tag/users/",nom = "un tag", nom_liste = "Liste des Tags", Membres = "Utilisateurs", t = 'True')


@route.route('tags/delete/<id_tag>',methods=['GET','POST'])
def delete(id_tag):
    TTags.delete(id_tag)
    return redirect(url_for('tags.tags'))


@route.route('tag/add/new',defaults={'id_tag': None}, methods=['GET','POST'])
@route.route('tag/update/<id_tag>',methods=['GET','POST'])
def addorupdate(id_tag):
    form = t_tagsforms.Tag()
    form.id_tag_type.choices = BibTagTypes.choixSelect('id_tag_type','tag_type_name')
    if id_tag == None:
        if request.method =='POST':
            if form.validate() and form.validate_on_submit():
                form_tag = pops(form.data)
                form_tag.pop('id_tag')
                TTags.post(form_tag)
                return redirect(url_for('tags.tags'))
            else:
                flash(form.errors)
        return render_template('tag.html', form = form)
    else:
        tag = TTags.get_one(id_tag)
        if request.method == 'GET':
            form = process(form,tag)
        if request.method == 'POST':
            if form.validate() and form.validate_on_submit():
                form_tag = pops(form.data)
                form_tag['id_tag'] = tag['id_tag']
                TTags.update(form_tag)
                return redirect(url_for('tags.tags'))
            else:
                flash(form.errors)
        return render_template('tag.html',form = form)

@route.route('tag/users/<id_tag>', methods=['GET','POST'])
def tag_users(id_tag):
    # affichage des utlisateurs
    entete = [ 'id role', 'nom role']
    colonne = [ 'id_role', 'prenom_role', 'nom_role']
    filters = [{'col': 'groupe', 'filter': 'False'}]
    
    contenu = TRoles.get_all(colonne,filters, False)
    filters2 = [{'col': 'groupe', 'filter': 'True'}]
    contenu2 = TRoles.get_all(colonne,filters2)
    col = [ 'id_role', 'nom_role']
    tab =[]
    tab2 = []
    tab3 = []
    for d in contenu:
        t = dict()
        t['id_role'] = d['id_role']
        t['nom_role'] = d['prenom_role']+ ' '+d['nom_role']
        tab.append(t)
    for d in contenu2:
        t = dict()
        t['id_role'] = d['id_role']
        if d['prenom_role'] == None:
            t['nom_role'] =d['nom_role']
        else :
            t['nom_role'] = d['prenom_role']+ ' '+d['nom_role']        
        tab2.append(t)
    
    # affichage des utilisateurs du tag
    entete2 =[ 'id role', 'nom role']
    colonne2 = ['id_role','prenom_role', 'nom_role']
    q = db.session.query(TRoles)
    q = q.join(CorRoleTag)
    q = q.filter(id_tag == CorRoleTag.id_tag  )
    data =  [data.as_dict(False) for data in q.all()]
    for d in data:
        t = dict()
        t['id_role'] = d['id_role']
        if d['prenom_role'] == None:
            t['nom_role'] =d['nom_role']
        else :
            t['nom_role'] = d['prenom_role']+ ' '+d['nom_role']        
        tab3.append(t)

    return render_template("tobelong.html", entete = entete , ligne = col, table = tab, table3= tab2, entete2 = entete2, ligne2 = col, table2 =tab3, group = 'True'   )
    


def pops(form):
    form.pop('csrf_token')
    form.pop('submit')
    return form

def process(form,tag):
    form.id_tag_type.process_data(tag['id_tag_type'])
    form.tag_name.process_data(tag['tag_name'])
    form.tag_label.process_data(tag['tag_label'])
    form.tag_code.process_data(tag['tag_code'])
    form.tag_desc.process_data(tag['tag_desc'])
    return form



# NON UTILISE
# @route.route('/tag', methods=['GET','POST'])
# def tag():
#     form = t_tagsforms.Tag()
#     form.id_tag_type.choices =BibTagTypes.choixSelect('id_tag_type','tag_type_name')
#     if request.method =='POST':
#         if form.validate() and form.validate_on_submit():
#             form_tag = form.data
#             form_tag.pop('csrf_token')
#             form_tag.pop('submit')
#             form_tag.pop('id_tag')
#             TTags.post(form_tag)
#             return redirect(url_for('tags.tags'))
#         else:
#             flash(form.errors)
#     return render_template('tag.html', form = form)


# @route.route('tags/update/<id_tag>',methods=['GET','POST'])
# def update(id_tag):
#     entete =['ID','ID type', 'CODE', 'Nom', 'Label', 'Description']
#     colonne = ['id_tag','id_tag_type','tag_code','tag_name','tag_label','tag_desc']
#     contenu = TTags.get_all(colonne)
#     # test
#     tag = TTags.get_one(id_tag)
#     form = t_tagsforms.Tag()
#     form.id_tag_type.choices = BibTagTypes.choixSelect('id_tag_type','tag_type_name')
#     if request.method == 'GET':
#         form.id_tag_type.process_data(tag['id_tag_type'])
#     if request.method == 'POST':
#         if form.validate() and form.validate_on_submit():
#             form_tag = form.data
#             form_tag.pop('csrf_token')
#             form_tag.pop('submit')
#             form_tag['id_tag'] = tag['id_tag']
#             TTags.update(form_tag)
#             return redirect(url_for('tags.tags'))
#         else:
#             flash(form.errors)
#     return render_template('affichebase.html' ,entete = entete ,ligne = colonne,  table = contenu,  cle = 'id_tag', cheminM = '/tags/update/', cheminS = '/tags/delete/', test ='tag.html', form = form, code = tag['tag_code'], name = tag['tag_name'], label = tag['tag_label'], desc = tag['tag_desc'])
