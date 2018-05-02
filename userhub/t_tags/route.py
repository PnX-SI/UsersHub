from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from userhub import genericRepository
from userhub.t_roles import forms as t_rolesforms
from userhub.models import TRoles
from userhub.models import Bib_Organismes, CorRoles, TTags
from userhub.utils.utilssqlalchemy import json_resp
from userhub.env import db

route =  Blueprint('tags',__name__)

@route.route('/tags', methods=['GET','POST'])
def tags():
    entete =['ID','ID type', 'CODE', 'Nom', 'Label', 'Description']
    colonne = ['id_tag','id_tag_type','tag_name','tag_name','tag_label','tag_desc']
    contenu = TTags.get_all(colonne)
    return render_template('affichebase.html' ,entete = entete ,ligne = colonne,  table = contenu,  cle = 'id_tag', cheminM = '', cheminS = '')


