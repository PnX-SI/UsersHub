from app.env import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import select, func
from app.utils.utilssqlalchemy import serializable
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey, distinct
from app.genericRepository import GenericRepository




@serializable
class CorOrganismeTag(GenericRepository):
    __tablename__ = 'cor_organism_tag'
    __table_args__= {'schema':'utilisateurs'}
    id_organism = db.Column(db.Integer,ForeignKey('utilisateurs.bib_organismes.id_organisme'), primary_key = True)
    id_tag = db.Column(db.Integer, ForeignKey('utilisateurs.t_tags.id_tag'), primary_key = True)

    @classmethod
    def add_cor(cls,id_tag,tab_id):
        dict_add = dict()
        dict_add["id_tag"] = id_tag 
        for d in tab_id:
            dict_add["id_organism"] = d
            cls.post(dict_add)

    @classmethod
    def del_cor(cls,id_tag,tab_id):
        for d in tab_id:
            cls.query.filter(cls.id_tag == id_tag).filter(cls.id_organism == d).delete()
            db.session.commit()

@serializable
class CorTagsRelations(GenericRepository):
    __tablename__ = 'cor_tags_relations'
    __table_args__ = {'schema':'utilisateurs'}
    id_tag_l = db.Column(db.Integer, primary_key = True)
    id_tag_r = db.Column(db.Integer, primary_key = True)
    relation_type = db.Column(db.Unicode)



    @classmethod
    def add_cor(cls,id_group,tab_id):
        dict_add = dict()
        dict_add["id_role_groupe"] = id_group 
        for d in tab_id:
            dict_add["id_role_utilisateur"] = d
            cls.post(dict_add)
    
    @classmethod
    def del_cor(cls,id_group,tab_id):
        for d in tab_id:
            cls.query.filter(cls.id_role_groupe == id_group).filter(cls.id_role_utilisateur == d).delete()
            db.session.commit()


@serializable
class CorRoleTag(GenericRepository):
    __tablename__ = 'cor_role_tag'
    __table_args__= {'schema':'utilisateurs'}
    id_role = db.Column(db.Integer,ForeignKey('utilisateurs.t_roles.id_role'), primary_key = True)
    id_tag = db.Column(db.Integer, ForeignKey('utilisateurs.t_tags.id_tag'),primary_key = True)


    @classmethod
    def add_cor(cls,id_tag,tab_id):
        dict_add = dict()
        dict_add["id_tag"] = id_tag 
        for d in tab_id:
            dict_add["id_role"] = d
            cls.post(dict_add)
    
    @classmethod
    def del_cor(cls,id_tag,tab_id):
        for d in tab_id:
            cls.query.filter(cls.id_tag == id_tag).filter(cls.id_role == d).delete()
            db.session.commit()
    




@serializable
class CorRoleMenu(GenericRepository):
    __tablename__= 'CorRoleMenu'
    __table_args__= {'schema':'utilisateurs'}
    id_role = db.Column(db.Integer,ForeignKey('utilisateurs.t_roles.id_role'), primary_key = True)
    id_menu = db.Column(db.Integer,ForeignKey('utilisateurs.t_menus.id_menu'), primary_key = True)

@serializable
class CorRoleDroitApplication(GenericRepository):
    __tablename__ = 'cor_role_droit_application'
    __table_args__= {'schema':'utilisateurs'}
    id_role = db.Column(db.Integer,ForeignKey('utilisateurs.t_roles.id_role'), primary_key = True)
    id_droit = db.Column(db.Integer,ForeignKey('utilisateurs.bib_droits.id_droit'), primary_key = True)
    id_application = db.Column(db.Integer, ForeignKey('utilisateurs.t_application.id_application'), primary_key = True)


@serializable
class CorApplicationTag(GenericRepository):
    __tablename__ = "cor_application_tag"
    __table_args__ = {'schema':'utilisateurs'}
    id_application = db.Column(db.Integer, ForeignKey('utilisateurs.t_applications.id_application'), primary_key = True)
    id_tag = db.Column(db.Integer,ForeignKey('utilisateurs.t_tags.id_tag'), primary_key = True)

    @classmethod
    def add_cor(cls,id_tag,tab_id):
        dict_add = dict()
        dict_add["id_tag"] = id_tag 
        for d in tab_id:
            dict_add["id_application"] = d
            cls.post(dict_add)
    
    @classmethod
    def del_cor(cls,id_tag,tab_id):
        for d in tab_id:
            cls.query.filter(cls.id_tag == id_tag).filter(cls.id_application == d).delete()
            db.session.commit()

