# import os
from flask import Blueprint, Response
from flask import request, jsonify
# from werkzeug.utils import secure_filename
# from app.config import UPLOAD_DIR
# from app.utils.file_upload_helpers import allowed_file
from app.services.processing import handle_file_upload

file_upload_bp = Blueprint('file_upload', __name__)

@file_upload_bp.route("/", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"msg": "No file part"}), 400
    
    file = request.files["file"]

    # if file.filename == "":
    #     return jsonify({"msg": "No selected file"}), 400

    # if not allowed_file(file.filename):
    #     return jsonify({"msg": "Invalid file type"}), 400

    # filename = secure_filename(file.filename)
    # file_path = os.path.join(UPLOAD_DIR, filename)
    # file.save(file_path)

    result = handle_file_upload(file)
    response = Response(result, mimetype='application/json')

    # return jsonify({"msg": "File uploaded successfully", "file_path": file_path}), 200
    return response, 200