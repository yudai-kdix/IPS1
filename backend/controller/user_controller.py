from flask import Flask,  request, jsonify
from flask_cors import CORS, cross_origin
import jwt
from werkzeug.security import generate_password_hash

from backend.models.user import User
from backend import app

CORS(app)
    
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    # 仮のユーザーデータ（実際にはデータベースから取得）
    user = User.find_by_name(data['username'])
    # ユーザー名とパスワードのチェック（ここではダミーチェック）
    if user:
        if user.check_password(data['password']):
            token = jwt.encode({'user_id': user.id}, app.config['SECRET_KEY'], algorithm=app.config['ALGORITHM'])
            return jsonify({'token': token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/signup', methods=['POST', 'OPTIONS'])
def signup():
    data = request.json
    print(data)
    if not User.find_by_name(data['username']):
        new_user = User(name=data['username'], password=generate_password_hash(data['password']))
        new_user.save()
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'message': 'Username already exists'}), 409


@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.find_by_id(user_id)
    if user:
        user_data = {'id': user.id, 'username': user.name}
        return jsonify(user_data)
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = User.find_by_id(user_id)
    if user:
        user.name = data.get('username', user.name)
        if 'password' in data:
            user.password = generate_password_hash(data['password'])
        user.save()
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.find_by_id(user_id)
    if user:
        user.delete()
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404
    

def decode_token(token):
    try:
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=[app.config['ALGORITHM']])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    

def get_user_id_from_token():
    token = request.headers.get('Authorization')
    if token:
        decoded = decode_token(token)
        if decoded:
            return decoded['user_id']
    return None