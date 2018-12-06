from flask import current_app,Blueprint, jsonify
from app.env import db
from app.models import TRoles, Bib_Organismes


def admin_valide(id,pw):
    q = db.session.query(TRoles)
    q =q.filter(TRoles.identifiant == 'admin')
    data = q.all()
    for trole in data:
        if trole.identifiant == id and trole.pass_plus == pw:
            return True
    return False

def utilisateurs():
    q = db.session.query(TRoles)
    return [user.as_dict() for user in q.all()]

def getUser(id_role):
    q = db.session.query(TRoles)
    q = q.filter(TRoles.id_role == id_role)
    user = q.one()
    print(user.organisme_rel)
    return user.as_dict(True)
    

def addorupdateuser(user_dict):
    print(user_dict)
    if 'id_role' in user_dict:
        new_user = TRoles(**user_dict)
        db.session.merge(new_user)
        db.session.commit()
    else :
        print('bjr')
        new_user = TRoles(**user_dict)
        db.session.add(new_user)
        db.session.commit()



def deleteuser(id):
    q = db.session.query(TRoles)
    q =q.filter(TRoles.id_role == id)
    db.session.delete(q.one())
    db.session.commit()



