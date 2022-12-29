from flask import Blueprint, request, jsonify
import json
import jwt
from app.auth.models import User
import os
from bson import ObjectId
from flask_pydantic import validate
from app.auth.schema import  LoginData, UserModel


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/signup', methods=['POST'])
@validate()
def register(body: UserModel):
    user_obj = User.objects(email=body.email)
    if user_obj:
        return jsonify({'message': 'Email already registered'}), 409
    
    user_obj = User(username=body.username, email=body.email).save()
    user_obj.set_password(body.password)

    return jsonify({'username': user_obj.username, 'email': user_obj.email}), 201


@auth.route('/login', methods=['POST'])
@validate()
def login(body: LoginData):
    user = User.objects(email=body.email).first()
    if not user:
        return jsonify({"message": "Email doesn't exists"}), 404

    if user.check_password(body.password):
        token = jwt.encode({'user_id': str(user.id)},
                           os.environ.get('SECRET_KEY','this is a secret key'),
                           algorithm='HS256')
        return jsonify({'logged in successfully': token}), 200


@auth.route('/users', methods=['GET'])
def view_users():
    if request.environ.get('is_admin'):
        user_objs = User.objects()
        if not user_objs:
            return jsonify({"message": "No users found"}), 404

        return jsonify(user_objs), 200

    return jsonify({"error": "Unauthorized"}), 403

@auth.route('/users/<id>', methods=['GET'])
def get_user(id:str):
    if request.environ.get('is_admin'):
        user_obj = User.objects(id=ObjectId(id))
        if not user_obj:
            return jsonify({"message": "User doesn't  exists"}), 404

        return jsonify(user_obj), 200

    return jsonify({"error": "Unauthorized"}), 401


@auth.route('/users/<id>', methods=['PUT'])
@validate()
def update_user(id:str, body: UserModel):
    if request.environ.get('is_admin'):
        user_obj = User.objects(id=ObjectId(id)).first()
        if not user_obj :
            return jsonify({"message": "User doesn't  exists"}),404
        user_obj.update(username=body.username,email=body.email)
        user_obj.set_password(body.password)
        updated_user_obj = User.objects(id=id).first()
        return jsonify(updated_user_obj), 200

    return jsonify({"error": "Unauthorized"}), 401


@auth.route('/users/create', methods=['POST'])
@validate()
def create_user(body: UserModel):
    if request.environ.get('is_admin'):
        user_obj = User.objects(email=body.email)
        if user_obj:
            return jsonify({"message":"Email already registered"}),409
        user_obj = User(username=body.username,email=body.email)
        user_obj.set_password(body.password)
        user_obj.save()
        return jsonify(user_obj), 201

    return jsonify({"error": "Unauthorized"}), 401


@auth.route('/users/<id>', methods=['DELETE'])
def delete_user(id:str):
    if request.environ.get('is_admin'):
        user_obj = User.objects(id=ObjectId(id))
        if not user_obj :
            return jsonify({"message": "User doesn't  exists"}),404
        user_obj.delete()
        return jsonify({"message": "Successfully Deleted"}), 200

    return jsonify({"error": "Unauthorized"}), 401

@auth.route('/validate', methods=['POST'])
def validate():
    user_id = request.environ.get('user_id')
    return jsonify({'user_id': user_id}), 200
    
