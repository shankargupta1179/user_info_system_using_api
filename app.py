import os
from flask import Flask
from flask_smorest import Api
from db import db
from flask_jwt_extended import JWTManager
from resources.user import blp as UserBluePrint
from resources.auth import blp as AuthBluePrint

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = " REST API Project"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["SQLALCHEMY_DATABASE_URI"] =db_url or  os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    

    api = Api(app)
    app.config["JWT_SECRET_KEY"] ="jose"
    jwt = JWTManager(app)

    @app.before_first_request
    def create_tables():
        import models
        db.create_all()

    api.register_blueprint(UserBluePrint)
    api.register_blueprint(AuthBluePrint)

    return app