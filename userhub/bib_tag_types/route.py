from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from userhub import genericRepository
from userhub.bib_tag_types import forms as tag_typeforms
from userhub.models import BibTagTypes
from userhub.utils.utilssqlalchemy import json_resp

route = Blueprint('tag_type',__name__)

@route.route('/tag_types',methods=['GET','POST'])
def tag_types():
    entete = ['ID', 'Nom', 'Description']
    colonne = ['id_tag_type','tag_type_name','tag_type_desc']
    contenu = BibTagTypes.get_all()
    return render_template('affichebase.html', table = contenu, entete = entete, ligne = colonne, cheminM = "", cle = "id_tag_type", cheminS = "")

@route.route('/tag_type',methods=['GET','POST'])
def tag_type():
    form = tag_typeforms.TagTypes()
    if request.method == 'POST':
        if form.validate() and form.validate_on_submit() :
            form_tagtypes = form.data
            form_tagtypes.pop('csrf_token')
            form_tagtypes.pop('id_tag_type')
            form_tagtypes.pop('submit')
            BibTagTypes.post(form_tagtypes)
        else:
            flash(form.errors)
    return render_template('tagtypes.html', form = form)