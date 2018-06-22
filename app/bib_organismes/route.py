from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from app import genericRepository
from app.bib_organismes import forms as bib_organismeforms
from app.models import Bib_Organismes
from config import config

route =  Blueprint('organisme',__name__)

"""
Route des Organismes
"""

@route.route('organisms/list', methods=['GET','POST'])
def organisms():

    """
    Route qui affiche la liste des Organismes
    Retourne un template avec pour paramètres :
                                            - une entête de tableau --> fLine
                                            - le nom des colonnes de la base --> line
                                            - le contenu du tableau --> table
                                            - le chemin de mise à jour --> pathU 
                                            - le chemin de suppression --> pathD
                                            - le chemin d'ajout --> pathA
                                            - une clé (clé primaire dans la plupart des cas) --> key
                                            - un nom (nom de la table) pour le bouton ajout --> name
                                            - un nom de listes --> name_list
    """

    fLine = [ 'ID','Nom', 'Adresse', 'Code_Postal', 'Ville', 'Telephone', 'Fax', 'Email']
    columns = ['id_organisme','nom_organisme','adresse_organisme', 'cp_organisme','ville_organisme','tel_organisme','fax_organisme','email_organisme']
    contents = Bib_Organismes.get_all(columns)
    return render_template('table_database.html', table = contents, fLine = fLine,line = columns, pathU = config.URL_APPLICATION +'/organism/update/', key= 'id_organisme', pathD = config.URL_APPLICATION + '/organisms/delete/', pathA= config.URL_APPLICATION +'/organism/add/new',name = "un organisme", name_list = "Organismes" )


@route.route('organism/add/new', defaults={'id_organisme': None}, methods=['GET','POST'])
@route.route('organism/update/<id_organisme>', methods=['GET','POST'])
def addorupdate(id_organisme):

    """
    Route affichant un formulaire vierge ou non (selon l'url) pour ajouter ou mettre à jour un organisme
    L'envoie du formulaire permet l'ajout ou la mise à jour de l'éléments dans la base
    Retourne un template accompagné du formulaire
    Une fois le formulaire validé on retourne une redirection vers la liste d'organisme
    """

    form = bib_organismeforms.Organisme()
    if id_organisme == None:
        if request.method == 'POST':
            if form.validate_on_submit() and form.validate():
                form_org =  pops(form.data)
                form_org.pop('id_organisme')
                Bib_Organismes.post(form_org)
                return redirect(url_for('organisme.organisms'))
            else:
                errors =  form.errors
                if(errors['nom_organisme'] != None):
                    flash("Champ 'Nom Organisme' vide, veillez à le remplir afin de valider le formulaire. ")
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
                errors =  form.errors
                if(errors['nom_organisme'] != None):
                    flash("Champ 'Nom Organisme' vide, veillez à le remplir afin de valider le formulaire. ")
    return render_template('organism.html',form = form, title = "Formulaire Organisme")        





@route.route('organisms/delete/<id_organisme>', methods = ['GET', 'POST'])
def delete(id_organisme):
    
    """
    Route qui supprime un organisme dont l'id est donné en paramètres dans l'url
    Retourne une redirection vers la liste d'organismes
    """

    Bib_Organismes.delete(id_organisme)
    return redirect(url_for('organisme.organisms'))


def pops(form):

    """
    Methode qui supprime les éléments indésirables du formulaires
    Avec pour paramètre un formulaire
    """
    form.pop('submit')
    form.pop('csrf_token')
    return form

def process(form,org):

    """
    Methode qui rempli le formulaire par les données de l'éléments concerné
    Avec pour paramètres un formulaire et un organisme
    """

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


# @route.route('organism/members/<id_organisme', methods=['GET','POST'])
# def members(id_organisme):
#     # liste 
#     entete = ['Nom', 'Adresse', 'Code_Postal', 'Ville', 'Telephone', 'Fax', 'Email', 'ID']
#     colonne = ['nom_organisme','adresse_organisme', 'cp_organisme','ville_organisme','tel_organisme','fax_organisme','email_organisme','id_organisme']
#     contenu = Bib_Organismes.get_all(colonne)
#     return render_template('affichebase.html', table = contenu, entete = entete,ligne = colonne)
