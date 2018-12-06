from flask import (
    Blueprint, redirect, url_for, render_template,
    request, flash
)

from pypnusershub import routes as fnauth

from app.env import URL_REDIRECT

from app import genericRepository
from app.bib_organismes import forms as bib_organismeforms
from app.models import Bib_Organismes, TRoles
from config import config


route = Blueprint('organisme', __name__)

"""
Route des Organismes
"""


@route.route('organisms/list', methods=['GET', 'POST'])
@fnauth.check_auth(3, False, URL_REDIRECT)
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

    fLine = ['ID', 'Nom',  'Adresse',  'Code_Postal',  'Ville',  'Telephone', 'Fax',  'Email']
    columns = [
        'id_organisme', 'nom_organisme', 'adresse_organisme',
        'cp_organisme', 'ville_organisme', 'tel_organisme',
        'fax_organisme', 'email_organisme'
    ]
    contents = Bib_Organismes.get_all(columns)
    return render_template(
        'table_database.html',
        table=contents,
        fLine=fLine,
        line=columns,
        pathI=config.URL_APPLICATION + '/organism/info/',
        pathU=config.URL_APPLICATION + '/organism/update/',
        key='id_organisme',
        pathD=config.URL_APPLICATION + '/organisms/delete/',
        pathA=config.URL_APPLICATION + '/organism/add/new',
        name="un organisme",
        name_list="Organismes",
        see='True'
    )


@route.route('organism/add/new', defaults={'id_organisme': None}, methods=['GET', 'POST'])
@route.route('organism/update/<id_organisme>', methods=['GET', 'POST'])
@fnauth.check_auth(6, False, URL_REDIRECT)
def addorupdate(id_organisme):
    """
    Route affichant un formulaire vierge ou non (selon l'url) pour ajouter ou mettre à jour un organisme
    L'envoie du formulaire permet l'ajout ou la mise à jour de l'éléments dans la base
    Retourne un template accompagné du formulaire
    Une fois le formulaire validé on retourne une redirection vers la liste d'organisme
    """

    form = bib_organismeforms.Organisme()
    if id_organisme == None:
        if request.method == 'POST':
            if form.validate_on_submit() and form.validate():
                form_org = pops(form.data)
                form_org.pop('id_organisme')
                Bib_Organismes.post(form_org)
                return redirect(url_for('organisme.organisms'))
            else:
                errors = form.errors
                if(errors['nom_organisme'] != None):
                    flash("Champ 'Nom Organisme' vide, veillez à le remplir afin de valider le formulaire. ")
    else:
        org = Bib_Organismes.get_one(id_organisme)
        if request.method == 'GET':
            form = process(form, org)
        if request.method == 'POST':
            if form.validate_on_submit() and form.validate():
                form_org = pops(form.data)
                form_org['id_organisme'] = org['id_organisme']
                Bib_Organismes.update(form_org)
                return redirect(url_for('organisme.organisms'))
            else:
                errors = form.errors
                if(errors['nom_organisme'] != None):
                    flash("Champ 'Nom Organisme' vide, veillez à le remplir afin de valider le formulaire. ")
    return render_template('organism.html', form=form, title="Formulaire Organisme")


@route.route('organisms/delete/<id_organisme>', methods=['GET', 'POST'])
@fnauth.check_auth(6, False, URL_REDIRECT)
def delete(id_organisme):
    """
    Route qui supprime un organisme dont l'id est donné en paramètres dans l'url
    Retourne une redirection vers la liste d'organismes
    """

    Bib_Organismes.delete(id_organisme)
    return redirect(url_for('organisme.organisms'))


# @route.route('organism/info/<id_organisme>', methods=['GET', 'POST'])
# @fnauth.check_auth(3, False, URL_REDIRECT)
# def get_info(id_organisme):
#     org = Bib_Organismes.get_one(id_organisme)
#     array_user = TRoles.get_all(as_model=True)
#     array_user = array_user.filter(TRoles.id_organisme == id_organisme)
#     array_user = [data.as_dict_full_name() for data in array_user.all()]
#     tab_u = []
#     for user in array_user:
#         tab_u.append(user['full_name'])
#     d_tag = CorOrganismeTag.get_all(recursif=True, as_model=True)
#     d_tag = d_tag.filter(CorOrganismeTag.id_organism == id_organisme)
#     tag = [data.as_dict() for data in d_tag.all()]
#     tab_t = []
#     if tag != None:
#         for t in tag:
#             tab_t.append(TTags.get_one(t['id_tag'])['tag_name'])

#     return render_template('info_org.html', elt=org, tab_u=tab_u, tag=tab_t)


def pops(form):

    """
    Methode qui supprime les éléments indésirables du formulaires
    Avec pour paramètre un formulaire
    """
    form.pop('submit')
    form.pop('csrf_token')
    return form

def process(form, org):

    """
    Methode qui rempli le formulaire par les données de l'éléments concerné
    Avec pour paramètres un formulaire et un organisme
    """

    form.nom_organisme.process_data(org['nom_organisme'])
    form.cp_organisme.process_data(org['cp_organisme'])
    form.adresse_organisme.process_data(org['adresse_organisme'])
    form.ville_organisme.process_data(org['ville_organisme'])
    form.tel_organisme.process_data(org['tel_organisme'])
    form.fax_organisme.process_data(org['fax_organisme'])
    form.email_organisme.process_data(org['email_organisme'])
    form.email_organisme.process_data(org['url_organisme'])
    form.email_organisme.process_data(org['url_logo'])
    return form
