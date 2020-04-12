from urllib.parse import parse_qs
from bson.json_util import dumps
from flask import Flask, request, jsonify
import json
import ast
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash


DATABASE = MongoClient()['restfulapi'] # DB_NAME
DEBUG = True
client = MongoClient('localhost', 27017)

	
app = Flask(__name__)


# Select the database
#run docker with mongodb   
# docker run -d -p 27017:27017 -v ~/data:/data/db mongo
db = client.restfulapi


##------
user = db.users

##-------

jwt = JWTManager(app)

# JWT Config
app.config["JWT_SECRET_KEY"] = "blablabla"
secret="blabla"


@app.route("/register", methods=["POST"])
## curl -X POST -F 'first_name=Eldar' -F 'last_name=Garayev'  -F 'email=1@1.ru' -F 'password=password'  http://localhost:5001/register
def register():
    email = request.form["email"]
    # test = User.query.filter_by(email=email).first()
    test = user.find_one({"email": email})
    if test:
        return jsonify(message="User Already Exist"), 409
    else:
        #import jwt
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        password_hash=generate_password_hash(password)
        email = request.form["email"]
        user_info = dict(first_name=first_name, last_name=last_name, email=email, password=password_hash)
        user.insert_one(user_info)
        return jsonify(message="User added sucessfully"), 201


@app.route("/login", methods=["POST"])
## curl -d '{"email": "1@1.ru", "password": "password"}' -H "Content-Type: application/json" -X POST http://localhost:5001/login
def login():
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
    else:
        email = request.form["email"]
        password = request.form["password"]

		
    hashed_pass=user.find_one({"email": email})
    hashed_pass = hashed_pass['password']
    if check_password_hash(hashed_pass, password):
	
        access_token = create_access_token(identity=email)
        return jsonify(message="Login Succeeded!", access_token=access_token), 201
    else:
        return jsonify(message="Bad Email or Password"), 401

#app.run(debug=True)
if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5001)