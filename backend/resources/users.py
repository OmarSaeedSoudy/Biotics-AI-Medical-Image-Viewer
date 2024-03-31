from flask.views import MethodView
from flask_smorest import abort, Blueprint
from passlib.hash import pbkdf2_sha256
from flask import make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from db import db
from models import UserModel
from schemas import UserCreateSchema, UserLoginSchema
from blocklist import BLOCKLIST

# Initialize Blueprint for Users API Endpoints
blp = Blueprint("Users", "users", description="Users API Endpoints")

# User Registration Endpoint
@blp.route("/user/register")
class UserRegister(MethodView):
    @blp.arguments(UserCreateSchema)
    def post(self, user_data):
        """
        Endpoint to register a new user.
        
        Parameters:
            user_data (dict): User data including username and password
        
        Returns:
            dict: Success message and access token
        """
        # Check if username already exists
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="Username Already Exists")
        
        # Hash the password using pbkdf2_sha256
        hashed_password = pbkdf2_sha256.hash(user_data['password'])
        
        # Create new user object
        user = UserModel(
            username = user_data['username'],
            password = hashed_password
        )
        
        # Add user to database and commit
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return {
            "message": "User Created Successfully.",
            "access_token": access_token
        },  201
    

# User Login Endpoint
@blp.route("/user/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        """
        Endpoint to login a user.
        
        Parameters:
            user_data (dict): User data including username and password
        
        Returns:
            dict: Success message and access token
        """
        # Query user from database
        user = UserModel.query.filter(UserModel.username == user_data['username']).first()
        
        # Verify password
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            # Create access token
            access_token = create_access_token(identity=user.id)
            
            # Create HTTP response
            response = make_response({
                "message": "Login successful",
                "access_token": access_token
            })
            
            # Set cookie with access token
            response.set_cookie("jwtToken", value=access_token, httponly=True, secure=True)
            
            # Set CORS headers
            response.headers.add("Access-Control-Allow-Credentials", "true")
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
            response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
            
            return response
        
        abort(401, message="Invalid Credentials.")
    

# User Logout Endpoint
@blp.route("/user/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        """
        Endpoint to logout a user.
        
        Returns:
            dict: Success message
        """
        # Get JWT token from current request
        jti = get_jwt()["jti"]
        
        # Add token to blocklist
        BLOCKLIST.add(jti)
        
        return {
            "message": "Successfully Signed Out."
        }


# User Detail and Deletion Endpoint
@blp.route("/user/<int:user_id>")
class UserDetail(MethodView):
    @jwt_required()
    def get(self, user_id):
        """
        Endpoint to get user details.
        
        Parameters:
            user_id (int): User ID
        
        Returns:
            dict: User details
        """
        user = UserModel.query.get_or_404(user_id)
        return user
    
    @jwt_required()
    def delete(self, user_id):
        """
        Endpoint to delete a user.
        
        Parameters:
            user_id (int): User ID
        
        Returns:
            dict: Success message
        """
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {
            "message": "User Deleted Successfully."
        }, 200
