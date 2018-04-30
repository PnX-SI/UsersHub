

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired

class LogUser(FlaskForm):
    username = StringField('pseudo', validators=[DataRequired()])
    password = PasswordField('mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')
    deconnexion = SubmitField('Se deconnecter')

class Utilisateur(FlaskForm):

    nom_role =  StringField('Nom', validators=[DataRequired()])
    prenom_role = StringField( 'Prenom', validators=[DataRequired()])
    id_organisme = SelectField('Choix Organisme',coerce=int ,choices = [], default = -1)
    pass_plus = StringField('Password', validators= [DataRequired()])
    mdpconf = StringField('Confirmation', validators= [DataRequired()])
    desc_role = StringField('Description du role' , validators = [DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    groupe = HiddenField('groupe', default = None)
    remarques = StringField('Remarques', validators=[DataRequired()])
    id_role = HiddenField('id')
    submit = SubmitField('Envoyer')


    

    
