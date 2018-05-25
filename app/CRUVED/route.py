from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from app import genericRepository
from app.CRUVED import forms as Cruvedforms
from app.models import TTags,BibTagTypes, TApplications, CorRoleTag, TRoles, CorOrganismeTag, Bib_Organismes, CorApplicationTag, CorAppPrivileges, VUsersactionForallGnModules
from app.utils.utilssqlalchemy import json_resp
from app.env import db
from sqlalchemy import distinct,tuple_
from pypnusershub.db.tools import cruved_for_user_in_app, get_or_fetch_user_cruved

route =  Blueprint('cruved',__name__)

@route.route('CRUVED/list', methods=['GET','POST'])
def CRUVED():
    fLine = ['ID', 'Nom']
    columns = ['id_role','full_name']
    fLineCruved = ['Application','C','R','U','V','E','D']
    q = TRoles.get_all(as_model=True)
    data = TRoles.test_group([data.as_dict_full_name() for data in q.all()])
    if request.method == 'GET':
        return render_template('CRUVED.html',fLine = fLine, line = columns,fLineCruved = fLineCruved, table = data, key = 'id_role', pathC = '/CRUVED/user/',pathU='' ,group = 'groupe',name_list = 'Liste d\'Utilisateurs et de Groupes')       
    if request.method =='POST':
        return redirect(url_for('cruved.cruved_one'))




@route.route('CRUVED/user/<id_role>',methods=['GET','POST'])
def cruved_one(id_role):
    fLine = ['ID', 'Nom']
    columns = ['id_role','full_name']
    fLineCruved = ['Application','C','R','U','V','E','D']
    columnsCruved = [ 'nom_application','C','R','U','V','E','D']
    q = TRoles.get_all(as_model=True)
    data = TRoles.test_group([data.as_dict_full_name() for data in q.all()])
    print(data)        
    contents = get_cruved_one(id_role)
    return render_template('CRUVED.html',fLine = fLine, line = columns, table = data,fLineCruved = fLineCruved,lineCruved = columnsCruved,tableCruved=contents, key = 'id_role', pathC = '', pathU='' , group = 'groupe',name_list = 'Liste d\'Utilisateurs et de Groupes',name_role =' contents[0]["full_name"]')       

# @route.route('CRUVED/add/new', defautls={'id_role':None,'id_application':None}, methods=['GET','POST'])
# @route.route('CRUVED/update/<id_role>/<id_application>', methods=['GET','POST'])
# def addorupdate(id_role,id_application):
#     return ""


def get_cruved_one(id_role):
    q = db.session.query(distinct(CorAppPrivileges.id_application),TRoles).filter(CorAppPrivileges.id_role == id_role)
    q = q.join(TRoles,CorAppPrivileges.id_role == TRoles.id_role)
    App = [data[0] for data in q.all()]
    role =  [data[1].as_dict_full_name() for data in q.all()]
    tab_dict=[]
    if role != []:
        role = role[0]
        cruved_dict = {}
        for id_app in App:
            app = TApplications.get_one(id_app)
            cruved = cruved_for_user_in_app(role['id_role'],id_app,app['id_parent'])
            tdict = [ 'nom_application','C','R','U','V','E','D','id_role','full_name'] 
            d_data = [app['nom_application'],cruved['C'],cruved['R'],cruved['U'],cruved['V'],cruved['E'],cruved['D'],role['id_role'],role['full_name']]
            tdict = dict(zip(tdict,d_data))
            tab_dict.append(tdict)
    return tab_dict 




@route.route('CRUVED/<id_role>',methods=['GET','POST']) 
def cruved_user(id_role):
    contents = get_cruved_all_test()
    print(contents)
    tab_choices = get_tab_choice()
    form = Cruvedforms
    # if request.methods =='GET':
    return ''

def get_tab_choice():
    tab_choices = TTags.choixSelect('tag_code','tag_name',1)
    int_tab = []
    for t in tab_choices:
        int_tab.append((int(t[0]),t[1]))
    tab_choices = int_tab
    return tab_choices


def get_cruved_all_test(id_role):
    q = db.session.query(distinct(CorAppPrivileges.id_application),TRoles).filter(CorAppPrivileges.id_role == id_role)
    q = q.join(TRoles,CorAppPrivileges.id_role == TRoles.id_role)
    App = [data[0] for data in q.all()]
    role =  [data[1].as_dict_full_name() for data in q.all()]
    tab_dict=[]
    if role != []:
        role = role[0]
        cruved_dict = {}
        for id_app in App:
            app = TApplications.get_one(id_app)
            cruved = cruved_for_user_in_app(role['id_role'],id_app,app['id_parent'])
            tdict = [ 'nom_application','C','R','U','V','E','D','id_role','full_name'] 
            d_data = [app['nom_application'],cruved['C'],cruved['R'],cruved['U'],cruved['V'],cruved['E'],cruved['D'],role['id_role'],role['full_name']]
            tdict = dict(zip(tdict,d_data))
            tab_dict.append(tdict)
    return tab_dict 

    # already_exists = None
    # tdict = {}
    # tab_dict = []
    # for d in data:
    #     if (d['id_role'],d['id_application']) != already_exists :
    #         data_app = TApplications.get_one(d['id_application'])
    #         cruved = cruved_for_user_in_app(d['id_role'],d['id_application'],data_app['id_parent'])
    #         data_role = TRoles.get_one(d['id_role'])
    #         if data_role['groupe'] == True:
    #             tdict = ['id_role','full_name','C','R','U','V','E','D', 'nom_application','groupe'] 
    #             d_data = [d['id_role'],d['full_name'],cruved['C'],cruved['R'],cruved['U'],cruved['V'],cruved['E'],cruved['D'],data_app['nom_application'],'True']
    #         else :
    #             tdict = ['id_role','full_name','C','R','U','V','E','D', 'nom_application','groupe'] 
    #             d_data = [d['id_role'],d['full_name'],cruved['C'],cruved['R'],cruved['U'],cruved['V'],cruved['E'],cruved['D'],data_app['nom_application'],data_role['groupe']]
    #         tdict = dict(zip(tdict,d_data))
    #         tab_dict.append(tdict) 
    #         print(tdict)
    #     already_exists = (d['id_role'],d['id_application'])
    # return(tab_dict)


        
      