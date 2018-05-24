from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from app import genericRepository
from app.CRUVED import forms as Cruvedforms
from app.models import TTags,BibTagTypes, TApplications, CorRoleTag, TRoles, CorOrganismeTag, Bib_Organismes, CorApplicationTag, CorAppPrivileges, VUsersactionForallGnModules
from app.utils.utilssqlalchemy import json_resp
from app.env import db
from pypnusershub.db.tools import cruved_for_user_in_app, get_or_fetch_user_cruved

route =  Blueprint('cruved',__name__)

@route.route('CRUVED/list', methods=['GET','POST'])
def CRUVED():
    fLine = ['ID', 'Nom', "Create", "Read", "Update","Validate","Export","Delete","Application"]
    columns = ['id_role','full_name','C','R','U','V','E','D','nom_application']
    contents = get_cruved_all()
    return render_template('CRUVED.html',fLine = fLine, line = columns, table = contents, key = '', pathU = '', pathD = '',group = 'groupe',name_list = 'Liste de CRUVED')


def get_cruved_all():
    q = VUsersactionForallGnModules.get_all(as_model = True)
    data = [data.as_dict_full_name() for data in q.all()]
    already_exists = None
    tdict = {}
    tab_dict = []
    for d in data:
        if (d['id_role'],d['id_application']) != already_exists :
            cruved = cruved_for_user_in_app(d['id_role'],d['id_application'])
            data_app = TApplications.get_one(d['id_application'])
            data_role = TRoles.get_one(d['id_role'])
            if data_role['groupe'] == True:
                tdict = ['id_role','full_name','C','R','U','V','E','D', 'nom_application','groupe'] 
                d_data = [d['id_role'],d['full_name'],cruved['C'],cruved['R'],cruved['U'],cruved['V'],cruved['E'],cruved['D'],data_app['nom_application'],'True']
            else :
                tdict = ['id_role','full_name','C','R','U','V','E','D', 'nom_application','groupe'] 
                d_data = [d['id_role'],d['full_name'],cruved['C'],cruved['R'],cruved['U'],cruved['V'],cruved['E'],cruved['D'],data_app['nom_application'],data_role['groupe']]
            tdict = dict(zip(tdict,d_data))
            tab_dict.append(tdict) 
        already_exists = (d['id_role'],d['id_application'])
    return(tab_dict)



@route.route('CRUVED/test',methods= ['GET','POST'])
def test():
    fLine = ['ID', 'Nom', "Create", "Read", "Update","Validate","Export","Delete","Application"]
    columns = ['id_role','full_name','C','R','U','V','E','D','nom_application']
    contents = get_cruved_all_test()
    return render_template('CRUVED.html',fLine = fLine, line = columns, table = contents, key = '', pathU = '', pathD = '',group = 'groupe')       
    
def get_cruved_all_test():
    q = VUsersactionForallGnModules.get_all(as_model = True)
    data = [data.as_dict_full_name() for data in q.all()]
    already_exists = None
    tdict = {}
    tab_dict = []
    for d in data:
        if (d['id_role'],d['id_application']) != already_exists :
            cruved = cruved_for_user_in_app(d['id_role'],d['id_application'])
            data_app = TApplications.get_one(d['id_application'])
            data_role = TRoles.get_one(d['id_role'])
            if data_role['groupe'] == True:
                tdict = ['id_role','full_name','C','R','U','V','E','D', 'nom_application','groupe'] 
                d_data = [d['id_role'],d['full_name'],cruved['C'],cruved['R'],cruved['U'],cruved['V'],cruved['E'],cruved['D'],data_app['nom_application'],'True']
            else :
                tdict = ['id_role','full_name','C','R','U','V','E','D', 'nom_application','groupe'] 
                d_data = [d['id_role'],d['full_name'],cruved['C'],cruved['R'],cruved['U'],cruved['V'],cruved['E'],cruved['D'],data_app['nom_application'],data_role['groupe']]
            tdict = dict(zip(tdict,d_data))
            tab_dict.append(tdict) 
            print(tdict)
        already_exists = (d['id_role'],d['id_application'])
    return(tab_dict)


        
      