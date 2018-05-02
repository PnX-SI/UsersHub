from userhub.env import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import select, func
from userhub.utils.utilssqlalchemy import serializable
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey
from userhub.genericRepository import GenericRepository

@serializable
class  Bib_Organismes(GenericRepository):
    __tablename__ = 'bib_organismes'
    __table_args__={'schema':'utilisateurs'}
    id_organisme = db.Column(db.Integer, primary_key = True)
    #uuid_organisme = db.Column(UUID(as_uuid=True), default = selesct([func.uuid_generate_v4()]))
    nom_organisme = db.Column(db.Unicode)
    adresse_organisme = db.Column(db.Unicode)
    cp_organisme = db.Column(db.Unicode)
    ville_organisme = db.Column(db.Unicode)
    tel_organisme = db.Column(db.Unicode)
    fax_organisme = db.Column(db.Unicode)
    email_organisme = db.Column(db.Unicode)    
    id_parent = db.Column(db.Integer)



@serializable
class TRoles(GenericRepository):
    __tablename__ = 't_roles'
    __table_args__={'schema':'utilisateurs'}
    id_role = db.Column(db.Integer, primary_key = True)
    groupe = db.Column(db.Boolean)
    uuid_role = db.Column(UUID(as_uuid=True), default=select([func.uuid_generate_v4()]))
    identifiant = db.Column(db.Unicode)
    nom_role = db.Column(db.Unicode)
    prenom_role = db.Column(db.Unicode)
    desc_role = db.Column(db.Unicode)
    # pass = db.Column(db.Unicode)
    pass_plus = db.Column(db.Unicode)
    email = db.Column(db.Unicode)
    id_organisme =db.Column(db.Unicode, ForeignKey('utilisateurs.bib_organismes.id_organisme')) 
    organisme_rel = relationship("Bib_Organismes")
    organisme = db.Column(db.Unicode)
    id_unite = db.Column(db.Integer)
    remarques = db.Column(db.Unicode)
    pn = db.Column(db.Boolean)
    session_appli = (db.Unicode)


@serializable
class TApplications(GenericRepository):
    __tablename__='t_applications'
    __table_args__ = {'schema':'utilisateurs'}
    id_application = db.Column(db.Integer, primary_key = True)
    nom_application = db.Column(db.Unicode)
    desc_application = db.Column(db.Unicode)
    id_parent = db.Column(db.Unicode)

   

@serializable
class TTags(GenericRepository):
    __tablename__ = 't_tags'
    __table_args__ = {'schema':'utilisateurs'}
    id_tag = db.Column(db.Integer,primary_key = True)
    id_tag_type = db.Column(db.Integer)
    tag_code = db.Column(db.Unicode)
    tag_name = db.Column(db.Unicode)
    tag_label = db.Column(db.Unicode)
    tag_desc = db.Column(db.Unicode)

@serializable
class TMenu(GenericRepository):
    __tablename__ = 't_menus'
    __table_args__ = {'schema':'utilisateurs'}
    id_menu = db.Column(db.Integer, primary_key = True)
    nom_menu = db.Column(db.Unicode)
    desc_menu = db.Column(db.Unicode)
    id_application = db.Column(db.Unicode)

@serializable
class CorTagsRelations(GenericRepository):
    __tablename__ = 'cor_tags_relations'
    __table_args__ = {'schema':'utilisateurs'}
    id_tag_l = db.Column(db.Integer, primary_key = True)
    id_tag_r = db.Column(db.Integer, primary_key = True)
    relation_type = db.Column(db.Unicode)


@serializable
class CorRoles(GenericRepository):
    __tablename__= 'cor_roles'
    __table_args__ = {'schema':'utilisateurs'}
    id_role_groupe = db.Column(db.Integer, primary_key = True)
    id_role_utilisateur = db.Column(db.Integer, ForeignKey('utilisateurs.t_roles.id_role'),primary_key = True )
    t_roles = db.relationship('TRoles')


@serializable
class CorRoleTag(GenericRepository):
    __tablename__ = 'cor_role_tag'
    __table_args__= {'schema':'utilisateurs'}
    id_role = db.Column(db.Integer, primary_key = True)
    id_tag = db.Column(db.Integer, primary_key = True)

@serializable
class CorRoleMenu(GenericRepository):
    __tablename__= 'CorRoleMenu'
    __table_args__= {'schema':'utilisateurs'}
    id_role = db.Column(db.Integer, primary_key = True)
    id_menu = db.Column(db.Integer,primary_key = True)

@serializable
class CorRoleDroitApplication(GenericRepository):
    __tablename__ = 'cor_role_droit_application'
    __table_args__= {'schema':'utilisateurs'}
    id_role = db.Column(db.Integer, primary_key = True)
    id_droit = db.Column(db.Integer, primary_key = True)
    id_application = db.Column(db.Integer, primary_key = True)

@serializable
class CorOrganismeTag(GenericRepository):
    __tablename__ = 'cor_organisme_tag'
    __table_args__= {'schema':'utilisateurs'}
    id_organisme = db.Column(db.Integer, primary_key = True)
    id_tag = db.Column(db.Integer, primary_key = True)

@serializable
class CorApplicationTag(GenericRepository):
    __tablename__ = "cor_appplication_tag"
    __table_args__ = {'schema':'utilsateurs'}
    id_application = db.Column(db.Integer, primary_key = True)
    id_tag = db.Column(db.Integer, primary_key = True)

@serializable
class CorAppPrivileges(GenericRepository):
    __tablename__ = 'cor_app_privileges'
    __table_args__ = {'schema':'utilsateurs'}
    id_application = db.Column(db.Integer, primary_key = True)
    id_tag = db.Column(db.Integer, primary_key = True)

    
@serializable
class BibUnites(GenericRepository):
    __tablename__ = 'bib_unites'
    __table_args__ = {'schema': 'utilisateurs'}
    id_unite = db.Column(db.Integer, primary_key = True)
    nom_unite = db.Column(db.Unicode)
    adresse_unite = db.Column(db.Unicode)
    cp_unite = db.Column(db.Unicode)
    ville_unite = db.Column(db.Unicode)
    tel_unite = db.Column(db.Unicode)
    fax_unite = db.Column(db.Unicode)
    email_unite = db.Column(db.Unicode)


@serializable
class BibTagTypes(GenericRepository):
    __tablename__ = 'bib_tag_types'
    __table_args__ = {'schema':'utilsateurs'}
    id_tag_type = db.Column(db.Integer, primary_key = True)
    tag_type_name = db.Column(db.Unicode)
    tag_type_desc = db.Column(db.Unicode)

@serializable
class BibDroits(GenericRepository):
    __tablename__ = 'bib_droits'
    __table_args__ = {'schema':'utilsateurs'}
    id_droit = db.Column(db.Integer, primary_key = True)
    nom_droit = db.Column(db.Unicode)
    desc_droit = db.Column(db.Unicode)