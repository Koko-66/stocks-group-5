from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators

from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
#importing database
from src.database import User

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    # checks password/username lengths and that username is alphanumeric without spaces
    if len(password) < 6:
        return jsonify({'Error': "Your password must have at least 6 characters"}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({'Error': "Your username must have at least 3 characters"}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify(
            {'Error': "Username should be alphanumeric and should not contain any spaces"}), HTTP_400_BAD_REQUEST

    # checking if email is valid
    if not validators.email(email):
        return jsonify({'Error': "Invalid email address"}), HTTP_400_BAD_REQUEST

    #checking if email already exists in database
    if User.objects.filter_by(email=email).first() is not None:
        if not validators.email(email):
            return jsonify({'Error': "Account with this email address already exists"}), HTTP_409_CONFLICT

    # checking if username already exists in database
    if User.objects.filter_by(username=username).first() is not None:
        if not validators.email(email):
            return jsonify({'Error': "This username is already taken"}), HTTP_409_CONFLICT
    return "Successful registration!"


    #hashing
    pwd_hash=generate_password_hash(password)

    #save new user to our db




@auth.get('/me')
def mer():
    return {"user": "me"}
