from flask import (
    current_app,
    redirect,
    url_for,
    render_template,
    Blueprint,
    request,
    flash,
    current_app,
)

from pypnusershub import routes as fnauth
from pypnusershub.db.models import check_and_encrypt_password


from app.t_roles import forms as t_rolesforms
from app.models import TRoles, Bib_Organismes, CorRoles
from app.utils.utils_all import strigify_dict
from app.env import db


URL_REDIRECT = current_app.config["URL_REDIRECT"]
URL_APPLICATION = current_app.config["URL_APPLICATION"]

route = Blueprint("user", __name__)


@route.route("users/list", methods=["GET"])
@fnauth.check_auth(
    3,
    False,
    redirect_on_expiration=URL_REDIRECT,
    redirect_on_invalid_token=URL_REDIRECT,
    redirect_on_insufficient_right=URL_REDIRECT,
)
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
    fLine = [
        "Id",
        "Identifiant",
        "Nom",
        "Prenom",
        "Email",
        "Organisme",
        "Remarques",
        "Actif",
        "pass_plus",
        "pass_md5",
        "Autres",
    ]  # noqa
    columns = [
        "id_role",
        "identifiant",
        "nom_role",
        "prenom_role",
        "email",
        "nom_organisme",
        "remarques",
        "active",
        "pass_plus",
        "pass_md5",
        "champs_addi",
    ]  # noqa
    filters = [{"col": "groupe", "filter": "False"}]
    contents = TRoles.get_all(columns, filters, order_by="identifiant", order="asc")
    tab = []
    for data in contents:
        data["nom_organisme"] = (
            data["organisme_rel"]["nom_organisme"]
            if data.get("organisme_rel")
            else None
        )
        if data["pass_plus"] == "" or data["pass_plus"] is None:
            data["pass_plus"] = "Non"
        else:
            data["pass_plus"] = "Oui"
        if data["pass_md5"] == "" or data["pass_md5"] is None:
            data["pass_md5"] = "Non"
        else:
            data["pass_md5"] = "Oui"
        tab.append(data)

    return render_template(
        "table_database.html",
        fLine=fLine,
        line=columns,
        table=tab,
        see="True",
        key="id_role",
        pathI=URL_APPLICATION + "/user/info/",
        pathU=URL_APPLICATION + "/user/update/",
        pathD=URL_APPLICATION + "/users/delete/",
        pathA=URL_APPLICATION + "/user/add/new",
        pathZ=URL_APPLICATION + "/user/pass/",
        passPlusCol="True",
        passMd5Col="True",
        name="un utilisateur",
        name_list="Utilisateurs",
    )


@route.route("user/add/new", methods=["GET", "POST"])
@route.route("user/update/<id_role>", methods=["GET", "POST"])
@fnauth.check_auth(
    6,
    False,
    redirect_on_expiration=URL_REDIRECT,
    redirect_on_invalid_token=URL_REDIRECT,
)
def addorupdate(id_role=None):
    """
    Route affichant un formulaire vierge ou non (selon l'url) pour ajouter ou mettre à jour un utilisateurs
    L'envoie du formulaire permet l'ajout ou la mise à jour de l'utilisateur dans la base
    Retourne un template accompagné du formulaire pré-rempli ou non selon le paramètre id_role
    Une fois le formulaire validé on retourne une redirection vers la liste des utilisateurs
    """
    form = t_rolesforms.Utilisateur()
    form.id_organisme.choices = Bib_Organismes.choixSelect(
        "id_organisme", "nom_organisme", order_by="nom_organisme"
    )
    form.a_groupe.choices = TRoles.choix_group("id_role", "nom_role", aucun=None)

    if id_role is not None:
        user = TRoles.get_one(id_role, as_model=True)
        user_as_dict = user.as_dict_full_name()
        # format group to prepfil the form
        formated_groups = [group.id_role for group in TRoles.get_user_groups(id_role)]
        if request.method == "GET":
            form = process(form, user_as_dict, formated_groups)

    if request.method == "POST":
        if form.validate_on_submit() and form.validate():
            groups = form.data["a_groupe"]
            form_user = pops(form.data)
            form_user["groupe"] = False
            form_user.pop("id_role")

            # if a password is set
            # check they are the same
            if form.pass_plus.data:
                try:
                    (
                        form_user["pass_plus"],
                        form_user["pass_md5"],
                    ) = check_and_encrypt_password(
                        form.pass_plus.data,
                        form.mdpconf.data,
                        current_app.config["PASS_METHOD"] == "md5"
                        or current_app.config["FILL_MD5_PASS"],
                    )
                except Exception as exp:
                    flash(str(exp), "error")
                    return render_template(
                        "user.html", form=form, title="Formulaire Utilisateur"
                    )

            if id_role is not None:
                # HACK a l'update on remet a la main les mdp
                # car on les masque dans le form
                form_user["pass_plus"] = user.pass_plus
                form_user["pass_md5"] = user.pass_md5
                form_user["id_role"] = user.id_role
                new_role = TRoles.update(form_user)
            else:
                new_role = TRoles.post(form_user)
            # set groups
            if len(groups) > 0:
                if id_role:
                    # first delete all groups of the user
                    cor_role_to_delete = CorRoles.get_all(
                        params=[{"col": "id_role_utilisateur", "filter": id_role}],
                        as_model=True,
                    )
                    for cor_role in cor_role_to_delete:
                        db.session.delete(cor_role)
                    db.session.commit()
                for group in groups:
                    # add new groups
                    new_group = CorRoles(
                        id_role_groupe=group, id_role_utilisateur=new_role.id_role
                    )
                    db.session.add(new_group)
                db.session.commit()
            return redirect(url_for("user.users"))

        else:
            flash(strigify_dict(form.errors), "error")
    return render_template(
        "user.html", form=form, title="Formulaire Utilisateur", id_role=id_role
    )


