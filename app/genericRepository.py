from sqlalchemy.sql import text
from app.env import db


class GenericRepository(db.Model):
    __abstract__ = True

    """
    Classe abstraite contenant des méthodes générique d'ajout/suppression/lecture/mise à jour de la base
    """

    @classmethod
    def get_one(cls, id, as_model=False):
        """
        Methode qui retourne un dictionnaire d'un élément d'un Model
        Avec pour paramètres l'id de l'élément
        Si as_model != False alors au lieu de retourner un dictionnaire on retourne l'object du modèle
        """
        if id == None:
            return None

        if as_model == False:
            data = db.session.query(cls).get(id)
            return data.as_dict(True)
        else:
            return db.session.query(cls).get(id)

    @classmethod
    def get_all(
        cls,
        columns=None,
        params=None,
        recursif=True,
        as_model=False,
        order_by=None,
        order="asc",
    ):

        """
        Methode qui retourne un dictionnaire de tout les éléments d'un Model
        Avec pour paramètres:
                            columns un tableau des colonnes que l'ont souhaite récupérer
                            params un tableau contenant un dictionnaire de filtre [{'col': colonne à filtrer, 'filter': paramètre de filtrage}]
                            si recursif != True on désactive la fonction récursive du as_dict()
                            si as_model != False alors au lieu de retourner un dictionnaire on retourne une requête
        Si as_model != False alors au lieu de retourner un dictionnaire on retourne un tableau d'objets du modèle
        """

        data = None
        q = db.session.query(cls)
        if params:
            q = db.session.query(cls)
            for param in params:
                nom_col = getattr(cls, param["col"])
                q = q.filter(nom_col == param["filter"])
        if order_by:
            order_col = getattr(cls, order_by)
            order_col = order_col.desc() if order == "desc" else order_col.asc()
            q = q.order_by(order_col)
        data = q.all()
        if as_model:
            return data
        return [d.as_dict(recursif, columns) for d in data]

    @classmethod
    def post(cls, entity_dict):

        """
        Methode qui ajoute un élément à une table
        Avec pour paramètres un dictionnaire de cet élément
        Retourne le modèle nouvellement ajouté
        """
        try:
            model = cls(**entity_dict)
            db.session.add(model)
            db.session.commit()
            return model

        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def update(cls, entity_dict):

        """
        Methode qui met à jour un élément
        Avec pour paramètre un dictionnaire de cet élément
        Retourne le modèle mis à jour
        """
        try:
            model = cls(**entity_dict)
            db.session.merge(model)
            db.session.commit()
            return model
        except Exception as e:
            print(e)
            db.session.rollback()
            raise

    @classmethod
    def delete(cls, id):

        """
        Methode qui supprime un élement d'une table à partir d'un id donné
        Avec pour paramètre un id (clé primaire)
        """
        try:
            db.session.delete(db.session.query(cls).get(id))
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def choixSelect(cls, id, nom, aucun=None, order_by=None):

        """
        Methode qui retourne un tableau de tuples d'id  et de nom
        Avec pour paramètres un id et un nom
        Le paramètre aucun si il a une valeur permet de rajouter le tuple (-1,Aucun) au tableau
        """

        data = cls.get_all(order_by=order_by)
        choices = []
        for d in data:
            choices.append((d[id], d[nom]))
        if aucun != None:
            choices.append((-1, "Aucun"))
        return choices

    # def get_column_name(cls,columns=None):
    #     if columns:
    #         for col in cls.__table__.columns.keys()

    #     return cls.__table__.columns.keys()

