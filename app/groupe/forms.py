from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired


class Group(FlaskForm):

    """
    Classe du formulaire des Groupes
    """

    nom_role = StringField("Nom du groupe", validators=[DataRequired()])
    desc_role = StringField('Description du groupe', validators=[DataRequired()])
    groupe = BooleanField('groupe', validators=[DataRequired()])
    id_role = HiddenField('id')
    submit = SubmitField('Envoyer')