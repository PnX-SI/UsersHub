import hashlib

from flask import current_app, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, distinct, or_, desc
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import select, func
from sqlalchemy.orm import synonym, relationship, backref
from pypnusershub.db.models import check_and_encrypt_password

from app.env import db
from app.utils.utilssqlalchemy import serializable
from app.genericRepository import GenericRepository


"""
    Fichier contenant les models de la base de données
"""


@serializable
class Bib_Organismes(GenericRepository):
    """
    Model de la table Bib_Organismes

    """

    __tablename__ = "bib_organismes"
    __table_args__ = {"schema": "utilisateurs", "extend_existing": True}
    id_organisme = db.Column(db.Integer, primary_key=True)
    uuid_organisme = db.Column(
        UUID(as_uuid=True), default=select([func.uuid_generate_v4()])
    )
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

    __tablename__ = "t_roles"
    __table_args__ = {"schema": "utilisateurs", "extend_existing": True}

    id_role = db.Column(db.Integer, primary_key=True)
    groupe = db.Column(db.Boolean)
    uuid_role = db.Column(UUID(as_uuid=True), default=select([func.uuid_generate_v4()]))
    identifiant = db.Column(db.Unicode)
    nom_role = db.Column(db.Unicode)
    prenom_role = db.Column(db.Unicode)
    desc_role = db.Column(db.Unicode)
    pass_md5 = db.Column("pass", db.Unicode)
    pass_plus = db.Column(db.Unicode)
    email = db.Column(db.Unicode)
    id_organisme = db.Column(
        db.Integer, ForeignKey("utilisateurs.bib_organismes.id_organisme")
    )
    organisme_rel = relationship("Bib_Organismes")
    remarques = db.Column(db.Unicode)
    active = db.Column(db.Boolean)
    pass5 = db.Column("pass", db.Unicode)
    pass_plus = db.Column(db.Unicode)
    champs_addi = db.Column(JSONB)
    date_insert = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    date_update = db.Column(db.DateTime, default=db.func.now(), nullable=False, onupdate=db.func.now())

    # Add synonym for column pass
    # Hack because pass is an python reserved word
    pass_md5 = synonym("pass5")

    def set_password(self, password, password_confirmation):
        (self.pass_plus, self.pass_md5) = check_and_encrypt_password(
            password,
            password_confirmation,
            current_app.config["PASS_METHOD"] == "md5"
            or current_app.config["FILL_MD5_PASS"],
        )

    @classmethod
    def choixSelect(cls, id="id_role", nom="full_name", aucun=None):
        """
        Methode qui retourne une tableau de tuples d'id
            de roles et de nom de roles ACTIF
        Avec pour paramètres un id de role et un nom de role
        Le paramètre aucun si il a une valeur permet
            de rajouter le tuple (-1,Aucun) au tableau
        """

        # recupère tous les role actif
        roles = cls.get_all(as_model=True, params=[{"col": "active", "filter": True}])

        choices = []
        for role in roles:
            role_as_dict = role.as_dict_full_name()
            choices.append((role_as_dict[id], role_as_dict[nom]))
        if aucun != None:
            choices.append((-1, "Aucun"))
        return choices

    @classmethod
    def choix_group(cls, id, nom, aucun=None):
        """
        Methode qui retourne une tableau de tuples d'id
            de groupes et de nom de goupes
        Avec pour paramètres un id de groupe et un nom de groupe
        Le paramètre aucun si il a une valeur permet
            de rajouter le tuple (-1,Aucun) au tableau
        """

        q = db.session.query(cls).order_by(cls.identifiant)
        q = q.filter(cls.groupe == True)
        data = [data.as_dict(True) for data in q.all()]
        choices = []
        for d in data:
            choices.append((d[id], d[nom]))
        if aucun != None:
            choices.append((-1, "Aucun"))
        return choices

    @classmethod
    def get_user_groups(cls, id_role):
        """
        Get all groups of a user
        Parameters:
            id_role (int): the user's id
        Return:
            Array<TRoles>
        """
        cor_role_query = db.session.query(CorRoles.id_role_groupe).filter(
            CorRoles.id_role_utilisateur == id_role
        )
        return db.session.query(TRoles).filter(TRoles.id_role.in_(cor_role_query)).all()

    @classmethod
    def get_user_lists(cls, id_role):
        """
        Get all lists of a user
        Parameters:
            id_role (int): the user's id
        Return:
            Array<TListes>
        """
        # get ids_role list from user and user groups
        ids_role = [id_role]
        ids_group = [group.id_role for group in cls.get_user_groups(id_role)]
        for id in ids_group:
            ids_role.append(id)
        cor_role_list_query = db.session.query(CorRoleListe.id_liste).filter(
            CorRoleListe.id_role.in_(ids_role)
        )
        return (
            db.session.query(TListes)
            .filter(TListes.id_liste.in_(cor_role_list_query))
            .all()
        )

    @classmethod
    def get_user_app_profils(cls, id_role, id_application=None):
        """
        Get all listapp profils of a user
        Parameters:
            id_role (int): the user's id
            id_application optional (int): application id
        Return:
            Array<CorRoleAppProfil>
        """
        # get ids_role list from user and user groups
        ids_role = [id_role]
        ids_group = [group.id_role for group in cls.get_user_groups(id_role)]
        for id in ids_group:
            ids_role.append(id)
        # get right rows in cor_role_app_profil
        q = (
            db.session.query(CorRoleAppProfil)
            .distinct(CorRoleAppProfil.id_application)
            .filter(CorRoleAppProfil.id_role.in_(ids_role))
        )
        if id_application:
            q = q.filter(CorRoleAppProfil.id_application == id_application)
        q = q.order_by(CorRoleAppProfil.id_application)
        rights = q.all()
        return rights

    def get_full_name(self):
        """
        Methode qui concatène le nom et prénom du role
        retourne un nom complet
        """

        if self.prenom_role == None:
            full_name = self.nom_role
        else:
            full_name = self.nom_role + " " + self.prenom_role
        return full_name

    def as_dict_full_name(self):
        """
        Methode qui ajout le nom complet d'un role au dictionnaire
            qui le défini
        retourne un dictionnaire d'un utilisateur avec une nouvelle 'full_name'
        """

        full_name = self.get_full_name()
        user_as_dict = self.as_dict()
        user_as_dict["full_name"] = full_name
        return user_as_dict

    @classmethod
    def test_group(cls, tab):
        """
        Methode qui test si le tableau contient un élement groupe = False,
        Si c'est le cas alors on remplace le boolean par un string du même nom
        retourne un tableau avec le groupe sous forme de string
        """

        table = []
        for d in tab:
            if d["groupe"] is False:
                d["groupe"] = "False"
            else:
                d["groupe"] = "True"
            table.append(d)
        return table

    @classmethod
    def get_user_in_list(cls, id_liste):
        """
        Methode qui retourne un dictionnaire des roles d'une liste
        Avec pour paramètre un id_liste
        """

        q = db.session.query(cls).filter(cls.active == True)
        q = q.order_by(desc(cls.nom_role))
        q = q.join(CorRoleListe)
        q = q.filter(id_liste == CorRoleListe.id_liste)
        data = [data.as_dict_full_name() for data in q.all()]
        return data

    @classmethod
    def get_user_out_list(cls, id_liste):
        """
        Methode qui retourne un dictionnaire de roles n'appartenant
            pas à une liste
        Avec pour paramètre un id_liste
        """

        q = db.session.query(cls)
        q = q.order_by(desc(cls.nom_role))
        subquery = (
            db.session.query(CorRoleListe.id_role)
            .filter(CorRoleListe.id_liste == id_liste)
            .all()
        )

        q = q.filter(cls.id_role.notin_(subquery))
        # TODO filtrer les roles actifs
        data = [data.as_dict_full_name() for data in q.all()]
        return data

    @classmethod
    def get_user_in_group(cls, id_groupe):
        """
        Methode qui retourne un dictionnaire de role appartenant à un groupe
        Avec pour paramètres un id de role
        """
        q = db.session.query(cls).filter(cls.active == True)
        q = q.order_by(desc(cls.groupe))
        q = q.join(CorRoles)
        q = q.filter(id_groupe == CorRoles.id_role_groupe)
        data = [data.as_dict_full_name() for data in q.all()]
        return data

    @classmethod
    def get_user_out_group(cls, id_groupe):
        """
        Methode qui retourne un dictionnaire de role n'appartenant pas
            à un groupe donné
        Avec pour paramètre un id de role
        """

        q = db.session.query(cls).filter(cls.id_role != id_groupe)
        q = q.order_by(desc(cls.groupe))
        subquery = db.session.query(CorRoles.id_role_utilisateur).filter(
            CorRoles.id_role_groupe == id_groupe
        )

        subquery2 = db.session.query(CorRoles.id_role_groupe).filter(
            CorRoles.id_role_utilisateur == id_groupe
        )  # TODO a vérifier (problème de récursivité)

        q = q.filter(cls.id_role.notin_(subquery))
        q = q.filter(cls.id_role.notin_(subquery2))
        # TODO filtrer les roles actifs
        data = [data.as_dict_full_name() for data in q.all()]
        return data

    @classmethod
    def get_user_profil_in_app(cls, id_application):

        """
        Methode qui retourne un dictionnaire de roles avec leur profil sur une application
        Avec pour paramètre un id d'application
        Ne retourne que les utilisateurs actifs
        """
        # get the user
        data = (
            db.session.query(cls, TProfils)
            .join(CorRoleAppProfil, cls.id_role == CorRoleAppProfil.id_role)
            .join(TProfils, TProfils.id_profil == CorRoleAppProfil.id_profil)
            .filter(cls.active == True)
            .filter(CorRoleAppProfil.id_application == id_application)
            .order_by(desc(cls.groupe))
            .all()
        )
        user_with_profil = []
        for d in data:
            user = d[0].as_dict_full_name()
            user["id_profil"] = d[1].id_profil
            user["profil"] = d[1].nom_profil
            user_with_profil.append(user)
        return user_with_profil

    @classmethod
    def get_user_profil_out_app(cls, id_application):

        """
        Methode qui retourne un dictionnaire de roles n'ayant pas de droits
            sur une application
        Avec pour paramètre un id d'application
        """

        q = db.session.query(cls)
        q = q.order_by(desc(cls.groupe))
        subquery = db.session.query(distinct(CorRoleAppProfil.id_role)).filter(
            CorRoleAppProfil.id_application == id_application
        )
        q = q.filter(cls.id_role.notin_(subquery))
        return [data.as_dict_full_name() for data in q.all()]

    @classmethod
    def get_groups(cls):

        """
        Methode qui retourne une liste des roles
            de type groupe
        """
        q = db.session.query(cls).filter(TRoles.groupe == True)
        return q.all()


