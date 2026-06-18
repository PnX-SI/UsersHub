from flask import (
    redirect,
    url_for,
    render_template,
    Blueprint,
    request,
    flash,
    jsonify,
    current_app,
)
import json
import sqlalchemy as sa
from pypnusershub import routes as fnauth

from app.env import db
from app.groupe import forms as groupeforms
from app.models import TRoles
from app.models import CorRoles
from app.utils.utils_all import strigify_dict


URL_REDIRECT = current_app.config["URL_REDIRECT"]
URL_APPLICATION = current_app.config["URL_APPLICATION"]

route = Blueprint("groupe", __name__)

MEMBER_TABLE_COLUMNS = [
    {"data": "select", "orderable": False, "searchable": False},
    {"data": "id_role"},
    {"data": "full_name"},
]


def _is_datatables_request():
    return request.args.get("draw") is not None


def _parse_pending_ids(name):
    raw_value = request.args.get(name, default="[]", type=str)
    try:
        values = json.loads(raw_value)
    except ValueError:
        return []
    ids = []
    for value in values:
        try:
            ids.append(int(value))
        except (TypeError, ValueError):
            continue
    return ids


def _build_membership_row(row):
    return {
        "select": '<input type="checkbox" class="membership-check">',
        "id_role": row.id_role,
        "full_name": row.full_name or "",
        "groupe": "True" if row.groupe else "False",
    }


def _base_role_members_query():
    return db.session.query(
        TRoles.id_role.label("id_role"),
        TRoles.groupe.label("groupe"),
        sa.func.concat(
            sa.func.coalesce(TRoles.nom_role, ""),
            sa.literal(" "),
            sa.func.coalesce(TRoles.prenom_role, ""),
        ).label("full_name"),
        TRoles.identifiant.label("identifiant"),
        TRoles.nom_role.label("nom_role"),
        TRoles.prenom_role.label("prenom_role"),
        TRoles.active.label("active"),
    )


def _build_group_members_query(id_groupe, panel, pending_add_ids, pending_del_ids):
    query = _base_role_members_query()
    pending_add_query = _base_role_members_query().filter(TRoles.id_role.in_(pending_add_ids))
    pending_del_query = _base_role_members_query().filter(TRoles.id_role.in_(pending_del_ids))

    if panel == "selected":
        query = (
            query.join(CorRoles, CorRoles.id_role_utilisateur == TRoles.id_role)
            .filter(CorRoles.id_role_groupe == id_groupe)
        )
        if pending_del_ids:
            query = query.filter(~TRoles.id_role.in_(pending_del_ids))
        if pending_add_ids:
            query = query.union(pending_add_query)
        return query

    subquery = db.session.query(CorRoles.id_role_utilisateur).filter(
        CorRoles.id_role_groupe == id_groupe
    )
    subquery2 = db.session.query(CorRoles.id_role_groupe).filter(
        CorRoles.id_role_utilisateur == id_groupe
    )
    query = (
        query.filter(TRoles.id_role != id_groupe)
        .filter(TRoles.id_role.notin_(subquery))
        .filter(TRoles.id_role.notin_(subquery2))
    )
    if pending_add_ids:
        query = query.filter(~TRoles.id_role.in_(pending_add_ids))
    if pending_del_ids:
        query = query.union(pending_del_query)
    return query


def _apply_members_search(query, search_value):
    if not search_value:
        return query
    pattern = f"%{search_value.strip()}%"
    return query.filter(
        sa.or_(
            sa.cast(sa.column("id_role"), sa.String).ilike(pattern),
            sa.func.coalesce(sa.column("full_name"), "").ilike(pattern),
            sa.func.coalesce(sa.column("identifiant"), "").ilike(pattern),
            sa.func.coalesce(sa.column("nom_role"), "").ilike(pattern),
            sa.func.coalesce(sa.column("prenom_role"), "").ilike(pattern),
        )
    )


def _apply_members_ordering(query):
    order_column_index = request.args.get("order[0][column]", default=2, type=int)
    requested_column = request.args.get(
        f"columns[{order_column_index}][data]",
        default=MEMBER_TABLE_COLUMNS[min(order_column_index, len(MEMBER_TABLE_COLUMNS) - 1)]["data"],
        type=str,
    )
    order_direction = request.args.get("order[0][dir]", default="asc", type=str)
    sortable_columns = {
        "id_role": sa.column("id_role"),
        "full_name": sa.func.lower(sa.func.coalesce(sa.column("full_name"), "")),
    }
    sort_expr = sortable_columns.get(requested_column, sortable_columns["full_name"])
    sort_expr = sort_expr.desc() if order_direction == "desc" else sort_expr.asc()
    return query.order_by(sort_expr, sa.column("id_role").asc())


def _group_members_datatables_response(id_groupe):
    panel = request.args.get("panel", default="available", type=str)
    draw = request.args.get("draw", default=1, type=int)
    start = max(request.args.get("start", default=0, type=int), 0)
    length = request.args.get("length", default=25, type=int)
    search_value = request.args.get("search[value]", default="", type=str)
    pending_add_ids = _parse_pending_ids("pending_add")
    pending_del_ids = _parse_pending_ids("pending_del")

    base_query = _build_group_members_query(id_groupe, panel, pending_add_ids, pending_del_ids).subquery()
    query = db.session.query(base_query)
    total_count = query.order_by(None).count()
    filtered_query = _apply_members_search(query, search_value)
    filtered_count = filtered_query.order_by(None).count()
    ordered_query = _apply_members_ordering(filtered_query)
    page_size = filtered_count if length < 0 else length
    rows = ordered_query.offset(start).limit(page_size).all()

    return jsonify(
        {
            "draw": draw,
            "recordsTotal": total_count,
            "recordsFiltered": filtered_count,
            "data": [_build_membership_row(row) for row in rows],
        }
    )


@route.route("groups/list", methods=["GET", "POST"])
@fnauth.check_auth(
    3,
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

    group = TRoles.get_one(id_groupe)
    header = ["ID", "Nom"]
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
    if _is_datatables_request():
        return _group_members_datatables_response(id_groupe)
    return render_template(
        "tobelong.html",
        fLine=header,
        info="Membres du groupe '" + group["nom_role"] + "'",
        membership_mode=True,
        available_table_id="user",
        selected_table_id="adding_table",
        data_ajax_url=url_for("groupe.membres", id_groupe=id_groupe),
        table_columns=MEMBER_TABLE_COLUMNS,
        available_title="Utilisateurs disponibles",
        selected_title="Membres du groupe",
    )


@route.route("group/delete/<id_groupe>", methods=["GET", "POST"])
@fnauth.check_auth(
    6,
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
