

import hashlib

from app.env import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import select, func


from flask_bcrypt import (
    generate_password_hash
)

from app.utils.utilssqlalchemy import serializable
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey, distinct, or_, desc
from app.genericRepository import GenericRepository
from config import config


"""Fichier contenant les models de la base de données"""


@serializable
class CorOrganismeTag(GenericRepository):

    """ Classe de correspondance entre la table bib_organismes et la table t_tags"""

    __tablename__ = 'cor_organism_tag'
    __table_args__= {'schema':'utilisateurs'}
    id_organism = db.Column(db.Integer,ForeignKey('utilisateurs.bib_organismes.id_organisme'), primary_key = True)
    id_tag = db.Column(db.Integer, ForeignKey('utilisateurs.t_tags.id_tag'), primary_key = True)

    @classmethod
    def add_cor(cls,id_tag,tab_id):

        """
        Methode qui permet d'ajouter des relations organismes tags a la base

        Avec pour paramètres un id de tag et un tableau d'id d'organismes
        """

        dict_add = dict()
        dict_add["id_tag"] = id_tag
        for d in tab_id:
            dict_add["id_organism"] = d
            cls.post(dict_add)

    @classmethod
    def del_cor(cls,id_tag,tab_id):

        """
        Methode qui permet de supprimer des relationss organismes tag à la base

        Avec pour paramètres un id de tag et un tableau d'id d'organismes
        """

        for d in tab_id:
            cls.query.filter(cls.id_tag == id_tag).filter(cls.id_organism == d).delete()
            db.session.commit()

@serializable
class CorTagsRelations(GenericRepository):

    """ Classe de correspondance entre tags"""

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

    """ Classe de correspondance entre la table t_roles et la table t_tags"""

    __tablename__ = 'cor_role_tag'
    __table_args__= {'schema':'utilisateurs'}
    id_role = db.Column(db.Integer,ForeignKey('utilisateurs.t_roles.id_role'), primary_key = True)
    id_tag = db.Column(db.Integer, ForeignKey('utilisateurs.t_tags.id_tag'),primary_key = True)


    @classmethod
    def add_cor(cls,id_tag,tab_id):

        """
        Methode qui ajoute des relations roles tag

        Avec pour paramètres un id de tag et un tableau d'id de roles
        """

        dict_add = dict()
        dict_add["id_tag"] = id_tag
        for d in tab_id:
            dict_add["id_role"] = d
            cls.post(dict_add)

    @classmethod
    def del_cor(cls,id_tag,tab_id):

        """
        Methode qui supprime des relation roles tag

        Avec pour paramètres un id de tag et un tableau d'id de roles
        """

        for d in tab_id:
            cls.query.filter(cls.id_tag == id_tag).filter(cls.id_role == d).delete()
            db.session.commit()



@serializable
class CorRoleTagApplication(GenericRepository):

    """Classe de correspondance entre la table t_roles, t_tags et t_applications"""

    __tablename__= "cor_role_tag_application"
    __table_args__={'schema':'utilisateurs'}
    id_role = db.Column(db.Integer,ForeignKey('utilisateurs.t_roles.id_role'), primary_key = True)
    id_tag = db.Column(db.Integer,ForeignKey('utilisateurs.t_tags.id_tag'), primary_key = True)
    id_application = db.Column(db.Integer, ForeignKey('utilisateurs.t_applications.id_application'), primary_key = True)

    @classmethod
    def add_cor(cls,id_app,tab_right):
        dict_add = {}
        for d in tab_right:
            dict_add = {'id_role':d['id_role'],'id_tag':d['id_right'], 'id_application': id_app }
            cls.post(dict_add)

    @classmethod
    def del_cor(cls,id_app,tab_right):
       for t in tab_right:
            print(t)
            cls.query.filter(cls.id_role == t['id_role']).filter(cls.id_tag == t['id_right']).filter(cls.id_application == id_app).delete()
            db.session.commit()

