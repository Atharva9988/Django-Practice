from home.models import Cricketers
import time
from django.core.mail import send_mail
from django.conf import settings


def run_this_function():
    print("Function Started")
    print("Function Running...")
    print("Function Running....")
    time.sleep(2)
    print("Function Run Successfully")

def send_email_to_clients():
    subject = "This email is sent from Django application"
    message = "This is a test email sent from Django application using Gmail SMTP server."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["atharvathorve2@gmail.com"]
    send_mail(subject, message, from_email, recipient_list)