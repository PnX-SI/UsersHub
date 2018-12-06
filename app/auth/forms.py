'''
    INUTILE
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class Admin(FlaskForm):
    username = StringField('pseudo', validators=[DataRequired()])
    password = PasswordField('mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')
    deconnexion = SubmitField('Se deconnecter')