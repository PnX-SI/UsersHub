from flask import redirect, url_for, render_template, Blueprint, request, flash, jsonify, current_app
from pypnusershub import routes as fnauth

from app.groupe import forms as groupeforms
from app.models import TRoles
from app.models import CorRoles
from app.utils.utils_all import strigify_dict


URL_REDIRECT = current_app.config['URL_REDIRECT']
URL_APPLICATION = current_app.config['URL_APPLICATION']

route = Blueprint("groupe", __name__)


@route.route("groups/list", methods=["GET", "POST"])
@fnauth.check_auth(
    3,
    False,
    redirect_on_expiration=URL_REDIRECT,
    redirect_on_invalid_token=URL_REDIRECT,
)
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

    fLine = ["ID groupe", "nom", "description"]
    columns = ["id_role", "nom_role", "desc_role"]
    filters = [{"col": "groupe", "filter": "True"}]
    contents = TRoles.get_all(columns, filters, order_by="identifiant")
    return render_template(
        "table_database.html",
        fLine=fLine,
        line=columns,
        table=contents,
        key="id_role",
        pathI=URL_APPLICATION + "/group/info/",
        pathU=URL_APPLICATION + "/group/update/",
        pathD=URL_APPLICATION + "/group/delete/",
        pathA=URL_APPLICATION + "/group/add/new",
        pathP=URL_APPLICATION + "/group/members/",
        name="un groupe",
        name_list="Groupes",
        otherCol="True",
        Members="Membres",
        see="True",
    )


@route.route("group/add/new", methods=["GET", "POST"])
@route.route("group/update/<id_role>", methods=["GET", "POST"])
@fnauth.check_auth(
    6,
    False,
    redirect_on_expiration=URL_REDIRECT,
    redirect_on_invalid_token=URL_REDIRECT,
)
def addorupdate(id_role=None):

    """
    Route affichant un formulaire vierge ou non (selon l'url) pour ajouter ou mettre à jour un groupe
    L'envoie du formulaire permet l'ajout ou la maj du groupe dans la base
    Retourne un template accompagné d'un formulaire pré-rempli ou non selon le paramètre id_role
    Une fois le formulaire validé on retourne une redirection vers la liste de groupe
    """
    form = groupeforms.Group()
    form.groupe.process_data(True)
    if id_role == None:
        if request.method == "POST":
            if form.validate_on_submit() and form.validate():
                form_group = pops(form.data)
                form_group.pop("id_role")
                # set the group as active default
                form_group["active"] = True
                TRoles.post(form_group)
                return redirect(url_for("groupe.groups"))
            else:
                errors = form.errors
        return render_template("group.html", form=form, title="Formulaire Groupe")
    else:
        group = TRoles.get_one(id_role)
        if request.method == "GET":
            form = process(form, group)
        if request.method == "POST":
            if form.validate_on_submit() and form.validate():
                form_group = pops(form.data)
                form_group["id_role"] = group["id_role"]
                TRoles.update(form_group)
                return redirect(url_for("groupe.groups"))
            else:
                errors = form.errors
                flash(strigify_dict(errors), "error")
        return render_template("group.html", form=form, title="Formulaire Groupe")


@route.route("group/members/<id_groupe>", methods=["GET", "POST"])
@fnauth.check_auth(
    6,
    False,
    redirect_on_expiration=URL_REDIRECT,
    redirect_on_invalid_token=URL_REDIRECT,
)
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
    group = TRoles.get_one(id_groupe)
    header = ["ID", "Nom"]
    data = ["id_role", "full_name"]
    if request.method == "POST":
        data = request.get_json()
        new_users_in_group = data["tab_add"]
        new_users_out_group = data["tab_del"]
        try:
            CorRoles.add_cor(id_groupe, new_users_in_group)
            CorRoles.del_cor(id_groupe, new_users_out_group)
        except Exception as e:
            return jsonify(str(e)), 500
        return jsonify({"redirect": url_for("groupe.groups")}), 200
    return render_template(
        "tobelong.html",
        fLine=header,
        data=data,
        table=users_out_group,
        table2=users_in_group,
        group="groupe",
        info="Membres du groupe '" + group["nom_role"] + "'",
    )


@route.route("group/delete/<id_groupe>", methods=["GET", "POST"])
@fnauth.check_auth(
    6,
    False,
    redirect_on_expiration=URL_REDIRECT,
    redirect_on_invalid_token=URL_REDIRECT,
)
def delete(id_groupe):
    """
    Route qui supprime un groupe dont l'id est donné en paramètres dans l'url
    Retourne une redirection vers la liste de groupe
    """

    TRoles.delete(id_groupe)
    return redirect(url_for("groupe.groups"))


@route.route("group/info/<id_role>", methods=["GET", "POST"])
@fnauth.check_auth(
    3,
    False,
    redirect_on_expiration=URL_REDIRECT,
    redirect_on_invalid_token=URL_REDIRECT,
)
def info(id_role):
    group = TRoles.get_one(id_role)
    members = TRoles.get_user_in_group(id_role)
    lists = TRoles.get_user_lists(id_role)
    rights = TRoles.get_user_app_profils(id_role)
    return render_template(
        "info_group.html",
        group=group,
        members=members,
        lists=lists,
        rights=rights,
        pathU=URL_APPLICATION + "/group/update/",
    )


def pops(form):
    """
    Methode qui supprime les éléments indésirables du formulaires
    Avec pour paramètre un formulaire
    """

    form.pop("submit")
    form.pop("csrf_token")
    return form


def process(form, group):
    """
    Methode qui rempli le formulaire par les données de l'éléments concerné
    Avec pour paramètres un formulaire et un groupe
    """

    form.nom_role.process_data(group["nom_role"])
    form.desc_role.process_data(group["desc_role"])
    return form