@serializable
class CorAppPrivileges(GenericRepository):
    __tablename__ = 'cor_app_privileges'
    __table_args__ = {'schema':'utilisateurs'}
    id_application = db.Column(db.Integer, ForeignKey('utilisateurs.t_roles.id_role'), primary_key = True)
    id_tag_object = db.Column(db.Integer, primary_key = True)
    id_role = db.Column(db.Integer, ForeignKey('utilisateurs.t_roles.id_role'), primary_key = True)
    id_tag_action = db.Column(db.Integer)
  
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

    @classmethod
    def get_orgs_in_tag(cls,id_tag):
        q =db.session.query(cls)
        q = q.join(CorOrganismeTag)
        q = q.filter(id_tag == CorOrganismeTag.id_tag)
        data =  [data.as_dict() for data in q.all()]
        return data 
    
    @classmethod
    def get_orgs_out_tag(cls,id_tag):
        q = db.session.query(cls)
        subquery = db.session.query(CorOrganismeTag.id_organism).filter(id_tag == CorOrganismeTag.id_tag)
        q = q.filter(cls.id_organisme.notin_(subquery))
        data =  [data.as_dict() for data in q.all()]
        return data

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
    
    
   
    @classmethod
    def choix_group(cls,id,nom,aucun = None):
        q = db.session.query(cls)
        q = q.filter(cls.groupe == True )
        data = [data.as_dict(True) for data in q.all()]
        choices = []
        for d in data :
            choices.append((d[id], d[nom]))
        if aucun != None :
            choices.append((-1,'Aucun'))
        return choices

    
    def get_full_name(self):
        if self.prenom_role == None:
            full_name = self.nom_role
        else :
            full_name = self.nom_role + ' '+ self.prenom_role
        return full_name
       
    def as_dict_full_name(self):
        full_name = self.get_full_name()
        user_as_dict = self.as_dict()
        user_as_dict['full_name'] = full_name
        return user_as_dict
       

    @classmethod
    def test_group(cls,tab):
        table = []
        for d in tab :
            if d['groupe'] == False:
                d['groupe'] = 'False'
            else :
                d['groupe'] = 'True'
            table.append(d)
        return table

    @classmethod
    def get_user_in_tag(cls, id_tag):
        q = db.session.query(cls)
        q = q.join(CorRoleTag)
        q = q.filter(id_tag == CorRoleTag.id_tag  )        
        data =  [data.as_dict_full_name() for data in q.all()]
        return data   


    @classmethod
    def get_user_out_tag(cls,id_tag):
        q = db.session.query(cls)
        subquery = db.session.query(CorRoleTag.id_role).filter(id_tag == CorRoleTag.id_tag)
        q = q.filter(cls.id_role.notin_(subquery))
        data =  [data.as_dict_full_name() for data in q.all()]
        return data

    @classmethod
    def get_user_in_group(cls, id_groupe):
        """

        """
        q = db.session.query(cls)
        q = q.join(CorRoles)
        q = q.filter(id_groupe == CorRoles.id_role_groupe )
        data =  [data.as_dict_full_name() for data in q.all()]
        return data

    @classmethod
    def get_user_out_group(cls,id_groupe):
        q = db.session.query(cls)
        subquery = db.session.query(CorRoles.id_role_utilisateur).filter(id_groupe == CorRoles.id_role_groupe )
        q = q.filter(cls.id_role.notin_(subquery))
        data =  [data.as_dict_full_name() for data in q.all()]
        return data



    @classmethod
    def get_user_in_application(cls,id_application):
        q = db.session.query(cls)
        q = q.join(CorAppPrivileges, TRoles.id_role == CorAppPrivileges.id_role)
        q = q.filter(id_application ==  CorAppPrivileges.id_application )
        for data in q.all():
            data.as_dict() 
        data =  [data.as_dict_full_name() for data in q.all()]
        return data 

    @classmethod
    def get_user_out_application(cls,id_application):
        q = db.session.query(cls)
        subquery = db.session.query(distinct(CorAppPrivileges.id_role)).filter(id_application == CorAppPrivileges.id_application)
        q = q.filter(cls.id_role.notin_(subquery))
        return  [data.as_dict_full_name() for data in q.all()]

