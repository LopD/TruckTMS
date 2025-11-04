## rest framework
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

## django lib
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

'''
    Sends a verification email to the given user. The user should be an instance of get_user_model() and it should have a valid email address.
'''
class VerificationEmailSender():
    
    def send(user):
        
        ## create token
        from core.token import EmailVerificationToken
        token = EmailVerificationToken.for_user(user)

        ## create the absolute url to the front end site
        relative_link = reverse('email-verify')
        from django.conf import settings
        frontend_site = settings.FRONTEND_DOMAIN
        absurl = f"http://{frontend_site}{relative_link}?token={str(token)}" ## TODO: change the current_site to hit the frontend confirmation view

        ## create and send the email
        email_body = render_to_string('verify_email.html', {
            'user': user,
            'domain': frontend_site,
            'activation_url': absurl,
        })

        email = EmailMessage(
            subject='Activate your account',
            body=email_body,
            from_email='no-reply@example.com',
            to=[user.email],
        )
        email.content_subtype = "html"
        email.send()




        