from email import message
from flask import request
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
api_key = "PMAK-63510c63c920ab1483870f6b-5423565c43709d85b21ff5b6b1cbf70bf3"
@blp.route("/users")
class Users(MethodView):
    @jwt_required()
    @blp.response(200,PlainUserSchema(many=True))
    def get(self):
        response = request.get_json()
        passed_key = response["api_key"]
        if passed_key!=api_key:
            abort(message="Sorry you are not allowed to view this resource")
        else :
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
    


