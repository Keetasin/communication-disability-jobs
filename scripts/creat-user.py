import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from website import create_app, db
from website.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # ผู้พิการ 1
    user1 = User(
        email="keetasin01@gmail.com",
        password=generate_password_hash("Kongsee", method='pbkdf2:sha256'),
        first_name="สมชาย",
        last_name="หูหนวก",
        role="disabled",
        disability_type="ผู้พิการทางการได้ยิน",
        skills="พิมพ์ดีด, ตัดต่อวิดีโอ",
        resume_text="จบการศึกษาด้านมัลติมีเดีย",
        resume_video_url="https://example.com/video1",
        location="กรุงเทพฯ",
        digital_skill_level="กลาง"
    )

    # ผู้พิการ 2
    user2 = User(
        email="keetasin02@gmail.com",
        password=generate_password_hash("Kongsee", method='pbkdf2:sha256'),
        first_name="สมหญิง",
        last_name="ไร้เสียง",
        role="disabled",
        disability_type="ผู้พิการทางการได้ยิน",
        skills="Photoshop, Canva",
        resume_text="มีประสบการณ์ออกแบบโปสเตอร์",
        resume_video_url="https://example.com/video2",
        location="เชียงใหม่",
        digital_skill_level="สูง"
    )

    # ผู้ว่าจ้าง 1
    employer1 = User(
        email="keetasin001@gmail.com",
        password=generate_password_hash("Kongsee", method='pbkdf2:sha256'),
        first_name="Human",
        last_name="Resource",
        role="employer",
        company_name="บริษัทเทคโนโลยีไทย",
        contact_person="คุณมนัส",
        contact_phone="0891234567",
        contact_email="contact@company.com",
        address="กรุงเทพฯ"
    )

    # ผู้ว่าจ้าง 2
    employer2 = User(
        email="keetasin002@gmail.com",
        password=generate_password_hash("Kongsee", method='pbkdf2:sha256'),
        first_name="Startup",
        last_name="Owner",
        role="employer",
        company_name="ThaiStartup",
        contact_person="คุณกานต์",
        contact_phone="0869876543",
        contact_email="info@startup.com",
        address="ขอนแก่น"
    )

    db.session.add_all([user1, user2, employer1, employer2])
    db.session.commit()

    print("🎉 Users created successfully!")
