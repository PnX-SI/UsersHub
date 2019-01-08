from flask import (
    redirect, url_for, render_template,
    Blueprint, request, flash
)

from flask_bcrypt import (
    generate_password_hash
)

from pypnusershub import routes as fnauth

from app.env import URL_REDIRECT
from app.t_roles import forms as t_rolesforms
from app.models import (
    TRoles, Bib_Organismes, CorRoles
)
from app.utils.utils_all import strigify_dict
from app.env import db

from config import config
route = Blueprint('user', __name__)


@route.route('users/list', methods=['GET'])
@fnauth.check_auth(3, False, URL_REDIRECT)
def users():

    """
    Route qui affiche la liste des utilisateurs
    Retourne un template avec pour paramètres :
                                            - une entête de tableau --> fLine
                                            - le nom des colonnes de la base --> line
                                            - le contenu du tableau --> table
                                            - le chemin de mise à jour --> pathU
                                            - le chemin de suppression --> pathD
                                            - le chemin d'ajout --> pathA
                                            - le chemin de la page d'information --> pathI
                                            - une clé (clé primaire dans la plupart des cas) --> key
                                            - un nom (nom de la table) pour le bouton ajout --> name
                                            - un nom de listes --> name_list
                                            - ajoute une colonne pour accéder aux infos de l'utilisateur --> see
    """
    fLine = ['Id', 'Identifiant', 'Nom', 'Prenom', 'Email', 'Organisme', 'Remarques', 'Actif', 'pass']  # noqa
    columns = ['id_role', 'identifiant', 'nom_role', 'prenom_role', 'email', 'nom_organisme', 'remarques', 'active', 'pass_plus']  # noqa
    filters = [{'col': 'groupe', 'filter': 'False'}]
    contents = TRoles.get_all(columns, filters)
    print(contents)
    tab = []
    for data in contents:
        data['nom_organisme'] = data['organisme_rel']['nom_organisme'] if data.get('organisme_rel') else None
        if data['pass_plus'] == '' or  data['pass_plus'] is None:
            data['pass_plus'] = 'Non'
        else:
            data['pass_plus'] = 'Oui'
        tab.append(data)

    return render_template(
        "table_database.html",
        fLine=fLine,
        line=columns,
        table=tab,
        see="False",
        key="id_role",
        pathI=config.URL_APPLICATION + "/user/info/",
        pathU=config.URL_APPLICATION + "/user/update/",
        pathD=config.URL_APPLICATION + "/users/delete/",
        pathA=config.URL_APPLICATION + "/user/add/new",
        pathZ=config.URL_APPLICATION + "/user/pass/",
        passCol='True',
        name="un utilisateur",
        name_list="Utilisateurs"
    )


@route.route('user/add/new', methods=['GET', 'POST'])
@route.route('user/update/<id_role>', methods=['GET', 'POST'])
@fnauth.check_auth(6, False, URL_REDIRECT)
def addorupdate(id_role=None):
    """
    Route affichant un formulaire vierge ou non (selon l'url) pour ajouter ou mettre à jour un utilisateurs
    L'envoie du formulaire permet l'ajout ou la mise à jour de l'utilisateur dans la base
    Retourne un template accompagné du formulaire pré-rempli ou non selon le paramètre id_role
    Une fois le formulaire validé on retourne une redirection vers la liste des utilisateurs
    """
    form = t_rolesforms.Utilisateur()
    form.id_organisme.choices = Bib_Organismes.choixSelect(
        'id_organisme',
        'nom_organisme'
    )
    form.a_groupe.choices = TRoles.choix_group('id_role', 'nom_role', aucun=None)

    if id_role is not None:
        user = TRoles.get_one(id_role, as_model=True)
        user_as_dict = user.as_dict_full_name()
        # format group to prepfil the form
        formated_groups = [group.id_role for group in TRoles.get_users_groupe(id_role)]
        if request.method == 'GET':
            form = process(form, user_as_dict, formated_groups)

    if request.method == 'POST':
        if form.validate_on_submit() and form.validate():
            groups = form.data['a_groupe']
            form_user = pops(form.data)
            form_user['groupe'] = False
            form_user.pop('id_role')

            # if a password is set
            # check they are the same
            if form.pass_plus.data:
                try:
                    (
                        form_user['pass_plus'], form_user['pass_md5']
                    ) = TRoles.set_password(
                        form.pass_plus.data, form.mdpconf.data
                    )
                except Exception as exp:
                    flash(str(exp))
                    return render_template(
                        'user.html', form=form, title="Formulaire Utilisateur"
                    )

            if id_role is not None:
                #HACK a l'update on remet a la main les mdp
                # car on les masque dans le form
                form_user['pass_plus'] = user.pass_plus
                form_user['pass_md5'] = user.pass_md5
                form_user['id_role'] = user.id_role
                new_role = TRoles.update(form_user)
            else:
                new_role = TRoles.post(form_user)
            # set groups
            if len(groups) > 0:
                if id_role:
                    #first delete all groups of the user
                    cor_role_to_delete = CorRoles.get_all(
                        params=[{'col': 'id_role_utilisateur', 'filter': id_role}],
                        as_model=True
                    )
                    print(cor_role_to_delete)
                    for cor_role in cor_role_to_delete:
                        db.session.delete(cor_role)
                    db.session.commit()
                for group in groups:
                    # add new groups
                    new_group = CorRoles(id_role_groupe=group, id_role_utilisateur=new_role.id_role)
                    db.session.add(new_group)
                db.session.commit()
            return redirect(url_for('user.users'))

        else:
            flash(strigify_dict(form.errors))
    return render_template(
        'user.html', form=form, title="Formulaire Utilisateur", id_role=id_role
    )