@serializable
class CorApplicationTag(GenericRepository):

    """ Classe de correspondance entre la table t_applications et la table t_tags"""

    __tablename__ = "cor_application_tag"
    __table_args__ = {'schema':'utilisateurs'}
    id_application = db.Column(db.Integer, ForeignKey('utilisateurs.t_applications.id_application'), primary_key = True)
    id_tag = db.Column(db.Integer,ForeignKey('utilisateurs.t_tags.id_tag'), primary_key = True)

    @classmethod
    def add_cor(cls,id_tag,tab_id):

        """
        Methode qui ajoute des relations applications tag

        Avec pour paramètres un id de tag et un tableau d'id d'applications
        """

        dict_add = dict()
        dict_add["id_tag"] = id_tag
        for d in tab_id:
            dict_add["id_application"] = d
            cls.post(dict_add)

    @classmethod
    def del_cor(cls,id_tag,tab_id):

        """
        Methode qui supprime des relations applications tag

        Avec pour paramètres un id de tag et un tableau d'id d'applications
        """

        for d in tab_id:
            cls.query.filter(cls.id_tag == id_tag).filter(cls.id_application == d).delete()
            db.session.commit()

@serializable
class CorAppPrivileges(GenericRepository):

    """
    Classe de correspondance entre la table t_applications,la table t_tags, la table t_roles

    Cette classe permet d'établir un Cruved à un role pour une application,
    une ligne représente de la table représente une relation d'un tag sur un role pour une application avec une portée
    """

    __tablename__ = 'cor_app_privileges'
    __table_args__ = {'schema':'utilisateurs'}
    id_application = db.Column(db.Integer, ForeignKey('utilisateurs.t_roles.id_role'), primary_key = True)
    id_tag_object = db.Column(db.Integer, primary_key = True)
    id_role = db.Column(db.Integer, ForeignKey('utilisateurs.t_roles.id_role'), primary_key = True)
    id_tag_action = db.Column(db.Integer)

    @classmethod
    def delete(cls,id_tag,id_role,id_app):

        """
        Methode qui permet la suppression d'une ligne de cette table,
        avec pour paramètres un id de tag, un id de role et un id d'application
        """

        cls.query.filter(cls.id_tag_object == id_tag).filter(cls.id_application == id_app).filter(cls.id_role == id_role).delete()
        db.session.commit()

@serializable
class  Bib_Organismes(GenericRepository):

    """
    Model de la table Bib_Organismes

    """
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

        """
        Méthode qui retourne les organismes étiqueté par un tag donné
        Avec pour paramètre un id de tag
        """

        q =db.session.query(cls)
        q = q.join(CorOrganismeTag)
        q = q.filter(id_tag == CorOrganismeTag.id_tag)
        data =  [data.as_dict() for data in q.all()]
        return data

    @classmethod
    def get_orgs_out_tag(cls,id_tag):

        """
        Méthode qui retourne les organismes non étiqueté par un tag donné
        Avec pour paramètre un id de tag
        """

        q = db.session.query(cls)
        subquery = db.session.query(CorOrganismeTag.id_organism).filter(id_tag == CorOrganismeTag.id_tag)
        q = q.filter(cls.id_organisme.notin_(subquery))
        data =  [data.as_dict() for data in q.all()]
        return data

