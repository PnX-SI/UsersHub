
from flask_sqlalchemy import SQLAlchemy

from config import config

"""
Création de la base avec sqlalchemy
"""

db = SQLAlchemy()
# URL_REDIRECT = None
URL_REDIRECT = "{}/{}".format(config.URL_APPLICATION, "login/")
