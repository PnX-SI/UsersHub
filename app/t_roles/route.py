from flask import (
    current_app,
    redirect,
    url_for,
    render_template,
    Blueprint,
    request,
    flash,
    jsonify,
)
import re
import sqlalchemy as sa
from time import perf_counter

from pypnusershub import routes as fnauth
from pypnusershub.db.models import check_and_encrypt_password

from app.t_roles import forms as t_rolesforms
from app.models import TRoles, Bib_Organismes, CorRoles
from app.observability import set_request_observability_fields
from app.utils.utils_all import strigify_dict
from app.env import db


URL_APPLICATION = current_app.config["URL_APPLICATION"]

route = Blueprint("user", __name__)

USER_LIST_DT_COLUMNS = [
    {"data": "id_role"},
    {"data": "identifiant"},
    {"data": "nom_role"},
    {"data": "prenom_role"},
    {"data": "email"},
    {"data": "nom_organisme"},
    {"data": "remarques"},
    {"data": "active"},
    {"data": "pass_plus"},
    {"data": "pass_md5"},
    {"data": "action_password", "orderable": False, "searchable": False},
    {"data": "action_info", "orderable": False, "searchable": False},
    {"data": "action_update", "orderable": False, "searchable": False},
    {"data": "action_delete", "orderable": False, "searchable": False},
]


def _is_datatables_request():
    return request.args.get("draw") is not None


def _normalize_user_boolean(value):
    return "Oui" if value else "Non"


def _build_user_action(path, title, icon, button_class="secondary"):
    return (
        f'<a href="{path}">'
        f'<button type="submit" class="btn btn-{button_class} btn-sm " title="{title}">'
        f'<i class="fa {icon} font-medium" aria-hidden="true" title="{title}"></i>'
        f"</button>"
        f"</a>"
    )


def _build_delete_user_action(path, title):
    return (
        f'<button onClick="deleteRaw(\'{path}\')" type="submit" class="btn btn-danger btn-sm">'
        f'<i class="fa fa-trash font-medium" aria-hidden="true" title="{title}"></i>'
        f"</button>"
    )


def _serialize_user_list_row(row):
    user_id = row.id_role
    pass_action_title = (
        "Modifier le mot de passe"
        if row.pass_plus or row.pass_md5
        else "Ajouter un mot de passe"
    )
    pass_action_class = "secondary" if row.pass_plus or row.pass_md5 else "light"

    return {
        "id_role": user_id,
        "identifiant": row.identifiant or "",
        "nom_role": row.nom_role or "",
        "prenom_role": row.prenom_role or "",
        "email": row.email or "",
        "nom_organisme": row.nom_organisme or "",
        "remarques": row.remarques or "",
        "active": "True" if row.active else "False",
        "pass_plus": _normalize_user_boolean(row.pass_plus),
        "pass_md5": _normalize_user_boolean(row.pass_md5),
        "action_password": _build_user_action(
            f"{URL_APPLICATION}/user/pass/{user_id}",
            pass_action_title,
            "fa-key",
            button_class=pass_action_class,
        ),
        "action_info": _build_user_action(
            f"{URL_APPLICATION}/user/info/{user_id}", "Voir", "fa-eye"
        ),
        "action_update": _build_user_action(
            f"{URL_APPLICATION}/user/update/{user_id}",
            "Editer un utilisateur",
            "fa-pencil",
        ),
        "action_delete": _build_delete_user_action(
            f"{URL_APPLICATION}/users/delete/{user_id}", "Supprimer un utilisateur"
        ),
    }


def _build_users_list_query():
    return (
        db.session.query(
            TRoles.id_role.label("id_role"),
            TRoles.identifiant.label("identifiant"),
            TRoles.nom_role.label("nom_role"),
            TRoles.prenom_role.label("prenom_role"),
            TRoles.email.label("email"),
            Bib_Organismes.nom_organisme.label("nom_organisme"),
            TRoles.remarques.label("remarques"),
            TRoles.active.label("active"),
            TRoles.pass_plus.label("pass_plus"),
            TRoles.pass_md5.label("pass_md5"),
        )
        .outerjoin(Bib_Organismes, Bib_Organismes.id_organisme == TRoles.id_organisme)
        .filter(TRoles.groupe.is_(False))
    )


