from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path,getenv
from flask_login import LoginManager
from dotenv import load_dotenv
import sqlalchemy

load_dotenv()
secret_key = getenv("secret_key")
sqlalchemy_database_uri = getenv("sqlalchemy_database_uri")
db_name = getenv("db_name")

db = SQLAlchemy()

def create_app():

    app = Flask(__name__,template_folder='../../../frontend/templates',static_folder="../../../frontend/static")
    app.config["SECRET_KEY"] = secret_key

    app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri

    db.init_app(app)

    from .models import User,Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    return app

def create_database(app):
    if not path.exists("../../backend/database"+ db_name):
        db.create_all(app = app)
        print("Database Created")
    
    elif path.exists("../../backend/database"+ db_name):
        print("Database already created, please delete it and try again.")
