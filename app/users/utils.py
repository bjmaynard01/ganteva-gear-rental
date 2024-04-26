from app import mail, db
from flask import render_template, current_app, url_for
from app.users.models import User
import uuid
from werkzeug.security import generate_password_hash
import datetime
import random


def send_registration_mail(mail_to, to_name, email, cc):
    html = render_template('users/registration_email.html', name=to_name, email=email)
    try:
        mail.send_message( 
            recipients=mail_to, 
            subject=current_app.config.get('REGISTRATION_SUBJECT'),
            cc = cc,
            html=html
        )
    
    except Exception as error:
        return "Error encounted trying to send mail message.", error
    
def clear_user_table():
    users = User.query.all()
    for user in users:
        db.session.delete(user)

    db.session.commit()

def gen_uuid_key():
    uuids = str(uuid.uuid4()) + str(uuid.uuid4())
    key = uuids.replace('-', '')
    return key

def gen_users(num_users):
    
    for i in range(0, num_users):
        fname = 'Test' + str(i)
        lname = 'User' + str(i)
        email = 'testuser' + str(i) + '@test.com'
        passwd = 'test' + str(i)
        hash = generate_password_hash(passwd)
        phone = '214-543-000' + str(i)
        user = User(fname=fname, lname=lname, email=email, password_hash=hash, phone=phone, confirmed=False, is_admin=False)
        db.session.add(user)
    db.session.commit()
    return 'Created ' + str(i) + 'test users.'

def generate_random_date(start_date, end_date, k):
    date_range = end_date - start_date
    for _ in range(k):
        random_days = random.randint(0, date_range.days)
        random_date = start_date + datetime.timedelta(days=random_days)
    return random_date


def send_password_reset_email(user, reset_password_url, user_email):
    html = render_template('users/password_reset_email.html', user=user, reset_password_url=reset_password_url)

    try: 
        mail.send_message(
            recipients = [user_email],
            subject = current_app.config.get('PASSWORD_RESET_SUBJECT'),
            html = html
        )

    except Exception as error:
        return "Error encountered when trying to send password reset email.", error