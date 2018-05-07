from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from app import genericRepository
from app.bib_tag_types import forms as tag_typeforms
from app.models import BibTagTypes
from app.utils.utilssqlalchemy import json_resp

route = Blueprint('tags_types',__name__)

@route.route('tags_types/add',methods=['GET','POST'])
def tags_types():
    entete = ['ID', 'Nom', 'Description']
    colonne = ['id_tag_type','tag_type_name','tag_type_desc']
    contenu = BibTagTypes.get_all()
    # test
    form = tag_typeforms.TagTypes()
    if request.method == 'POST':
        if form.validate() and form.validate_on_submit() :
            form_tagtypes = form.data
            form_tagtypes.pop('csrf_token')
            form_tagtypes.pop('submit')
            BibTagTypes.post(form_tagtypes)
            return redirect(url_for('tags_types.tags_types'))
        else:
            flash(form.errors)
    return render_template('affichebase.html', table = contenu, entete = entete, ligne = colonne, cheminM = "/tags_types/update/", cle = "id_tag_type", cheminS = "/tags_types/delete/", test = 'tagtypes.html', form = form)



@route.route('tags_types/update/<id_tag_type>',methods=['GET','POST'])
def update(id_tag_type):
    entete = ['ID', 'Nom', 'Description']
    colonne = ['id_tag_type','tag_type_name','tag_type_desc']
    contenu = BibTagTypes.get_all()
    # test
    tag_type = BibTagTypes.get_one(id_tag_type)
    print(tag_type)
    form = tag_typeforms.TagTypes()
    if request.method == 'POST':
        if form.validate_on_submit() and form.validate():
            print('coucou')
            form_tagtypes = form.data
            form_tagtypes.pop('csrf_token')
            form_tagtypes.pop('submit')
            print(form_tagtypes)
            BibTagTypes.update(form_tagtypes)
            print(tag_type)
            return redirect(url_for('tags_types.tags_types'))
        else:
            flash(form.errors)
    return render_template('affichebase.html', table = contenu, entete = entete, ligne = colonne, cheminM = "/tags_types/update/", cle = "id_tag_type", cheminS = "/tags_types/delete/", test ='tagtypes.html', form = form, id_tag_type = tag_type['id_tag_type'], tag_type_name = tag_type['tag_type_name'], tag_type_desc = tag_type['tag_type_desc'])

@route.route('tags_types/delete/<id_tag_type>',methods=['GET','POST'])
def delete(id_tag_type):
    BibTagTypes.delete(id_tag_type)
    return redirect(url_for('tags_types.tags_types'))

#  NON UTILISE

@route.route('/tag_type',methods=['GET','POST'])
def tag_type():
    form = tag_typeforms.TagTypes()
    if request.method == 'POST':
        if form.validate() and form.validate_on_submit() :
            form_tagtypes = form.data
            form_tagtypes.pop('csrf_token')
            form_tagtypes.pop('submit')
            BibTagTypes.post(form_tagtypes)
            return redirect(url_for('tag_type.tag_types'))
        else:
            flash(form.errors)
    return render_template('tagtypes.html', form = form)