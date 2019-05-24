from flask import Flask
from flask_login import LoginManager
from .db import db, migrate
from flask_migrate import Migrate

# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db}


def create_app():
    #set up app configuration (including databse URI connection)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py') #load configuration from instance folder. this overrides the setups from Config object
    # setup login manager
    login_manager = LoginManager()
    login_manager.login_view = 'login'

    with app.app_context():
        #initialize the db with app then import the modelsexit to create the tables in DB
        db.init_app(app)

        from . import models
        db.create_all()

        #init with migration
        migrate.init_app(app, db)

        #initialize the login_manager and set login_view and session_protection
        login_manager.init_app(app)
        login_manager.login_view = 'login'

        #import routes
        from . import routes

        return app