@serializable
class CorRoles(GenericRepository):

    """
    Classe de correspondance entre un utilisateur et un groupe
    """

    __tablename__ = "cor_roles"
    __table_args__ = {"schema": "utilisateurs", "extend_existing": True}
    id_role_groupe = db.Column(db.Integer, primary_key=True)
    id_role_utilisateur = db.Column(
        db.Integer, ForeignKey("utilisateurs.t_roles.id_role"), primary_key=True
    )
    t_roles = db.relationship("TRoles")

    @classmethod
    def test_role_in_grp(cls, id_role, id_group):
        """
        Methode qui retourne vrai si le role
            appartient au groupe
        """
        in_grp = (
            db.session.query(CorRoles)
            .filter(CorRoles.id_role_utilisateur == id_role)
            .filter(CorRoles.id_role_groupe == id_group)
            .all()
        )
        if in_grp:
            return True
        return False

    @classmethod
    def add_cor(cls, id_group, ids_role):

        """
        Methode qui ajoute des relations roles <-> groupe
        Avec pour paramètres un id de groupe(id_role)
            et un tableau d'id de roles
        """

        dict_add = dict()
        dict_add["id_role_groupe"] = id_group
        for d in ids_role:
            dict_add["id_role_utilisateur"] = d
            cls.post(dict_add)

    @classmethod
    def del_cor(cls, id_group, ids_role):

        """
        Methode qui supprime des relations roles <-> groupe
        Avec pour paramètres un id de groupe(id_role) et un tableau
            d'id de roles
        """

        for d in ids_role:
            cls.query.filter(cls.id_role_groupe == id_group).filter(
                cls.id_role_utilisateur == d
            ).delete()
            db.session.commit()


