from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from app import genericRepository
from app.CRUVED import forms as Cruvedforms
from app.models import TTags,BibTagTypes, TApplications, CorRoleTag, TRoles, CorOrganismeTag, Bib_Organismes, CorApplicationTag, CorAppPrivileges, VUsersactionForallGnModules
from app.utils.utilssqlalchemy import json_resp
from app.env import db
from sqlalchemy import distinct,tuple_, desc, or_
from pypnusershub.db.tools import cruved_for_user_in_app, get_or_fetch_user_cruved
import shelve
from config import config

route =  Blueprint('cruved',__name__)


"""
Route du Cruved
"""

@route.route('CRUVED/list', methods=['GET','POST'])
def CRUVED():

    """
    Route qui affiche la liste des Roles avec un tableau de cruved vide
    Retourne un template avec pour paramètres :
                                            - une entête de tableau des roles --> fLine
                                            - une entête de tableau du Cruved --> fLineCruved
                                            - le nom des colonnes de la roles --> line
                                            - le contenu de la table des roles --> table
                                            - le chemin de mise à jour --> pathU 
                                            - le chemin affichant le cruved d'un roles --> pathC
                                            - une clé (clé primaire dans la plupart des cas) --> key
                                            - un nom de listes --> name_list
                                            - mise en page si le role est un groupe --> group
    """

    fLine = ['ID', 'Nom']
    columns = ['id_role','full_name']
    fLineCruved = ['Application','Create','Read','Update','Validate','Export','Delete']
    q = TRoles.get_all(as_model=True)
    q = q.order_by(desc(TRoles.groupe))
    data = TRoles.test_group([data.as_dict_full_name() for data in q.all()])
    if request.method == 'GET':
        return render_template('CRUVED.html',fLine = fLine, line = columns,fLineCruved = fLineCruved, table = data, key = 'id_role', pathC = config.URL_APPLICATION +'/CRUVED/user/',pathU='',group = 'groupe',name_list = 'Utilisateurs et Groupes')       
    if request.method =='POST':
        return redirect(url_for('cruved.cruved_one'))




@route.route('CRUVED/user/<id_role>',methods=['GET','POST'])
def cruved_one(id_role):
    
    """
    Route qui affiche la liste des Roles avec un tableau de cruved correspondant à celui de l'id_role passé en paramètre
    Retourne un template avec pour paramètres :
                                            - une entête de tableau des roles --> fLine
                                            - une entête de tableau du Cruved --> fLineCruved
                                            - le nom des colonnes des roles --> line
                                            - le nom des colonnes du cruved --> lineCruved
                                            - le contenu de la table des roles  --> table
                                            - le contenu du tableau du cruved pour un roles --> tableCruved
                                            - le chemin de mise à jour --> pathU 
                                            - le chemin de mise à jour (séparation entre l'id role et l'id application) --> pathUu
                                            - le chemin affichant le cruved d'un role --> pathC
                                            - le chemin d'ajout d'un cruved à un role --> pathA
                                            - une clé (clé primaire dans la plupart des cas) --> key
                                            - une id de role --> id_r
                                            - une id d'application --> app
                                            - un nom de listes --> name_list
                                            - mise en page si le role est un groupe --> group
                                            - nom du role --> name_role
    """

    fLine = ['ID', 'Nom']
    columns = ['id_role','full_name']
    fLineCruved = ['Application','Create','Read','Update','Validate','Export','Delete']
    columnsCruved = [ 'nom_application','C','R','U','V','E','D']
    q = TRoles.get_all(as_model=True)
    q = q.order_by(desc(TRoles.groupe))
    data = TRoles.test_group([data.as_dict_full_name() for data in q.all()])
    contents = get_cruved_one(id_role)
    if contents == []:
        role = TRoles.get_one(id_role,as_model = True).as_dict_full_name()
        app = None
    else:
        role = contents[0]
        app =  contents[0]['id_application']
    return render_template('CRUVED.html',fLine = fLine, line = columns, table = data,fLineCruved = fLineCruved,lineCruved = columnsCruved,tableCruved=contents, key = 'id_role',  key_app = 'id_application',id_r=role['id_role'],  pathC = '', pathU=config.URL_APPLICATION +'/CRUVED/update/',pathUu = '/' ,pathA= config.URL_APPLICATION +'/CRUVED/add/new/'  , group = 'groupe',name_list = 'Liste d\'Utilisateurs et de Groupes',name_role =role['full_name'])       

# @route.route('CRUVED/add/new', defautls={'id_role':None,'id_application':None}, methods=['GET','POST'])
# @route.route('CRUVED/update/<id_role>/<id_application>', methods=['GET','POST'])
# def addorupdate(id_role,id_application):
#     return ""


