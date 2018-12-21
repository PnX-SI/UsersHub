from flask import (
    redirect, url_for, render_template,
    Blueprint, request,  flash
)

from pypnusershub import routes as fnauth

from app.env import URL_REDIRECT
from app.t_profils import forms as t_profilsforms
from app.models import (
    TProfils, TApplications, CorProfilForApp,
    TRoles, Bib_Organismes, CorRoleAppProfil
)
from config import config

route = Blueprint('profils', __name__)

"""
Routes des profils
"""


@route.route('profils/list', methods=['GET', 'POST'])
@fnauth.check_auth(3, False, URL_REDIRECT)
def profils():
    """
    Route qui affiche la liste des profils
    Retourne un template avec pour paramètres :
                                            - une entête de tableau --> fLine
                                            - le nom des colonnes de la base --> line
                                            - le contenu du tableau --> table
                                            - le chemin de mise à jour --> pathU
                                            - le chemin de suppression --> pathD
                                            - le chemin d'ajout --> pathA
                                            - le chemin des roles du profil --> pathP
                                            - une clé (clé primaire dans la plupart des cas) --> key
                                            - un nom (nom de la table) pour le bouton ajout --> name
                                            - un nom de listes --> name_list
                                            - ajoute une colonne de bouton ('True' doit être de type string)--> otherCol
                                            - nom affiché sur le bouton --> Members
    """

    fLine = ['ID', 'CODE', 'Nom', 'Description']
    columns = ['id_profil',  'code_profil', 'nom_profil', 'desc_profil']
    tab = [data for data in TProfils.get_all()]
    return render_template(
        'table_database.html',
        fLine=fLine,
        line=columns,
        table=tab,
        key='id_profil',
        pathU=config.URL_APPLICATION + '/profil/update/',
        pathD=config.URL_APPLICATION + '/profil/delete/',
        pathA=config.URL_APPLICATION + '/profil/add/new',
        name="un profil",
        name_list="Profils",
        otherCol='False',
        profil_app='True',
        App="Application"
     )


@route.route('profil/delete/<id_profil>', methods=['GET', 'POST'])
@fnauth.check_auth(6, False, URL_REDIRECT)
def delete(id_profil):
    """
    Route qui supprime un profil dont l'id est donné en paramètres dans l'url
    Retourne une redirection vers la liste de profil
    """

    TProfils.delete(id_profil)
    return redirect(url_for('profils.profils'))


@route.route('profil/add/new', defaults={'id_profil': None}, methods=['GET', 'POST'])
@route.route('profil/update/<id_profil>', methods=['GET', 'POST'])
@fnauth.check_auth(6, False, URL_REDIRECT)
def addorupdate(id_profil):
    """
    Route affichant un formulaire vierge ou non (selon l'url) pour ajouter ou mettre à jour un profil
    L'envoie du formulaire permet l'ajout ou la maj du profil dans la base
    Retourne un template accompagné d'un formulaire pré-rempli ou non selon le paramètre id_profil
    Une fois le formulaire validé on retourne une redirection vers la liste de profil
    """

    form = t_profilsforms.Profil()
    if id_profil == None:
        if request.method == 'POST':
            if form.validate() and form.validate_on_submit():
                form_profil = pops(form.data)
                form_profil.pop('id_profil')
                TProfils.post(form_profil)
                return redirect(url_for('profils.profils'))
        return render_template('profil.html', form=form, title="Formulaire Profil")
    else:
        profil = TProfils.get_one(id_profil)
        if request.method == 'GET':
            form = process(form, profil)
        if request.method == 'POST':
            if form.validate() and form.validate_on_submit():
                form_profil = pops(form.data)
                form_profil['id_profil'] = profil['id_profil']
                TProfils.update(form_profil)
                return redirect(url_for('profils.profils'))
        return render_template('profil.html', form=form, title="Formulaire Profil")

def pops(form):
    """
    Methode qui supprime les éléments indésirables du formulaires
    Avec pour paramètre un formulaire
    """

    form.pop('csrf_token')
    form.pop('submit')
    return form


def process(form, profil):
    """
    Methode qui rempli le formulaire par les données de l'éléments concerné
    Avec pour paramètres un formulaire et un profil
    """

    form.nom_profil.process_data(profil['nom_profil'])
    form.code_profil.process_data(profil['code_profil'])
    form.desc_profil.process_data(profil['desc_profil'])
    return form