def _apply_users_list_search(query, search_value):
    if not search_value:
        return query

    pattern = f"%{search_value.strip()}%"
    return query.filter(
        sa.or_(
            TRoles.identifiant.ilike(pattern),
            TRoles.nom_role.ilike(pattern),
            TRoles.prenom_role.ilike(pattern),
            TRoles.email.ilike(pattern),
            TRoles.remarques.ilike(pattern),
            Bib_Organismes.nom_organisme.ilike(pattern),
        )
    )


def _apply_users_list_status_filter(query, status_value):
    normalized = (status_value or "all").strip().lower()
    if normalized == "true":
        return query.filter(TRoles.active.is_(True))
    if normalized == "false":
        return query.filter(
            sa.or_(TRoles.active.is_(False), TRoles.active.is_(None))
        )
    return query


def _render_user_form(form, id_role=None):
    return render_template(
        "user.html",
        form=form,
        title="Formulaire Utilisateur",
        id_role=id_role,
        autocomplete_organism_url=url_for("api.autocomplete_organisms"),
    )


def _flash_form_errors(errors):
    flash(strigify_dict(errors), "error")


def _coerce_optional_organism_id(raw_organism_id):
    if raw_organism_id in (None, "", "-1"):
        return None
    try:
        return int(raw_organism_id)
    except (TypeError, ValueError):
        return None


def _encrypt_password_fields(password, confirmation):
    return check_and_encrypt_password(
        password,
        confirmation,
        current_app.config["PASS_METHOD"] == "md5"
        or current_app.config["FILL_MD5_PASS"],
    )


def _replace_user_groups(id_role, groups):
    cor_role_to_delete = CorRoles.get_all(
        params=[{"col": "id_role_utilisateur", "filter": id_role}],
        as_model=True,
    )
    for cor_role in cor_role_to_delete:
        db.session.delete(cor_role)
    for group in groups:
        db.session.add(CorRoles(id_role_groupe=group, id_role_utilisateur=id_role))
    db.session.commit()


def _apply_users_list_ordering(query):
    order_column_index = request.args.get("order[0][column]", default=1, type=int)
    order_direction = request.args.get("order[0][dir]", default="asc", type=str)
    requested_column = request.args.get(
        f"columns[{order_column_index}][data]",
        default=USER_LIST_DT_COLUMNS[min(order_column_index, len(USER_LIST_DT_COLUMNS) - 1)]["data"],
        type=str,
    )

    sortable_columns = {
        "id_role": TRoles.id_role,
        "identifiant": sa.func.lower(sa.func.coalesce(TRoles.identifiant, "")),
        "nom_role": sa.func.lower(sa.func.coalesce(TRoles.nom_role, "")),
        "prenom_role": sa.func.lower(sa.func.coalesce(TRoles.prenom_role, "")),
        "email": sa.func.lower(sa.func.coalesce(TRoles.email, "")),
        "nom_organisme": sa.func.lower(sa.func.coalesce(Bib_Organismes.nom_organisme, "")),
        "remarques": sa.func.lower(sa.func.coalesce(TRoles.remarques, "")),
        "active": TRoles.active,
        "pass_plus": sa.func.coalesce(TRoles.pass_plus, ""),
        "pass_md5": sa.func.coalesce(TRoles.pass_md5, ""),
    }
    sort_expr = sortable_columns.get(requested_column, sortable_columns["identifiant"])
    sort_expr = sort_expr.desc() if order_direction == "desc" else sort_expr.asc()
    return query.order_by(sort_expr, TRoles.id_role.asc())


