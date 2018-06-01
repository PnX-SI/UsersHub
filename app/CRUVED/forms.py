from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField, RadioField,SelectMultipleField, widgets, Form
from wtforms.validators import DataRequired, Email

class Scope(FlaskForm):

    """
    Classe du formulaire des portées du cruved
    """

    scopeCreate = SelectField('Portee Create',coerce=int ,choices = [], default = 0)
    scopeRead = SelectField('Portee Read',coerce = int, choices = [],default = 0)
    scopeUpdate = SelectField('Portee Update',coerce = int, choices = [],default = 0)
    scopeValidate = SelectField('Portee Validate',coerce = int, choices = [],default = 0)
    scopeExport = SelectField('Portee Export',coerce = int, choices = [],default = 0)
    scopeDelete = SelectField('Portee Delete',coerce = int, choices = [],default = 0)
    submit = SubmitField('Enregistrer')

class Name_App(FlaskForm):

    """
    Classe du formulaire du nom et de l'application pour un cruved 
    """
    full_name_role = SelectField("Nom ",coerce=int ,choices = [])
    app = SelectField('Application',coerce = int, choices = [], default = 14)
    