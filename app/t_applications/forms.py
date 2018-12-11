
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired


class Application(FlaskForm):
    """
    Classe du formulaire des applications
    """

    nom_application = StringField('Nom', validators = [DataRequired(message = 'Le nom est obligatoire')])
    code_application = StringField('Code',validators = [DataRequired(message = 'Le code est obligatoire')])
    desc_application = StringField('Description')
    id_parent = SelectField('Application parent',coerce=int ,choices = [])
    id_application = HiddenField('id')
    submit = SubmitField('Enregistrer')
    
class AppProfil(FlaskForm):
    """
    Classe du formulaire de droit d'un role pour une appli
    """

    profil = SelectField('Profil',coerce=int ,choices = [])
