from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db=SQLAlchemy()
DB_NAME="database.db"

def create_app():
    global app
    app=Flask(__name__)
    app.config['SECRET_KEY']='secretkey'
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .auth.controller import auth_blueprint
    app.register_blueprint(
        auth_blueprint,
        url_prefix=f"/api/{auth_blueprint.url_prefix}",
    )

    from .md.controller import md_blueprint
    app.register_blueprint(
        md_blueprint,
        url_prefix=f"/api/{md_blueprint.url_prefix}",
    )
    
    from app.md.models import User,Note

    create_database(app)

    return app

def create_database(app):
    with app.app_context():
        db.create_all()