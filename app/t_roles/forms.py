'''
    Définition du formulaire : création/modification d'un role
'''

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, HiddenField, SelectField,
    RadioField, BooleanField, SelectMultipleField, TextAreaField, widgets,
    validators
)
from wtforms.validators import DataRequired, Email


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class Utilisateur(FlaskForm):
    active = BooleanField('Actif', validators=[DataRequired()], description='Utilisateur actif ?')
    nom_role = StringField('Nom', validators=[DataRequired()])
    prenom_role = StringField('Prenom')
    desc_role = TextAreaField('Prenom')
    id_organisme = SelectField('Organisme', coerce=int, choices=[], default=-1)
    a_groupe = SelectMultipleField('Groupe', choices=[], coerce=int)
    identifiant = StringField('Identifiant')
    pass_plus = PasswordField('Mot de passe')
    mdpconf = PasswordField('Confirmation')
    email = StringField('E-mail', validators=[validators.Optional(), Email()])
    groupe = HiddenField('groupe', default=None)
    remarques = TextAreaField('Remarques')
    id_role = HiddenField('id')
    submit = SubmitField('Enregistrer')



