from . import mails
# from Quickcash.app import db,admin , mail1
from .. import mail1
from flask_mail import Mail,Message




def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender='cashq261@gmail.com'
    )
    mail1.send(msg)