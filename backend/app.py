from flask import Flask, request, jsonify, render_template, redirect, session, url_for
import requests
from flask_cors import CORS
from config import OPENWEATHER_API_KEY, DEEPSEEK_API_KEY, SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from jokes import temp_jokes, wind_jokes, humidity_jokes, cloud_jokes
import random
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError, JWTExtendedException
from dotenv import load_dotenv
import os
from routes.auth import auth_bp
from routes.weather import weather_bp
from datetime import timedelta
from database import db, migrate
from authlib.integrations.flask_client import OAuth
from oauth_util import configure_oauth, google_bp
from extensions import redis_client
from flask_migrate import Migrate

app = Flask(__name__)
# app = Flask(__name__, template_folder="../frontend", static_folder="../frontend/js")

CORS(app, resources={r"/*": {"origins": "http://localhost:8000"}}, supports_credentials=True)
# CORS(app, supports_credentials=True)

# load_dotenv()

# Database config from .envz``
# db_user = os.getenv("DB_USER")
# db_password = os.getenv("DB_PASSWORD")
# db_host = os.getenv("DB_HOST")
# db_name = os.getenv("DB_NAME")

#SQL things
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
# migrate = Migrate()

#jwt things
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)

# Session configuration for OAuth
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
jwt = JWTManager(app)

# Register OAuth + Blueprints

configure_oauth(app) 
app.register_blueprint(auth_bp)
app.register_blueprint(google_bp)
app.register_blueprint(weather_bp)



# with app.app_context():
#     db.create_all()
#     print("✅ Users table created!")

# Flask routes
@app.route("/api/health")
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route("/api/check-auth")
def check_auth():
    try:
        verify_jwt_in_request(optional=True)
        current_user = get_jwt_identity()
        if current_user:
            return jsonify({"authenticated": True, "username": current_user}), 200
        else:
            return jsonify({"authenticated": False}), 401
    except JWTExtendedException:
        return jsonify({"authenticated": False}), 401

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/debug/routes")
def debug_routes():
    return {
        "routes": [str(rule) for rule in app.url_map.iter_rules()]
    }



if __name__ == "__main__":
    app.run(debug=True)

#add reddis
#dockerize this app, what is kernal? VM ware