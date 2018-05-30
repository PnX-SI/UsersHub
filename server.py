from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.env import db
import config



""" Serveur de l'application UsersHub """



app = Flask(__name__, template_folder= "app/templates" , static_folder = 'app/static' )

app.secret_key = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
db.init_app(app)
with app.app_context():

    from app.t_roles import route
    app.register_blueprint(route.route,  url_prefix='/')

    from app.bib_organismes import route
    app.register_blueprint(route.route,  url_prefix='/')

    from app.groupe import route
    app.register_blueprint(route.route,  url_prefix='/')

    from app.t_applications import route
    app.register_blueprint(route.route, url_prefix='/')

    from app.t_tags import route
    app.register_blueprint(route.route, url_prefix='/')

    from app.bib_tag_types import route
    app.register_blueprint(route.route, url_prefix='/')

    from app.auth import route
    app.register_blueprint(route.route, url_prefix='/log')

    from app.CRUVED import route
    app.register_blueprint(route.route, url_prefix='/')


if __name__ == '__main__':
    app.run(debug=True)