@serializable
class TRoles(GenericRepository):

    """
    Model de la table t_roles
    """

    __tablename__ = 't_roles'
    __table_args__={'schema':'utilisateurs'}
    id_role = db.Column(db.Integer, primary_key = True)
    groupe = db.Column(db.Boolean)
    uuid_role = db.Column(UUID(as_uuid=True), default=select([func.uuid_generate_v4()]))
    identifiant = db.Column(db.Unicode)
    nom_role = db.Column(db.Unicode)
    prenom_role = db.Column(db.Unicode)
    desc_role = db.Column(db.Unicode)
    pass_md5 = db.Column("pass", db.Unicode)
    pass_plus = db.Column(db.Unicode)
    email = db.Column(db.Unicode)
    id_organisme =db.Column(db.Unicode, ForeignKey('utilisateurs.bib_organismes.id_organisme'))
    organisme_rel = relationship("Bib_Organismes")
    id_unite = db.Column(db.Integer)
    remarques = db.Column(db.Unicode)
    pn = db.Column(db.Boolean)
    session_appli = (db.Unicode)


    def fill_password(self, password, password_confirmation):
        (self.pass_plus, self.pass_md5) = self.set_password( password, password_confirmation)

    @classmethod
    def set_password(cls, password, password_confirmation):
        if not password:
            raise ValueError("Password is null")
        if password != password_confirmation:
            raise ValueError("Password doesn't match")

        try:
            pass_plus = generate_password_hash(password.encode('utf-8')).decode('utf-8')
            pass_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()
        except Exception as e:
            raise e

        return (pass_plus, pass_md5)

    @classmethod
    def choixSelect(cls,id,nom,aucun = None):

        """
        Methode qui retourne une tableau de tuples d'id de roles et de nom de roles
        Avec pour paramètres un id de role et un nom de role
        Le paramètre aucun si il a une valeur permet de rajouter le tuple (-1,Aucun) au tableau
        """

        q = cls.get_all(as_model =True)
        data =[data.as_dict_full_name() for data in q.all()]
        choices = []
        for d in data :
            choices.append((d[id], d[nom]))
        if aucun != None :
            choices.append((-1,'Aucun'))
        return choices

    @classmethod
    def choix_group(cls,id,nom,aucun = None):

        """
        Methode qui retourne une tableau de tuples d'id de groupes et de nom de goupes
        Avec pour paramètres un id de groupe et un nom de groupe
        Le paramètre aucun si il a une valeur permet de rajouter le tuple (-1,Aucun) au tableau
        """

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

        """
        Methode qui concatène le nom et prénom du role
        retourne un nom complet
        """

        if self.prenom_role == None:
            full_name = self.nom_role
        else :
            full_name = self.nom_role + ' '+ self.prenom_role
        return full_name

    def as_dict_full_name(self):

        """
        Methode qui ajout le nom complet d'un role au dictionnaire qui le défini
        retourne un dictionnaire d'un utilisateur avec une nouvelle 'full_name'
        """

        full_name = self.get_full_name()
        user_as_dict = self.as_dict()
        user_as_dict['full_name'] = full_name
        return user_as_dict


    @classmethod
    def test_group(cls,tab):

        """
        Methode qui test si le tableau contient un élement groupe = False,
        Si c'est le cas alors on remplace le boolean par un string du même nom
        retourne un tableau avec le groupe sous forme de string
        """

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

        """
        Methode qui retourne un dictionnaire de roles étiqueté par un tag donné
        Avec pour paramètre un id de tag
        """

        q = db.session.query(cls)
        q = q.order_by(desc(cls.groupe))
        q = q.join(CorRoleTag)
        q = q.filter(id_tag == CorRoleTag.id_tag  )
        data =  [data.as_dict_full_name() for data in q.all()]
        return data


    @classmethod
    def get_user_out_tag(cls,id_tag):

        """
        Methode qui retourne un dictionnaire de roles non étiqueté par un tag donné
        Avec pour paramètres un id de tag
        """

        q = db.session.query(cls)
        q = q.order_by(desc(cls.groupe))
        subquery = db.session.query(CorRoleTag.id_role).filter(id_tag == CorRoleTag.id_tag)
        q = q.filter(cls.id_role.notin_(subquery))
        data =  [data.as_dict_full_name() for data in q.all()]
        return data

    @classmethod
    def get_user_in_group(cls, id_groupe):

        """
        Methode qui retourne un dictionnaire de role appartenant à un groupe donné
        Avec pour paramètres un id de role
        """
        q = db.session.query(cls)
        q = q.order_by(desc(cls.groupe))
        q = q.join(CorRoles)
        q = q.filter(id_groupe == CorRoles.id_role_groupe )
        data =  [data.as_dict_full_name() for data in q.all()]
        return data

    @classmethod
    def get_user_out_group(cls,id_groupe):

        """
        Methode qui retourne un dictionnaire de role n'appartenant pas à un groupe donné
        Avec pour paramètre un id de role
        """

        q = db.session.query(cls).filter(cls.id_role != id_groupe)
        q = q.order_by(desc(cls.groupe))
        subquery = db.session.query(CorRoles.id_role_utilisateur).filter(id_groupe == CorRoles.id_role_groupe )
        subquery2 = db.session.query(CorRoles.id_role_groupe).filter(CorRoles.id_role_utilisateur == id_groupe) #a vérifier (problème de récursivité)
        q = q.filter(cls.id_role.notin_(subquery))
        q = q.filter(cls.id_role.notin_(subquery2))
        data =  [data.as_dict_full_name() for data in q.all()]
        return data



    @classmethod
    def get_user_right_in_application(cls,id_application):

        """
        Methode qui retourne un dictionnaire de roles ayant les droits sur une application donné
        Avec pour paramètre un id d'application
        """

        q = db.session.query(cls, CorRoleTagApplication)
        q = q.order_by(desc(cls.groupe))
        q = q.join(CorRoleTagApplication, TRoles.id_role == CorRoleTagApplication.id_role)
        q = q.filter(id_application ==  CorRoleTagApplication.id_application )
        data = q.all()
        data =  [{'role':d[0].as_dict_full_name(), 'right':d[1].as_dict()} for d in data]

        return data

    @classmethod
    def get_user_out_application(cls,id_application):

        """
        Methode qui retourne un dictionnaire de roles ayant les droits sur une application donné
        Avec pour paramètre un id d'application
        """

        q = db.session.query(cls)
        q = q.order_by(desc(cls.groupe))
        subquery = db.session.query(distinct(CorRoleTagApplication.id_role)).filter(id_application == CorRoleTagApplication.id_application)
        q = q.filter(cls.id_role.notin_(subquery))
        return  [data.as_dict_full_name() for data in q.all()]

