
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired


class Tag(FlaskForm):
    
    """
    Classe du formulaire des tags
    """

    id_tag = HiddenField('id')
    id_tag_type = SelectField('Type de tag', coerce=int ,choices = [])
    tag_code = StringField('Code')
    tag_name = StringField('Nom', validators = [DataRequired()])
    tag_label = StringField('Label')
    tag_desc = StringField('Description')
    submit = SubmitField('Enregistrer')