from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class Group(FlaskForm):

    """
    Classe du formulaire des Groupes
    """
    nom_role = StringField("Nom", validators=[DataRequired(message='Ce champ est obligatoire')])
    desc_role = TextAreaField('Description')
    groupe = BooleanField('groupe', validators=[DataRequired(message='Ce champ est obligatoire')])
    id_role = HiddenField('id')
    submit = SubmitField('Enregistrer')