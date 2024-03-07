from flask import Blueprint, request, jsonify
from flask_cors import CORS 
from src.utils.Security import Security
from src.services.Convert.Convert import Convert
from werkzeug.utils import secure_filename

main = Blueprint('convertfiletoformat_blueprint', __name__)
CORS(main, supports_credentials=True)

ALLOWED_EXTENSIONS_FILE = {'xls', 'xlsx', 'csv', 'ods'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_FILE

@main.route('/file-to-format', methods=['POST'])
def convert_file_format():
    encoded_token = Security.get_token_from_request(request.headers)
    has_access = Security.has_access(encoded_token)
    if has_access:
        if 'file' not in request.files:
            return jsonify({'message': "File is required"})        
        file = request.files['file']
        if file.filename =='':
            return jsonify({'message': "No selected file"})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            jsonData = Convert.convert_file_to_format(file)
        return jsonify({"fileName": filename, "extension": filename.rsplit('.', 1)[1].lower(), "items":jsonData})
    else:
        response = jsonify({'message': "Unauthorized"})
        return response, 401
 
@main.route('/format-to-file', methods=['POST'])
def convert_format_file():
    response = jsonify({'message': "Service not available"})
    return response, 200