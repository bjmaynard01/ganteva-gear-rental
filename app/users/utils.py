from app import mail, db
from flask import render_template, current_app
from app.models import User
import uuid


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
