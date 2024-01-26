"""
Fonctions utilitaires
"""

import json
from functools import wraps

from dateutil import parser
from flask import Response, current_app
from werkzeug.datastructures import Headers

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import ColumnProperty


# def testDataType(value, sqlType, paramName):
#     if sqlType == DB.Integer or isinstance(sqlType, (DB.Integer)):
#         try:
#             int(value)
#         except Exception as e:
#             return '{0} must be an integer'.format(paramName)
#     if sqlType == DB.Numeric or isinstance(sqlType, (DB.Numeric)):
#         try:
#             float(value)
#         except Exception as e:
#             return '{0} must be an float (decimal separator .)'\
#                 .format(paramName)
#     elif sqlType == DB.DateTime or isinstance(sqlType, (DB.Date, DB.DateTime)):
#         try:
#             dt = parser.parse(value)
#         except Exception as e:
#             return '{0} must be an date (yyyy-mm-dd)'.format(paramName)
#     return None

"""
    Liste des types de donnees sql qui
    necessite une sérialisation particulière en
     MANQUE FLOAT
"""
SERIALIZERS = {
    "date": lambda x: str(x) if x else None,
    "datetime": lambda x: str(x) if x else None,
    "time": lambda x: str(x) if x else None,
    "timestamp": lambda x: str(x) if x else None,
    "uuid": lambda x: str(x) if x else None,
}


class GenericTable:
    """
    Classe permettant de créer à la volée un mapping
        d'une vue avec la base de données par rétroingénierie
    """

    def __init__(self, tableName, schemaName, geometry_field):
        meta = MetaData(schema=schemaName, bind=DB.engine)
        meta.reflect(views=True)
        try:
            self.tableDef = meta.tables["{}.{}".format(schemaName, tableName)]
        except KeyError:
            raise KeyError("table doesn't exists")

        self.geometry_field = geometry_field

        # Mise en place d'un mapping des colonnes en vue d'une sérialisation
        self.serialize_columns = [
            (name, SERIALIZERS.get(db_col.type.__class__.__name__.lower(), lambda x: x))
            for name, db_col in self.tableDef.columns.items()
            if not db_col.type.__class__.__name__ == "Geometry"
        ]
        self.columns = [column.name for column in self.tableDef.columns]

    def as_dict(self, data):
        return {
            item: _serializer(getattr(data, item))
            for item, _serializer in self.serialize_columns
        }


def serializeQuery(data, columnDef):
    rows = [
        {
            c["name"]: getattr(row, c["name"])
            for c in columnDef
            if getattr(row, c["name"]) is not None
        }
        for row in data
    ]
    return rows


def serializeQueryTest(data, columnDef):
    rows = list()
    for row in data:
        inter = {}
        for c in columnDef:
            if getattr(row, c["name"]) is not None:
                if isinstance(c["type"], (DB.Date, DB.DateTime, UUID)):
                    inter[c["name"]] = str(getattr(row, c["name"]))
                elif isinstance(c["type"], DB.Numeric):
                    inter[c["name"]] = float(getattr(row, c["name"]))
                elif not isinstance(c["type"], Geometry):
                    inter[c["name"]] = getattr(row, c["name"])
        rows.append(inter)
    return rows


def serializeQueryOneResult(row, columnDef):
    row = {
        c["name"]: getattr(row, c["name"])
        for c in columnDef
        if getattr(row, c["name"]) is not None
    }
    return row


def serializable(cls):
    """
    Décorateur de classe pour les DB.Models
    Permet de rajouter la fonction as_dict qui est basée sur le mapping SQLAlchemy
    """

    """
        Liste des propriétés sérialisables de la classe
        associées à leur sérializer en fonction de leur type
    """
    cls_db_columns = []
    for prop in cls.__mapper__.column_attrs:
        if isinstance(prop, ColumnProperty) and len(prop.columns) == 1:
            db_col = prop.columns[0]
            # HACK
            #  -> Récupération du nom de l'attribut sans la classe
            name = str(prop).split(".", 1)[1]
            if not db_col.type.__class__.__name__ == "Geometry":
                cls_db_columns.append(
                    (
                        name,
                        SERIALIZERS.get(
                            db_col.type.__class__.__name__.lower(), lambda x: x
                        ),
                    )
                )

    """
        Liste des propriétés synonymes
        sérialisables de la classe
        associées à leur sérializer en fonction de leur type
    """
    for syn in cls.__mapper__.synonyms:
        col = cls.__mapper__.c[syn.name]
        # if column type is geometry pass
        if col.type.__class__.__name__ == "Geometry":
            pass

        # else add synonyms in columns properties
        cls_db_columns.append(
            (syn.key, SERIALIZERS.get(col.type.__class__.__name__.lower(), lambda x: x))
        )

    """
        Liste des propriétés de type relationship
        uselist permet de savoir si c'est une collection de sous objet
        sa valeur est déduite du type de relation
        (OneToMany, ManyToOne ou ManyToMany)
    """
    cls_db_relationships = [
        (db_rel.key, db_rel.uselist) for db_rel in cls.__mapper__.relationships
    ]

    def serializefn(self, recursif=False, columns=()):
        """
        Méthode qui renvoie les données de l'objet sous la forme d'un dict
        Parameters
        ----------
            recursif: boolean
                Spécifie si on veut que les sous objet (relationship)
                soit également sérialisé
            columns: liste
                liste des colonnes qui doivent être prises en compte
        """
        if columns:
            fprops = list(filter(lambda d: d[0] in columns, cls_db_columns))
        else:
            fprops = cls_db_columns

        out = {item: _serializer(getattr(self, item)) for item, _serializer in fprops}

        if recursif is False:
            return out
        for rel, uselist in cls_db_relationships:
            if getattr(self, rel) is None:
                break

            if uselist is True:
                out[rel] = [x.as_dict(recursif) for x in getattr(self, rel)]
            else:
                out[rel] = getattr(self, rel).as_dict(recursif)

        return out

    cls.as_dict = serializefn
    return cls


def json_resp(fn):
    """
    Décorateur transformant le résultat renvoyé par une vue
    en objet JSON
    """

    @wraps(fn)
    def _json_resp(*args, **kwargs):
        res = fn(*args, **kwargs)
        if isinstance(res, tuple):
            res, status = res
        else:
            status = 200

        if not res:
            status = 404
            res = {"message": "not found"}

        return Response(json.dumps(res), status=status, mimetype="application/json")

    return _json_resp


def csv_resp(fn):
    """
    Décorateur transformant le résultat renvoyé en un fichier csv
    """

    @wraps(fn)
    def _csv_resp(*args, **kwargs):
        res = fn(*args, **kwargs)
        filename, data, columns, separator = res
        outdata = [separator.join(columns)]

        headers = Headers()
        headers.add("Content-Type", "text/plain")
        headers.add(
            "Content-Disposition", "attachment", filename="export_%s.csv" % filename
        )

        for o in data:
            outdata.append(
                separator.join(
                    '"%s"' % (o.get(i), "")[o.get(i) is None] for i in columns
                )
            )
        out = "\r\n".join(outdata)
        return Response(out, headers=headers)

    return _csv_resp
