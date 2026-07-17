import os
from flask_sqlalchemy import SQLAlchemy

"""
Création de la base avec sqlalchemy
"""

os.environ["FLASK_SQLALCHEMY_DB"] = "app.env.db"
db = SQLAlchemy()
