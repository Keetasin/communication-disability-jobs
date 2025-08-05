from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from . import db
import pytz
from .models import Job, JobApplication, ChatMessage


views = Blueprint('views', __name__)

@views.route('/')
def welcome():
    return render_template('welcome.html', user=current_user)

@views.route('/home')
def home():
    return render_template('home.html', user=current_user)


@views.route('/account')
@login_required
def account():
    user = current_user
    current_date = datetime.now(pytz.timezone('Asia/Bangkok')).date()

    return render_template(
        'account.html', 
        user=user, 
        current_date=current_date,
    )

@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        user = current_user
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')

        if user.role == 'disabled':
            user.disability_type = request.form.get('disability_type')
            user.skills = request.form.get('skills')
            user.resume_text = request.form.get('resume_text')
            user.resume_video_url = request.form.get('resume_video_url')
            user.location = request.form.get('location')
            user.digital_skill_level = request.form.get('digital_skill_level')
            user.training_completed = bool(request.form.get('training_completed'))

        elif user.role == 'employer':
            user.company_name = request.form.get('company_name')
            user.contact_person = request.form.get('contact_person')
            user.contact_phone = request.form.get('contact_phone')
            user.contact_email = request.form.get('contact_email')
            user.address = request.form.get('address')
            user.company_website = request.form.get('company_website')
            user.company_description = request.form.get('company_description')

        db.session.commit()
        flash('Profile updated successfully!', category='success')
        return redirect(url_for('views.account'))

    return render_template('edit_profile.html', user=current_user)


