from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from app import genericRepository
from app.bib_organismes import forms as bib_organismeforms
from app.models import Bib_Organismes

route =  Blueprint('organisme',__name__)

@route.route('organisms/list', methods=['GET','POST'])
def organisms():
    fLine = [ 'ID','Nom', 'Adresse', 'Code_Postal', 'Ville', 'Telephone', 'Fax', 'Email']
    columns = ['id_organisme','nom_organisme','adresse_organisme', 'cp_organisme','ville_organisme','tel_organisme','fax_organisme','email_organisme']
    contents = Bib_Organismes.get_all(columns)
    return render_template('table_database.html', table = contents, fLine = fLine,line = columns, pathU = '/organism/update/', key= 'id_organisme', pathD = '/organisms/delete/', pathA= '/organism/add/new',name = "un organisme", name_list = "Listes des organismes" )


@route.route('organism/add/new', defaults={'id_organisme': None}, methods=['GET','POST'])
@route.route('organism/update/<id_organisme>', methods=['GET','POST'])
def addorupdate(id_organisme):
    form = bib_organismeforms.Organisme()
    if id_organisme == None:
        if request.method == 'POST':
            if form.validate_on_submit() and form.validate():
                form_org =  pops(form.data)
                form_org.pop('id_organisme')
                Bib_Organismes.post(form_org)
                return redirect(url_for('organisme.organisms'))
            else:
                flash(form.errors)
    else:
        org = Bib_Organismes.get_one(id_organisme)
        if request.method =='GET':
            form = process(form,org)
        if request.method == 'POST':
            if form.validate_on_submit() and form.validate() :
                form_org = pops(form.data)
                form_org['id_organisme'] = org['id_organisme']
                Bib_Organismes.update(form_org)
                return redirect(url_for('organisme.organisms'))
            else:
                flash(form.errors)
    return render_template('organism.html',form = form)        





@route.route('organisms/delete/<id_organisme>', methods = ['GET', 'POST'])
def delete(id_organisme):
    Bib_Organismes.delete(id_organisme)
    return redirect(url_for('organisme.organisms'))


# @route.route('organism/members/<id_organisme', methods=['GET','POST'])
# def members(id_organisme):
#     # liste 
#     entete = ['Nom', 'Adresse', 'Code_Postal', 'Ville', 'Telephone', 'Fax', 'Email', 'ID']
#     colonne = ['nom_organisme','adresse_organisme', 'cp_organisme','ville_organisme','tel_organisme','fax_organisme','email_organisme','id_organisme']
#     contenu = Bib_Organismes.get_all(colonne)
#     return render_template('affichebase.html', table = contenu, entete = entete,ligne = colonne)


def pops(form):
    form.pop('submit')
    form.pop('csrf_token')
    return form

def process(form,org):
    form.nom_organisme.process_data(org['nom_organisme'])
    form.cp_organisme.process_data(org['cp_organisme'])
    form.adresse_organisme.process_data(org['adresse_organisme'])
    form.ville_organisme.process_data(org['ville_organisme'])
    form.tel_organisme.process_data(org['tel_organisme'])
    form.fax_organisme.process_data(org['fax_organisme'])
    form.email_organisme.process_data(org['email_organisme'])
    return form

# NON UTILISE

# @route.route('/organisme', methods=['GET','POST'])
# def organisme():
#     formu = bib_organismeforms.Organisme()
#     if request.method == 'POST':
#         if formu.validate_on_submit() and formu.validate():
#             form_org = formu.data
#             form_org.pop('id_organisme')
#             form_org.pop('submit')
#             form_org.pop('csrf_token')        
#             Bib_Organismes.post(form_org)
#             return redirect(url_for('organisme.organismes'))
#         else:
#             flash(formu.errors)
#     return render_template('organisme.html', form = formu)



#     @route.route('organisms/update/<id_organisme>', methods=['GET','POST'])
# def organismes_unique(id_organisme):
#     entete = ['Nom', 'Adresse', 'Code Postal', 'Ville', 'Telephone', 'Fax', 'Email', 'ID']
#     colonne = ['nom_organisme','adresse_organisme', 'cp_organisme','ville_organisme','tel_organisme','fax_organisme','email_organisme','id_organisme']
#     contenu = Bib_Organismes.get_all(colonne)
#     # test
#     org = Bib_Organismes.get_one(id_organisme)
#     form = bib_organismeforms.Organisme()
#     if request.method == 'POST':
#         if form.validate_on_submit() and form.validate() :
#             form_org = form.data
#             form_org['id_organisme'] = org['id_organisme']
#             form_org.pop('submit')
#             form_org.pop('csrf_token')
#             Bib_Organismes.update(form_org)
#             return redirect(url_for('organisme.organismes'))
#         else:
#             flash(form.errors)
#     return render_template('affichebase.html', table = contenu, entete = entete,ligne = colonne, cheminM = '/organisms/update/', cle= 'id_organisme', cheminS = '/organisms/delete/', test= 'organisme.html', form = form, nom_organisme = org['nom_organisme'], adresse_organisme = org['adresse_organisme'], cp_organisme = org['cp_organisme'], ville_organisme = org['ville_organisme'],tel_organisme = org['tel_organisme'], fax_organisme = org['fax_organisme'], email_organisme = org['email_organisme'] )