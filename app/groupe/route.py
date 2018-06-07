from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from app import genericRepository
from app.t_roles import forms as t_rolesforms
from app.groupe import forms as groupeforms
from app.models import TRoles
from app.models import Bib_Organismes, CorRoles
from app.utils.utilssqlalchemy import json_resp
from app.env import db

route = Blueprint('groupe', __name__)

@route.route('groups/list', methods=['GET','POST'])
def groups():

    """
    Route qui affiche la liste des groupes
    Retourne un template avec pour paramètres :
                                            - une entête de tableau --> fLine
                                            - le nom des colonnes de la base --> line
                                            - le contenu du tableau --> table
                                            - le chemin de mise à jour --> pathU 
                                            - le chemin de suppression --> pathD
                                            - le chemin d'ajout --> pathA
                                            - le chemin des membres du groupe --> pathP
                                            - une clé (clé primaire dans la plupart des cas) --> key
                                            - un nom (nom de la table) pour le bouton ajout --> name
                                            - un nom de listes --> name_list
                                            - ajoute une colonne de bouton ('True' doit être de type string)--> otherCol
                                            - nom affiché sur le bouton --> Members  
    """

    fLine = ['ID groupe', 'nom', 'description' ]
    columns = ['id_role', 'nom_role', 'desc_role']
    filters = [{'col': 'groupe', 'filter': 'True'}]
    contents = TRoles.get_all(columns,filters)
    return render_template('table_database.html', fLine = fLine , line = columns, table = contents ,  key = "id_role", pathU = "/group/update/", pathD = "/groups/delete/", pathA = '/group/add/new', pathP = '/groups/members/',name = "un groupe", name_list = "Liste des Groupes", otherCol = 'True', Members = "Membres",)


@route.route('group/add/new',defaults={'id_role': None}, methods=['GET','POST'])
@route.route('group/update/<id_role>', methods=['GET','POST'])
def addorupdate(id_role):

    """
    Route affichant un formulaire vierge ou non (selon l'url) pour ajouter ou mettre à jour un groupe
    L'envoie du formulaire permet l'ajout ou la maj du groupe dans la base
    Retourne un template accompagné d'un formulaire pré-rempli ou non selon le paramètre id_role
    Une fois le formulaire validé on retourne une redirection vers la liste de groupe
    """

    form = groupeforms.Group()
    form.groupe.process_data(True)
    if id_role == None:
        if request.method == 'POST':
            if form.validate_on_submit() and form.validate():
                form_group = pops(form.data)
                form_group.pop('id_role')
                TRoles.post(form_group)
                return redirect(url_for('groupe.groups'))
            else:
                errors =  form.errors
                if(errors['nom_role'] != None):
                    flash("Champ 'Nom' vide, veillez à le remplir afin de valider le formulaire. ")
        return render_template('group.html', form = form)
    else :
        group = TRoles.get_one(id_role)
        if request.method =='GET':
            form = process(form,group)
        if request.method == 'POST':
            if form.validate_on_submit() and form.validate():
                form_group = pops(form.data)
                form_group['id_role'] = group['id_role']
                TRoles.update(form_group)
                return redirect(url_for('groupe.groups'))
            else:
                errors =  form.errors
                if(errors['nom_role'] != None):
                    flash("Champ 'Nom' vide, veillez à le remplir afin de valider le formulaire. ")
        return render_template('group.html', form = form)



  
@route.route('groups/members/<id_groupe>', methods=['GET','POST'])
def membres(id_groupe):

    """
    Route affichant la liste des roles n'appartenant pas au groupe vis à vis de ceux qui appartiennent à celui ci.
    Avec pour paramètre un id de groupe (id_role)
    Retourne un template avec pour paramètres:
                                            - une entête des tableaux --> fLine
                                            - le nom des colonnes de la base --> data
                                            - liste des roles n'appartenant pas au groupe --> table
                                            - liste des roles appartenant au groupe --> table2
                                            - variable qui permet a jinja de colorer une ligne si celui-ci est un groupe --> group 
    """

    users_in_group = TRoles.test_group(TRoles.get_user_in_group(id_groupe))
    users_out_group = TRoles.test_group(TRoles.get_user_out_group(id_groupe))
    print(users_in_group)
    print(users_out_group)
    header = ['ID', 'Nom']
    data = ['id_role','full_name']
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        new_users_in_group = data["tab_add"]
        new_users_out_group = data["tab_del"]
        CorRoles.add_cor(id_groupe,new_users_in_group)
        CorRoles.del_cor(id_groupe,new_users_out_group)
    return render_template("tobelong.html", fLine = header, data = data, table = users_out_group, table2 = users_in_group, group = 'groupe'  )




