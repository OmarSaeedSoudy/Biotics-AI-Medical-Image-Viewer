from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from resources.users import blp as UserBlueprint
from resources.patients import blp as ParientsBlueprint
from resources.medical_records import blp as MedicalRecordsBlueprint
from flask_cors import CORS
from db import db
import models
from blocklist import BLOCKLIST
import secrets
import os


def create_app():
    """App Initializing"""
    app = Flask(__name__)

    CORS(app, supports_credentials=True)
    
    """App Configurations"""
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Biotics AI Backend"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    secret_key = secrets.SystemRandom().getrandbits(128)
    app.config["JWT_SECRET_KEY"] = str(secret_key)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///my_sqlite_database.db") #Creates a SQLite Database in the local directory
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    """Flask Smorets API Initializing"""
    api = Api(app)

    """Json Web Token Initializing"""
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (jsonify({
            "description": "Token has been revoked.",
            "error": "token_revoked"
        }),  401)
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (jsonify({
            "message":  "Signature Verification Failed.",
            "error": "Invalid access token."
        }), 401)
        
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify({
            "message":  "Signature Verification Failed.",
            "error": "Invalid access token."
        }), 401)
        
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({
            "description": "Request does not contain an access token.",
            "error": "authorization_required"
        }), 401)

    """Database Initializiing"""
    db.init_app(app)        
    with app.app_context():
        db.create_all()

    """Flask Smorest API Routes using Blueprint Registeration"""
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ParientsBlueprint)
    api.register_blueprint(MedicalRecordsBlueprint)

    return app





# if __name__ == '__main__':
#     # Bind to 0.0.0.0 to make it accessible outside the container
#     app.run(host='0.0.0.0', port=5000)