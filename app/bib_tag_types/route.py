from flask import (
    redirect, url_for, render_template,
    Blueprint, request, flash
)

from pypnusershub import routes as fnauth

from app.env import URL_REDIRECT

from app.bib_tag_types import forms as tag_typeforms
from app.models import BibTagTypes
from config import config

route = Blueprint('tags_types', __name__)

"""
Route des types de tag
"""


@route.route('tags_types/list', methods=['GET', 'POST'])
@fnauth.check_auth(3, False, URL_REDIRECT)
def tags_types():

    """
    Route qui affiche la liste des Types de tag
    Retourne un template avec pour paramètres :
        - une entête de tableau --> fLine
        - le nom des colonnes de la base --> line
        - le contenu du tableau --> table
        - le chemin de mise à jour --> pathU
        - le chemin de suppression --> pathD
        - le chemin d'ajout --> pathA
        - une clé (clé primaire dans la plupart des cas) --> key
        - un nom (nom de la table) pour le bouton ajout --> name
        - un nom de listes --> name_list
    """

    fLine = ['ID', 'Nom', 'Description']
    columns = ['id_tag_type','tag_type_name','tag_type_desc']
    contents = BibTagTypes.get_all()
    return render_template(
        'table_database.html',
        table=contents,
        fLine=fLine,
        line=columns,
        pathU=config.URL_APPLICATION + "/tag_type/update/",
        key="id_tag_type",
        pathD=config.URL_APPLICATION + "/tags_types/delete/",
        pathA=config.URL_APPLICATION + '/tag_type/add/new',
        name="type de tag",
        name_list="Types de Tags"
    )


@route.route('tag_type/add/new', defaults={'id_tag_type': None}, methods=['GET', 'POST'])
@route.route('tag_type/update/<id_tag_type>', methods=['GET','POST'])
@fnauth.check_auth(6, False, URL_REDIRECT)
def addorupdate(id_tag_type):

    """
    Route affichant un formulaire vierge ou non (selon l'url) pour ajouter ou mettre à jour un type de tag
    L'envoie du formulaire permet l'ajout ou la mise à jour de l'éléments dans la base
    Retourne un template accompagné du formulaire pré-rempli ou non selon le paramètre id_tag_type
    Une fois le formulaire validé on retourne une redirection vers la liste de type de tag
    """

    form = tag_typeforms.TagTypes()
    if id_tag_type == None:
        if request.method == 'POST':
            if form.validate() and form.validate_on_submit() :
                form_tagtypes = pops(form.data)
                BibTagTypes.post(form_tagtypes)
                return redirect(url_for('tags_types.tags_types'))
            else:
                errors =  form.errors
                if(errors['id_tag_type'] != None):
                    flash("Champ 'ID' vide, veillez à le remplir afin de valider le formulaire. ")
                if(errors['tag_type_name'] != None):
                    flash("Champ 'Nom' vide, veillez à le remplir afin de valider le formulaire. ")
                if(errors['tag_type_desc'] != None):
                    flash("Champ 'Description' vide, veillez à le remplir afin de valider le formulaire. ")
        return render_template('tagtypes.html', form=form, title="Formulaire Type Tag")
    else:
        tag_type = BibTagTypes.get_one(id_tag_type)
        if request.method == 'GET':
            form = process(form,tag_type)
        if request.method == 'POST':
            if form.validate_on_submit() and form.validate():
                form_tagtypes = pops(form.data)
                BibTagTypes.update(form_tagtypes)
                return redirect(url_for('tags_types.tags_types'))
            else:
                errors =  form.errors
                if(errors['id_tag_type'] != None):
                    flash("Champ 'ID' vide, veillez à le remplir afin de valider le formulaire. ")
                if(errors['tag_type_name'] != None):
                    flash("Champ 'Nom' vide, veillez à le remplir afin de valider le formulaire. ")
                if(errors['tag_type_desc'] != None):
                    flash("Champ 'Description' vide, veillez à le remplir afin de valider le formulaire. ")
        return render_template('tagtypes.html', form=form , title="Formulaire Type Tag")


@route.route('tags_types/delete/<id_tag_type>', methods=['GET', 'POST'])
@fnauth.check_auth(6, False, URL_REDIRECT)
def delete(id_tag_type):

    """
    Route qui supprime un type de tag dont l'id est donné en paramètres dans l'url
    Retourne une redirection vers la liste d'organismes
    """

    BibTagTypes.delete(id_tag_type)
    return redirect(url_for('tags_types.tags_types'))


def pops(form):

    """
    Methode qui supprime les éléments indésirables du formulaires
    Avec pour paramètre un formulaire
    """

    form.pop('submit')
    form.pop('csrf_token')
    return form


def process(form, tag_type):

    """
    Methode qui rempli le formulaire par les données de l'éléments concerné
    Avec pour paramètres un formulaire et un type de tag
    """

    form.id_tag_type.process_data(tag_type['id_tag_type'])
    form.tag_type_name.process_data(tag_type['tag_type_name'])
    form.tag_type_desc.process_data(tag_type['tag_type_desc'])
    return form
