# https://flask-jwt-extended.readthedocs.io/en/stable/
from flask import Flask, redirect
from flask import jsonify
from flask import request
from flask import render_template

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies

from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)

# Setup DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'sqlite.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Here you can globally configure all the ways you want to allow JWTs to
# be sent to your web application. By default, this will be only headers.
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SECURE"] = False

# Change this in your code!
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Token expires (hours=1) or (days=30) etc

jwt = JWTManager(app)

# DB model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(50),nullable=False,unique=True)
    passWord = db.Column(db.String(300),nullable=False,unique=False)


# create DB
db.create_all()
# Confirm add data to DB
db.session.commit()




#  MAIN CODE
@app.route("/login_with_cookies", methods=["POST","GET"])
def login_with_cookies():
    if request.method == "POST":
        # # RESTAPI 
        # user_name = request.json["username"]
        # pass_word = request.json["password"]
        
        user_name = request.form["username"]
        pass_word = request.form["password"]
        
        user = User.query.filter_by(userName=user_name).first()

        
        if user is None:
            return jsonify({"error": "Unauthorized, no such user"}), 401, {"Refresh": "1; url=/login_with_cookies"}
        elif pass_word != user.passWord:
            return jsonify({"error": "Incorrect Password"}), 401, {"Refresh": "1; url=/login_with_cookies"}

        else:
             # if user_name != "test" or pass_word != "test":
            #     return jsonify({"msg": "Bad username or password"}), 401
            username_variable= user.userName
            response = jsonify({"msg": "login successful"},{"Welcome": username_variable})
            access_token = create_access_token(identity=user_name)
            # set the access token to cookies
            set_access_cookies(response, access_token)

            # To print the cookies access token
            # print(request.cookies.get("access_token_cookie"))


        return response,{"Refresh": "1; url=/login_with_cookies"}

    else:
        return render_template("login_with_cookies.html")

# MAIN CODE
@app.route("/logout_with_cookies", methods=["POST","GET"])
def logout_with_cookies():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    #  can redirect after 1 second - {"Refresh": "1; url=https://google.com"}
    return response,{"Refresh": "1; url=/login_with_cookies"}

# MAIN CODE
@app.route("/protected", methods=["GET", "POST"])
@jwt_required()
def protected():
    return jsonify(Congratulations="Login successful")

# MAIN CODE
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method =="POST":
        
        user_name = request.form["username"]
        pass_word = request.form["password"]
        user = User.query.filter_by(userName=user_name).first()

        if user is None:
            registerAdd = User(userName=user_name, passWord=pass_word)

            db.session.add(registerAdd)
            db.session.commit()
            response = jsonify({"msg": "register successful"})
            return response,{"Refresh": "1; url=/login_with_cookies"}
        else:
            response = jsonify({"msg": "user already exists"})
            return response,{"Refresh": "1; url=/login_with_cookies"}

    else:
        return render_template("register.html")



@app.route("/", methods=["GET"])
def index():
    return redirect("/login_with_cookies")


@app.route("/login_without_cookies", methods=["POST","GET"])
def login_without_cookies():
    if request.method == "POST":
        user_name = request.form["username"]
        pass_word = request.form["password"]

        if user_name != "test" or pass_word != "test":
            return jsonify({"msg": "Bad username or password"}), 401
        response = jsonify({"msg": "login successful"})
        access_token = create_access_token(identity=user_name)

        # access_token = create_access_token(identity="example_user")
        return jsonify(access_token=access_token)
    else:
        return render_template("login_without_cookies.html")



@app.route("/only_headers")
@jwt_required(locations=["headers"])
def only_headers():
    return jsonify(foo="baz")


if __name__ == "__main__":
    app.run()