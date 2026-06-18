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
from app.liste import forms as listeforms
from app.models import TListes, CorRoleListe, TRoles
from app.utils.utils_all import strigify_dict

URL_REDIRECT = current_app.config["URL_REDIRECT"]
URL_APPLICATION = current_app.config["URL_APPLICATION"]


route = Blueprint("liste", __name__)

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


def _build_list_members_query(id_liste, panel, pending_add_ids, pending_del_ids):
    query = _base_role_members_query()
    pending_add_query = _base_role_members_query().filter(TRoles.id_role.in_(pending_add_ids))
    pending_del_query = _base_role_members_query().filter(TRoles.id_role.in_(pending_del_ids))

    if panel == "selected":
        query = (
            query.join(CorRoleListe, CorRoleListe.id_role == TRoles.id_role)
            .filter(CorRoleListe.id_liste == id_liste)
        )
        if pending_del_ids:
            query = query.filter(~TRoles.id_role.in_(pending_del_ids))
        if pending_add_ids:
            query = query.union(pending_add_query)
        return query

    subquery = (
        ~db.session.query(CorRoleListe)
        .filter(CorRoleListe.id_liste == id_liste)
        .filter(CorRoleListe.id_role == TRoles.id_role)
        .exists()
    )
    query = query.filter(subquery)
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


def _list_members_datatables_response(id_liste):
    panel = request.args.get("panel", default="available", type=str)
    draw = request.args.get("draw", default=1, type=int)
    start = max(request.args.get("start", default=0, type=int), 0)
    length = request.args.get("length", default=25, type=int)
    search_value = request.args.get("search[value]", default="", type=str)
    pending_add_ids = _parse_pending_ids("pending_add")
    pending_del_ids = _parse_pending_ids("pending_del")

    base_query = _build_list_members_query(id_liste, panel, pending_add_ids, pending_del_ids).subquery()
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


@route.route("lists/list", methods=["GET", "POST"])
@fnauth.check_auth(
    3,
)
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

    fLine = ["ID", "Code", "Nom", "Description"]
    columns = ["id_liste", "code_liste", "nom_liste", "desc_liste"]
    contents = TListes.get_all(order_by="nom_liste")
    return render_template(
        "table_database.html",
        fLine=fLine,
        line=columns,
        table=contents,
        key="id_liste",
        pathI=URL_APPLICATION + "/list/info/",
        pathU=URL_APPLICATION + "/list/update/",
        pathD=URL_APPLICATION + "/list/delete/",
        pathA=URL_APPLICATION + "/list/add/new",
        pathP=URL_APPLICATION + "/list/members/",
        name="une liste",
        name_list="Listes",
        otherCol="True",
        Members="Membres",
        see="True",
    )


@route.route("list/add/new", defaults={"id_liste": None}, methods=["GET", "POST"])
@route.route("list/update/<id_liste>", methods=["GET", "POST"])
@fnauth.check_auth(
    6,
)
def addorupdate(id_liste):
    """
    Route affichant un formulaire vierge ou non (selon l'url) pour ajouter ou mettre à jour une liste
    L'envoie du formulaire permet l'ajout ou la maj de la liste dans la base
    Retourne un template accompagné d'un formulaire pré-rempli ou non selon le paramètre id_liste
    Une fois le formulaire validé on retourne une redirection vers la liste des listes
    """

    form = listeforms.List()
    if id_liste == None:
        if request.method == "POST":
            if form.validate_on_submit() and form.validate():
                form_list = pops(form.data)
                form_list.pop("id_liste")
                TListes.post(form_list)
                return redirect(url_for("liste.lists"))
        return render_template("list.html", form=form, title="Formulaire Liste")
    else:
        list = TListes.get_one(id_liste)
        if request.method == "GET":
            form = process(form, list)
        if request.method == "POST":
            if form.validate_on_submit() and form.validate():
                form_list = pops(form.data)
                form_list["id_liste"] = list["id_liste"]
                TListes.update(form_list)
                return redirect(url_for("liste.lists"))
            else:
                flash(strigify_dict(form.errors))
        return render_template("list.html", form=form, title="Formulaire Liste")


@route.route("list/members/<id_liste>", methods=["GET", "POST"])
@fnauth.check_auth(
    6,
)
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

    mylist = TListes.get_one(id_liste)
    header = ["ID", "Nom"]
    if request.method == "POST":
        data = request.get_json()
        new_users_in_list = data["tab_add"]
        new_users_out_list = data["tab_del"]
        try:
            CorRoleListe.add_cor(id_liste, new_users_in_list)
            CorRoleListe.del_cor(id_liste, new_users_out_list)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        return jsonify({"redirect": url_for("liste.lists")}), 200
    if _is_datatables_request():
        return _list_members_datatables_response(id_liste)
    return render_template(
        "tobelong.html",
        fLine=header,
        info="Membres de la liste '" + mylist["nom_liste"] + "'",
        membership_mode=True,
        available_table_id="user",
        selected_table_id="adding_table",
        data_ajax_url=url_for("liste.membres", id_liste=id_liste),
        table_columns=MEMBER_TABLE_COLUMNS,
        available_title="Utilisateurs disponibles",
        selected_title="Membres de la liste",
    )


@route.route("list/delete/<id_liste>", methods=["GET", "POST"])
@fnauth.check_auth(
    6,
)
def delete(id_liste):
    """
    Route qui supprime une liste dont l'id est donné en paramètres dans l'url
    Retourne une redirection vers la liste des listes
    """
    TListes.delete(id_liste)
    return redirect(url_for("liste.lists"))


@route.route("list/info/<id_liste>", methods=["GET"])
@fnauth.check_auth(3)
def info(id_liste):
    mylist = TListes.get_one(id_liste)
    members = (
        db.session.query(CorRoleListe).filter(CorRoleListe.id_liste == id_liste).all()
    )
    return render_template("info_list.html", mylist=mylist, members=members)


def pops(form):
    """
    Methode qui supprime les éléments indésirables du formulaires
    Avec pour paramètre un formulaire
    """

    form.pop("submit")
    form.pop("csrf_token")
    return form


def process(form, list):
    """
    Methode qui rempli le formulaire par les données de l'éléments concerné
    Avec pour paramètres un formulaire et une liste
    """

    form.nom_liste.process_data(list["nom_liste"])
    form.code_liste.process_data(list["code_liste"])
    form.desc_liste.process_data(list["desc_liste"])
    return form
