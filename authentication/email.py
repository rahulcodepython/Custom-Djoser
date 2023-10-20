from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from . import models


def ActivationEmail(user):
    if settings.SEND_ACTIVATION_EMAIL is True:
        uid = models.ActivationCode.objects.get(user=user).uid
        token = models.ActivationCode.objects.get(user=user).token

        link = settings.FRONTEND_URL + settings.ACTIVATION_URL + uid + '/' + token

        subject = "Verify Your Email Address - Action Required"
        html_body = render_to_string("activation.html", {
            'user': user,
            'company_name': settings.COMPANY_NAME,
            'host_email': settings.EMAIL_HOST_USER,
            'link': link
        })

        msg = EmailMultiAlternatives(
            subject=subject, from_email=settings.EMAIL_HOST_USER, to=[user.email])
        msg.attach_alternative(html_body, "text/html")
        msg.send()


def ResetPasswordConfirmation(user):
    if settings.SEND_RESET_PASSWORD_CONFIRMATION_EMAIL is True:
        uid = models.ResetPasswordCode.objects.get(user=user).uid
        token = models.ResetPasswordCode.objects.get(user=user).token

        link = settings.FRONTEND_URL + \
            settings.RESET_PASSWORD_CONFIRMATION_URL + uid + '/' + token

        subject = "Reset Password Confirmation - Action Required"
        html_body = render_to_string("reset_password_confirmation.html", {
            'user': user,
            'company_name': settings.COMPANY_NAME,
            'host_email': settings.EMAIL_HOST_USER,
            'link': link
        })

        msg = EmailMultiAlternatives(
            subject=subject, from_email=settings.EMAIL_HOST_USER, to=[user.email])
        msg.attach_alternative(html_body, "text/html")
        msg.send()
