"""
    Définition du formulaire : création/modification d'un role
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    HiddenField,
    SelectField,
    RadioField,
    BooleanField,
    SelectMultipleField,
    TextAreaField,
    widgets,
    validators,
)
from wtforms.validators import DataRequired, Email


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class Utilisateur(FlaskForm):
    active = BooleanField("Actif", default=True, false_values=(False, "false"))
    nom_role = StringField(
        "Nom",
        validators=[DataRequired(message="Le nom de l'utilisateur est obligatoire")],
    )
    prenom_role = StringField("Prenom")
    desc_role = TextAreaField("Description")
    id_organisme = SelectField("Organisme", coerce=int, choices=[], default=-1)
    a_groupe = SelectMultipleField("", choices=[], coerce=int)
    identifiant = StringField("Identifiant")
    pass_plus = PasswordField("Mot de passe")
    mdpconf = PasswordField("Confirmation")
    email = StringField(
        "E-mail",
        validators=[validators.Optional(), Email(message="L'email est incorect")],
    )
    groupe = HiddenField("groupe", default=None)
    remarques = TextAreaField("Commentaire")
    id_role = HiddenField("id")
    submit = SubmitField("Enregistrer")


class UserPass(FlaskForm):
    pass_plus = PasswordField("Mot de passe")
    mdpconf = PasswordField("Confirmation")
    id_role = HiddenField("id")
    submit = SubmitField("Enregistrer")
