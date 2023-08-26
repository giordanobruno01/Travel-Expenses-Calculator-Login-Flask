from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from project import db, create_app, models

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'giordano-secrets'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
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

