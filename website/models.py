from flask_login import UserMixin
from . import db
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # ฟิลด์ทั่วไป
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150))
    role = db.Column(db.String(20), nullable=False)  # 'disabled' หรือ 'employer'
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # ฟิลด์เสริมทั่วไป
    profile_picture_url = db.Column(db.String(255))
    bio = db.Column(db.Text)

    # ฟิลด์สำหรับผู้พิการทางการได้ยิน (role = 'disabled')
    disability_type = db.Column(db.String(100))  # เช่น "ผู้พิการทางการได้ยิน"
    skills = db.Column(db.Text)  # ทักษะที่มี
    resume_text = db.Column(db.Text)  # เรซูเม่แบบข้อความ
    resume_video_url = db.Column(db.String(255))  # URL ของวิดีโอ
    location = db.Column(db.String(100))  # ที่อยู่ เช่น ตำบล อำเภอ จังหวัด
    digital_skill_level = db.Column(db.String(50))  # เช่น "พื้นฐาน", "กลาง", "สูง"
    training_completed = db.Column(db.Boolean, default=False)

    # ฟิลด์สำหรับผู้ว่าจ้าง (role = 'employer')
    company_name = db.Column(db.String(150))
    contact_person = db.Column(db.String(150))
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(150))
    address = db.Column(db.String(255))
    company_website = db.Column(db.String(255))
    company_description = db.Column(db.Text)
    verified_employer = db.Column(db.Boolean, default=False)
