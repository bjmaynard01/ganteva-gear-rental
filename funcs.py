from app import app, mail, db
from flask import render_template


def send_registration_mail(mail_to, to_name, email, cc_list):
    html = render_template('registration_email.html', name=to_name, email=email)
    try:
        mail.send_message( 
            recipients=mail_to, 
            subject='Thank You for Registering with GanTeva\'s Gear Rental Site',
            cc = [cc_list],
            html=html
        )
    
    except Exception as error:
        return "Error encounted trying to send mail message.", error