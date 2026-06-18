"""
Route des Organismes
"""

from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    request,
    flash,
    current_app,
    jsonify,
)
import sqlalchemy as sa
from time import perf_counter

from pypnusershub import routes as fnauth

from app.bib_organismes import forms as bib_organismeforms
from app.env import db
from app.models import Bib_Organismes, TRoles
from app.observability import set_request_observability_fields
from app.utils.utils_all import strigify_dict


URL_APPLICATION = current_app.config["URL_APPLICATION"]
route = Blueprint("organisme", __name__)

ORGANISM_LIST_DT_COLUMNS = [
    {"data": "id_organisme"},
    {"data": "nom_organisme"},
    {"data": "adresse_organisme"},
    {"data": "cp_organisme"},
    {"data": "ville_organisme"},
    {"data": "tel_organisme"},
    {"data": "fax_organisme"},
    {"data": "email_organisme"},
    {"data": "action_info", "orderable": False, "searchable": False},
    {"data": "action_update", "orderable": False, "searchable": False},
    {"data": "action_delete", "orderable": False, "searchable": False},
]


def _is_datatables_request():
    return request.args.get("draw") is not None


def _has_organism_additional_data_column():
    cache = current_app.extensions.setdefault("usershub_optional_columns", {})
    cache_key = "utilisateurs.bib_organismes.additional_data"
    if cache_key not in cache:
        try:
            columns = sa.inspect(db.engine).get_columns(
                "bib_organismes", schema="utilisateurs"
            )
            cache[cache_key] = any(
                column["name"] == "additional_data" for column in columns
            )
        except sa.exc.SQLAlchemyError:
            current_app.logger.warning(
                "Unable to inspect optional column utilisateurs.bib_organismes.additional_data",
                exc_info=True,
            )
            cache[cache_key] = False
    return cache[cache_key]


def _get_organism_additional_fields(id_organisme):
    if not _has_organism_additional_data_column():
        return {}

    additional_data = db.session.execute(
        sa.text(
            """
            SELECT additional_data
            FROM utilisateurs.bib_organismes
            WHERE id_organisme = :id_organisme
            """
        ),
        {"id_organisme": id_organisme},
    ).scalar_one_or_none()
    return additional_data if isinstance(additional_data, dict) else {}


def _build_organism_action(path, title, icon, button_class="secondary"):
    return (
        f'<a href="{path}">'
        f'<button type="submit" class="btn btn-{button_class} btn-sm " title="{title}">'
        f'<i class="fa {icon} font-medium" aria-hidden="true" title="{title}"></i>'
        f"</button>"
        f"</a>"
    )


def _build_delete_organism_action(path, title):
    return (
        f'<button onClick="deleteRaw(\'{path}\')" type="submit" class="btn btn-danger btn-sm">'
        f'<i class="fa fa-trash font-medium" aria-hidden="true" title="{title}"></i>'
        f"</button>"
    )


def _build_organisms_query():
    return db.session.query(
        Bib_Organismes.id_organisme.label("id_organisme"),
        Bib_Organismes.nom_organisme.label("nom_organisme"),
        Bib_Organismes.adresse_organisme.label("adresse_organisme"),
        Bib_Organismes.cp_organisme.label("cp_organisme"),
        Bib_Organismes.ville_organisme.label("ville_organisme"),
        Bib_Organismes.tel_organisme.label("tel_organisme"),
        Bib_Organismes.fax_organisme.label("fax_organisme"),
        Bib_Organismes.email_organisme.label("email_organisme"),
    )


def _apply_organisms_search(query, search_value):
    if not search_value:
        return query

    pattern = f"%{search_value.strip()}%"
    return query.filter(
        sa.or_(
            Bib_Organismes.nom_organisme.ilike(pattern),
            Bib_Organismes.adresse_organisme.ilike(pattern),
            Bib_Organismes.cp_organisme.ilike(pattern),
            Bib_Organismes.ville_organisme.ilike(pattern),
            Bib_Organismes.tel_organisme.ilike(pattern),
            Bib_Organismes.fax_organisme.ilike(pattern),
            Bib_Organismes.email_organisme.ilike(pattern),
        )
    )