def get_cruved_one(id_role):

    """
    Methode qui retourne un dictionnaire contenant :    'nom_application',
                                                        'C',
                                                        'R',
                                                        'U',
                                                        'V',
                                                        'E',
                                                        'D',
                                                        'id_role',
                                                        'full_name',
                                                        'id_application'

    sauf si aucun rôle est associé à un droit cruved dans ce cas là la methode retourne un tableau vide                                                    
    """

    user = TRoles.get_one(id_role)
    role = dict()
    if  user['prenom_role'] != None :
        role['full_name'] = user['nom_role'] +' '+ user['prenom_role']
    else :
        role['full_name'] = user['nom_role']
    app = TApplications.get_all(as_model= True)
    app = app.filter(or_(TApplications.id_parent == config.ID_GEONATURE,TApplications.id_application == config.ID_GEONATURE))
    App = [data.as_dict() for data in app.all()]
    tab_dict=[]
    test = cruved_for_user_in_app(1000148,14)
    for app_c in App:
        cruved = cruved_for_user_in_app(id_role,app_c['id_application'],app_c['id_parent'])
        if cruved != {'C': '0', 'D': '0', 'V': '0', 'U': '0', 'E': '0', 'R': '0'} :
            tdict = [ 'nom_application','C','R','U','V','E','D','id_role','full_name','id_application'] 
            d_data = [app_c['nom_application'],cruved['C'],cruved['R'],cruved['U'],cruved['V'],cruved['E'],cruved['D'],user['id_role'],role['full_name'],app_c['id_application']]
            tdict = dict(zip(tdict,d_data))
            tab_dict.append(tdict)
    return tab_dict 




@route.route('CRUVED/update/<id_role>/<id_application>',methods=['GET','POST'])
@route.route('CRUVED/add/new/<id_role>',defaults={'id_application': None},methods=['GET','POST']) 
def cruved_user(id_role, id_application):

    """
    Route affichant un formulaire vierge ou non selon l'url) pour ajouter ou mettre à jour un cruved d'un role pour une application
    L'envoie du formulaire permet l'ajout ou la mise à jour de l'éléments dans la base
    Retourne un template accompagné d'un formulaire, pré-rempli si on met à jour des données ou vierge si on créer des nouvelles données 
    Une fois le formulaire validé, on retourne une redirection vers la liste de roles et leur cruved associé, si c'est une édition d'un cruved alors on retourne en plus le paramètre active qui desactive le champs applications
    """

    tab_choices = get_tab_choice()
    form = Cruvedforms.Scope()
    form_na = Cruvedforms.Name_App()
    form_na.full_name_role.choices = TRoles.choixSelect('id_role','full_name')
    form.scopeCreate.choices = tab_choices
    form.scopeRead.choices = tab_choices
    form.scopeUpdate.choices = tab_choices
    form.scopeValidate.choices = tab_choices
    form.scopeExport.choices = tab_choices
    form.scopeDelete.choices = tab_choices
    form_na.app.choices = TApplications.choix_app_cruved('id_application','nom_application')
    cruved = get_cruved_one(id_role)
    data = request.get_json()
    if id_application == None:
        for c in cruved:
            for app in form_na.app.choices:
                if c['nom_application'] == app[1]:
                    form_na.app.choices.remove(app)
        if request.method =='GET':
            form_na.full_name_role.process_data(id_role)
        if request.method == 'POST':
            if form.validate() and form.validate_on_submit() :
                form_data = {"id_role":id_role,"id_application":form_na.app.data}
                form_scope = pops(form.data)
                for scope in form_scope:
                    if form_scope[scope] != 0:
                        # print("id_tag_action")
                        # print(config.ID_TAG_CREATE)
                        # print("id_tag_object" )
                        # print(form_scope[scope])
                        # print(form_data)
                        if scope == "scopeCreate":
                            CorAppPrivileges.post({"id_tag_action":config.ID_TAG_CREATE,"id_tag_object":form_scope[scope],**form_data})
                        if scope == "scopeRead":
                            CorAppPrivileges.post({"id_tag_action":config.ID_TAG_READ,"id_tag_object":form_scope[scope],**form_data})
                        if scope == "scopeUpdate":
                            CorAppPrivileges.post({"id_tag_action":config.ID_TAG_UPDATE,"id_tag_object":form_scope[scope],**form_data})
                        if scope == "scopeValidate":
                            CorAppPrivileges.post({"id_tag_action":config.ID_TAG_VALIDATE,"id_tag_object":form_scope[scope],**form_data})
                        if scope == "scopeExport":
                            CorAppPrivileges.post({"id_tag_action":config.ID_TAG_EXPORT,"id_tag_object":form_scope[scope],**form_data})
                        if scope == "scopeDelete": 
                            CorAppPrivileges.post({"id_tag_action":config.ID_TAG_DELETE,"id_tag_object":form_scope[scope],**form_data})
            return redirect(url_for('cruved.cruved_one', id_role = id_role))
        return render_template('CRUVED_forms.html', form = form,form_na = form_na, title = "Formulaire de CRUVED")
    else :
        for c in cruved :
            if c['id_application'] == int(id_application):
                CRUVED = c
        CRUVED = convert_code_to_id(CRUVED)
        if request.method == 'GET':
            form_na.full_name_role.process_data(id_role)
            form_na.app.process_data(id_application)
            form.scopeCreate.process_data(CRUVED['C'])
            form.scopeRead.process_data(CRUVED['R'])
            form.scopeUpdate.process_data(CRUVED['U'])
            form.scopeValidate.process_data(CRUVED['V'])
            form.scopeExport.process_data(CRUVED['E'])
            form.scopeDelete.process_data(CRUVED['D'])
        if request.method == 'POST':
            if form.validate() and form.validate_on_submit() :
                form_data = {"id_role":id_role,"id_application":id_application}
                form_scope = pops(form.data)
                for scope in form_scope:
                    if scope == "scopeCreate" and form_scope[scope] != CRUVED['C']:
                        CorAppPrivileges.delete(CRUVED['C'],form_data['id_role'],form_data['id_application'])
                        if form_scope[scope] !=0 :
                            CorAppPrivileges.post({"id_tag_action":config.ID_TAG_CREATE,"id_tag_object":form_scope[scope],**form_data})
                    if scope == "scopeRead" and form_scope[scope] != CRUVED['R']:
                        CorAppPrivileges.delete(CRUVED['R'],form_data['id_role'],form_data['id_application'])
                        if form_scope[scope] !=0 :
                            CorAppPrivileges.post({"id_tag_action":config.ID_TAG_READ,"id_tag_object":form_scope[scope],**form_data})
                    if scope == "scopeUpdate" and form_scope[scope] != CRUVED['U']:
                        CorAppPrivileges.delete(CRUVED['U'],form_data['id_role'],form_data['id_application'])
                        if form_scope[scope] !=0 :
                            CorAppPrivileges.post({"id_tag_action":config.ID_TAG_UPDATE,"id_tag_object":form_scope[scope],**form_data})
                    if scope == "scopeValidate" and form_scope[scope] != CRUVED['V']:
                        CorAppPrivileges.delete(CRUVED['V'],form_data['id_role'],form_data['id_application'])
                        if form_scope[scope] !=0 :
                            CorAppPrivileges.post({"id_tag_action":config.ID_TAG_VALIDATE,"id_tag_object":form_scope[scope],**form_data})
                    if scope == "scopeExport" and form_scope[scope] != CRUVED['E']:
                        CorAppPrivileges.delete(CRUVED['E'],form_data['id_role'],form_data['id_application'])
                        if form_scope[scope] !=0 :
                            CorAppPrivileges.post({"id_tag_action":config.ID_TAG_EXPORT,"id_tag_object":form_scope[scope],**form_data})
                    if scope == "scopeDelete" and form_scope[scope] != CRUVED['D']:
                        CorAppPrivileges.delete(CRUVED['D'],form_data['id_role'],form_data['id_application']) 
                        if form_scope[scope] !=0 :
                            CorAppPrivileges.post({"id_tag_action":config.ID_TAG_DELETE,"id_tag_object":form_scope[scope],**form_data})
            return redirect(url_for('cruved.cruved_one',  id_role = id_role))
        return render_template('CRUVED_forms.html', form = form,form_na = form_na, active = 'True', title = "Formulaire de CRUVED")

