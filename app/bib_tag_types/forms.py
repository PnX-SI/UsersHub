from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired

class TagTypes(FlaskForm):

    """
    Classe du formulaire des types de tag
    """

    id_tag_type = StringField('ID', validators=[DataRequired()])
    tag_type_name = StringField('Nom', validators=[DataRequired()])
    tag_type_desc = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Envoyer')