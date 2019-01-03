from flask import (
    redirect, url_for, render_template,
    Blueprint, request, flash, jsonify
)
from pypnusershub import routes as fnauth

from app.env import URL_REDIRECT
from app.liste import forms as listeforms
from app.models import TListes, CorRoleListe, TRoles
from config import config

route = Blueprint('liste', __name__)


@route.route('lists/list', methods=['GET', 'POST'])
@fnauth.check_auth(3, False, URL_REDIRECT)
def lists():
    """
    Route qui affiche la liste des listes
    Retourne un template avec pour paramètres :
        - une entête de tableau --> fLine
        - le nom des colonnes de la base --> line
        - le contenu du tableau --> table
        - le chemin de mise à jour --> pathU
        - le chemin de suppression --> pathD
        - le chemin d'ajout --> pathA
        - le chemin des membres de la liste --> pathP
        - une clé (clé primaire dans la plupart des cas) --> key
        - un nom (nom de la table) pour le bouton ajout --> name
        - un nom de liste --> name_list
        - ajoute une colonne de bouton ('True' doit être de type string)--> otherCol
        - nom affiché sur le bouton --> Members
    """

    fLine = ['ID', 'Code', 'Nom', 'Description']
    columns = ['id_liste', 'code_liste', 'nom_liste', 'desc_liste']
    contents = TListes.get_all()
    return render_template(
        'table_database.html',
        fLine=fLine,
        line=columns,
        table=contents,
        key="id_liste",
        pathI=config.URL_APPLICATION + '/list/info/',
        pathU=config.URL_APPLICATION + "/list/update/",
        pathD=config.URL_APPLICATION + "/list/delete/",
        pathA=config.URL_APPLICATION + '/list/add/new',
        pathP=config.URL_APPLICATION + '/list/members/',
        name="une liste",
        name_list="Listes",
        otherCol='True',
        Members="Membres",
        see='False'
    )


@route.route('list/add/new', defaults={'id_liste': None}, methods=['GET', 'POST'])
@route.route('list/update/<id_liste>', methods=['GET', 'POST'])
@fnauth.check_auth(6, False, URL_REDIRECT)
def addorupdate(id_liste):
    """
    Route affichant un formulaire vierge ou non (selon l'url) pour ajouter ou mettre à jour une liste
    L'envoie du formulaire permet l'ajout ou la maj de la liste dans la base
    Retourne un template accompagné d'un formulaire pré-rempli ou non selon le paramètre id_liste
    Une fois le formulaire validé on retourne une redirection vers la liste des listes
    """

    form = listeforms.List()
    if id_liste == None:
        if request.method == 'POST':
            if form.validate_on_submit() and form.validate():
                form_list = pops(form.data)
                form_list.pop('id_liste')
                TListes.post(form_list)
                return redirect(url_for('liste.lists'))
        return render_template('list.html', form=form, title="Formulaire Liste")
    else:
        list = TListes.get_one(id_liste)
        if request.method == 'GET':
            form = process(form, list)
        if request.method == 'POST':
            if form.validate_on_submit() and form.validate():
                form_list = pops(form.data)
                form_list['id_liste'] = list['id_liste']
                TListes.update(form_list)
                return redirect(url_for('liste.lists'))
            else:
                flash(form.errors)
        return render_template('list.html', form=form, title="Formulaire Liste")


@route.route('list/members/<id_liste>', methods=['GET', 'POST'])
@fnauth.check_auth(6, False, URL_REDIRECT)
def membres(id_liste):
    """
    Route affichant la liste des listes n'appartenant pas à la liste vis à vis de ceux qui appartiennent à celle-ci.
    Avec pour paramètre un id de liste (id_liste)
    Retourne un template avec pour paramètres:
        - une entête des tableaux --> fLine
        - le nom des colonnes de la base --> data
        - liste des listes n'appartenant pas à la liste --> table
        - liste des listes appartenant à la liste --> table2
    """

    users_in_list = TRoles.test_group(TRoles.get_user_in_list(id_liste))
    users_out_list = TRoles.test_group(TRoles.get_user_out_list(id_liste))
    mylist = TListes.get_one(id_liste)
    header = ['ID', 'Nom']
    data = ['id_role', 'full_name']
    if request.method == 'POST':
        data = request.get_json()
        new_users_in_list = data["tab_add"]
        new_users_out_list = data["tab_del"]
        try:
            CorRoleListe.add_cor(id_liste, new_users_in_list)
            CorRoleListe.del_cor(id_liste, new_users_out_list)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        return jsonify({'redirect': url_for('liste.lists')}), 200
    return render_template(
        "tobelong.html",
        fLine=header,
        data=data,
        table=users_out_list,
        table2=users_in_list,
        info="Membres de la liste '" + mylist['nom_liste'] + "'"
     )


@route.route('list/delete/<id_liste>', methods=['GET', 'POST'])
@fnauth.check_auth(6, False, URL_REDIRECT)
def delete(id_liste):
    """
    Route qui supprime une liste dont l'id est donné en paramètres dans l'url
    Retourne une redirection vers la liste des listes
    """

    TListes.delete(id_liste)
    return redirect(url_for('liste.lists'))


# @route.route('list/info/<id_liste>', methods=['GET', 'POST'])
# @fnauth.check_auth(3, False, URL_REDIRECT)
# def get_info(id_liste):
#     user = TListes.get_one(id_liste)
#     members = TListes.get_user_in_list(id_liste)
#     tab_usr = []
#     if members != None:
#         for usr in members:
#             tab_usr.append(usr["full_name"])
#     d_tag = CorRoleTag.get_all(recursif=True, as_model=True)
#     d_tag = d_tag.filter(CorRoleTag.id_liste == id_liste)
#     tag = [data.as_dict() for data in d_tag.all()]
#     tab_t = []
#     if tag != None:
#         for t in tag:
#             tab_t.append(TTags.get_one(t['id_tag'])['tag_name'])
#     Cruved = get_cruved_one(id_liste)
#     fLineCruved = ['Application', 'Create', 'Read', 'Update', 'Validate', 'Export', 'Delete']
#     if Cruved != []:
#         columnsCruved = ['nom_application', 'C', 'R', 'U', 'V', 'E', 'D']
#         return render_template(
#             "info_list.html",
#             elt=user,
#             members=tab_usr,
#             tag=tab_t,
#             fLineCruved=fLineCruved,
#             lineCruved=columnsCruved,
#             tableCruved=Cruved,
#             id_r=id_liste,
#             id_app=Cruved[0]['id_application'],
#             pathU=config.URL_APPLICATION + '/CRUVED/update/',
#             pathUu='/'
#         )
#     else:
#         return render_template(
#             "info_list.html",
#             elt=user,
#             members=tab_usr,
#             tag=tab_t,
#             Cruved='False',
#             fLineCruved=fLineCruved
#          )


def pops(form):
    """
    Methode qui supprime les éléments indésirables du formulaires
    Avec pour paramètre un formulaire
    """

    form.pop('submit')
    form.pop('csrf_token')
    return form


def process(form, list):
    """
    Methode qui rempli le formulaire par les données de l'éléments concerné
    Avec pour paramètres un formulaire et une liste
    """

    form.nom_liste.process_data(list['nom_liste'])
    form.code_liste.process_data(list['code_liste'])
    form.desc_liste.process_data(list['desc_liste'])
    return form