@route.route("user/pass/<id_role>", methods=["GET", "POST"])
@fnauth.check_auth(
    6,
    False,
    redirect_on_expiration=URL_REDIRECT,
    redirect_on_invalid_token=URL_REDIRECT,
)
def updatepass(id_role=None):
    """
    Route affichant un formulaire permettant de changer le pass des utilisateurs
    L'envoie du formulaire permet la mise à jour du pass de l'utilisateur dans la base
    Retourne un template accompagné du formulaire pré-rempli ou non selon le paramètre id_role
    Une fois le formulaire validé on retourne une redirection vers la liste des utilisateurs
    """
    form = t_rolesforms.UserPass()
    myuser = TRoles.get_one(id_role)

    if request.method == "POST":
        if form.validate_on_submit() and form.validate():
            form_user = pops(form.data, False)
            form_user.pop("id_role")
            # check if passwords are the same
            if form.pass_plus.data:
                try:
                    (
                        form_user["pass_plus"],
                        form_user["pass_md5"],
                    ) = check_and_encrypt_password(
                        form.pass_plus.data,
                        form.mdpconf.data,
                        current_app.config["PASS_METHOD"] == "md5"
                        or current_app.config["FILL_MD5_PASS"],
                    )
                except Exception as exp:
                    flash({"password": [exp]}, "error")
                    return render_template(
                        "user_pass.html",
                        form=form,
                        title="Changer le mot de passe de l'utilisateur '"
                        + myuser["nom_role"]
                        + " "
                        + myuser["prenom_role"]
                        + "'",
                        id_role=id_role,
                    )
            form_user["id_role"] = id_role
            TRoles.update(form_user)
            return redirect(url_for("user.users"))
        else:
            flash(strigify_dict(form.errors), "error")

    return render_template(
        "user_pass.html",
        form=form,
        title="Changer le mot de passe de l'utilisateur '"
        + myuser["nom_role"]
        + " "
        + myuser["prenom_role"]
        + "'",
        id_role=id_role,
    )


@route.route("users/delete/<id_role>", methods=["GET", "POST"])
@fnauth.check_auth(
    6,
    False,
    redirect_on_expiration=URL_REDIRECT,
    redirect_on_invalid_token=URL_REDIRECT,
)
def deluser(id_role):
    """
    Route qui supprime un utilisateurs dont l'id est donné en paramètres dans l'url
    Retourne une redirection vers la liste d'utilisateurs
    """
    TRoles.delete(id_role)
    return redirect(url_for("user.users"))


@route.route("user/info/<id_role>", methods=["GET", "POST"])
@fnauth.check_auth(6, False, URL_REDIRECT)
def info(id_role):
    user = TRoles.get_one(id_role)
    organisme = (
        Bib_Organismes.get_one(user["id_organisme"]) if user["id_organisme"] else None
    )
    groups = TRoles.get_user_groups(id_role)
    lists = TRoles.get_user_lists(id_role)
    rights = TRoles.get_user_app_profils(id_role)
    return render_template(
        "info_user.html",
        user=user,
        organisme=organisme,
        groups=groups,
        lists=lists,
        rights=rights,
        pathU=URL_APPLICATION + "/user/update/",
    )


def pops(form, with_group=True):
    """
    Methode qui supprime les éléments indésirables du formulaires
    Avec pour paramètre un formulaire
    """
    form.pop("mdpconf")
    form.pop("submit")
    form.pop("csrf_token")
    if with_group:
        form.pop("a_groupe")
    return form


def process(form, user, groups):
    """
    Methode qui rempli le formulaire par les données de l'éléments concerné
    Avec pour paramètres un formulaire, un user et les groupes
     auxquels il appartient
    """
    form.active.process_data(user["active"])
    form.id_organisme.process_data(user["id_organisme"])
    form.nom_role.process_data(user["nom_role"])
    form.prenom_role.process_data(user["prenom_role"])
    form.email.process_data(user["email"])
    form.remarques.process_data(user["remarques"])
    form.identifiant.process_data(user["identifiant"])
    form.champs_addi.process_data(user["champs_addi"])
    form.a_groupe.process_data(groups)
    return form


@route.route("test", methods=["GET", "POST"])
def test(id_role):
    fLine = [{"key": "test1", "label": "Test 1"}, {"key": "test2", "label": "Test 2"}]

    tab = [{"test1": "test1", "test2": "Test 1"}, {"test1": "test2", "test2": "Test 2"}]
    return render_template("generic_table.html", fLine=fLine, table=tab)
