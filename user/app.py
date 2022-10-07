from flask import Flask,request
import uuid
users = {}


app = Flask(__name__)

@app.get("/users")
def get_users():
    return {"users":list(users.values())}


@app.post("/users")
def create_user():
    request_data = request.get_json()
    user_id = uuid.uuid1()
    new_user = {**request_data,"id":user_id}
    users[user_id] = new_user
    return new_user,201


@app.put("/users/<uuid:id>")
def edit_user(id):
    request_data = request.get_json()
    try:
        data = users[id]
        data |= request_data
        return {"message":"Details edited"}
    except KeyError:
        return {"message":"No such user found"},404


@app.delete("/users/<uuid:id>")
def delete_user(id):
    try:
        del users[id]
        return {"message":"User Deleted Successfully"}
    except:
        return {"message":"No such user found in the data"}