@serializable
class TListes(GenericRepository):

    """
    Model de la table t_listes
    """

    __tablename__ = "t_listes"
    __table_args__ = {"schema": "utilisateurs", "extend_existing": True}
    id_liste = db.Column(db.Integer, primary_key=True)
    code_liste = db.Column(db.Unicode)
    nom_liste = db.Column(db.Unicode)
    desc_liste = db.Column(db.Unicode)


@serializable
class CorRoleListe(GenericRepository):
    """ Classe de correspondance entre la table t_roles et la table t_listes"""

    __tablename__ = "cor_role_liste"
    __table_args__ = {"schema": "utilisateurs"}
    id_role = db.Column(
        db.Integer, ForeignKey("utilisateurs.t_roles.id_role"), primary_key=True
    )
    id_liste = db.Column(
        db.Integer, ForeignKey("utilisateurs.t_listes.id_liste"), primary_key=True
    )
    role_rel = relationship("TRoles")

    @classmethod
    def add_cor(cls, id_liste, ids_role):
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
    def del_cor(cls, id_liste, ids_role):
        """
        Methode qui supprime des relations roles <-> liste

        Avec pour paramètres un id de liste et un tableau d'id de roles
        """

        for d in ids_role:
            cls.query.filter(cls.id_liste == id_liste).filter(cls.id_role == d).delete()
            db.session.commit()


