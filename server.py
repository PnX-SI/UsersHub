from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.env import db
from config import config



""" Serveur de l'application UsersHub """


class ReverseProxied(object):

    def __init__(self, app, script_name=None, scheme=None, server=None):
        self.app = app
        self.script_name = script_name
        self.scheme = scheme
        self.server = server

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '') or self.script_name
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        scheme = environ.get('HTTP_X_SCHEME', '') or self.scheme
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        server = environ.get('HTTP_X_FORWARDED_SERVER', '') or self.server
        if server:
            environ['HTTP_HOST'] = server
        return self.app(environ, start_response)


app = Flask(__name__, template_folder= "app/templates" , static_folder = 'app/static' )

app.wsgi_app = ReverseProxied(app.wsgi_app, script_name=config.URL_APPLICATION)

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

    from app.API import route
    app.register_blueprint(route.route, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=config.DEBUG, port=config.PORT)