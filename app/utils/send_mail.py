from django.core.mail import send_mail
from django.conf import settings


def send_email(**kwargs):
    full_name = kwargs.get("full_name")
    email = kwargs.get("email")
    subject = "Bienvenido a nuestra aplicación"
    message = f"Hola {full_name},\
        \n\nBienvenido a nuestra aplicación! Su cuenta ha sido creada correctamente."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [
        email,
    ]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