@serializable
class TApplications(GenericRepository):

    """
    Model de la table t_applications
    """

    __tablename__ = "t_applications"
    __table_args__ = {"schema": "utilisateurs", "extend_existing": True}
    id_application = db.Column(db.Integer, primary_key=True)
    code_application = db.Column(db.Unicode)
    nom_application = db.Column(db.Unicode)
    desc_application = db.Column(db.Unicode)
    id_parent = db.Column(db.Unicode)


@serializable
class TProfils(GenericRepository):
    """
    Model de la classe t_profils
    """

    __tablename__ = "t_profils"
    __table_args__ = {"schema": "utilisateurs", "extend_existing": True}
    id_profil = db.Column(db.Integer, primary_key=True)
    code_profil = db.Column(db.Unicode)
    nom_profil = db.Column(db.Unicode)
    desc_profil = db.Column(db.Unicode)

    @classmethod
    def get_profils_in_app(cls, id_application):
        """
        Methode qui retourne tous les profils autorisés dans une app
        Parameters:
            id_app (int): l'id de l'application
        Returns:
            Array<TProfils>
        """
        return (
            db.session.query(TProfils)
            .join(CorProfilForApp, CorProfilForApp.id_profil == TProfils.id_profil)
            .filter(CorProfilForApp.id_application == id_application)
            .order_by(TProfils.code_profil)
            .all()
        )

    @classmethod
    def get_profil_in_app_with_code(cls, id_application, code_profil):
        """
            Methode qui retourne un profil à partir de son code
        """
        return (
            db.session.query(TProfils)
            .join(CorProfilForApp, CorProfilForApp.id_profil == TProfils.id_profil)
            .filter(CorProfilForApp.id_application == id_application)
            .filter(TProfils.code_profil == str(code_profil))
            .first()
        )

    @classmethod
    def get_profils_out_app(cls, id_application):
        """
        Methode qui retourne un dictionnaire des profils non utilisés
            pour une application
        Avec pour paramètre un id application
        """

        q = db.session.query(cls)
        subquery = db.session.query(CorProfilForApp.id_profil).filter(
            CorProfilForApp.id_application == id_application
        )
        q = q.filter(cls.id_profil.notin_(subquery))
        return [data.as_dict() for data in q.all()]

    @classmethod
    def choixSelect(
        cls, key="id_profil", label="nom_profil", id_application=None
    ):  # noqa
        """
        Methode qui retourne un tableau de tuples d'id profil et de
            nom de profil
        Ce que l'on met en key et label sont paramétrable

        """
        if id_application:
            profils = cls.get_profils_in_app(id_application)
            return [(getattr(d, key), getattr(d, label)) for d in profils]
        return [(getattr(d, key), getattr(d, label)) for d in cls.get_all()]


