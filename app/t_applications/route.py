from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from app import genericRepository
from app.t_applications import forms as t_applicationsforms
from app.models import TRoles
from app.models import Bib_Organismes, CorRoles, TApplications, CorAppPrivileges, TTags, CorRoleTagApplication
from app.utils.utilssqlalchemy import json_resp
from app.env import db
from config import config


route =  Blueprint('application',__name__)

@route.route('applications/list', methods=['GET','POST'])
def applications():

    """
    Route qui affiche la liste des applications
    Retourne un template avec pour paramètres :
                                            - une entête de tableau --> fLine
                                            - le nom des colonnes de la base --> line
                                            - le contenu du tableau --> table
                                            - le chemin de mise à jour --> pathU 
                                            - le chemin de suppression --> pathD
                                            - le chemin d'ajout --> pathA
                                            - une clé (clé primaire dans la plupart des cas) --> key
                                            - un nom (nom de la table) pour le bouton ajout --> name
                                            - un nom de liste --> name_list
                                            - empeche l'ajout de droits à des utilisateurs pour l'application géonature ou les applications filles --> id_geonature
                                            - ajoute une colonne de bouton ('True doit être de type string) --> app_geonature
                                            - nom affiché sur le bouton --> Members

    """

    fLine = ['ID','Nom','Description', ' Parent']
    columns = ['id_application','nom_application','desc_application','app_parent']
    contents = TApplications.get_all()
    for data in contents :
        if data['id_parent'] != None :
            parent =  TApplications.get_one(data['id_parent'])
            data.update({'app_parent' : parent['nom_application']})
        else :
            parent = ""
            data.update({'app_parent' : parent})
    return render_template('table_database.html', table = contents, fLine = fLine, line = columns, pathU = config.URL_APPLICATION +"/application/update/", key= "id_application", pathD=config.URL_APPLICATION +"/applications/delete/", pathA = config.URL_APPLICATION +'/application/add/new',pathP= config.URL_APPLICATION +'/application/users/', name = 'une application', name_list = "Applications", id_geonature = config.ID_GEONATURE ,app_geonature = 'True', Members = "Utilisateurs" )    



@route.route('application/add/new',defaults={'id_application': None}, methods=['GET','POST'])
@route.route('application/update/<id_application>',methods=['GET','POST'])
def addorupdate(id_application):

    """
    Route affichant un formulaire vierge ou non (selon l'url) pour ajouter ou mettre à jour une application
    L'envoie du formulaire permet l'ajout ou la maj d'une application dans la base
    Retourne un template accompagné d'un formulaire pré-rempli ou non selon le paramètre id_application
    Une fois le formulaire validé on retourne une redirection vers la liste d'application
    """

    form = t_applicationsforms.Application()
    form.id_parent.choices = TApplications.choixSelect('id_application','nom_application',1)
    if id_application == None:
        form.id_parent.process_data(-1)
        if request.method == 'POST': 
            if form.validate() and form.validate_on_submit():
                form_app = pops(form.data)
                if form.id_parent.data == -1:
                    form_app['id_parent'] = None
                form_app.pop('id_application')
                TApplications.post(form_app)
                return redirect(url_for('application.applications'))
            else :
                errors =  form.errors
                if(errors['nom_application'] != None):
                    flash("Champ 'Nom' vide, veillez à le remplir afin de valider le formulaire. ")
        return render_template('application.html', form= form, title = "Formulaire Application")
    else :
        application = TApplications.get_one(id_application)
        form.id_parent.choices.remove((application['id_application'],application['nom_application'])) 
        if request.method == 'GET':
            if application['id_parent'] == None:
                    form.id_parent.process_data(-1)
            else:
                form.id_parent.process_data(application['id_parent'])
            form_app = process(form,application) 
        if request.method == 'POST':
            if form.validate_on_submit() and form.validate():
                form_app = pops(form.data)
                if form.id_parent.data == -1:
                    form_app['id_parent'] = None
                form_app['id_application'] = application['id_application']
                TApplications.update(form_app)
                return redirect(url_for('application.applications'))
            else :
                errors =  form.errors
                if(errors['nom_application'] != None):
                    flash("Champ 'Nom' vide, veillez à le remplir afin de valider le formulaire. ")
        return render_template('application.html', form= form, title = "Formulaire Application")
        



@route.route('applications/delete/<id_application>', methods=['GET','POST'])
def delete(id_application):

    """
    Route qui supprime une application dont l'id est donné en paramètres dans l'url
    Retourne une redirection vers la liste de groupe
    """

    TApplications.delete(id_application)
    return redirect(url_for('application.applications'))



