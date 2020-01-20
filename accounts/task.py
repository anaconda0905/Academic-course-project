from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def user_send_mail(user, password=None, host=settings.EMAIL_HOST_USER):
    send_mail('Account Password', 'UserName: {}\n'
                                  'First Name: {}\n'
                                  'Last Name: {}\n'
                                  'Password for your account is {}'
                                  ''.format(user.username, user.first_name, user.last_name, password),
              host,
              [user.email])
