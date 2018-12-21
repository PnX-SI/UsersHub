from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class Profil(FlaskForm):
    """
    Classe du formulaire des profils
    """

    id_profil = HiddenField('Id')
    code_profil = StringField('Code', validators = [DataRequired(message = 'Le nom du profil est obligatoire')])
    nom_profil = StringField('Nom', validators = [DataRequired(message = 'Le code du profil est obligatoire')])
    desc_profil = StringField('Description')
    submit = SubmitField('Enregistrer')

