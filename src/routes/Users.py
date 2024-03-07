from flask import Blueprint, request, jsonify, Response
from flask_cors import CORS
from bson import json_util
from bson.objectid import ObjectId
from ..database.db import mongo 
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('users_blueprint', __name__)
CORS(main, supports_credentials=True)

@main.route('/', methods=['GET'])
def get_users():
    users_bson = mongo.db.users.find()
    users = json_util.dumps(users_bson)
    return Response(users, mimetype='application/json')

@main.route('/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')

@main.route('/', methods=['POST'])
def create_user():
    hashed_password = generate_password_hash(request.json['password'])
    id = mongo.db.users.insert_one({
        'name': request.json['name'],
        'lastname': request.json['lastname'],
        'username': request.json['username'],
        'email': request.json['email'],
        'password': hashed_password
    })
    response = {
        'id': str(id),
        'username': request.json['username'],
        'email': request.json['email'],
    }
    return jsonify(response, 200)

@main.route('/<id>', methods=['PUT'])
def update_user(id):
    hashed_password = generate_password_hash(request.json['password'])
    mongo.db.users.update_one({'_id': ObjectId(id)}, { '$set': {
        'name': request.json['name'],
        'lastname': request.json['lastname'],
        'username': request.json['username'],
        'password': hashed_password
    }})
    response = jsonify({'message': 'User '+id+' was updated'})
    return response

@main.route('/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User '+id+' was deleted'})
    return response

@main.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource not found' + request.url,
        'status': 404
    }
    return message