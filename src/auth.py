from flask import Blueprint


auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.post('/register')
def register():
    return "Successful registration!"


@auth.get('/me')
def mer():
    return {"user": "me"}
