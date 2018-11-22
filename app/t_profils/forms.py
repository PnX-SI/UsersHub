
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class profil(FlaskForm):
    
    """
    Classe du formulaire des profils
    """

    id_profil = HiddenField('id')
    code_profil = StringField('Code', validators = [DataRequired()])
    nom_profil = StringField('Nom', validators = [DataRequired()])
    desc_profil = StringField('Description')
    submit = SubmitField('Enregistrer')