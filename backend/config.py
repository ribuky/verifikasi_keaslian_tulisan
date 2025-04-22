import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    # SQLALCHEMY_DATABASE_URI = os.getenv(
    #     "DATABASE_URL", "mysql+pymysql://root:@localhost/verifikasi_tugas"
    # )
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://verifikasi_user:passwordku123@localhost/verifikasi_tugas"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecret")

    # Folder untuk menyimpan gambar tugas
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "static/uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    
