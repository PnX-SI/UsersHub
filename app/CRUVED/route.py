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


    return render_template('table_database.html',)

@route.route('CRUVED/test',methods= ['GET','POST'])
def test():
    fLine = ['ID', 'Nom', "Create", "Read", "Update","Validate","Export","Delete","Application"]
    columns = ['id_role','full_name']
    print(VUsersactionForallGnModules.get_all())
    print('\n\n')
    print(cruved_for_user_in_app())
    print('\n\n')
    # print(get_or_fetch_user_cruved(1,14))
    return ""
