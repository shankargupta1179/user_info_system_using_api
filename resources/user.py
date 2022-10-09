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
    @blp.response(200,PlainUserSchema(many=True))
    def get(self):
        return UserModel.query.all()
    
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
    @blp.arguments(UserUpdateSchema)
    @blp.response(200,PlainUserSchema)
    def put(self,user_data,user_id):
        user = UserModel.query.get(user_id)
        if user:
            #return user
            return user_data["name"]
            user.name = user_data["name"]
            user.address= user_data["address"]
            user.contact = user_data["contact"]
            # user.dob = user_data["dob"]
            # user.gender = user_data["gender"]
        else:
            user = UserModel(id=user_id,**user_data)

        db.session.add(user)
        db.session.commit()

        return user

    def delete(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"message":"User deleted successfully"}
    
from flask import Flask,request
import uuid

users = {}

# this is user python file
#app = Flask(__name__)

# @app.get("/users")
# def get_users():
#     return {"users":list(users.values())}


# @app.post("/users")
# def create_user():
#     request_data = request.get_json()
#     user_id = uuid.uuid1()
#     new_user = {**request_data,"id":user_id}
#     users[user_id] = new_user
#     return new_user,201


# @app.put("/users/<uuid:id>")
# def edit_user(id):
#     request_data = request.get_json()
#     try:
#         data = users[id]
#         data |= request_data
#         return {"message":"Details edited"}
#     except KeyError:
#         return {"message":"No such user found"},404


# @app.delete("/users/<uuid:id>")
# def delete_user(id):
#     try:
#         del users[id]
#         return {"message":"User Deleted Successfully"}
#     except:
#         return {"message":"No such user found in the data"}