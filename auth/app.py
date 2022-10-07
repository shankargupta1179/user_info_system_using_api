from flask import Flask,request
import uuid

auth = {}

app = Flask(__name__)

@app.post("/login")
def login():
    request_data = request.get_json()
    if request_data["password"] == auth[request_data["username"]]:
        return {"message":"Login Successful"}
    return {"message":"Invalid Credentials "}

@app.post("/signup")
def signup():
    request_data = request.get_json()
    username = request_data["username"]
    password = request_data["password"]
    new_user = {**request_data,"id":username}
    auth[username] = password
    return new_user , 201