from userhub.env import db



class GenericRepository(db.Model):
    __abstract__ = True


    @classmethod
    def get_one(cls,id):
        data = db.session.query(cls).get(id)
        return data.as_dict(True)

    @classmethod
    def get_all(cls,columns=None, params = None):
        if params == None :
            return [data.as_dict(True,columns) for data in db.session.query(cls).all()]
        else:
            q = db.session.query(cls)
            for param in params : 
                nom_col = getattr(cls,param['col'])
                q = q.filter(nom_col == param['filter'])
            return [data.as_dict(True,columns) for data in q.all()]



    @classmethod
    def post(cls, entity_dict):
        db.session.add(cls(**entity_dict))
        db.session.commit()

    @classmethod
    def update(cls, entity_dict):
        db.session.merge(cls(**entity_dict))
        db.session.commit()

    @classmethod
    def delete(cls,id):
        db.session.delete(db.session.query(cls).get(id))
        db.session.commit()

    @classmethod
    def choixOrg(cls):
        return ""


    
    # @classmethod
    # def get_column_name(cls,columns=None):
    #     if columns:
    #         for col in cls.__table__.columns.keys()

    #     return cls.__table__.columns.keys()



    