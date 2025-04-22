from flask import Blueprint, request, jsonify
from flask import send_from_directory, current_app, url_for
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt, jwt_required, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app.models import User, db
from app.models import Student, Notification, Assignment, HandwritingSample, VerificationLog, AssignmentStatus
from app.extensions import db, model, blocked_tokens
from app.utils import save_file
from datetime import datetime
from flasgger import swag_from
import os
import json
import tensorflow as tf
import cv2
import numpy as np

api_bp = Blueprint("api", __name__)

# <==========================================Awal Auth============================================>
@api_bp.route("/register", methods=["POST"])
@jwt_required()
@swag_from({
    "summary": "Register User",
    "description": "Mendaftarkan user baru sebagai admin atau guru (hanya oleh admin).",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "password": {"type": "string"},
                    "role": {"type": "string", "enum": ["admin", "guru"]}
                },
                "required": ["username", "password", "role"]
            }
        }
    ],
    "responses": {
        201: {"description": "User berhasil didaftarkan"},
        400: {"description": "Data tidak valid atau username sudah digunakan"},
        403: {"description": "Hanya admin yang dapat mendaftarkan user"}
    }
})
def register():
    """✅ Endpoint: Register user baru, hanya untuk ADMIN"""

    # Ambil user dari JWT payload
    current_user = int(get_jwt_identity())

    # Validasi role (pastikan format current_user dict)
    if isinstance(current_user, dict):
        user_role = current_user.get("role")
    else:
        return jsonify({"message": "❌ Payload JWT tidak valid!"}), 400

    if user_role != "admin":
        return jsonify({"message": "❌ Hanya admin yang dapat mendaftarkan user baru!"}), 403

    data = request.get_json()
    username = data.get("username", "").strip().lower()
    password = data.get("password", "")
    role = data.get("role")

    # Validasi input
    if not username or not password or role not in ["admin", "guru"]:
        return jsonify({"message": "❌ Data tidak valid!"}), 400

    if len(password) < 6:
        return jsonify({"message": "❌ Password minimal 6 karakter!"}), 400

    # Cek username sudah ada
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "❌ Username sudah digunakan!"}), 400

    # Simpan user
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, role=role)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "✅ User berhasil didaftarkan!",
        "username": username,
        "role": role
    }), 201

