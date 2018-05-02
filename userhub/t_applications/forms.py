
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired


class Application(FlaskForm):
    nom_application = StringField('Nom',validators=[DataRequired()])
    desc_application = StringField('Description', validators=[DataRequired()])
    id_parent = SelectField('Choix application parent',coerce=int ,choices = [])
    id_application = HiddenField('id')
    submit = SubmitField('Envoyer')
