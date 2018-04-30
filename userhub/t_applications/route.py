from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from userhub import genericRepository
from userhub.t_applications import forms as t_applicationsforms
from userhub.models import TRoles
from userhub.models import Bib_Organismes, CorRoles, TApplications
from userhub.utils.utilssqlalchemy import json_resp


route =  Blueprint('application',__name__)

@route.route('/applications', methods=['GET','POST'])
def applications():
    entete = ['ID','Nom','Description', 'ID Parent']
    colonne = ['id_application','nom_application','desc_application','id_parent']
    contenu = TApplications.get_all(colonne)
    return render_template('affichebase.html', table = contenu, entete = entete, ligne = colonne, cheminM = "/application/applications/", cle= "id_application", cheminS="/application/application/delete/")    

@route.route('/application', methods=['GET','POST'])
def application():
    form = t_applicationsforms.Application()
    form.id_parent.choices = TApplications.choixApp()
   
    if request.method == 'POST': 
        if form.validate() and form.validate_on_submit():
            form_app = form.data
            if form.id_parent.data == -1:
                 form_app['id_parent'] = None
            form_app.pop('id_application')
            form_app.pop('csrf_token')
            form_app.pop('submit')
            TApplications.post(form_app)
            return redirect(url_for('application.applications'))
        else :
            flash(form.errors)
    return render_template('application.html', form= form )


@route.route('/application/delete/<id_application>', methods=['GET','POST'])
def delete(id_application):
    TApplications.delete(id_application)
    return redirect(url_for('application.applications'))

@route.route('/applications/<id_application>', methods=['GET','POST'])
def update(id_application):
    form = t_applicationsforms.Application()
    application = TApplications.get_one(id_application)
    tab = TApplications.choixApp()
    tab.remove((application['id_application'],application['nom_application']))
    form.id_parent.choices = tab
    print('coucou')  
    if request.method == 'POST':
        if form.validate_on_submit() and form.validate():
            form_app = form.data
            print('coucou2')
            if form.id_parent.data == -1:
                  form_app['id_parent'] = None
            form_app['id_application'] = application['id_application']
            form_app.pop('csrf_token')
            form_app.pop('submit')
            TApplications.update(form_app)
            return redirect(url_for('application.applications'))
        else :
            flash(form.errors)
    return render_template('application.html', form= form, nom_application = application['nom_application'], desc_application= application['desc_application'] , id_parent = application['id_parent'])