def _users_list_datatables_response():
    draw = request.args.get("draw", default=1, type=int)
    start = max(request.args.get("start", default=0, type=int), 0)
    length = request.args.get("length", default=25, type=int)
    search_value = request.args.get("search[value]", default="", type=str)
    status_filter = request.args.get("status_filter", default="all", type=str)

    base_query = _build_users_list_query()
    total_count = (
        db.session.query(sa.func.count(TRoles.id_role))
        .filter(TRoles.groupe.is_(False))
        .scalar()
    )
    filtered_query = _apply_users_list_status_filter(base_query, status_filter)
    filtered_query = _apply_users_list_search(filtered_query, search_value)
    filtered_count = filtered_query.order_by(None).count()
    ordered_query = _apply_users_list_ordering(filtered_query)

    page_size = filtered_count if length < 0 else length
    fetch_started_at = perf_counter()
    rows = ordered_query.offset(start).limit(page_size).all()
    fetch_duration_ms = int((perf_counter() - fetch_started_at) * 1000)

    prepare_started_at = perf_counter()
    data = [_serialize_user_list_row(row) for row in rows]
    prepare_duration_ms = int((perf_counter() - prepare_started_at) * 1000)

    set_request_observability_fields(
        rendered_object_count=len(data),
        rendered_object_label="users_list_page",
        list_fetch_duration_ms=fetch_duration_ms,
        list_prepare_duration_ms=prepare_duration_ms,
        list_total_count=total_count,
        list_filtered_count=filtered_count,
        users_list_fetch_duration_ms=fetch_duration_ms,
        users_list_prepare_duration_ms=prepare_duration_ms,
        users_list_total_count=total_count,
        users_list_filtered_count=filtered_count,
        users_list_status_filter=status_filter,
    )

    return jsonify(
        {
            "draw": draw,
            "recordsTotal": total_count,
            "recordsFiltered": filtered_count,
            "data": data,
        }
    )


@route.route("users/list", methods=["GET"])
@fnauth.check_auth(
    3,
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
    ]  # noqa
    if _is_datatables_request():
        return _users_list_datatables_response()

    return render_template(
        "table_database.html",
        fLine=fLine,
        line=columns,
        table=[],
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
        datatable_server_side=True,
        datatable_ajax_url=url_for("user.users"),
        datatable_columns=USER_LIST_DT_COLUMNS,
        datatable_order=[[1, "asc"]],
        datatable_page_length=25,
        datatable_extra_filters=[
            {
                "id": "users-status-filter",
                "name": "status_filter",
                "label": "Statut utilisateur",
                "value": "all",
                "options": [
                    {"value": "all", "label": "Tous"},
                    {"value": "true", "label": "Actifs"},
                    {"value": "false", "label": "Inactifs"},
                ],
            }
        ],
    )


@route.route("user/add/new", methods=["GET", "POST"])
@route.route("user/update/<id_role>", methods=["GET", "POST"])
@fnauth.check_auth(
    6,
)
def addorupdate(id_role=None):
    """
    Route affichant un formulaire vierge ou non (selon l'url) pour ajouter ou mettre à jour un utilisateurs
    L'envoie du formulaire permet l'ajout ou la mise à jour de l'utilisateur dans la base
    Retourne un template accompagné du formulaire pré-rempli ou non selon le paramètre id_role
    Une fois le formulaire validé on retourne une redirection vers la liste des utilisateurs
    """
    form = t_rolesforms.Utilisateur()
    form.a_groupe.choices = sorted(
        TRoles.choix_group("id_role", "nom_role", aucun=None),
        key=lambda choice: (choice[1] or "").casefold(),
    )

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
            form_user.pop("organisme_label", None)

            raw_organism_id = form_user.get("id_organisme")
            form_user["id_organisme"] = _coerce_optional_organism_id(raw_organism_id)
            if (
                raw_organism_id not in (None, "", "-1")
                and form_user["id_organisme"] is None
            ):
                _flash_form_errors(
                    {"id_organisme": ["L'organisme sélectionné est invalide."]}
                )
                return _render_user_form(form, id_role=id_role)

            # if a password is set
            # check they are the same
            if form.pass_plus.data:
                try:
                    form_user["pass_plus"], form_user["pass_md5"] = _encrypt_password_fields(
                        form.pass_plus.data,
                        form.mdpconf.data,
                    )
                except Exception as exp:
                    flash(str(exp), "error")
                    return _render_user_form(form, id_role=id_role)

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
            if id_role:
                _replace_user_groups(new_role.id_role, groups)
            elif len(groups) > 0:
                for group in groups:
                    db.session.add(
                        CorRoles(
                            id_role_groupe=group,
                            id_role_utilisateur=new_role.id_role,
                        )
                    )
                db.session.commit()
            return redirect(url_for("user.users"))

        else:
            _flash_form_errors(form.errors)
    return _render_user_form(form, id_role=id_role)


