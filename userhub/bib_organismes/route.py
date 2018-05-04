from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from userhub import genericRepository
from userhub.bib_organismes import forms as bib_organismeforms
from userhub.models import Bib_Organismes

route =  Blueprint('organisme',__name__)

@route.route('/organismes', methods=['GET','POST'])
def organismes():
    entete = ['Nom', 'Adresse', 'Code Postal', 'Ville', 'Telephone', 'Fax', 'Email', 'ID']
    colonne = ['nom_organisme','adresse_organisme', 'cp_organisme','ville_organisme','tel_organisme','fax_organisme','email_organisme','id_organisme']
    contenu = Bib_Organismes.get_all(colonne)
    #  test
    formu = bib_organismeforms.Organisme()
    if request.method == 'POST':
        if formu.validate_on_submit() and formu.validate():
            form_org = formu.data
            form_org.pop('id_organisme')
            form_org.pop('submit')
            form_org.pop('csrf_token')        
            Bib_Organismes.post(form_org)
            return redirect(url_for('organisme.organismes'))
        else:
            flash(formu.errors)

    return render_template('affichebase.html', table = contenu, entete = entete,ligne = colonne, cheminM = '/bib_organismes/organismes/', cle= 'id_organisme', cheminS = '/bib_organismes/organismes/delete/', test= 'organisme.html', form = formu)




@route.route('/organismes/<id_organisme>', methods=['GET','POST'])
def organismes_unique(id_organisme):
    entete = ['Nom', 'Adresse', 'Code Postal', 'Ville', 'Telephone', 'Fax', 'Email', 'ID']
    colonne = ['nom_organisme','adresse_organisme', 'cp_organisme','ville_organisme','tel_organisme','fax_organisme','email_organisme','id_organisme']
    contenu = Bib_Organismes.get_all(colonne)
    # test
    org = Bib_Organismes.get_one(id_organisme)
    form = bib_organismeforms.Organisme()
    if request.method == 'POST':
        if form.validate_on_submit() and form.validate() :
            form_org = form.data
            form_org['id_organisme'] = org['id_organisme']
            form_org.pop('submit')
            form_org.pop('csrf_token')
            Bib_Organismes.update(form_org)
            return redirect(url_for('organisme.organismes'))
        else:
            flash(form.errors)
    return render_template('affichebase.html', table = contenu, entete = entete,ligne = colonne, cheminM = '/bib_organismes/organismes/', cle= 'id_organisme', cheminS = '/bib_organismes/organismes/delete/', test= 'organisme.html', form = form, nom_organisme = org['nom_organisme'], adresse_organisme = org['adresse_organisme'], cp_organisme = org['cp_organisme'], ville_organisme = org['ville_organisme'],tel_organisme = org['tel_organisme'], fax_organisme = org['fax_organisme'], email_organisme = org['email_organisme'] )


@route.route('/organismes/delete/<id_organisme>', methods = ['GET', 'POST'])
def delete(id_organisme):
    Bib_Organismes.delete(id_organisme)
    return redirect(url_for('organisme.organismes'))

# NON UTILISE

@route.route('/organisme', methods=['GET','POST'])
def organisme():
    formu = bib_organismeforms.Organisme()
    if request.method == 'POST':
        if formu.validate_on_submit() and formu.validate():
            form_org = formu.data
            form_org.pop('id_organisme')
            form_org.pop('submit')
            form_org.pop('csrf_token')        
            Bib_Organismes.post(form_org)
            return redirect(url_for('organisme.organismes'))
        else:
            flash(formu.errors)
    return render_template('organisme.html', form = formu)