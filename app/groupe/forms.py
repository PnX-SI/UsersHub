from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import DataRequired


class Group(FlaskForm):
    """
    Classe du formulaire des Groupes
    """

    nom_role = StringField(
        "Nom", validators=[DataRequired(message="Le nom du group est obligatoire")]
    )
    desc_role = TextAreaField("Description")
    groupe = BooleanField(
        "groupe",
        validators=[DataRequired(message="L'information 'groupe' est obligatoire")],
    )
    id_role = HiddenField("id")
    submit = SubmitField("Enregistrer")