@serializable
class CorRoles(GenericRepository):

    """
    Classe de correspondance entre un utilisateurs et un groupes
    """
    __tablename__= 'cor_roles'
    __table_args__ = {'schema':'utilisateurs'}
    id_role_groupe = db.Column(db.Integer, primary_key = True)
    id_role_utilisateur = db.Column(db.Integer, ForeignKey('utilisateurs.t_roles.id_role'),primary_key = True )
    t_roles = db.relationship('TRoles')


    @classmethod
    def add_cor(cls,id_group,tab_id):

        """
        Methode qui ajoute des relations roles groupe
        Avec pour paramètres un id de groupe(id_role) et un tableau d'id de roles
        """

        dict_add = dict()
        dict_add["id_role_groupe"] = id_group
        for d in tab_id:
            dict_add["id_role_utilisateur"] = d
            cls.post(dict_add)

    @classmethod
    def del_cor(cls,id_group,tab_id):

        """
        Methode qui supprime des relations roles groupe
        Avec pour paramètres un id de groupe(id_role) et un tableau d'id de roles
        """

        for d in tab_id:
            cls.query.filter(cls.id_role_groupe== id_group).filter(cls.id_role_utilisateur == d).delete()
            db.session.commit()


@serializable
class TApplications(GenericRepository):

    """
    Model de la table t_applications
    """

    __tablename__='t_applications'
    __table_args__ = {'schema':'utilisateurs'}
    id_application = db.Column(db.Integer, primary_key = True)
    nom_application = db.Column(db.Unicode)
    desc_application = db.Column(db.Unicode)
    id_parent = db.Column(db.Unicode)

    @classmethod
    def get_applications_in_tag(cls, id_tag):

        """
        Methode qui retourne un dictionnaire d'application étiqueté par un tag donné
        Avec pour paramètre un id de tag
        """

        q = db.session.query(cls)
        q = q.join(CorApplicationTag)
        q = q.filter(id_tag == CorApplicationTag.id_tag  )
        data =  [data.as_dict() for data in q.all()]
        return data


    @classmethod
    def get_applications_out_tag(cls,id_tag):

        """
        Methode qui retourne un dictionnaire d'application non étiqueté par un tag donné
        Avec pour paramètre un id de tag
        """

        q = db.session.query(cls)
        subquery = db.session.query(CorApplicationTag.id_application).filter(id_tag == CorApplicationTag.id_tag)
        q = q.filter(cls.id_application.notin_(subquery))
        data =  [data.as_dict() for data in q.all()]
        return data

    @classmethod
    def choix_app_cruved(cls,id_app,nom,aucun = None):

        """
        Methode qui retourne une tableau de tuples d'id d'applications et de nom d'applications
        Avec pour paramètres un id id d'application et un nom d'application
        Le paramètre aucun si il a une valeur permet de rajouter le tuple (-1,Aucun) au tableau
        """

        q = cls.get_all(as_model = True).filter(or_(cls.id_application == config.ID_GEONATURE,cls.id_parent == config.ID_GEONATURE))
        data = [data.as_dict() for data in q.all()]
        choices = []
        for d in data :
            choices.append((d[id_app], d[nom]))
        if aucun != None :
            choices.append((-1,'Aucun'))
        return choices