@views.route('/post-job', methods=['GET', 'POST'])
@views.route('/post-job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def post_job(job_id=None):
    if current_user.role == 'disabled' and request.method == 'POST':
        flash('You are not allowed to post jobs.', 'error')
        return redirect(url_for('views.all_jobs'))

    job = None
    if job_id:
        job = Job.query.get_or_404(job_id)
        if job.employer != current_user:
            flash('You are not allowed to edit this job.', 'error')
            return redirect(url_for('views.all_jobs'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        salary = request.form.get('salary')

        if job:  # แก้ไขงาน
            job.title = title
            job.description = description
            job.location = location
            job.salary = salary
            flash('Job updated successfully!', 'success')
        else:  # เพิ่มงานใหม่
            job = Job(
                title=title,
                description=description,
                location=location,
                salary=salary,
                employer=current_user
            )
            db.session.add(job)
            flash('Job posted successfully!', 'success')

        db.session.commit()
        return redirect(url_for('views.all_jobs'))

    return render_template('post_job.html', job=job, user=current_user)


from sqlalchemy.orm import joinedload

@views.route('/jobs')
def all_jobs():
    jobs = Job.query.options(joinedload(Job.applications)) \
        .filter(~Job.applications.any(JobApplication.status == 'accepted')) \
        .order_by(Job.posted_at.desc()) \
        .all()
    return render_template('all_jobs.html', jobs=jobs, user=current_user)


@views.route('/apply/<int:job_id>', methods=['POST'])
@login_required
def apply_job(job_id):
    if current_user.role != 'disabled':
        flash('Only users with disabilities can apply for jobs.', 'error')
        return redirect(url_for('views.all_jobs'))

    job = Job.query.get_or_404(job_id)

    # เช็คว่าผู้ใช้สมัครไปแล้วหรือยัง
    existing = JobApplication.query.filter_by(job_id=job_id, applicant_id=current_user.id).first()
    if existing:
        flash('คุณสมัครงานนี้ไปแล้ว', 'info')
        return redirect(url_for('views.all_jobs'))

    application = JobApplication(job_id=job_id, applicant_id=current_user.id)
    db.session.add(application)
    db.session.commit()
    flash(f'สมัครงาน "{job.title}" เรียบร้อยแล้ว!', 'success')
    return redirect(url_for('views.all_jobs'))

@views.route('/employer/jobs')
@login_required
def employer_jobs():
    if current_user.role != 'employer':
        flash('หน้าสำหรับผู้ว่าจ้างเท่านั้น', 'error')
        return redirect(url_for('views.home'))

    jobs = Job.query.filter_by(employer_id=current_user.id).order_by(Job.posted_at.desc()).all()
    return render_template('employer_jobs.html', jobs=jobs, user=current_user)


@views.route('/employer/application/<int:application_id>')
@login_required
def view_applicant(application_id):
    if current_user.role != 'employer':
        flash('หน้าสำหรับผู้ว่าจ้างเท่านั้น', 'error')
        return redirect(url_for('views.home'))

    application = JobApplication.query.get_or_404(application_id)

    # ตรวจสอบว่า application นี้เป็นของงานผู้ว่าจ้าง
    if application.job.employer_id != current_user.id:
        flash('คุณไม่มีสิทธิ์ดูข้อมูลนี้', 'error')
        return redirect(url_for('views.employer_jobs'))

    return render_template('view_applicant.html', application=application, user=current_user)


@views.route('/my-applications')
@login_required
def my_applications():
    if current_user.role != 'disabled':
        flash('หน้านี้สำหรับผู้พิการเท่านั้น', 'error')
        return redirect(url_for('views.home'))

    # กรองเฉพาะที่ applicant_id = current_user.id และ status != 'accepted'
    applications = JobApplication.query \
        .filter_by(applicant_id=current_user.id) \
        .filter(JobApplication.status != 'accepted') \
        .order_by(JobApplication.applied_at.desc()) \
        .all()

    return render_template('my_applications.html', applications=applications, user=current_user)



@views.route('/chat/<int:application_id>', methods=['GET', 'POST'])
@login_required
def chat(application_id):
    application = JobApplication.query.get_or_404(application_id)

    # ตรวจสอบสิทธิ์
    if current_user.id not in [application.applicant_id, application.job.employer_id]:
        flash('คุณไม่มีสิทธิ์เข้าถึงการแชทนี้', 'error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            new_msg = ChatMessage(
                application_id=application_id,
                sender_id=current_user.id,
                content=message
            )
            db.session.add(new_msg)
            db.session.commit()
            return redirect(url_for('views.chat', application_id=application_id))

    chat_history = ChatMessage.query.filter_by(application_id=application_id).order_by(ChatMessage.timestamp).all()
    return render_template('chat.html', chat_history=chat_history, application=application, user=current_user)


@views.route('/delete-job/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.employer_id != current_user.id:
        flash('คุณไม่มีสิทธิ์ลบโพสต์งานนี้', 'error')
        return redirect(url_for('views.employer_jobs'))
    
    # ลบผู้สมัครที่เกี่ยวข้องก่อน
    JobApplication.query.filter_by(job_id=job.id).delete()
    db.session.delete(job)
    db.session.commit()
    flash('ลบโพสต์งานเรียบร้อยแล้ว', 'success')
    return redirect(url_for('views.employer_jobs'))


from .models import ChatMessage  # ตรวจสอบว่ามี import แล้ว

@views.route('/accept-applicant/<int:application_id>', methods=['POST'])
@login_required
def accept_applicant(application_id):
    application = JobApplication.query.get_or_404(application_id)
    
    if application.job.employer_id != current_user.id:
        flash('คุณไม่มีสิทธิ์ตอบรับผู้สมัครนี้', 'error')
        return redirect(url_for('views.employer_jobs'))

    if application.status == 'accepted':
        flash('คุณได้ตอบรับผู้สมัครนี้ไปแล้ว', 'info')
        return redirect(url_for('views.view_applicant', application_id=application.id))

    # อัปเดตสถานะ
    application.status = 'accepted'
    
    # เพิ่มข้อความอัตโนมัติในแชท
    auto_msg = ChatMessage(
        application_id=application.id,
        sender_id=current_user.id,
        content=f"สวัสดี {application.applicant.first_name}, ทางเราขอตอบรับคุณเข้าทำงานในตำแหน่ง \"{application.job.title}\" ครับ/ค่ะ 🎉"
    )
    db.session.add(auto_msg)
    
    # Commit ทั้ง status และข้อความ
    db.session.commit()

    flash(f'คุณตอบรับ {application.applicant.first_name} เข้าทำงานแล้ว!', 'success')
    return redirect(url_for('views.view_applicant', application_id=application.id))


@views.route('/accepted-jobs')
@login_required
def accepted_jobs():
    if current_user.role != 'disabled':
        flash('หน้านี้สำหรับผู้พิการเท่านั้น', 'error')
        return redirect(url_for('views.home'))

    accepted_apps = JobApplication.query.filter_by(
        applicant_id=current_user.id,
        status='accepted'
    ).all()

    return render_template('accepted_jobs.html', applications=accepted_apps, user=current_user)
