'''
    Définition du formulaire : création/modification d'un role
'''

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, HiddenField, SelectField,
    SelectMultipleField, TextAreaField, widgets,
    validators
)
from wtforms.validators import DataRequired, Email


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class Utilisateur(FlaskForm):
    nom_role = StringField('Nom', validators=[DataRequired()])
    prenom_role = StringField('Prenom')
    id_organisme = SelectField('Organisme', coerce=int, choices=[], default=-1)
    a_groupe = SelectMultipleField('Groupe', choices=[], coerce=int)
    identifiant = StringField('Identifiant (login)', validators=[DataRequired()])
    pass_plus = PasswordField('Mot de passe', validators=[DataRequired()])
    mdpconf = PasswordField('Entrez le mot de passe à nouveau', validators=[DataRequired()])
    email = StringField('E-mail', validators=[validators.Optional(), Email()])
    groupe = HiddenField('groupe', default=None)
    remarques = TextAreaField('Commentaire')
    id_role = HiddenField('id')
    submit = SubmitField('Enregistrer')