@serializable
class TTags(GenericRepository):

    """
    Model de la classe t_tags
    """

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

        """
        Methode qui retourne une tableau de tuples de code de tags et de nom de tags
        Avec pour paramètres un code de tag et un nom de tag
        Le paramètre aucun si il a une valeur permet de rajouter le tuple (0,Aucun) au tableau
        """

        data = cls.get_all()
        choices = []
        for d in data :
            if d['id_tag_type'] == 5:
                choices.append((d[tag_code], d[nom]))
        if aucun != None :
            choices.append((0,'Aucun'))
        return choices

    @classmethod
    def choixSelectTag(cls,id,nom,aucun = None):

        """
        Methode qui retourne une tableau de tuples d'id de tag et de nom de tag de type privilège
        Avec pour paramètres un id de tag et un nom de tag
        Le paramètre aucun si il a une valeur permet de rajouter le tuple (-1,Aucun) au tableau
        """

        q = cls.get_all(as_model =True).filter(TTags.id_tag_type == 3)
        data =[data.as_dict() for data in q.all()]
        choices = []
        for d in data :
            choices.append((d[id], d[nom]))
        if aucun != None :
            choices.append((-1,'Aucun'))
        return choices


@serializable
class BibUnites(GenericRepository):

    """
    Model de la table bib_unites
    """

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

    """
    Model de la table bib_tag_types
    """

    __tablename__ = 'bib_tag_types'
    __table_args__ = {'schema':'utilisateurs'}
    id_tag_type = db.Column(db.Integer, primary_key = True)
    tag_type_name = db.Column(db.Unicode)
    tag_type_desc = db.Column(db.Unicode)


@serializable
class CorRoleMenu(GenericRepository):

    """Vue de correspondance entre la table t_roles et la vue t_menus"""

    __tablename__= 'cor_role_menu'
    __table_args__= {'schema':'utilisateurs'}
    id_role = db.Column(db.Integer,ForeignKey('utilisateurs.t_roles.id_role'), primary_key = True)
    id_menu = db.Column(db.Integer,ForeignKey('utilisateurs.t_menus.id_menu'), primary_key = True)

@serializable
class CorRoleDroitApplication(GenericRepository):

    """ Vue de correspondance entre la table t_applications, t_roles et la vue bib_droits"""

    __tablename__ = 'cor_role_droit_application'
    __table_args__= {'schema':'utilisateurs'}
    id_role = db.Column(db.Integer,ForeignKey('utilisateurs.t_roles.id_role'), primary_key = True)
    id_droit = db.Column(db.Integer,ForeignKey('utilisateurs.bib_droits.id_droit'), primary_key = True)
    id_application = db.Column(db.Integer, ForeignKey('utilisateurs.t_applications.id_application'), primary_key = True)

@serializable
class VTMenu(GenericRepository):

    """
    Model de la Vue t_menus
    """

    __tablename__ = 't_menus'
    __table_args__ = {'schema':'utilisateurs'}
    id_menu = db.Column(db.Integer, primary_key = True)
    nom_menu = db.Column(db.Unicode)
    desc_menu = db.Column(db.Unicode)
    id_application = db.Column(db.Unicode)

@serializable
class VBibDroits(GenericRepository):

    """
    Model de la Vue bib_droits
    """

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

        """
        Methode qui concatène le nom et prénom du role
        retourne un nom complet
        """

        if self.prenom_role == None:
            full_name = self.nom_role
        else :
            full_name = self.nom_role + ' '+ self.prenom_role
        return full_name

    def as_dict_full_name(self):

        """
        Methode qui ajout le nom complet d'un role au dictionnaire qui le défini
        retourne un dictionnaire d'un utilisateur avec une nouvelle 'full_name'
        """

        full_name = self.get_full_name()
        user_as_dict = self.as_dict()
        user_as_dict['full_name'] = full_name
        return user_as_dict

