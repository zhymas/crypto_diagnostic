from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task(name='send_verification_email')
def send_verification_email(email, token, username):
    subject = 'Verify your email'
    message = f'Dear {username}, Click http://localhost:8000/api/v1/users/verify-email?token={token} here to verify your email'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    return True