@serializable
class CorRoles(GenericRepository):
    __tablename__= 'cor_roles'
    __table_args__ = {'schema':'utilisateurs'}
    id_role_groupe = db.Column(db.Integer, primary_key = True)
    id_role_utilisateur = db.Column(db.Integer, ForeignKey('utilisateurs.t_roles.id_role'),primary_key = True )
    t_roles = db.relationship('TRoles')


    @classmethod
    def add_cor(cls,id_group,tab_id):
        dict_add = dict()
        dict_add["id_role_group"] = id_group 
        for d in tab_id:
            dict_add["id_role_utilisateur"] = d
            cls.post(dict_add)
    
    @classmethod
    def del_cor(cls,id_group,tab_id):
        for d in tab_id:
            cls.query.filter(cls.id_role_groupe== id_group).filter(cls.id_role_utilisateur == d).delete()
            db.session.commit()
    

@serializable
class TApplications(GenericRepository):
    __tablename__='t_applications'
    __table_args__ = {'schema':'utilisateurs'}
    id_application = db.Column(db.Integer, primary_key = True)
    nom_application = db.Column(db.Unicode)
    desc_application = db.Column(db.Unicode)
    id_parent = db.Column(db.Unicode)

    @classmethod
    def get_applications_in_tag(cls, id_tag):
        q = db.session.query(cls)
        q = q.join(CorApplicationTag)
        q = q.filter(id_tag == CorApplicationTag.id_tag  )        
        data =  [data.as_dict() for data in q.all()]
        return data   


    @classmethod
    def get_applications_out_tag(cls,id_tag):
        q = db.session.query(cls)
        subquery = db.session.query(CorApplicationTag.id_application).filter(id_tag == CorApplicationTag.id_tag)
        q = q.filter(cls.id_application.notin_(subquery))
        data =  [data.as_dict() for data in q.all()]
        return data
   

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

    @classmethod
    def choixSelect(cls,tag_code,nom,aucun = None):
        data = cls.get_all()
        choices = []
        for d in data :
            if d['id_tag_type'] == 5:  
                choices.append((d[tag_code], d[nom]))
        if aucun != None :
            choices.append((-1,'Aucun'))
        return choices
   
@serializable
class TMenu(GenericRepository):
    __tablename__ = 't_menus'
    __table_args__ = {'schema':'utilisateurs'}
    id_menu = db.Column(db.Integer, primary_key = True)
    nom_menu = db.Column(db.Unicode)
    desc_menu = db.Column(db.Unicode)
    id_application = db.Column(db.Unicode)

  
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
    __table_args__ = {'schema':'utilisateurs'}
    id_tag_type = db.Column(db.Integer, primary_key = True)
    tag_type_name = db.Column(db.Unicode)
    tag_type_desc = db.Column(db.Unicode)



@serializable
class BibDroits(GenericRepository):
    __tablename__ = 'bib_droits'
    __table_args__ = {'schema':'utilisateurs'}
    id_droit = db.Column(db.Integer, primary_key = True)
    nom_droit = db.Column(db.Unicode)
    desc_droit = db.Column(db.Unicode)

@serializable
class VUsersactionForallGnModules(GenericRepository):
    '''
    Droit d'acces d'un user particulier a une application particuliere
    '''
    __tablename__ = 'v_usersaction_forall_gn_modules'
    __table_args__ = {'schema': 'utilisateurs'}
    id_role = db.Column(db.Integer, primary_key=True)
    nom_role = db.Column(db.Unicode)
    prenom_role = db.Column(db.Unicode)
    id_application = db.Column(db.Integer, primary_key=True)
    id_organisme = db.Column(db.Integer)
    id_tag_action = db.Column(db.Integer, primary_key=True)
    tag_action_code = db.Column(db.Unicode)
    id_tag_object = db.Column(db.Integer, primary_key=True)
    tag_object_code = db.Column(db.Unicode)

    def __repr__(self):
        return """VUsersactionForallGnModules
            role='{}' action='{}' porté='{}' app='{}'>""".format(
                self.id_role, self.tag_action_code,
                self.tag_object_code, self.id_application
            )

    def get_full_name(self):
        if self.prenom_role == None:
            full_name = self.nom_role
        else :
            full_name = self.nom_role + ' '+ self.prenom_role
        return full_name
       
    def as_dict_full_name(self):
        full_name = self.get_full_name()
        user_as_dict = self.as_dict()
        user_as_dict['full_name'] = full_name
        return user_as_dict