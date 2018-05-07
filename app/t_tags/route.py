from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from app import genericRepository
from app.t_tags import forms as t_tagsforms
from app.models import TTags,BibTagTypes, TApplications
from app.utils.utilssqlalchemy import json_resp
from app.env import db

route =  Blueprint('tags',__name__)

@route.route('tags/add', methods=['GET','POST'])
def tags():
    entete =['ID','ID type', 'CODE', 'Nom', 'Label', 'Description']
    colonne = ['id_tag','id_tag_type','tag_name','tag_name','tag_label','tag_desc']
    contenu = TTags.get_all(colonne)
    # test
    form = t_tagsforms.Tag()
    form.id_tag_type.choices =BibTagTypes.choixSelect('id_tag_type','tag_type_name')
    if request.method =='POST':
        if form.validate() and form.validate_on_submit():
            form_tag = form.data
            form_tag.pop('csrf_token')
            form_tag.pop('submit')
            form_tag.pop('id_tag')
            TTags.post(form_tag)
            return redirect(url_for('tags.tags'))
        else:
            flash(form.errors)
    return render_template('affichebase.html' ,entete = entete ,ligne = colonne,  table = contenu,  cle = 'id_tag', cheminM = '/tags/update/', cheminS = '/tags/delete/', test = 'tag.html', form = form)



@route.route('tags/update/<id_tag>',methods=['GET','POST'])
def update(id_tag):
    entete =['ID','ID type', 'CODE', 'Nom', 'Label', 'Description']
    colonne = ['id_tag','id_tag_type','tag_name','tag_name','tag_label','tag_desc']
    contenu = TTags.get_all(colonne)
    # test
    tag = TTags.get_one(id_tag)
    form = t_tagsforms.Tag()
    form.id_tag_type.choices = BibTagTypes.choixSelect('id_tag_type','tag_type_name')
    if request.method == 'GET':
        form.id_tag_type.process_data(tag['id_tag_type'])
    if request.method == 'POST':
        if form.validate() and form.validate_on_submit():
            form_tag = form.data
            form_tag.pop('csrf_token')
            form_tag.pop('submit')
            form_tag['id_tag'] = tag['id_tag']
            TTags.update(form_tag)
            return redirect(url_for('tags.tags'))
        else:
            flash(form.errors)
    return render_template('affichebase.html' ,entete = entete ,ligne = colonne,  table = contenu,  cle = 'id_tag', cheminM = '/tags/update/', cheminS = '/tags/delete/', test ='tag.html', form = form, code = tag['tag_code'], name = tag['tag_name'], label = tag['tag_label'], desc = tag['tag_desc'])


@route.route('tags/delete/<id_tag>',methods=['GET','POST'])
def delete(id_tag):
    TTags.delete(id_tag)
    return redirect(url_for('tags.tags'))

# NON UTILISE
@route.route('/tag', methods=['GET','POST'])
def tag():
    form = t_tagsforms.Tag()
    form.id_tag_type.choices =BibTagTypes.choixSelect('id_tag_type','tag_type_name')
    if request.method =='POST':
        if form.validate() and form.validate_on_submit():
            form_tag = form.data
            form_tag.pop('csrf_token')
            form_tag.pop('submit')
            form_tag.pop('id_tag')
            TTags.post(form_tag)
            return redirect(url_for('tags.tags'))
        else:
            flash(form.errors)
    return render_template('tag.html', form = form)