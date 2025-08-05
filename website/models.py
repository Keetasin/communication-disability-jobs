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


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100))
    salary = db.Column(db.String(100))
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ความสัมพันธ์กับ User
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    employer = db.relationship('User', backref='jobs')


class JobApplication(db.Model):
    __tablename__ = 'job_applications'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ความสัมพันธ์
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))
    applicant = db.relationship('User', backref=db.backref('applications', lazy=True))


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('job_applications.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', backref='sent_messages')
    application = db.relationship('JobApplication', backref='chat_messages')

class Resume(db.Model):
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    birth_date = db.Column(db.Date())
    location = db.Column(db.String(100))
    disability_type = db.Column(db.String(100))
    disability_card_url = db.Column(db.String(255))  # path หรือ URL ของไฟล์
    disability_level = db.Column(db.String(50))
    assistive_technology = db.Column(db.Text)
    support_needs = db.Column(db.Text)  # บันทึกเป็น string (เช่น: "การเคลื่อนไหว,การสื่อสาร")
    confirmation_checked = db.Column(db.Boolean, default=False)
    education = db.Column(db.Text)
    work_experience = db.Column(db.Text)
    skills = db.Column(db.Text)
    portfolio = db.Column(db.Text)
    resume_video_url = db.Column(db.String(255))

    user = db.relationship('User', backref=db.backref('resume', uselist=False))