
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired


class Tag(FlaskForm):
    id_tag = HiddenField('id')
    id_tag_type = SelectField('ID type', coerce=int ,choices = [])
    tag_code = StringField('Code', validators=[DataRequired()])
    tag_name = StringField('Nom', validators=[DataRequired])
    tag_desc = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Envoyer')