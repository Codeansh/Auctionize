from flask import Blueprint, request, jsonify
import json
import jwt
from app.auth.models import User
import os
from bson import ObjectId

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/signup', methods=['POST'])
def register():
    data = json.loads(request.data)
    
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    user_obj = User.objects(email=email)
    if user_obj:
        return jsonify({'message': 'Email already registered'}), 409
    
    user_obj = User(username=username, email=email).save()
    user_obj.set_password(password)

    return jsonify({'username': user_obj.username, 'email': user_obj.email}), 201


@auth.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.data)
        email = data.get('email')
        password = data.get('password')
        user = User.objects(email=email).first()
        if not user:
            return jsonify({"message": "Email doesn't exists"}), 404

        if user.check_password(password):
            token = jwt.encode({'user_id': str(user.id)}, os.environ.get('SECRET_KEY'), algorithm='HS256')
            return jsonify({'logged in successfully': token}), 200


@auth.route('/users', methods=['GET'])
def view_users():
    if request.environ.get('is_admin'):
        user_objs = User.objects()
        return jsonify(user_objs), 200

    return jsonify({"error": "Unauthorized"}), 403

@auth.route('/users/<id>', methods=['GET'])
def get_user(id:str):
    if request.environ.get('is_admin'):
        user_obj = User.objects(id=ObjectId(id))
        return jsonify(user_obj), 200

    return jsonify({"error": "Unauthorized"}), 401


@auth.route('/users/<id>', methods=['PUT'])
def update_user(id:str):
    if request.environ.get('is_admin'):
        user_obj = User.objects(id=ObjectId(id))
        data = json.loads(request.data)
        user_obj.update(**data)
        updated_user_obj = User.objects(id=id).first()
        return jsonify(updated_user_obj), 200

    return jsonify({"error": "Unauthorized"}), 401


@auth.route('/users/create', methods=['POST'])
def create_user():
    print(request.environ.get('is_admin'))
    if request.environ.get('is_admin'):
        data = json.loads(request.data)
        user_obj = User(**data)
        user_obj.set_password(data.get('password'))
        user_obj.save()
        return jsonify(user_obj), 200

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
    
