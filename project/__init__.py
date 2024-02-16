from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from project import db, create_app, models

db = SQLAlchemy()

def create_app():
    app = Flask(__name__) 

    app.config['SECRET_KEY'] = 'giordano-secrets'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
   

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # db.create_all(app=create_app())
    with app.app_context():
        
        db.create_all()

    # blueprint for auth routes in our app
    from .auth import auth 
    app.register_blueprint(auth)
  
    # blueprint for non-auth parts of app
    from .main import main  
    app.register_blueprint(main)

    return app
    # export FLASK_APP=project
    # export FLASK_DEBUG=1
    # python3 -m venv auth
    