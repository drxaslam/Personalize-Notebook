from flask import request
from flask_restful import Resource
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash

from app.md.models import User
from app import db
from app.md.serilizer import UserSchema

class SignUpView(Resource):

    def post(self):
        data = request.get_json()
        existing_username = User.query.filter_by(username=data["username"]).first()
        print(existing_username)
        existing_email = User.query.filter_by(email=data["email"]).first()
        if existing_username:
            raise HTTPException({"username": "Username is already in use."})

        if existing_email:
            raise HTTPException({"email": "Email is already in use."})

        if len(data["name"]) < 2:
            raise HTTPException({"name":"First name must be greater than 1 character."})
        
        if data["password"] != data["password2"]:
            raise HTTPException({"password":"Passwords don't match."})
        
        if len(data["password"]) < 7:
            raise HTTPException({'password':'Password must be at least 7 characters.'})
        
        data['password'] = generate_password_hash(data['password'])
        
        user = User(name=data["name"],username=data["username"],email=data["email"],_password=data["password"])
        db.session.add(user)
        db.session.commit()

        return UserSchema().dump(user),201