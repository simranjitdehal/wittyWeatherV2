from flask import Blueprint, request, jsonify, render_template, redirect, session, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from flask_jwt_extended.exceptions import JWTExtendedException



auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not username or not email or not password or not confirm_password:
        return jsonify({"msg":"All fields are required"}), 400

    if password != confirm_password:
        return jsonify({"msg":"Passwords do not match"}), 400

    # check if username/email already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"msg":"Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"msg":"Email already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg":"User created successfully!"}), 201



#login route
@auth_bp.route("/api/login", methods=["POST", "GET"])
def login():
    # if request.method== "GET":
    #     return render_template("login.html")
    
    if request.method=="POST":
        data = request.get_json()
        username=data.get("username")
        password = data.get("password")

        if not (username) or not password:
            return jsonify({"msg":"Username or email and password required"}), 400
        
        user = None
        if username:
            user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({"msg": "User not registered in Database"}), 400
        
        if not check_password_hash(user.password_hash, password):
            return jsonify({"msg":"Invalid password or username"}), 400
        
        #create JWT token
        token = create_access_token(identity=username) # removed this :- csrf = True
        return jsonify({"access_token": token}), 200

        # return JSON with cookie
        response = jsonify({"success": True, "username": username})
        response.set_cookie(
        'access_token_cookie',
        token,
        httponly=True,
        secure=False,  # Set True in production with HTTPS
        samesite='Lax'
        )
        return response, 200

#logout rout
@auth_bp.route("/api/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        current_user = get_jwt_identity()
        if current_user:
            return jsonify({"msg":"Logged out successfully"}), 200
        else:
            return jsonify({"msg":"No active session"}), 200
    except JWTExtendedException as e:
        app.logger.warning("Logout JWT error: {e}")
        return jsonify({"error":"Invalid token"}), 401

@auth_bp.route("/api/me", methods=["GET"])
@jwt_required()
def me():
    user = get_jwt_identity()
    if user:
        return jsonify({"username":user}), 200
    return jsonify({"msg":"Unauthorized"}), 401