@route.route("user/pass/<id_role>", methods=["GET", "POST"])
@fnauth.check_auth(
    6,
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
    # Build title
    role_fullname = buildUserFullName(myuser)
    title = f"Changer le mot de passe de l'utilisateur '{role_fullname}'"

    if request.method == "POST":
        if form.validate_on_submit() and form.validate():
            form_user = pops(form.data, False)
            form_user.pop("id_role")
            # check if passwords are the same
            if form.pass_plus.data:
                try:
                    form_user["pass_plus"], form_user["pass_md5"] = _encrypt_password_fields(
                        form.pass_plus.data, form.mdpconf.data
                    )
                except Exception as exp:
                    _flash_form_errors({"password": [str(exp)]})
                    return render_template(
                        "user_pass.html",
                        form=form,
                        title=title,
                        id_role=id_role,
                    )
            form_user["id_role"] = id_role
            TRoles.update(form_user)
            return redirect(url_for("user.users"))
        else:
            _flash_form_errors(form.errors)

    return render_template(
        "user_pass.html",
        form=form,
        title=title,
        id_role=id_role,
    )


@route.route("users/delete/<id_role>", methods=["GET", "POST"])
@fnauth.check_auth(
    6,
)
def deluser(id_role):
    """
    Route qui supprime un utilisateurs dont l'id est donné en paramètres dans l'url
    Retourne une redirection vers la liste d'utilisateurs
    """

    TRoles.delete(id_role)
    return redirect(url_for("user.users"))


@route.route("user/info/<id_role>", methods=["GET", "POST"])
@fnauth.check_auth(6)
def info(id_role):
    user = TRoles.get_one(id_role)
    organisme = (
        Bib_Organismes.get_one(user["id_organisme"]) if user["id_organisme"] else None
    )
    additional_fields = (
        user.get("champs_addi") if isinstance(user.get("champs_addi"), dict) else {}
    )
    fallback_organism_name = additional_fields.get("organisme")
    fullname = buildUserFullName(user)
    groups = TRoles.get_user_groups(id_role)
    lists = TRoles.get_user_lists(id_role)
    rights = TRoles.get_user_app_profils(id_role)
    return render_template(
        "info_user.html",
        user=user,
        organisme=organisme,
        fullname=fullname,
        groups=groups,
        lists=lists,
        rights=rights,
        user_additional_fields=additional_fields,
        user_additional_field_exclude_keys=["organisme"] if fallback_organism_name else [],
        fallback_organism_name=fallback_organism_name,
        pathU=URL_APPLICATION + "/user/update/",
    )


def buildUserFullName(user):
    fullname = []
    if user["nom_role"]:
        fullname.append(user["nom_role"].upper())
    if user["prenom_role"]:
        fullname.append(user["prenom_role"].title())
    return " ".join(fullname)


@route.app_template_filter()
def pretty_json_key(key):
    return re.sub("([a-z])([A-Z])", r"\g<1> \g<2>", key)


def pops(form, with_group=True):
    """
    Methode qui supprime les éléments indésirables du formulaires
    Avec pour paramètre un formulaire
    """
    form = dict(form)
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
    form.id_organisme.process_data(
        "" if user["id_organisme"] is None else str(user["id_organisme"])
    )
    organisme_label = ""
    if user["id_organisme"]:
        organisme = Bib_Organismes.get_one(user["id_organisme"])
        if organisme:
            organisme_label = organisme["nom_organisme"] or ""
    form.organisme_label.process_data(organisme_label)
    form.nom_role.process_data(user["nom_role"])
    form.prenom_role.process_data(user["prenom_role"])
    form.email.process_data(user["email"])
    form.remarques.process_data(user["remarques"])
    form.identifiant.process_data(user["identifiant"])
    form.a_groupe.process_data(groups)
    return form


@route.route("test", methods=["GET", "POST"])
def test(id_role):
    fLine = [{"key": "test1", "label": "Test 1"}, {"key": "test2", "label": "Test 2"}]

    tab = [{"test1": "test1", "test2": "Test 1"}, {"test1": "test2", "test2": "Test 2"}]
    return render_template("generic_table.html", fLine=fLine, table=tab)
