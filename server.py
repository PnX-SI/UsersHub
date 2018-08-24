import json

from flask import Flask, redirect, url_for, request, session, render_template
from app.env import db
from config import config


"""
    Serveur de l'application UsersHub
"""
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


app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder='app/static'
)

app.wsgi_app = ReverseProxied(app.wsgi_app, script_name=config.URL_APPLICATION)

app.config.from_pyfile('config/config.py')
app.secret_key = config.SECRET_KEY

db.init_app(app)

with app.app_context():
    app.jinja_env.globals['url_application'] = app.config["URL_APPLICATION"]

    if config.ACTIVATE_APP:
        @app.route('/')
        def index():
            ''' Route par défaut de l'application '''
            return redirect(url_for('user.users'))

        @app.route('/constants.js')
        def constants_js():
            ''' Route des constantes javascript '''
            return render_template('constants.js')


        @app.after_request
        def after_login_method(response):
            if not request.cookies.get('token'):
                session["current_user"] = None

            if request.endpoint == 'auth.login' and response.status_code == 200:
                current_user = json.loads(response.get_data().decode('utf-8'))
                session["current_user"] = current_user["user"]

            return response



        from pypnusershub import routes
        app.register_blueprint(routes.routes, url_prefix='/pypn/auth')

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

        from app.auth import route
        app.register_blueprint(route.route,  url_prefix='/login')

    if config.ACTIVATE_API:
        from app.API import route_register
        app.register_blueprint(route_register.route, url_prefix='/api_register')


if __name__ == '__main__':
    app.run(debug=config.DEBUG, port=config.PORT)