@serializable
class CorProfilForApp(GenericRepository):
    """ Classe de correspondance entre la table t_applications et la table t_profils"""

    __tablename__ = "cor_profil_for_app"
    __table_args__ = {"schema": "utilisateurs", "extend_existing": True}
    id_application = db.Column(
        db.Integer,
        ForeignKey("utilisateurs.t_applications.id_application"),
        primary_key=True,
    )
    id_profil = db.Column(
        db.Integer, ForeignKey("utilisateurs.t_profils.id_profil"), primary_key=True
    )
    profil_rel = relationship("TProfils")

    @classmethod
    def add_cor(cls, id_application, ids_profil):
        """
        Methode qui ajoute des relations applications <-> profil

        Avec pour paramètres un id profil et un tableau d'id d'applications
        """

        dict_add = dict()
        dict_add["id_application"] = id_application
        for d in ids_profil:
            dict_add["id_profil"] = d
            cls.post(dict_add)

    @classmethod
    def del_cor(cls, id_application, ids_profil):
        """
        Methode qui supprime des relations applications <-> profil

        Avec pour paramètres un id profil et un tableau d'id d'applications
        """

        for d in ids_profil:
            cls.query.filter(cls.id_application == id_application).filter(
                cls.id_profil == d
            ).delete()
            db.session.commit()


@serializable
class CorRoleAppProfil(GenericRepository):
    """
    Classe de correspondance entre la table t_roles, t_profils et
        t_applications
    """

    __tablename__ = "cor_role_app_profil"
    __table_args__ = {"schema": "utilisateurs", "extend_existing": True}
    id_role = db.Column(
        db.Integer, ForeignKey("utilisateurs.t_roles.id_role"), primary_key=True
    )
    id_profil = db.Column(
        db.Integer, ForeignKey("utilisateurs.t_profils.id_profil"), primary_key=True
    )
    id_application = db.Column(
        db.Integer,
        ForeignKey("utilisateurs.t_applications.id_application"),
        primary_key=True,
    )
    is_default_group_for_app = db.Column(db.Boolean, default=False)

    role_rel = relationship("TRoles")
    application_rel = relationship("TApplications")
    profil_rel = relationship("TProfils")

    # surchage de la méthode get_one
    # car il n'y a pas de clé primaire unique sur une cor
    @classmethod
    def get_one(cls, id_role, id_application):
        return (
            db.session.query(cls)
            .filter_by(id_role=id_role, id_application=id_application)
            .first()
        )

    @classmethod
    def get_default_for_app(cls, id_application):
        return (
            db.session.query(cls)
            .filter_by(id_application=id_application)
            .filter_by(is_default_group_for_app=True)
            .first()
        )

    # surchage de la méthode delete car
    # il n'y a pas de clé primaire unique sur une cor
    # TODO cette méthode supprime tous les profils
    # pour une application et un role
    # faire une méthode qui supprime seulement
    # un enregistrement grace à une PK unique
    # necessite ne pas utiliser le template
    # table_database.html qui est trop génériqe
    @classmethod
    def delete(cls, id_role, id_application):
        cors = (
            db.session.query(cls)
            .filter_by(id_role=id_role, id_application=id_application)
            .all()
        )
        for cor in cors:
            db.session.delete(cor)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def add_cor(cls, id_app, tab_profil):
        dict_add = {}
        for d in tab_profil:
            dict_add = {
                "id_role": d["id_role"],
                "id_profil": d["id_profil"],
                "id_application": id_app,
            }
            cls.post(dict_add)

    @classmethod
    def del_cor(cls, id_app, tab_profil):
        for t in tab_profil:
            cls.query.filter(cls.id_role == t["id_role"]).filter(
                cls.id_profil == t["id_profil"]
            ).filter(cls.id_application == id_app).delete()
            db.session.commit()

