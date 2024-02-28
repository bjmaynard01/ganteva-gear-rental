from app import app, mail
from flask import render_template


def send_mail(mail_to, to_name, mail_subject):
    html = render_template('email.html', name=to_name, subject=mail_subject)
    try:
        mail.send_message( 
            recipients=[mail_to], 
            subject=mail_subject,
            cc = 'bryan@maynardfolks.com', 
            html=html
        )
    
    except Exception as error:
        return "Error encounted trying to send mail message.", error