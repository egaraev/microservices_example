import flask, os, socket, subprocess, requests, json, consul
from urllib.parse import parse_qs
from bson.json_util import dumps
from flask import Flask, request, jsonify, render_template, flash
import json
import ast
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, jwt_refresh_token_required, create_refresh_token,get_jwt_identity, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_wtf import FlaskForm

#time.sleep(5) # seconds

# fetch consul's ip, so that we can talk to it.
CONSUL_ALIAS = 'consul'
CONSUL_PORT = '8500'
CONSUL_IP = subprocess.check_output(['getent', 'hosts', CONSUL_ALIAS]).decode().split()[0]
# create consul instance (not agent, just python instance)
c = consul.Consul(host=CONSUL_IP, port=CONSUL_PORT)
# get mongodb IP
keyindex, mongodb_ip_bytes = c.kv.get('mongodb')
mongodb_ip = mongodb_ip_bytes['Value'].decode()


DATABASE = MongoClient()['restfulapi'] # DB_NAME
DEBUG = True
client = MongoClient(mongodb_ip, 27017)


	
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
#app.config['JWT_TOKEN_LOCATION'] = ['cookies']
#app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
#app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config["JWT_SECRET_KEY"] = "blablabla"
secret="blabla"



class RegistrationForm(Form):
    first_name = TextField('Fisrt_Name:', validators=[validators.required()])
    last_name = TextField('Last_Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])

	
	
	
@app.route("/", methods=["GET", "POST"])
## curl -X POST -F 'first_name=Eldar' -F 'last_name=Garayev'  -F 'email=1@1.ru' -F 'password=password'  http://localhost:5001/register
def register():
    form = RegistrationForm(request.form)
    print (form.errors)


	
    if request.method == "POST":
        email = request.form["email"]
        test = user.find_one({"email": email})
        if test:
            return jsonify(message="User Already Exist"), 409
        else:

            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            password = request.form["password"]
            password_hash=generate_password_hash(password)
            email = request.form["email"]
            user_info = dict(first_name=first_name, last_name=last_name, email=email, password=password_hash)
            user.insert_one(user_info)
        return jsonify(message="User added sucessfully"), 201

  
    return render_template('register.html', form=form)


class LoginForm(Form):
    email = TextField('Email:')
    password = TextField('Password:')	
	
@app.route("/login", methods=["GET", "POST"])
## curl -d '{"email": "1@1.ru", "password": "password"}' -H "Content-Type: application/json" -X POST http://localhost:5001/login
def login():
    form = LoginForm(request.form)
    print (form.errors)

    
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
		
    if request.method == "POST":
       email = request.form["email"]
       password = request.form["password"]
       test = user.find_one({"email": email})
       hashed_password=user.find_one({"email": email})
       hashed_pass = hashed_password['password']
	
       if test and check_password_hash(hashed_pass, password):
#          hashed_pass=user.find_one({"email": email})
#          hashed_pass = hashed_pass['password']
#          if check_password_hash(hashed_pass, password):
          access_token = create_access_token(identity=email)
          resp = jsonify({'login': True}, {'Access_token': access_token})
#          set_access_cookies(resp, access_token)
          return resp, 200
       else:
          return jsonify(message="Bad Email or Password"), 409
    return render_template('login.html', form=form)

#app.run(debug=True)
if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5001)