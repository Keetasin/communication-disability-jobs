from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        elif user:
            flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # ฟิลด์ทั่วไป
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role = request.form.get('role')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif role not in ['disabled', 'employer']:
            flash('Invalid user role.', category='error')
        else:
            # สร้าง user ตาม role
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=generate_password_hash(password1, method='pbkdf2:sha256'),
                role=role
            )

            if role == 'disabled':
                new_user.disability_type = request.form.get('disability_type')
                new_user.skills = request.form.get('skills')
                new_user.resume_text = request.form.get('resume_text')
                new_user.resume_video_url = request.form.get('resume_video_url')
                new_user.location = request.form.get('location')

            elif role == 'employer':
                new_user.company_name = request.form.get('company_name')
                new_user.contact_person = request.form.get('contact_person')
                new_user.contact_phone = request.form.get('contact_phone')
                new_user.contact_email = request.form.get('contact_email')
                new_user.address = request.form.get('address')

            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)