@route.route('user/pass/<id_role>', methods=['GET', 'POST'])
@fnauth.check_auth(6, False, URL_REDIRECT)
def updatepass(id_role=None):
    """
    Route affichant un formulaire permettant de changer le pass des utilisateurs
    L'envoie du formulaire permet la mise à jour du pass de l'utilisateur dans la base
    Retourne un template accompagné du formulaire pré-rempli ou non selon le paramètre id_role
    Une fois le formulaire validé on retourne une redirection vers la liste des utilisateurs
    """
    form = t_rolesforms.UserPass()
    myuser = TRoles.get_one(id_role)
    
    if request.method == 'POST':
        if form.validate_on_submit() and form.validate():
            form_user = pops(form.data)
            form_user.pop('id_role')
            # check if passwords are the same
            if form.pass_plus.data:
                try:
                    (
                        form_user['pass_plus'], form_user['pass_md5']
                    ) = TRoles.set_password(
                        form.pass_plus.data, form.mdpconf.data
                    )
                except Exception as exp:
                    flash({'password':[exp]})
                    return render_template(
                        'user_pass.html', form=form, title="Changer le mot de passe de l'utilisateur '" + myuser['nom_role'] + ' ' + myuser['prenom_role'] + "'", id_role=id_role
                    )
            form_user['id_role'] = id_role
            TRoles.update(form_user)
            return redirect(url_for('user.users'))
        else:
            flash(strigify_dict(form.errors))

    return render_template(
        'user_pass.html', form=form, title="Changer le mot de passe de l'utilisateur '" + myuser['nom_role'] + ' ' + myuser['prenom_role'] + "'", id_role=id_role
    )


@route.route('users/delete/<id_role>', methods=['GET', 'POST'])
@fnauth.check_auth(6, False, URL_REDIRECT)
def deluser(id_role):
    """
    Route qui supprime un utilisateurs dont l'id est donné en paramètres dans l'url
    Retourne une redirection vers la liste d'utilisateurs
    """
    TRoles.delete(id_role)
    return redirect(url_for('user.users'))


# @route.route('user/info/<id_role>', methods=['GET', 'POST'])
# @fnauth.check_auth(6, False, URL_REDIRECT)
# def get_info(id_role):
#     user = TRoles.get_one(id_role)
#     d_group = CorRoles.get_all(recursif=True, as_model=True)
#     d_group = d_group.filter(CorRoles.id_role_utilisateur == id_role)
#     group = [data.as_dict() for data in d_group.all()]
#     tab_g = []
#     if group != None:
#         for g in group:
#             tab_g.append(TRoles.get_one(g['id_role_groupe'])["nom_role"])
#     org = Bib_Organismes.get_one(user['id_organisme'])['nom_organisme']
#     d_tag = CorRoleTag.get_all(recursif=True, as_model=True)
#     d_tag = d_tag.filter(CorRoleTag.id_role == id_role)
#     tag = [data.as_dict() for data in d_tag.all()]
#     tab_t = []
#     if tag != None:
#         for t in tag:
#             tab_t.append(TTags.get_one(t['id_tag'])['tag_name'])
#     cruved = get_cruved_one(id_role)
#     print(cruved)
#     if not cruved:
#         id_app = None
#     else:
#         id_app = cruved[0]['id_application']
#     f_lines_cruved = ['Application', 'Create', 'Read', 'Update', 'Validate', 'Export', 'Delete']  # noqa
#     columns_cruved = ['nom_application', 'C', 'R', 'U', 'V', 'E', 'D']
#     return render_template(
#         "info_user.html",
#         elt=user,
#         group=tab_g,
#         org=org,
#         tag=tab_t,
#         fLineCruved=f_lines_cruved,
#         lineCruved=columns_cruved,
#         tableCruved=cruved,
#         id_r=id_role,
#         id_app=id_app,
#         pathU=config.URL_APPLICATION + '/CRUVED/update/',
#         pathUu='/'
#     )


def pops(form):
    """
    Methode qui supprime les éléments indésirables du formulaires
    Avec pour paramètre un formulaire
    """
    form.pop('mdpconf')
    form.pop('submit')
    form.pop('csrf_token')
    form.pop('a_groupe')
    return form


def process(form, user, groups):
    """
    Methode qui rempli le formulaire par les données de l'éléments concerné
    Avec pour paramètres un formulaire, un user et les groupes auxquels il appartient
    """
    form.active.process_data(user['active'])
    form.id_organisme.process_data(user['id_organisme'])
    form.nom_role.process_data(user['nom_role'])
    form.prenom_role.process_data(user['prenom_role'])
    form.email.process_data(user['email'])
    form.remarques.process_data(user['remarques'])
    form.identifiant.process_data(user['identifiant'])
    form.a_groupe.process_data(groups)
    return form
