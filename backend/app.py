from flask import Flask, request, jsonify, render_template, redirect, session, url_for
import requests
from flask_cors import CORS
from config import OPENWEATHER_API_KEY, DEEPSEEK_API_KEY, SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from jokes import temp_jokes, wind_jokes, humidity_jokes, cloud_jokes
import random
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from dotenv import load_dotenv
import os
from routes.auth import auth_bp
from routes.weather import weather_bp
from datetime import timedelta
from database import db
from authlib.integrations.flask_client import OAuth
from oauth_util import configure_oauth, google_bp


app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:8000"}}, supports_credentials=True)
CORS(app, supports_credentials=True)

# load_dotenv()

# Database config from .env
# db_user = os.getenv("DB_USER")
# db_password = os.getenv("DB_PASSWORD")
# db_host = os.getenv("DB_HOST")
# db_name = os.getenv("DB_NAME")

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["SECRET_KEY"] = JWT_SECRET_KEY

# Session configuration for OAuth
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
print(f"🔑 SECRET_KEY loaded: {app.config['SECRET_KEY'][:10]}...")  # Print first 10 chars

db.init_app(app)
jwt = JWTManager(app)

# Register OAuth + Blueprints

configure_oauth(app) 
app.register_blueprint(google_bp)
app.register_blueprint(weather_bp)



with app.app_context():
    db.create_all()
    print("✅ Users table created!")

# ------------------------
# Flask routes
# ------------------------
@app.route("/")
# @jwt_required()
def home():
    try:
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        return render_template("index.html", username=current_user)
    except NoAuthorizationError:
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

#add reddis
#dockerize this app, what is kernal? VM ware