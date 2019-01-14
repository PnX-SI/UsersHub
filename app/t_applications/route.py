from flask import (
    redirect, url_for, render_template,
    Blueprint, request, flash, jsonify
)

from app.env import db, URL_REDIRECT
from app.t_applications import forms as t_applicationsforms
from app.models import (
    TApplications, TRoles, TProfils, 
    CorProfilForApp, CorRoleAppProfil
)
from config import config

from pypnusershub import routes as fnauth

route = Blueprint('application', __name__)


@route.route('applications/list', methods=['GET', 'POST'])
@fnauth.check_auth(
    3, 
    False, 
    redirect_on_expiration=URL_REDIRECT, 
    redirect_on_invalid_token=URL_REDIRECT
)
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
        pathP=config.URL_APPLICATION + "/application_roles_profil/",
        pathR=config.URL_APPLICATION + "/application/profils/",
        pathI=config.URL_APPLICATION + "/application/info/",
        name="une application",
        name_list="Applications",
        otherCol='True',
        Members="Gérer les utilisateurs",
        permissions="True",
        Right="Profils disponibles",
        see="True"
    )


@route.route('application/info/<id_application>', methods=['GET'])
@fnauth.check_auth(3, False, URL_REDIRECT)
def info(id_application):
    """
    Route qui retourne une fiche de l'application
    et des roles qui disposent de profils pour elle.
    """
    application = TApplications.get_one(id_application)
    users = db.session.query(CorRoleAppProfil).filter(CorRoleAppProfil.id_application == id_application).all()
    profils = db.session.query(CorProfilForApp).filter(CorProfilForApp.id_application == id_application)
    return render_template(
        'info_application.html',
        application=application,
        users=users,
        profils=profils
    )


@route.route('application/add/new', defaults={'id_application': None}, methods=['GET', 'POST'])
@route.route('application/update/<id_application>', methods=['GET', 'POST'])
@fnauth.check_auth(
    6, 
    False, 
    redirect_on_expiration=URL_REDIRECT, 
    redirect_on_invalid_token=URL_REDIRECT
)
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
            profils_in_app = TProfils.get_profils_in_app(id_application)
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
            profils=profils_in_app,
            id_application=id_application
            )


@route.route('application/delete/<id_application>', methods=['GET', 'POST'])
@fnauth.check_auth(
    6, 
    False, 
    redirect_on_expiration=URL_REDIRECT, 
    redirect_on_invalid_token=URL_REDIRECT
)
def delete(id_application):
    """
    Route qui supprime une application dont l'id est donné en paramètres dans l'URL
    Retourne une redirection vers la liste de groupe
    """
    TApplications.delete(id_application)
    return redirect(url_for('application.applications'))


@route.route('application/profils/<id_application>', methods=['GET', 'POST'])
@fnauth.check_auth(
    6, 
    False, 
    redirect_on_expiration=URL_REDIRECT, 
    redirect_on_invalid_token=URL_REDIRECT
)
def profils_for_app(id_application):
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
        try:
            CorProfilForApp.add_cor(id_application, new_profils)
            CorProfilForApp.del_cor(id_application, delete_profils)
        except Exception as e:
            return jsonify(str(e)), 500
        return jsonify({'redirect': url_for('application.applications')}), 200
    return render_template(
        'app_profils.html',
        fLine=header,
        data=data,
        table=profils_out_app,
        table2=profils_in_app,
        info="Profils utilisables dans l'application " + app['nom_application']
    )



