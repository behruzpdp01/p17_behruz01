from root.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

def send_email(subject, message, to_email: list):
    send_mail('TEMASI', f'{subject} \n {message}', EMAIL_HOST_USER, to_email, False)
    return {"status": "success", "message": f"{'.'.join(to_email)}pochtaga yuborildi"}
