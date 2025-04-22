from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://verifikasi_user:passwordku123@localhost/verifikasi_tugas")

try:
    with engine.connect() as connection:
        print("✅ Berhasil terkoneksi ke database!")
except Exception as e:
    print("❌ Gagal konek ke DB:", e)
