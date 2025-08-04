from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime
from flask import current_app
from . import db
import pytz
from collections import Counter


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
