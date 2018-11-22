

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
class CorRoleListe(GenericRepository):

    """ Classe de correspondance entre la table t_roles et la table t_listes"""

    __tablename__ = 'cor_role_liste'
    __table_args__= {'schema':'utilisateurs'}
    id_role = db.Column(db.Integer,ForeignKey('utilisateurs.t_roles.id_role'), primary_key = True)
    id_liste = db.Column(db.Integer, ForeignKey('utilisateurs.t_listes.id_liste'),primary_key = True)


    @classmethod
    def add_cor(cls,id_liste,ids_role):

        """
        Methode qui ajoute des relations roles <-> liste

        Avec pour paramètres un id de liste et un tableau d'id de roles
        """

        dict_add = dict()
        dict_add["id_liste"] = id_liste
        for d in ids_role:
            dict_add["id_role"] = d
            cls.post(dict_add)

    @classmethod
    def del_cor(cls,id_liste,ids_role):

        """
        Methode qui supprime des relations roles <-> liste

        Avec pour paramètres un id de liste et un tableau d'id de roles
        """

        for d in ids_role:
            cls.query.filter(cls.id_liste == id_liste).filter(cls.id_role == d).delete()
            db.session.commit()



@serializable
class CorRoleAppProfil(GenericRepository):

    """Classe de correspondance entre la table t_roles, t_profils et t_applications"""

    __tablename__= "cor_role_app_profil"
    __table_args__={'schema':'utilisateurs'}
    id_role = db.Column(db.Integer,ForeignKey('utilisateurs.t_roles.id_role'), primary_key = True)
    id_profil = db.Column(db.Integer,ForeignKey('utilisateurs.t_profils.id_profil'), primary_key = True)
    id_application = db.Column(db.Integer, ForeignKey('utilisateurs.t_applications.id_application'), primary_key = True)

    @classmethod
    def add_cor(cls,id_app,tab_right):
        dict_add = {}
        for d in tab_right:
            dict_add = {'id_role':d['id_role'],'id_profil':d['id_right'], 'id_application': id_app }
            cls.post(dict_add)

    @classmethod
    def del_cor(cls,id_app,tab_right):
       for t in tab_right:
            cls.query.filter(cls.id_role == t['id_role']).filter(cls.id_profil == t['id_right']).filter(cls.id_application == id_app).delete()
            db.session.commit()

@serializable
class CorProfilForApp(GenericRepository):

    """ Classe de correspondance entre la table t_applications et la table t_profils"""

    __tablename__ = "cor_profil_for_app"
    __table_args__ = {'schema':'utilisateurs'}
    id_application = db.Column(db.Integer, ForeignKey('utilisateurs.t_applications.id_application'), primary_key = True)
    id_profil = db.Column(db.Integer,ForeignKey('utilisateurs.t_profils.id_profil'), primary_key = True)

    @classmethod
    def add_cor(cls,id_profil,ids_app):

        """
        Methode qui ajoute des relations applications <-> profil

        Avec pour paramètres un id profil et un tableau d'id d'applications
        """

        dict_add = dict()
        dict_add["id_profil"] = id_profil
        for d in ids_app:
            dict_add["id_application"] = d
            cls.post(dict_add)

    @classmethod
    def del_cor(cls,id_profil,ids_app):

        """
        Methode qui supprime des relations applications <-> profil

        Avec pour paramètres un id profil et un tableau d'id d'applications
        """

        for d in ids_app:
            cls.query.filter(cls.id_profil == id_profil).filter(cls.id_application == d).delete()
            db.session.commit()

@serializable
class  Bib_Organismes(GenericRepository):

    """
    Model de la table Bib_Organismes

    """
    __tablename__ = 'bib_organismes'
    __table_args__={'schema':'utilisateurs'}
    id_organisme = db.Column(db.Integer, primary_key = True)
    uuid_organisme = db.Column(UUID(as_uuid=True), default=select([func.uuid_generate_v4()]))
    nom_organisme = db.Column(db.Unicode)
    adresse_organisme = db.Column(db.Unicode)
    cp_organisme = db.Column(db.Unicode)
    ville_organisme = db.Column(db.Unicode)
    tel_organisme = db.Column(db.Unicode)
    fax_organisme = db.Column(db.Unicode)
    email_organisme = db.Column(db.Unicode)
    url_organisme = db.Column(db.Unicode)
    url_logo = db.Column(db.Unicode)
    id_parent = db.Column(db.Integer)

