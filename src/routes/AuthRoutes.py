from flask import Blueprint, request, jsonify
from flask_cors import CORS 
from src.models.User import User
from src.utils.Security import Security
from src.services.Authentication.AuthService import AuthService

main = Blueprint('auth_blueprint', __name__)
CORS(main, supports_credentials=True)

@main.route('/token', methods=['POST'])
def generate_token():
    try: 
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        _user = User(0, username, password, email)
        authenticated_user = AuthService.login(_user)
        if(authenticated_user != None):
            encoded_token = Security.generate_token(authenticated_user)
            return jsonify({'success': True, 'message': 'Authorized', 'token': encoded_token})
        else:
            response = jsonify({'success': False, 'message': 'Unauthorized', 'token': ''})
            return response, 401
    except Exception as ex:
        return jsonify({'success': False, 'message': ex.__cause__, 'token': ''})

@main.route('/verify-token', methods=['POST'])
def verify_token():
    withAccess = Security.verify_token(request.headers)
    if withAccess == True:
        payload = Security.get_payload_token(request.headers)
        return jsonify({'success': True, 'message': "Authorized access", 'token': '' }), 200 #"payload": payload
    else:
        return jsonify({'message': 'Unauthorized'}), 401