def _apply_organisms_ordering(query):
    order_column_index = request.args.get("order[0][column]", default=1, type=int)
    requested_column = request.args.get(
        f"columns[{order_column_index}][data]",
        default=ORGANISM_LIST_DT_COLUMNS[
            min(order_column_index, len(ORGANISM_LIST_DT_COLUMNS) - 1)
        ]["data"],
        type=str,
    )
    order_direction = request.args.get("order[0][dir]", default="asc", type=str)

    sortable_columns = {
        "id_organisme": Bib_Organismes.id_organisme,
        "nom_organisme": sa.func.lower(sa.func.coalesce(Bib_Organismes.nom_organisme, "")),
        "adresse_organisme": sa.func.lower(
            sa.func.coalesce(Bib_Organismes.adresse_organisme, "")
        ),
        "cp_organisme": sa.func.lower(sa.func.coalesce(Bib_Organismes.cp_organisme, "")),
        "ville_organisme": sa.func.lower(
            sa.func.coalesce(Bib_Organismes.ville_organisme, "")
        ),
        "tel_organisme": sa.func.lower(sa.func.coalesce(Bib_Organismes.tel_organisme, "")),
        "fax_organisme": sa.func.lower(sa.func.coalesce(Bib_Organismes.fax_organisme, "")),
        "email_organisme": sa.func.lower(
            sa.func.coalesce(Bib_Organismes.email_organisme, "")
        ),
    }
    sort_expr = sortable_columns.get(requested_column, sortable_columns["nom_organisme"])
    sort_expr = sort_expr.desc() if order_direction == "desc" else sort_expr.asc()
    return query.order_by(sort_expr, Bib_Organismes.id_organisme.asc())


def _serialize_organism_row(row):
    organism_id = row.id_organisme
    return {
        "id_organisme": organism_id,
        "nom_organisme": row.nom_organisme or "",
        "adresse_organisme": row.adresse_organisme or "",
        "cp_organisme": row.cp_organisme or "",
        "ville_organisme": row.ville_organisme or "",
        "tel_organisme": row.tel_organisme or "",
        "fax_organisme": row.fax_organisme or "",
        "email_organisme": row.email_organisme or "",
        "action_info": _build_organism_action(
            f"{URL_APPLICATION}/organism/info/{organism_id}", "Voir", "fa-eye"
        ),
        "action_update": _build_organism_action(
            f"{URL_APPLICATION}/organism/update/{organism_id}",
            "Editer un organisme",
            "fa-pencil",
        ),
        "action_delete": _build_delete_organism_action(
            f"{URL_APPLICATION}/organisms/delete/{organism_id}",
            "Supprimer un organisme",
        ),
    }


def _organisms_datatables_response():
    draw = request.args.get("draw", default=1, type=int)
    start = max(request.args.get("start", default=0, type=int), 0)
    length = request.args.get("length", default=25, type=int)
    search_value = request.args.get("search[value]", default="", type=str)

    base_query = _build_organisms_query()
    total_count = db.session.query(sa.func.count(Bib_Organismes.id_organisme)).scalar()
    filtered_query = _apply_organisms_search(base_query, search_value)
    filtered_count = filtered_query.order_by(None).count()
    ordered_query = _apply_organisms_ordering(filtered_query)

    page_size = filtered_count if length < 0 else length
    fetch_started_at = perf_counter()
    rows = ordered_query.offset(start).limit(page_size).all()
    fetch_duration_ms = int((perf_counter() - fetch_started_at) * 1000)

    prepare_started_at = perf_counter()
    data = [_serialize_organism_row(row) for row in rows]
    prepare_duration_ms = int((perf_counter() - prepare_started_at) * 1000)

    set_request_observability_fields(
        rendered_object_count=len(data),
        rendered_object_label="organisms_list_page",
        list_fetch_duration_ms=fetch_duration_ms,
        list_prepare_duration_ms=prepare_duration_ms,
        list_total_count=total_count,
        list_filtered_count=filtered_count,
    )

    return jsonify(
        {
            "draw": draw,
            "recordsTotal": total_count,
            "recordsFiltered": filtered_count,
            "data": data,
        }
    )