@api_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    """API hanya untuk Admin: Menampilkan semua user"""
    identity = get_jwt_identity()  # Tetap string

    user = User.query.get(int(identity))  # Cast ke int saat ambil dari DB
    if not user:
        return jsonify({"message": "❌ Pengguna tidak ditemukan!"}), 404

    if user.role.value != "admin":
        return jsonify({"message": "❌ Hanya admin yang dapat mengakses data pengguna!"}), 403

    users = User.query.all()
    user_list = [{
        "user_id": u.user_id,
        "username": u.username,
        "role": u.role.value,
        "created_at": u.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for u in users]

    return jsonify({"users": user_list}), 200

@api_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    """API untuk menghapus user (hanya admin)"""
    current_user = int(get_jwt_identity())
    if current_user["role"] != "admin":
        return jsonify({"message": "❌ Hanya admin yang dapat menghapus user!"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "❌ User tidak ditemukan!"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "✅ User berhasil dihapus!"}), 200

@api_bp.route("/login", methods=["POST"])
@swag_from({
    "summary": "Login User",
    "description": "User login untuk mendapatkan token JWT.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "password": {"type": "string"}
                },
                "required": ["username", "password"]
            }
        }
    ],
    "responses": {
        200: {"description": "Login berhasil, token JWT diberikan"},
        401: {"description": "Username atau password salah"}
    }
})
def login():
    """API untuk login dan mendapatkan token JWT"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Username atau password salah"}), 401

    additional_claims = {
        "role": user.role.value
    }

    access_token = create_access_token(identity=str(user.user_id), additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=str(user.user_id), additional_claims=additional_claims)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "role": user.role.value
    }), 200

@api_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    """Contoh rute yang hanya bisa diakses dengan JWT"""
    current_user = int(get_jwt_identity())
    return jsonify({"message": "Ini rute yang dilindungi!", "user": current_user}), 200

@api_bp.route("/reset_user", methods=["PUT"])
@jwt_required()
def reset_user():
    """API untuk mengganti username dan password user (Hanya bisa oleh admin)"""
    current_user = int(get_jwt_identity())
    if current_user["role"] != "admin":
        return jsonify({"message": "❌ Hanya admin yang dapat mengubah akun pengguna!"}), 403

    data = request.get_json()
    old_username = data.get("old_username")
    new_username = data.get("new_username")
    new_password = data.get("new_password")

    if not old_username or not new_username or not new_password:
        return jsonify({"message": "❌ Data tidak lengkap!"}), 400

    user = User.query.filter_by(username=old_username).first()
    if not user:
        return jsonify({"message": "❌ User tidak ditemukan!"}), 404

    # Jika username diubah dan sudah dipakai user lain
    if new_username != old_username and User.query.filter_by(username=new_username).first():
        return jsonify({"message": "❌ Username baru sudah digunakan!"}), 400

    # Update username dan password
    user.username = new_username
    user.password = generate_password_hash(new_password)

    db.session.commit()
    return jsonify({"message": f"✅ User '{old_username}' berhasil diperbarui!"}), 200

@api_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """API untuk logout (Menghaspu token dari sesi aktif)"""
    jti = get_jwt()["jti"] # Ambil JWT Token ID
    blocked_tokens.add(jti) # Tambahkan ke daftar blokir
    return jsonify({"message": "✅ Logout Berhasil!"}), 200

@api_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """API untuk mendapatkan Access Token baru menggunakan Refresh Token"""
    current_user = get_jwt_identity()  # Ambil user dari token lama
    new_access_token = create_access_token(identity=current_user)  # Buat token baru
    return jsonify({"access_token": new_access_token}), 200
# <==========================================Akhir Auth============================================>
# <==========================================Awal Students===========================================>
@api_bp.route("/students", methods=["POST"])
@jwt_required()
def add_student():
    """API untuk menambahkan siswa baru"""
    data = request.get_json()
    name = data.get("name")
    class_name = data.get("class_name")

    if not name or not class_name:
        return jsonify({"message": "Nama dan kelas harus diisi"}), 400

    new_student = Student(name=name, class_name=class_name)
    db.session.add(new_student)
    db.session.commit()

    return jsonify({"message": "Siswa berhasil ditambahkan!"}), 201

# <==================================Bagian Ambil Data============================================>
@api_bp.route("/students", methods=["GET"])
@jwt_required()
@swag_from({
    "responses": {
        200: {
            "description": "Daftar siswa berhasil diambil",
            "examples": {
                "application/json": {
                    "students": [
                        {"student_id": 1, "name": "Budi Santoso", "class_name": "10A"}
                    ]
                }
            }
        }
    }
})
def get_student():
    """API untuk mendapatkan daftar siswa"""
    identity = get_jwt_identity()
    print(f"[DEBUG] JWT Identity: {identity}")
    student = Student.query.all()
    student_list = [{"student_id": s.student_id, "name": s.name, "class_name": s.class_name} for s in student]

    return jsonify({"students": student_list}), 200

# <~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Bagian Edit~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
@api_bp.route("/students/<int:student_id>", methods=["PUT"])
@jwt_required()
def update_student(student_id):
    """API untuk mengedit data siswa"""
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "Siswa tidak ditemukan"}), 404

    data = request.get_json()
    name = data.get("name", student.name)  # Jika tidak ada, gunakan data lama
    class_name = data.get("class_name", student.class_name)

    student.name = name
    student.class_name = class_name

    db.session.commit()

    return jsonify({"message": "Siswa berhasil diperbarui!", "student": {
        "student_id": student.student_id,
        "name": student.name,
        "class_name": student.class_name
    }}), 200

# <~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Bagian Delete~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
@api_bp.route("/students/<int:student_id>", methods=["DELETE"])
@jwt_required()
def delete_student(student_id):
    """API untuk menghapus siswa dan semua handwriting sample yang terkait"""
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "Siswa tidak ditemukan"}), 404

    # Hapus semua handwriting sample milik siswa
    HandwritingSample.query.filter_by(student_id=student_id).delete()

    # Hapus siswa dari database
    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Siswa dan semua handwriting sample berhasil dihapus!"}), 200
# <==========================================Akhir Student============================================>
# <========================================Awal Upload Sample==========================================>
UPLOAD_FOLDER_SAMPLE = "static/uploads/handwriting_samples"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

if not os.path.exists(UPLOAD_FOLDER_SAMPLE):
    os.makedirs(UPLOAD_FOLDER_SAMPLE)

@api_bp.route("/upload_sample", methods=["POST"])
@jwt_required()
def upload_sample():
    """API untuk mengunggah sample tulisan tangan siswa"""
    if "file" not in request.files or "student_id" not in request.form:
        return jsonify({"message": "File dan siswa diperlukan!"}), 400
    
    file = request.files["file"]
    student_id = request.form["student_id"]
    description = request.form.get("description", "")

    # Periksa ekstensi file
    if "." in file.filename and file.filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSIONS:
        return jsonify({"message": "Format file tidak diizinkan"}), 400
    
    # Generate nama file baru
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    extension = file.filename.rsplit(".", 1)[1].lower()
    new_filename = f"sample({student_id})_{timestamp}.{extension}"
    
    # Simpan gambar ke folder static/uploads/handwriting_samples
    filename = secure_filename(new_filename)
    filepath = os.path.join(UPLOAD_FOLDER_SAMPLE, filename).replace(os.path.sep, "/")
    file.save(filepath)

    # Simpan ke database
    new_sample = HandwritingSample(
        student_id=student_id,
        image_path=filepath,
        description=description
    )
    db.session.add(new_sample)
    db.session.commit()

    return jsonify({"message": "Sample tulisan berhasil diunggah!", "filename": filename}), 201

@api_bp.route("/handwriting_samples", methods=["GET"])
@jwt_required()
def get_handwriting_samples():
    """API untuk mendapatkan daftar handwriting sample"""
    samples = HandwritingSample.query.all()
    sample_list = [{
        "sample_id": s.sample_id,
        "student_id": s.student_id,
        "image_path": s.image_path,
        "description": s.description
    } for s in samples]

    return jsonify({"samples": sample_list}), 200

# <~~~~~~~~~~~~~~~~~~~~~~~~~~Bagian Edit~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
@api_bp.route("/handwriting_samples/<int:sample_id>", methods=["PUT"])
@jwt_required()
def update_handwriting_sample(sample_id):
    """API untuk mengedit sample tulisan tangan siswa"""
    sample = HandwritingSample.query.get(sample_id)
    if not sample:
        return jsonify({"message": "Sample tidak ditemukan"}), 404

    data = request.form
    description = data.get("description", sample.description)

    # Cek apakah ada file baru yang diunggah
    if "file" in request.files:
        file = request.files["file"]
        if file.filename:  # Pastikan nama file tidak kosong
            if "." in file.filename and file.filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSIONS:
                return jsonify({"message": "Format file tidak diizinkan"}), 400

            # Hapus file lama
            if os.path.exists(sample.image_path):
                os.remove(sample.image_path)

            # Generate nama file baru
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d%H%M%S")
            extension = file.filename.rsplit(".", 1)[1].lower()
            new_filename = f"sample({sample.student_id})_{timestamp}.{extension}"

            filename = secure_filename(new_filename)
            filepath = os.path.join(UPLOAD_FOLDER_SAMPLE, filename)
            file.save(filepath)

            sample.image_path = filepath  # Update path gambar baru

    # Update deskripsi jika diubah
    sample.description = description
    db.session.commit()

    return jsonify({
        "message": "Sample berhasil diperbarui!",
        "sample": {
            "sample_id": sample.sample_id,
            "image_path": sample.image_path,
            "description": sample.description
        }
    }), 200

# <~~~~~~~~~~~~~~~~~~~~~~~~~~Bagian Delete~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
@api_bp.route("/handwriting_samples/<int:sample_id>", methods=["DELETE"])
@jwt_required()
def delete_handwriting_sample(sample_id):
    """API untuk menghapus sample tulisan tangan siswa"""
    sample = HandwritingSample.query.get(sample_id)
    if not sample:
        return jsonify({"message": "Sample tidak ditemukan"}), 404

    # Hapus file dari storage
    if os.path.exists(sample.image_path):
        os.remove(sample.image_path)

    # Hapus dari database
    db.session.delete(sample)
    db.session.commit()

    return jsonify({"message": "Sample berhasil dihapus!"}), 200
# <==========================================Akhir Upload Sample============================================>
# <==========================================Awal Upload Tugas============================================>
UPLOAD_FOLDER_ASSIGNMENT = "static/uploads/assignments"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Pastikan folder upload ada
if not os.path.exists(UPLOAD_FOLDER_ASSIGNMENT):
    os.makedirs(UPLOAD_FOLDER_ASSIGNMENT)

@api_bp.route("/upload_assignment", methods=["POST"])
@jwt_required()
def upload_assignment():
    """API untuk mengunggah tugas siswa"""
    if "file" not in request.files or "student_id" not in request.form:
        return jsonify({"message": "File dan Student ID diperlukan!"}), 400

    file = request.files["file"]
    student_id = request.form["student_id"]

    # Periksa ekstensi file
    if "." in file.filename and file.filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSIONS:
        return jsonify({"message": "Format file tidak diizinkan"}), 400

    # Generate nama file baru
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    extension = file.filename.rsplit(".", 1)[1].lower()
    new_filename = f"assignment({student_id})_{timestamp}.{extension}"
    
    filename = secure_filename(new_filename)
    filepath = os.path.join(UPLOAD_FOLDER_ASSIGNMENT, filename).replace(os.path.sep, "/")
    file.save(filepath)

    # Simpan ke database
    new_assignment = Assignment(
        student_id=student_id,
        image_path=filepath,
        # image_path = f"uploads/assignments/{filename}",
        status="Pending"
    )
    db.session.add(new_assignment)
    db.session.commit()

    return jsonify({"message": "Tugas berhasil diunggah!", "filename": filename}), 201

@api_bp.route("/assignments", methods=["GET"])
@jwt_required()
def get_assignments():
    """API untuk mendapatkan daftar tugas siswa"""
    status = request.args.get("status")  # Filter berdasarkan status
    student_id = request.args.get("student_id")  # Filter berdasarkan siswa

    query = Assignment.query

    if status:
        query = query.filter_by(status=status)
    if student_id:
        query = query.filter_by(student_id=student_id)

    assignments = query.all()

    assignment_list = []
    for a in assignments:
        assignment_list.append({
            "assignment_id": a.assignment_id,
            "student_id": a.student_id,
            "student_name": a.student.name,
            # "image_path": f"/api/uploads/assignments/{os.path.basename(a.image_path)}",
            "image_path": f"/static/uploads/assignments/{os.path.basename(a.image_path)}",
            "submission_date": a.submission_date.strftime("%Y-%m-%d") if a.submission_date else None,
            "status": a.status.value if a.status else "Pending",  # Pastikan status selalu ada
            "verified_at": a.verified_at.strftime("%Y-%m-%d %H:%M:%S") if a.verified_at else None
        })

    return jsonify({"assignments": assignment_list}), 200

@api_bp.route("/assignments/<int:assignment_id>", methods=["PUT"])
@jwt_required()
def update_assignment_status(assignment_id):
    """API untuk memperbarui status tugas setelah verifikasi"""
    data = request.get_json()
    status = data.get("status")

    # Pastikan staus valid
    if status not in ["Cocok", "Tidak_Cocok"]:
        return jsonify({"message": "Status tidak valid"}), 400
    # if status not in [s.value for s in AssignmentStatus]:
    #     return jsonify({"message": "Status tidak valid"}), 400
    
    # Cari tugas berdasarkan ID
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({"message": "Tugas tidak ditemukan"})
    
    # Update status dan waktu verifikasi
    assignment.status = status
    assignment.verified_at = datetime.utcnow()

    db.session.commit()

    return jsonify({"message": "Status tugas berhasil diperbarui!", "status": status}), 200

@api_bp.route("/assignments/<int:assignment_id>", methods=["DELETE"])
@jwt_required()
def delete_assignment(assignment_id):
    """API untuk menghapus tugas siswa"""
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({"message": "Tugas tidak ditemukan"}), 404

    # Hapus file gambar dari penyimpanan (opsional tapi disarankan)
    if os.path.exists(assignment.image_path):
        os.remove(assignment.image_path)

    # Hapus dari database
    db.session.delete(assignment)
    db.session.commit()

    return jsonify({"message": "Tugas berhasil dihapus!"}), 200

@api_bp.route("/notifications", methods=["GET"])
@jwt_required()
def get_notifications():
    """API untuk mendapatkan notifikasi pengguna"""
    user = get_jwt_identity()  # Ambil user_id dari JWT token
    notifications = Notification.query.filter_by(user_id=user["user_id"]).all()

    notif_list = [{"id": n.notification_id, "message": n.message, "status": n.status.value} for n in notifications]
    
    return jsonify({"notifications": notif_list}), 200

@api_bp.route("/notifications/<int:notification_id>", methods=["PUT"])
@jwt_required()
def mark_notification_as_read(notification_id):
    """API untuk menandai notifikasi sebagai dibaca"""
    notification = Notification.query.get(notification_id)
    
    if not notification:
        return jsonify({"message": "Notifikasi tidak ditemukan"}), 404

    notification.status = "Read"
    db.session.commit()

    return jsonify({"message": "Notifikasi ditandai sebagai dibaca!"}), 200

UPLOAD_FOLDER_VERIFY = "static/uploads/verify"
IMG_SIZE = 128

if not os.path.exists(UPLOAD_FOLDER_VERIFY):
    os.makedirs(UPLOAD_FOLDER_VERIFY)

def preprocess_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Gambar tidak ditemukan: {image_path}")

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"File gambar tidak valid atau rusak: {image_path}")

    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img.astype("float32") / 255.0
    return np.expand_dims(img, axis=[0, -1])

@api_bp.route("/verify", methods=["POST"])
@jwt_required()
def verify_assignment():
    # Lazy-load Siamese model hanya saat dibutuhkan
    from app.extensions import model, load_simese_model
    global model
    if model is None:
        print("🔄 Loading Siamese model...")
        load_simese_model()
        print("✅ Model loaded for verification.")

    if "file" not in request.files or "student_id" not in request.form:
        return jsonify({"message": "File dan student_id diperlukan!"}), 400

    file = request.files["file"]
    student_id = request.form["student_id"]
    verifier_id = int(get_jwt_identity())

    # Simpan file upload
    filename = f"verify_{student_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER_VERIFY, filename)
    file.save(filepath)

    # Ambil semua sampel tulisan siswa
    samples = HandwritingSample.query.filter_by(student_id=student_id).all()
    if not samples:
        return jsonify({"message": "❌ Tidak ada sampel tulisan untuk siswa ini!"}), 400

    # Preprocess gambar tugas yang di-upload
    uploaded_img = preprocess_image(filepath)
    similarity_scores = []

    for sample in samples:
        sample_img = preprocess_image(sample.image_path)
        prediction = model.predict([uploaded_img, sample_img])[0][0]
        similarity_scores.append(prediction)

    # Hitung rata-rata similarity
    avg_similarity = np.mean(similarity_scores)
    status_str = "Cocok" if avg_similarity >= 0.75 else "Tidak Cocok"
    status_enum = AssignmentStatus.COCOK if status_str == "Cocok" else AssignmentStatus.TIDAK_COCOK

    # Simpan log verifikasi ke DB
    assignment_id = request.form.get("assignment_id")
    assignment_id = int(assignment_id) if assignment_id else None

    new_log = VerificationLog(
        assignment_id=assignment_id,
        student_id=student_id,
        similarity_score=avg_similarity,
        verifier_id=verifier_id,
        status=status_enum,
        created_at=datetime.utcnow(),
    )
    db.session.add(new_log)
    db.session.commit()

    return jsonify({
        "message": "✅ Verifikasi selesai!",
        "similarity_score": float(round(avg_similarity, 4)),
        "status": status_str
    }), 200

@api_bp.route("/verification_logs", methods=["GET"])
@jwt_required()
def get_user_verification_logs():
    verifier_id = int(get_jwt_identity())

    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    query = VerificationLog.query.filter_by(verifier_id=verifier_id)

    try:
        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            query = query.filter(VerificationLog.created_at >= start_date)
        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            end_date = end_date.replace(hour=23, minute=59, second=59)
            query = query.filter(VerificationLog.created_at <= end_date)
    except ValueError:
        return jsonify({"message": "❌ Format tanggal tidak valid! Gunakan YYYY-MM-DD"}), 400

    logs = query.order_by(VerificationLog.created_at.desc()).all()
    if not logs:
        return jsonify({"message": "Tidak ada log ditemukan untuk user ini."}), 404

    result = []
    for log in logs:
        student = Student.query.get(log.student_id)
        result.append({
            "log_id": log.log_id,
            "assignment_id": log.assignment_id,
            "student_id": student.name if student else "Tidak Diketahui",
            "similarity_score": round(log.similarity_score, 4),
            "status": log.status.value,
            "created_at": log.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify({"logs": result}), 200

@api_bp.route("/assignments/<int:assignment_id>/verification_log", methods=["GET"])
@jwt_required()
def get_latest_verification_log(assignment_id):
    log = VerificationLog.query.filter_by(assignment_id=assignment_id)\
        .order_by(VerificationLog.created_at.desc()).first()

    if not log:
        return jsonify({"message": "Log verifikasi tidak ditemukan untuk Tugas ini"}), 404

    return jsonify({
        "assignment_id": log.assignment_id,
        "student_id": log.student_id,
        "similarity_score": round(log.similarity_score, 4),
        "status": log.status.value,
        "created_at": log.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }), 200

