import os
from werkzeug.utils import secure_filename
from app.services.processing.pdf_processor import process_pdf
from app.services.processing.image_processor import process_image
from app.config import UPLOAD_DIR

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'jpg', 'jpeg', 'png'}

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def allowed_file(filename):
    """Check if uploaded file is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_file_upload(file):
    """Handles file uploads and delegates processing"""

    if not file or file.filename == '':
        return {"error": "No file selected"}, 400

    if not allowed_file(file.filename):
        return {"error": "Invalid file type. Only PDFs are allowed."}, 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_DIR, filename)
    file.save(filepath)

    # Process the file based on type
    if filename.endswith('.pdf'):
        return process_pdf(filepath)
    elif filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        return process_image(filepath)
    else:
        return {"error": "Unsupported file type. Only PDFs and images are allowed."}, 400