@route.route('application/users/<id_application>', methods = ['GET','POST'])
def users(id_application):

    """
    Route affichant la liste des roles n'appartenant pas a l'application vis à vis de ceux qui appartiennent à celui ci.
    Avec pour paramètre un id d'application
    Retourne un template avec pour paramètres:
                                            - une entête des tableaux --> fLine
                                            - le nom des colonnes de la base --> data
                                            - liste des roles n'appartenant pas à l'application --> table
                                            - liste des roles appartenant à l'application--> table2
                                            - variable qui permet a jinja de colorer une ligne si celui-ci est un groupe --> group 
    """
    users_with_right = TRoles.get_user_right_in_application(id_application)
    only_role = []
    for role in users_with_right :
        role['role']['id_tag'] = role['right']['id_tag']
        role['role']['value'] = TTags.choixSelectTag('id_tag','tag_name')
        only_role.append(role['role'])
    users_in_app = TRoles.test_group(only_role)
    users_out_app = TRoles.test_group(TRoles.get_user_out_application(id_application))
    header = ['ID', 'Nom']
    data = ['id_role','full_name']
    app = TApplications.get_one(id_application)
    if request.method == 'POST':
        data = request.get_json()
        new_rights = data["tab_add"]
        delete_rights = data["tab_del"]
        print(delete_rights)
        CorRoleTagApplication.add_cor(id_application,new_rights)
        CorRoleTagApplication.del_cor(id_application,delete_rights)
    return render_template('tobelong.html', fLine = header, data = data, table = users_out_app, table2 = users_in_app, group = 'groupe', app = 'True', info = 'Droit des utilisateurs et des groupes sur  "'+app['nom_application']+'"') 



def pops(form):

    """
    Methode qui supprime les éléments indésirables du formulaires
    Avec pour paramètre un formulaire
    """

    form.pop('csrf_token')
    form.pop('submit')
    return form    

def process(form,application):
          
    """
    Methode qui rempli le formulaire par les données de l'éléments concerné
    Avec pour paramètres un formulaire et une application 
    """

    form.nom_application.process_data(application['nom_application'])
    form.desc_application.process_data(application['desc_application'])
    return form



#  NON UTILISE


# @route.route('/application', methods=['GET','POST'])
# def application():
#     form = t_applicationsforms.Application()
#     form.id_parent.choices = TApplications.choixSelect('id_application','nom_application',1)   
#     if request.method == 'POST': 
#         if form.validate() and form.validate_on_submit():
#             form_app = form.data
#             if form.id_parent.data == -1:
#                  form_app['id_parent'] = None
#             form_app.pop('id_application')
#             form_app.pop('csrf_token')
#             form_app.pop('submit')
#             TApplications.post(form_app)
#             return redirect(url_for('application.applications'))
#         else :
#             flash(form.errors)
#     return render_template('application.html', form= form )

# @route.route('applications/update/<id_application>', methods=['GET','POST'])
# def update(id_application):
#     entete = ['ID','Nom','Description', 'ID Parent']
#     colonne = ['id_application','nom_application','desc_application','id_parent']
#     contenu = TApplications.get_all(colonne)
#     # test
#     form = t_applicationsforms.Application()
#     application = TApplications.get_one(id_application)
#     tab = TApplications.choixSelect('id_application','nom_application',1)
#     tab.remove((application['id_application'],application['nom_application']))
#     form.id_parent.choices = tab
#     if request.method == 'GET':
#         print(form.id_parent.data)        
#         if application['id_parent'] == None:
#                 form.id_parent.process_data(-1)
#         else:
#             form.id_parent.process_data(application['id_parent'])  
#     if request.method == 'POST':
#         if form.validate_on_submit() and form.validate():
#             form_app = form.data
#             print('coucou2')
#             if form.id_parent.data == -1:
#                   form_app['id_parent'] = None
#             form_app['id_application'] = application['id_application']
#             form_app.pop('csrf_token')
#             form_app.pop('submit')
#             TApplications.update(form_app)
#             return redirect(url_for('application.applications'))
#         else :
#             flash(form.errors)
#     return render_template('affichebase.html', table = contenu, entete = entete, ligne = colonne, cheminM = "/applications/update/", cle= "id_application", cheminS="/applications/delete/", test ='application.html', form= form, nom_application = application['nom_application'], desc_application= application['desc_application'] )
