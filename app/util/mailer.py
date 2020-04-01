import os
from django.core.mail import send_mass_mail, send_mail

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_html_email(subject, html, mail_list):
  text_content = strip_tags(html)
  msg = EmailMultiAlternatives(subject, text_content, os.environ.get('EMAIL_USER'), [mail_list])
  msg.attach_alternative(html, "text/html")
  msg.send()

def send_tihlde_email(subject, message, mail_list):
  return send_mail(subject, message, os.environ.get('EMAIL_USER'), mail_list, fail_silently=False,)


def send_user_event_mail(is_on_wait, event, user):
  if is_on_wait:
    send_tihlde_email(
      "Du er satt på venteliste for event " + (event),
      "Inntil videre er du satt på venteliste",
      user
    )
  else:
    send_tihlde_email(
      "Du har fått plass på " + (event),
      "Gratulerer, du har fått plass på eventet " + (event),
      user
    )
  return None