#!/usr/bin/env python3
"""app.py - Basic Flask app"""
from flask import Flask, jsonify, request, abort, make_response
from flask import url_for, redirect
from auth import Auth


app = Flask(__name__)
auth = Auth()


@app.route('/', strict_slashes=False)
def index():
    """simple endpoint"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """register a user"""
    payload = None
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        auth.register_user(email, password)
        payload = {"email": email, "message": "user created"}
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify(payload)


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """log user in"""
    email = request.form.get('email')
    if not email:
        abort(401)
    password = request.form.get('password')
    if not password:
        abort(401)
    if auth.valid_login(email, password):
        session_id = auth.create_session(email)
        resp = make_response({"email": email, "message": "logged in"})
        resp.set_cookie('session_id', session_id)
        return resp
    abort(401)


@app.route('/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """logs user out"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = auth.get_user_from_session_id(session_id)
        if not user:
            abort(403)
        auth.destroy_session(user.id)
        return redirect(url_for('index')), 307
    abort(401)


@app.route('/profile', strict_slashes=False)
def profile():
    """User profile"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = auth.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email})
        abort(403)
    abort(401)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """get reset password token"""
    email = request.form.get('email')
    try:
        reset_token = auth.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
