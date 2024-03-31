from flask.views import MethodView
from flask_smorest import abort, Blueprint
from passlib.hash import pbkdf2_sha256
from flask import make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from db import db
from models import UserModel
from schemas import UserCreateSchema, UserLoginSchema
from blocklist import BLOCKLIST

blp = Blueprint("Users", "users", description="Users API Endpoints")

@blp.route("/user/register")
class UserRegister(MethodView):
    @blp.arguments(UserCreateSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="Username Already Exists")
        
        user = UserModel(
            username = user_data['username'],
            password = pbkdf2_sha256.hash(user_data['password'])
        )
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=user.id)
        return {
            "message": "User Created Successfully.",
            "access_token": access_token
        },  201
    

@blp.route("/user/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        print(user_data)
        user = UserModel.query.filter(UserModel.username == user_data['username']).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            response = make_response({
                "message": "Login successful",
                "access_token": access_token
            })
            response.set_cookie("jwtToken", value=access_token, httponly=True, secure=True)  # secure=True for HTTPS
            
            # Set CORS headers
            response.headers.add("Access-Control-Allow-Credentials", "true")
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
            response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

            print(response)
            return response
        
        abort(401, message="Invalid Credentials.")
    

@blp.route("/user/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self, user_data):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {
            "message": "Successfully Signed Out."
        }


@blp.route("/user/<int:user_id>")
class UserRegister(MethodView):
    @jwt_required()
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        print("User Query: ", user)
        return user
    
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {
            "message": "User Deleted Successfully."
        }, 200