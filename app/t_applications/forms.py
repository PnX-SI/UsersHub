
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired

from app.models import TRoles, TProfils, CorRoleAppProfil
from app.env import db


class Application(FlaskForm):
    """
    Classe du formulaire des applications
    """

    nom_application = StringField('Nom', validators = [DataRequired(message = "Le nom de l'application est obligatoire")])
    code_application = StringField('Code',validators = [DataRequired(message = "Le code de l'application est obligatoire")])
    desc_application = StringField('Description')
    id_parent = SelectField('Application parent',coerce=int ,choices = [])
    id_application = HiddenField('id')
    submit = SubmitField('Enregistrer')
    


class AppProfil(FlaskForm):
    """
    Classe du formulaire de profil d'un role pour une appli
    """
    role = SelectField('Role',coerce=int)
    profil = SelectField('Profil',coerce=int)
    submit = SubmitField('Enregistrer')


    # on surchage le constructeur de la classe pour y passer l'id_application en paramètre
    # et filter les listes déroulante des profils et des roles
    def __init__(self, id_application, *args, **kwargs):
        super(AppProfil, self).__init__(*args, **kwargs)
        # on ne met que les users qui n'ont pas déja un profil dans l'app
        # sous requete utilisateurs ayant deja un profil pour une app
        user_with_profil_in_app = db.session.query(
            CorRoleAppProfil.id_role
            ).filter(
                CorRoleAppProfil.id_application == id_application
        )
        users_no_profils_in_app = db.session.query(TRoles).filter(
            TRoles.id_role.notin_(user_with_profil_in_app)
        ).all()
        users_select_choices = []
        for user in users_no_profils_in_app:
            user_as_dict = user.as_dict_full_name()
            users_select_choices.append(
                 (user_as_dict['id_role'], user_as_dict['full_name']) 
            )
        self.role.choices = users_select_choices
        # choix des profils dispo pour une appli
        self.profil.choices = TProfils.choixSelect(id_application=id_application)