@route.route("organisms/list", methods=["GET", "POST"])
@fnauth.check_auth(
    3,
)
def organisms():
    """
    Route qui affiche la liste des Organismes
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
        "ID",
        "Nom",
        "Adresse",
        "Code postal",
        "Ville",
        "Telephone",
        "Fax",
        "Email",
    ]
    columns = [
        "id_organisme",
        "nom_organisme",
        "adresse_organisme",
        "cp_organisme",
        "ville_organisme",
        "tel_organisme",
        "fax_organisme",
        "email_organisme",
    ]
    if _is_datatables_request():
        return _organisms_datatables_response()

    return render_template(
        "table_database.html",
        table=[],
        fLine=fLine,
        line=columns,
        key="id_organisme",
        pathI=URL_APPLICATION + "/organism/info/",
        pathU=URL_APPLICATION + "/organism/update/",
        pathD=URL_APPLICATION + "/organisms/delete/",
        pathA=URL_APPLICATION + "/organism/add/new",
        name="un organisme",
        name_list="Organismes",
        see="True",
        datatable_server_side=True,
        datatable_ajax_url=url_for("organisme.organisms"),
        datatable_columns=ORGANISM_LIST_DT_COLUMNS,
        datatable_order=[[1, "asc"]],
        datatable_page_length=25,
    )


@route.route(
    "organism/add/new", defaults={"id_organisme": None}, methods=["GET", "POST"]
)
@route.route("organism/update/<id_organisme>", methods=["GET", "POST"])
@fnauth.check_auth(
    6,
)
def addorupdate(id_organisme):
    """
    Route affichant un formulaire vierge ou non (selon l'url) pour ajouter ou mettre à jour un organisme
    L'envoie du formulaire permet l'ajout ou la mise à jour de l'éléments dans la base
    Retourne un template accompagné du formulaire
    Une fois le formulaire validé on retourne une redirection vers la liste d'organisme
    """

    form = bib_organismeforms.Organisme()
    if id_organisme == None:
        if request.method == "POST":
            if form.validate_on_submit() and form.validate():
                form_org = pops(form.data)
                form_org.pop("id_organisme")
                Bib_Organismes.post(form_org)
                return redirect(url_for("organisme.organisms"))
            else:
                flash(strigify_dict(form.errors), "error")
    else:
        org = Bib_Organismes.get_one(id_organisme)
        if request.method == "GET":
            form = bib_organismeforms.Organisme(**org)
        if request.method == "POST":
            if form.validate_on_submit() and form.validate():
                form_org = pops(form.data)
                form_org["id_organisme"] = org["id_organisme"]
                Bib_Organismes.update(form_org)
                return redirect(url_for("organisme.organisms"))
            else:
                flash(strigify_dict(form.errors), "error")
    return render_template("organism.html", form=form, title="Formulaire Organisme")


@route.route("organisms/delete/<id_organisme>", methods=["GET", "POST"])
@fnauth.check_auth(
    6,
)
def delete(id_organisme):
    """
    Route qui supprime un organisme dont l'id est donné en paramètres dans l'url
    Retourne une redirection vers la liste d'organismes
    """

    Bib_Organismes.delete(id_organisme)
    return redirect(url_for("organisme.organisms"))


@route.route("organism/info/<id_organisme>", methods=["GET"])
@fnauth.check_auth(
    3,
)
def info(id_organisme):
    org = Bib_Organismes.get_one(id_organisme)
    q = TRoles.get_all(
        as_model=True,
        params=[
            {"col": "active", "filter": True},
            {"col": "id_organisme", "filter": id_organisme},
        ],
        order_by="nom_role",
    )
    users = [data.as_dict_full_name() for data in q]
    additional_fields = _get_organism_additional_fields(id_organisme)

    return render_template(
        "info_organisme.html",
        org=org,
        users=users,
        organism_additional_fields=additional_fields,
    )


def pops(form):
    """
    Methode qui supprime les éléments indésirables du formulaires
    Avec pour paramètre un formulaire
    """
    form.pop("submit")
    form.pop("csrf_token")
    return form