@route.route('groups/delete/<id_groupe>', methods=['GET','POST'])
def delete(id_groupe):

    """
    Route qui supprime un groupe dont l'id est donné en paramètres dans l'url
    Retourne une redirection vers la liste de groupe
    """

    TRoles.delete(id_groupe)
    return redirect(url_for('groupe.groups'))


def pops(form):

    """
    Methode qui supprime les éléments indésirables du formulaires
    Avec pour paramètre un formulaire
    """

    form.pop('submit')
    form.pop('csrf_token')
    return form


def process(form,group):
      
    """
    Methode qui rempli le formulaire par les données de l'éléments concerné
    Avec pour paramètres un formulaire et un groupe 
    """

    form.nom_role.process_data(group['nom_role'])
    form.desc_role.process_data(group['desc_role'])
    return form



# @route.route('test')
# def test():
#     print(TRoles.testGroup(TRoles.concat()))
#     return ""
    
    #  NON UTILISE
# @route.route('/groupe', methods=['GET','POST'])
# def groupe():
#     form = groupeforms.Groupe()
#     form.groupe.process_data(True)
#     if request.method == 'POST':
#         if form.validate_on_submit() and form.validate():
#             form_group = form.data
#             form_group.pop('id_role')
#             form_group.pop('csrf_token')
#             form_group.pop('submit')            
#             TRoles.post(form_group)
#             return redirect(url_for('groupe.groupes'))
#         else:
#             flash(form.errors)
#     return render_template('groupe.html', form = form)




# @route.route('groups/update/<id_groupe>', methods=['GET','POST'])
# def groupe_unique(id_groupe):
#     entete = ['ID groupe', 'nom', 'description' ]
#     colonne = ['id_role', 'nom_role', 'desc_role']
#     filters = [{'col': 'groupe', 'filter': 'True'}]
#     contenu = TRoles.get_all(colonne,filters)
#     #test
#     groupe = TRoles.get_one(id_groupe)
#     form = groupeforms.Groupe()
#     form.groupe.process_data(True)
#     if request.method == 'POST':
#         if form.validate_on_submit() and form.validate():
#             form_group = form.data
#             form_group['id_role'] = groupe['id_role']
#             form_group.pop('csrf_token')
#             form_group.pop('submit')
#             TRoles.update(form_group)
#             return redirect(url_for('groupe.groupes'))
#         else:
#             flash(form.errors)
#     return render_template('affichebase.html', entete = entete , ligne = colonne, table = contenu ,  cle = "id_role", cheminM = "/groups/update/", cheminS = "/groups/delete/", test ='groupe.html',form = form, nom_role = groupe['nom_role'], desc_role = groupe['desc_role'])



   
    
    # contenu = CorRoles.get_all(colonne,filters)
    # print(contenu)
    # print(contenu[0]["t_roles"]['identifiant'])


# @route.route('/mbgroupe/<id_groupe>', methods=['GET','POST'])
# def mbgroupe(id_groupe):
#     entete = ['identifiant', 'id role', 'prenom role', 'nom role']
#     colonne = ['identifiant','id_role','prenom_role', 'nom_role']
#     q = db.session.query(TRoles)
#     q = q.join(CorRoles)
#     q = q.filter(id_groupe == CorRoles.id_role_groupe  )
#     [data.as_dict(True) for data in q.all()]
#     return render_template('affichebase.html', entete = entete , ligne = colonne, table = [data.as_dict(True) for data in q.all()] , cle = "", cheminM = "", cheminS = "" )
      