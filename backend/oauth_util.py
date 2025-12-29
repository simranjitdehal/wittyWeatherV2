from flask import Flask, Blueprint, redirect, url_for, jsonify, request
from authlib.integrations.flask_client import OAuth
from datetime import datetime, timedelta
import jwt
import os

oauth = OAuth()


def configure_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

google_bp = Blueprint('google_auth', __name__)

@google_bp.route('/api/login/google')
def login_google():
    redirect_uri = url_for('google_auth.callback_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@google_bp.route('/api/callback/google')
def callback_google():
    token = oauth.google.authorize_access_token()
    resp = oauth.google.get('https://www.googleapis.com/oauth2/v1/userinfo')

    user_info = resp.json()
    print(user_info)

    # Extract key info
    email = user_info.get('email')
    name = user_info.get('name')

    # Create JWT
    jwt_payload = {
        'sub': email,
        'name': name,
        'exp': datetime.utcnow() + timedelta(hours=12)
    }

    jwt_token = jwt.encode(jwt_payload, os.getenv("JWT_SECRET_KEY"), algorithm='HS256')

    # Return to frontend with JWT
    # we can either:
    #   redirect with token in URL (less secure), or
    #   return JSON (recommended for APIs)
    # return jsonify({
    #     'access_token': jwt_token,
    #     'user': user_info
    # })
    # frontend_url = f"http://127.0.0.1:5000/login.html?token={jwt_token}&name={name}"
    frontend_url = f"https://spectacular-luck-production.up.railway.app/index.html?token={jwt_token}"
    return redirect(frontend_url)
    