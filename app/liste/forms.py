from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import DataRequired


class List(FlaskForm):
    """
    Classe du formulaire des listes
    """

    nom_liste = StringField("Nom", validators = [DataRequired(message = 'Le nom de la liste est obligatoire')])
    code_liste = StringField("Code", validators = [DataRequired(message = 'Le code de la liste est obligatoire')])
    desc_liste = TextAreaField('Description')
    id_liste = HiddenField('Id')
    submit = SubmitField('Enregistrer')