@route.route('application_roles_profil/<int:id_application>', methods=['GET', 'POST'])
@fnauth.check_auth(
    6, 
    False, 
    redirect_on_expiration=URL_REDIRECT, 
    redirect_on_invalid_token=URL_REDIRECT
)
def profils_in_app(id_application):
    """
    Route affichant la liste des roles ayant un profil pour une application
    Retourne un template avec pour paramètres :
                                        - une entête de tableau --> fLine
                                        - le nom des colonnes de la base --> line
                                        - le contenu du tableau --> table
                                        - le chemin de mise à jour --> pathU
                                        - le chemin de suppression --> pathD
                                        - le chemin d'ajout --> pathA
                                        - une clé (clé primaire dans la plupart des cas) --> key
                                        - l'id_application pour construire l'url de redirection -> key2
                                        - un nom (nom de la table) pour le bouton ajout --> name
                                        - un nom de liste --> name_list
                                        - ajoute une colonne de bouton ('True doit être de type string) --> permissions
                                        - nom affiché sur le bouton --> Members
    """
    users_in_app = TRoles.get_user_profil_in_app(id_application)
    application = TApplications.get_one(id_application)

    fLine = ['Id', 'Role', 'Profil']
    columns = ['id_role', 'full_name', 'profil']

    return render_template(
        'table_database.html',
        table=users_in_app,
        fLine=fLine,
        line=columns,
        key="id_role",
        key2=id_application,
        pathU=config.URL_APPLICATION + "/application/update/role_profil/",
        pathD=config.URL_APPLICATION + "/application/delete/role_profil/",
        pathA=config.URL_APPLICATION + "/application/add/role_profil/",
        name="un role pour l'application {}".format(application['nom_application']),
        name_list="Role(s) de l'application {}".format(application['nom_application']),
    )

@route.route('application/add/role_profil/<int:id_application>', methods=['GET', 'POST'])
@route.route('application/update/role_profil/<int:id_role>/<int:id_application>', methods=['GET', 'POST'])
@fnauth.check_auth(
    6, 
    False, 
    redirect_on_expiration=URL_REDIRECT, 
    redirect_on_invalid_token=URL_REDIRECT
)
def add_or_update_profil_for_role_in_app(id_application, id_role=None):
    """
        add or update un profil sur une application
        on part du principe qu'un role ne peut avoir qu'un profil dans une application
        TODO: pour mettre plusieurs profil a un role dans une appli: 
        rajouter une clé primaire a cor_role_app_profil pour gérer l'update
    """
    form = t_applicationsforms.AppProfil(id_application)
    application = TApplications.get_one(id_application)
    role = None
    title = "Ajouter un profil l'application {}".format(application['nom_application'])
    if id_role:
        role = TRoles.get_one(id_role, as_model=True).as_dict_full_name()
        title = "Editer le profil de {} dans l'application {}".format(
            role['full_name'],
            application['nom_application']
        )
        # preremplissage du formulaire
        profil_in_app = CorRoleAppProfil.get_one(id_role, id_application)
        form.profil.process_data(profil_in_app.id_profil)
        form.role.process_data(str(id_role))
        # HACK ajout de l'utilisateur courant dans la liste déroulante
        # sinon le formulaire ne passe pas
        form.role.choices.append((id_role, role['full_name']))

    if request.method == 'POST':
        # set new id__profil
        form.profil.process_data(request.form['profil'])
        if form.validate() and form.validate_on_submit():
            try:
                if id_role:
                    # on supprime d'abbord le profil pour une app
                    CorRoleAppProfil.delete(
                        id_role=id_role,
                        id_application=id_application
                    )
                # et on post
                CorRoleAppProfil.post(
                    {
                        'id_role': form.data['role'],
                        'id_profil': form.data['profil'],
                        'id_application': id_application
                    }
                )
            except Exception as e:
                redirect(url_for('application.add_or_update_profil_for_role_in_app', id_application=id_application))
                flash("Une erreur s'est produite, {}".format(e), 'error')
            flash('Profil ajouté/edité avec succès')
            return redirect(url_for('application.profils_in_app', id_application=id_application))

    return render_template(
        'application_role_profil_form.html',
        title=title,
        form=form,
        application=application,
        id_role=id_role
    )


@route.route('application/delete/role_profil/<id_role>/<id_application>', methods=['GET', 'POST'])
@fnauth.check_auth(
    6, 
    False, 
    redirect_on_expiration=URL_REDIRECT, 
    redirect_on_invalid_token=URL_REDIRECT
)
def delete_cor_role_app_profil(id_role, id_application):
    try:
        CorRoleAppProfil.delete(id_role, id_application)
    except Exception:
        flash("Une erreur s'est produite", 'error')
    flash("Profil supprimé avec succès")
    return redirect(
        url_for(
            'application.profils_in_app', id_application=id_application
        )
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
