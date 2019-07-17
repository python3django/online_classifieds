from celery import task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .token_generator import account_activation_token
from django.utils.http import urlsafe_base64_encode 
from django.utils.encoding import force_bytes
from .token_generator import account_activation_token
from django.contrib.auth.models import User


@task
def register_token(pk, current_site_domain):
    """
    Task to send an email token for registration
    """
    new_user = User.objects.get(pk=pk)
    email_subject = 'Activate Your Account'
    message = render_to_string('account/activate_account.html', {
                'user': new_user,
                'domain': current_site_domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user)
    })
    to_email = new_user.email
    email = EmailMessage(email_subject, message, to=[to_email])
    email.send()

