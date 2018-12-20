from flask import (
    redirect, url_for, render_template,
    Blueprint, request, flash
)

from app.env import URL_REDIRECT
from app.t_applications import forms as t_applicationsforms
from app.models import (
    TApplications, TRoles, TProfils, 
    CorProfilForApp, CorRoleAppProfil
)

from config import config

from pypnusershub import routes as fnauth

route = Blueprint('application', __name__)


@route.route('applications/list', methods=['GET', 'POST'])
@fnauth.check_auth(3, False, URL_REDIRECT)
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
                                            - ajoute une colonne de bouton ('True doit être de type string) --> permissions
                                            - nom affiché sur le bouton --> Members

    """

    fLine = ['ID', 'Code', 'Nom', 'Description']
    columns = ['id_application', 'code_application', 'nom_application', 'desc_application']
    contents = TApplications.get_all()
    for data in contents:
        if data['id_parent'] != None:
            parent = TApplications.get_one(data['id_parent'])
            data.update({'app_parent': parent['nom_application']})
        else:
            parent = ""
            data.update({'app_parent': parent})
    return render_template(
        'table_database.html',
        table=contents,
        fLine=fLine,
        line=columns,
        key="id_application",
        pathU=config.URL_APPLICATION + "/application/update/",
        pathD=config.URL_APPLICATION + "/application/delete/",
        pathA=config.URL_APPLICATION + "/application/add/new",
        pathP=config.URL_APPLICATION + "/application/rights/",
        name="une application",
        name_list="Applications",
        otherCol='True',
        Members="Gérer les utilisateurs",
        permissions="False",
    )


@route.route('application/add/new', defaults={'id_application': None}, methods=['GET', 'POST'])
@route.route('application/update/<id_application>', methods=['GET', 'POST'])
@fnauth.check_auth(6, False, URL_REDIRECT)
def addorupdate(id_application):
    """
    Route affichant un formulaire vierge ou non (selon l'url) pour ajouter ou mettre à jour une application
    L'envoie du formulaire permet l'ajout ou la maj d'une application dans la base
    Retourne un template accompagné d'un formulaire pré-rempli ou non selon le paramètre id_application
    Une fois le formulaire validé on retourne une redirection vers la liste d'application
    """

    form = t_applicationsforms.Application()
    form.id_parent.choices = TApplications.choixSelect('id_application', 'nom_application', 1)
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
        return render_template('application.html', form=form, title="Formulaire Application")
    else:
        application = TApplications.get_one(id_application)
        form.id_parent.choices.remove((
            application['id_application'],
            application['nom_application']
        ))
        if request.method == 'GET':
            if application['id_parent'] == None:
                form.id_parent.process_data(-1)
            else:
                form.id_parent.process_data(application['id_parent'])
            form_app = process(form, application)
        if request.method == 'POST':
            if form.validate_on_submit() and form.validate():
                form_app = pops(form.data)
                if form.id_parent.data == -1:
                    form_app['id_parent'] = None
                form_app['id_application'] = application['id_application']
                TApplications.update(form_app)
                return redirect(url_for('application.applications'))
        return render_template(
            'application.html',
             form=form,
             title="Formulaire Application",
             id_application=id_application
             )


@route.route('application/delete/<id_application>', methods=['GET', 'POST'])
@fnauth.check_auth(6, False, URL_REDIRECT)
def delete(id_application):
    """
    Route qui supprime une application dont l'id est donné en paramètres dans l'url
    Retourne une redirection vers la liste de groupe
    """

    TApplications.delete(id_application)
    return redirect(url_for('application.applications'))


@route.route('application/profils/<id_application>', methods=['GET', 'POST'])
@fnauth.check_auth(6, False, URL_REDIRECT)
def profils(id_application):
    """
    Route affichant la liste des profils utilisables par l'application et ceux disponibles.
    Avec pour paramètre un id d'application
    Retourne un template avec pour paramètres:
        - une entête des tableaux --> fLine
        - le nom des colonnes de la base --> data
        - liste des profils utilisables --> table
        - liste des profils non utilisables mais disponibles --> table2
    """
    profils_in_app = TProfils.get_profils_in_app(id_application)
    profils_out_app = TProfils.get_profils_out_app(id_application)
    header = ['ID', 'Profil']
    data = ['id_profil', 'nom_profil']
    app = TApplications.get_one(id_application)
    if request.method == 'POST':
        data = request.get_json()
        new_profils = data["tab_add"]
        delete_profils = data["tab_del"]
        CorProfilForApp.add_cor(id_application, new_profils)
        CorProfilForApp.del_cor(id_application, delete_profils)
    return render_template(
        'app_profils.html',
        fLine=header,
        data=data,
        table=profils_out_app,
        table2=profils_in_app,
        info="Profils utilisables dans l'application " + app['nom_application']
    )


@route.route('application/rights/<id_application>', methods=['GET', 'POST'])
@fnauth.check_auth(6, False, URL_REDIRECT)
def rights(id_application):
    """
    Route affichant le formulaire permettant de définir les permission des utilisateurs.
    Avec pour paramètre un id d'application
    Retourne un template avec pour paramètres:
        - une entête des tableaux --> fLine
        - le nom des colonnes de la base --> data
        - liste des roles sans permissions mais disponibles --> table
        - liste des roles avec des permissions --> table2
    """
    users_in_app = TRoles.get_user_profil_in_app(id_application)
    profils_in_app = [
        (profil.id_profil, profil.nom_profil)
        for profil in  TProfils.get_profils_in_app(id_application)
    ]
    for user in users_in_app:
        print(user)
    users_out_app = TRoles.get_user_profil_out_app(id_application)
    header = ['ID', 'Nom']
    data = ['id_role', 'full_name']
    app = TApplications.get_one(id_application)
    if request.method == 'POST':
        data = request.get_json()
        new_users = data["tab_add"]
        delete_users = data["tab_del"]
        CorRoleAppProfil.add_cor(id_application, new_users)
        CorRoleAppProfil.del_cor(id_application, delete_users)
    return render_template(
        'tobelong.html',
        fLine=header,
        data=data,
        table=users_out_app,
        table2=users_in_app,
        info="Permissions dans l'application " + app['nom_application'],
        profils_in_app=profils_in_app,
        app='True'
    )


def pops(form):
    """
    Methode qui supprime les éléments indésirables du formulaires
    Avec pour paramètre un formulaire
    """

    form.pop('csrf_token')
    form.pop('submit')
    return form


def process(form, application):
    """
    Methode qui rempli le formulaire par les données de l'éléments concerné
    Avec pour paramètres un formulaire et une application
    """

    form.nom_application.process_data(application['nom_application'])
    form.code_application.process_data(application['code_application'])
    form.desc_application.process_data(application['desc_application'])
    return form
