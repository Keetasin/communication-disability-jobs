from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from . import db
import pytz
from .models import Job


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
@login_required
def post_job():
    if current_user.role != 'employer':
        flash('Only employers can post jobs.', 'error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        salary = request.form.get('salary')

        new_job = Job(
            title=title,
            description=description,
            location=location,
            salary=salary,
            employer=current_user
        )
        db.session.add(new_job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('job.all_jobs'))

    # ✅ FIX: ส่ง user ไปด้วยเพื่อให้ base.html ไม่ error
    return render_template('post_job.html', user=current_user)



@views.route('/jobs')
def all_jobs():
    jobs = Job.query.order_by(Job.posted_at.desc()).all()
    return render_template('all_jobs.html', jobs=jobs, user=current_user)

