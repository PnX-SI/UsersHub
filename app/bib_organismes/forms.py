from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField, TextField
from wtforms.validators import DataRequired, Email
# from wtforms_components import IntergerField




class Organisme(FlaskForm):
        
    nom_organisme = StringField('Nom organisme', validators=[DataRequired()])
    adresse_organisme = StringField('Adresse', validators=[DataRequired()])
    cp_organisme = StringField('Code Postal', validators =[DataRequired()])
    ville_organisme = StringField ('Ville', validators=[DataRequired()])
    tel_organisme = StringField('Tel :', validators= [DataRequired()])
    # tel_organisme = PhoneNumberField('Numero de telephone',country_code='FI', display_format='national')
    fax_organisme = StringField('Fax', validators=[DataRequired()])
    email_organisme = StringField('Email', validators=[Email()])
    id_organisme = HiddenField('id')
    submit = SubmitField('Envoyer')