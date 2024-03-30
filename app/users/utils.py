from app import mail, db
from flask import render_template, current_app
from app.users.models import User
import uuid
from werkzeug.security import generate_password_hash


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