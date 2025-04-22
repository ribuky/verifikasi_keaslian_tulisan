from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from app.extensions import db, load_simese_model, blocked_tokens
from config import Config

# Inisialisasi ekstensi Flask
migrate = Migrate()
jwt = JWTManager()

def create_app():
    """Factory function untuk membuat instance Flask app"""
    app = Flask(
        __name__,
        static_folder="static",
        static_url_path="/static"
    )
    app.config.from_object(Config)

    # Inisialisasi ekstensi dengan app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)  # Mengizinkan akses dari frontend

    # Cek apakah token diblokir (sudah Logout)
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_data):
        return jwt_data["jti"] in blocked_tokens  # Cek apakah token ada dalam daftar blokir
    
    # Konfigurasi Swagger
    template = {
        "swagger": "2.0",
        "info": {
            "title": "API Verifikasi Tugas",
            "description": "Dokumentasi API untuk verifikasi tugas siswa dengan CNN & Siamese Network",
            "version": "1.0.0"
        },
        "basePath": "/api"  # Pastikan basePath sesuai dengan prefix Blueprint
    }
    
    Swagger(app, template=template)

    # Import model agar dikenali oleh Flask-Migrate
    from app import models

    # Muat model Siamese
    # load_simese_model()

    # Import dan registrasi blueprint (rute API)
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
