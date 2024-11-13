from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    HiddenField,
    validators,
)
from wtforms.validators import DataRequired, Email


def validate_code_postal(form, field):
    if len(field.data) != 5:
        raise validators.ValidationError(
            "Le code postal renseigné comporte plus/moins de 5 caractères"
        )


class Organisme(FlaskForm):
    """
    Classe du formulaire des Organismes
    """

    nom_organisme = StringField(
        "Nom de l'organisme",
        validators=[DataRequired(message="Le nom de l'organisme est obligatoire")],
    )
    adresse_organisme = StringField("Adresse")
    cp_organisme = StringField("Code Postal", validators=[validate_code_postal])
    ville_organisme = StringField("Ville")
    tel_organisme = StringField("Téléphone")
    fax_organisme = StringField("Fax")
    email_organisme = StringField(
        "E-mail",
        validators=[validators.Optional(), Email(message="L'email est incorect")],
    )
    url_organisme = StringField("URL du site web de l'organisme")
    url_logo = StringField("Logo (URL)")
    id_organisme = HiddenField("id")
    submit = SubmitField("Enregistrer")