def pops(form):

    """
    Methode qui supprime les éléments indésirables du formulaires
    Avec pour paramètre un formulaire
    """

    form.pop('submit')
    form.pop('csrf_token')
    return form

def convert_code_to_id(cruved):

    """
    Methode qui transforme l'id tag des portées en leur tag_code
    """

    test =  dict([(3,config.ID_TAG_ALLDATA), (1, config.ID_TAG_MYDATA), (2,config.ID_TAG_MYORGDATA),(0,0)]) 
    cruved['C'] = test[int(cruved['C'])]
    cruved['R'] = test[int(cruved['R'])]
    cruved['U'] = test[int(cruved['U'])]
    cruved['V'] = test[int(cruved['V'])]
    cruved['E'] = test[int(cruved['E'])]
    cruved['D'] = test[int(cruved['D'])]
    return cruved


def get_tab_choice():

    """
    Methode qui retourne le tableau de tuples des selectfield des portées
    """

    tab_choices = TTags.choixSelect('id_tag','tag_name',0)
    return tab_choices


def get_cruved_all_test(id_role):

    """
    Method de test pour recupérer le cruved d'un role
    """

    q = db.session.query(distinct(CorAppPrivileges.id_application),TRoles).filter(CorAppPrivileges.id_role == id_role)
    q = q.join(TRoles,CorAppPrivileges.id_role == TRoles.id_role)
    App = []
    role = []
    for data in q.all():
        App.append(data[0])
        role.append(data[1].as_dict_full_name())
    tab_dict=[]
    if role != []:
        role = role[0]
        cruved_dict = {}
        for id_app in App:
            app = TApplications.get_one(id_app)
            cruved = cruved_for_user_in_app(role['id_role'],id_app,app['id_parent'])
            tdict = [ 'nom_application','C','R','U','V','E','D','id_role','full_name','id_application'] 
            d_data = [app['nom_application'],cruved['C'],cruved['R'],cruved['U'],cruved['V'],cruved['E'],cruved['D'],role['id_role'],role['full_name'],id_app]
            tdict = dict(zip(tdict,d_data))
            tab_dict.append(tdict)
    return tab_dict 

  


        
      