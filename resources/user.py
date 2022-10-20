from email import message
from flask_jwt_extended import jwt_required
import jwt
from sqlalchemy import delete
from db import db 
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from sqlalchemy.exc import SQLAlchemyError
from models import UserModel
from schemas import PlainUserSchema, UserUpdateSchema

blp = Blueprint("Users","users",description="Operations on users")

@blp.route("/users")
class Users(MethodView):
    @jwt_required()
    @blp.response(200,PlainUserSchema(many=True))
    def get(self):
        return UserModel.query.all()
    
    @jwt_required()
    @blp.arguments(PlainUserSchema)
    @blp.response(200,PlainUserSchema)
    def post(self,user_data):
        user = UserModel(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="Error occurred while creating the user")
        return user,201

@blp.route("/users/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.arguments(UserUpdateSchema)
    @blp.response(200,PlainUserSchema)
    def put(self,user_data,user_id):
        user = UserModel.query.get(user_id)
        if user:
            user.name = user_data["name"]
            user.address = user_data["address"]
            user.contact = user_data["contact"]
        else:
            user = UserModel(id=user_id,**user_data)

        try:
            db.session.add(user)
            db.session.commit()
        except:
            abort(message="An error occurred while connecting to the database")
        return user

    @jwt_required()
    def delete(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except:
            abort(message="An error occurred while connecting to the database")
        return {"message":"User deleted successfully"}
    