@serializable
class TRoles(GenericRepository):

    """
    Model de la table t_roles
    """

    __tablename__ = 't_roles'
    __table_args__={'schema':'utilisateurs', 'extend_existing': True}
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
    active = db.Column(db.Boolean)
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
    def get_user_in_liste(cls, id_liste):

        """
        Methode qui retourne un dictionnaire des roles d'une liste
        Avec pour paramètre un id_liste
        """

        q = db.session.query(cls)
        q = q.order_by(desc(cls.groupe))
        q = q.join(CorRoleListe)
        q = q.filter(id_liste == CorRoleListe.id_liste  )
        data =  [data.as_dict_full_name() for data in q.all()]
        return data

    @classmethod
    def get_user_in_group(cls, id_groupe):

        """
        Methode qui retourne un dictionnaire de role appartenant à un groupe
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
        #TODO filtrer les roles actifs
        data =  [data.as_dict_full_name() for data in q.all()]
        return data

    @classmethod
    def get_user_right_in_application(cls,id_application):

        """
        Methode qui retourne un dictionnaire de roles ayant les droits sur une application donné
        Avec pour paramètre un id d'application
        """

        q = db.session.query(cls, CorRoleAppProfil)
        q = q.order_by(desc(cls.groupe))
        q = q.join(CorRoleAppProfil, TRoles.id_role == CorRoleAppProfil.id_role)
        q = q.filter(id_application ==  CorRoleAppProfil.id_application )
        data = q.all()
        data =  [{'role':d[0].as_dict_full_name(), 'right':d[1].as_dict()} for d in data]

        return data

    @classmethod
    def get_user_out_application(cls,id_application):

        """
        Methode qui retourne un dictionnaire de roles n'ayant pas de droits sur une application
        Avec pour paramètre un id d'application
        """

        q = db.session.query(cls)
        q = q.order_by(desc(cls.groupe))
        subquery = db.session.query(distinct(CorRoleAppProfil.id_role)).filter(id_application == CorRoleAppProfil.id_application)
        q = q.filter(cls.id_role.notin_(subquery))
        return  [data.as_dict_full_name() for data in q.all()]

@serializable
class CorRoles(GenericRepository):

    """
    Classe de correspondance entre un utilisateur et un groupe
    """
    __tablename__= 'cor_roles'
    __table_args__ = {'schema':'utilisateurs'}
    id_role_groupe = db.Column(db.Integer, primary_key = True)
    id_role_utilisateur = db.Column(db.Integer, ForeignKey('utilisateurs.t_roles.id_role'),primary_key = True )
    t_roles = db.relationship('TRoles')


    @classmethod
    def add_cor(cls,id_group,ids_role):

        """
        Methode qui ajoute des relations roles <-> groupe
        Avec pour paramètres un id de groupe(id_role) et un tableau d'id de roles
        """

        dict_add = dict()
        dict_add["id_role_groupe"] = id_group
        for d in ids_role:
            dict_add["id_role_utilisateur"] = d
            cls.post(dict_add)

    @classmethod
    def del_cor(cls,id_group,ids_role):

        """
        Methode qui supprime des relations roles <-> groupe
        Avec pour paramètres un id de groupe(id_role) et un tableau d'id de roles
        """

        for d in ids_role:
            cls.query.filter(cls.id_role_groupe== id_group).filter(cls.id_role_utilisateur == d).delete()
            db.session.commit()


@serializable
class TApplications(GenericRepository):

    """
    Model de la table t_applications
    """

    __tablename__='t_applications'
    __table_args__ = {'schema':'utilisateurs', 'extend_existing': True}
    id_application = db.Column(db.Integer, primary_key = True)
    code_application = db.Column(db.Unicode)
    nom_application = db.Column(db.Unicode)
    desc_application = db.Column(db.Unicode)
    id_parent = db.Column(db.Unicode)

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
class TProfils(GenericRepository):

    """
    Model de la classe t_profils
    """

    __tablename__ = 't_profils'
    __table_args__ = {'schema':'utilisateurs', 'extend_existing': True}
    id_profil = db.Column(db.Integer,primary_key = True)
    code_profil = db.Column(db.Unicode)
    nom_profil = db.Column(db.Unicode)
    desc_profil = db.Column(db.Unicode)

    @classmethod
    def get_profils_for_app(cls, id_application):

        """
        Methode qui retourne un dictionnaire des profils utilisable pour une application
        Avec pour paramètre un id de l'application
        """

        q = db.session.query(cls)
        q = q.join(CorProfilForApp)
        q = q.filter(id_profil == CorProfilForApp.id_application)
        return  [data.as_dict() for data in q.all()]

    @classmethod
    def get_profils_out_app(cls, id_application):

        """
        Methode qui retourne un dictionnaire des profils non utilisés pour une application
        Avec pour paramètre un id application
        """

        q = db.session.query(cls)
        subquery = db.session.query(CorProfilForApp.id_application).filter(id_application == CorProfilForApp.id_application)
        q = q.filter(cls.id_profil.notin_(subquery)) 
        return [data.as_dict() for data in q.all()]
    
    @classmethod
    def choixSelect(cls,code_profil,nom_profil):

        """
        Methode qui retourne un tableau de tuples de code profil et de nom de profil
        Avec pour paramètres un code de tag et un nom de tag
        """
        #TODO filtrer avec CorProfilForApp
        return [(d[code_profil], d[nom_profil]) for d in cls.get_all()]
