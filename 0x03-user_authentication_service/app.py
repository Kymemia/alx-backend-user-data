#!/usr/bin/env python3

"""
this is a Flask App that registers users
after getting their email and password
"""
import uuid
from auth import Auth
from flask import Flask, jsonify, request
from flask import abort, make_response, redirect, url_for

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """
    method definition that returns a JSON payload of the form
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """
    method definition to regiser a new user.
    Endpoint expects 2 form data fields, email && password
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email=email, password=password)
        return jsonify({"email": user.email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
    login function that responds to the POST /sessions route
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401, description="Incorrect login information.")

    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    logout function that responds to the DELETE /sessions route
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for("/"))
    else:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """
    function that responds to the GET /profile route
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    function that responds to the POST /reset_password route
    """
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)

        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
