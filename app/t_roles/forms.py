

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField, RadioField,SelectMultipleField, widgets, Form
from wtforms.validators import DataRequired, Email


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()





class Utilisateur(FlaskForm):

    nom_role =  StringField('Nom', validators=[DataRequired()])
    prenom_role = StringField( 'Prenom')
    id_organisme = SelectField('Choix Organisme',coerce=int ,choices = [], default = -1)
    a_groupe = MultiCheckboxField('Choix Groupe', choices = [], coerce=int)
    identifiant = StringField('Identifiant')
    pass_plus = PasswordField('Password')
    mdpconf = PasswordField('Confirmation')
    desc_role = StringField('Description du role' )
    email = StringField('E-mail' )
    groupe = HiddenField('groupe', default = None)
    remarques = StringField('Remarques')
    id_role = HiddenField('id')
    submit = SubmitField('Envoyer')
   
    


