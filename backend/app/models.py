# from flask_sqlalchemy import SQLAlchemy
from app.extensions import db
from datetime import datetime
from enum import Enum

# db = SQLAlchemy()

# ENUM untuk peran pengguna
class UserRole(Enum):
    ADMIN = "admin"
    GURU = "guru"

# ENUM untuk status tugas
class AssignmentStatus(Enum):
    PENDING = "Pending"
    COCOK = "Cocok"
    TIDAK_COCOK = "Tidak Cocok"

# ENUM untuk status notifikasi
class NotificationStatus(Enum):
    UNREAD = "Unread"
    READ = "Read"

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Disimpan dalam bentuk hash
    role = db.Column(db.Enum(UserRole), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # students = db.relationship("Student", backref="teacher", lazy=True)
    verification_logs = db.relationship("VerificationLog", backref="verifier", lazy=True)
    notifications = db.relationship("Notification", backref="user", lazy=True)

class Student(db.Model):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)  # `class` diganti `class_name`
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    handwriting_samples = db.relationship("HandwritingSample", backref="student", lazy=True)
    assignments = db.relationship("Assignment", backref="student", lazy=True)
    verification_logs = db.relationship("VerificationLog", backref="student", lazy=True)

class HandwritingSample(db.Model):
    __tablename__ = "handwriting_samples"

    sample_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True)

class Assignment(db.Model):
    __tablename__ = "assignments"

    assignment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    submission_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.Enum(AssignmentStatus), default=AssignmentStatus.PENDING)
    verified_at = db.Column(db.DateTime, nullable=True)

    verification_logs = db.relationship("VerificationLog", backref="assignment", lazy=True)

class VerificationLog(db.Model):
    __tablename__ = "verification_logs"

    log_id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.assignment_id"), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"), nullable=False)
    similarity_score = db.Column(db.Float, nullable=False)
    verifier_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    status = db.Column(db.Enum(AssignmentStatus), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    __tablename__ = "notifications"

    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(NotificationStatus), default=NotificationStatus.UNREAD)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
