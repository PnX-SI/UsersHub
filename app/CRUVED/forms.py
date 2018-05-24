from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField, RadioField,SelectMultipleField, widgets, Form
from wtforms.validators import DataRequired, Email

class Scope(FlaskForm):
    full_name_role = SelectField("Nom role",coerce=int ,choices = [], default = -1)
    scopeCreate = SelectField('Portee Create',coerce=int ,choices = [], default = -1)
    scopeRead = SelectField('Portee Read',coerce = int, choices = [],default = -1)
    scopeUpdate = SelectField('Portee Update',coerce = int, choices = [],default = -1)
    scopeValidate = SelectField('Portee Validate',coerce = int, choices = [],default = -1)
    scopeExport = SelectField('Portee Export',coerce = int, choices = [],default = -1)
    scopeDelete = SelectField('Portee Delete',coerce = int, choices = [],default = -1)
    app = SelectField('Application',coerce = int, choices = [], default = 14)