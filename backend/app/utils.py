import os
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """Cek apakah file memiliki ekstensi yang diizinkan"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

def save_file(file):
    """Menyimpan file ke folder upload"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_app.config["UPLOAD_FOLDER"]

        # Pastikan folder `uploads` sudah ada
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return filename
    return None
