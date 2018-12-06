from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class Group(FlaskForm):

    """
    Classe du formulaire des Groupes
    """
    nom_role = StringField("Nom", validators=[DataRequired()])
    desc_role = TextAreaField('Description')
    groupe = BooleanField('groupe', validators=[DataRequired()])
    id_role = HiddenField('id')
    submit = SubmitField('Enregistrer')