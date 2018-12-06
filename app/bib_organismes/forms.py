from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField, TextField
from wtforms.validators import DataRequired, Email
# from wtforms_components import IntergerField




class Organisme(FlaskForm):

    """
    Classe du formulaire des Organismes
    """
        
    nom_organisme = StringField('Nom organisme', validators=[DataRequired()])
    adresse_organisme = StringField('Adresse')
    cp_organisme = StringField('Code Postal')
    ville_organisme = StringField ('Ville')
    tel_organisme = StringField('Téléphone')
    # tel_organisme = PhoneNumberField('Numero de telephone',country_code='FI', display_format='national')
    fax_organisme = StringField('Fax')
    email_organisme = StringField('Email')
    id_organisme = HiddenField('id')
    submit = SubmitField('Enregistrer')