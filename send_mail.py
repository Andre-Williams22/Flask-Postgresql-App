import smtplib
from email.mime.text import MIMEText

def send_mail(customer, dealer, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '9d0e3cddc021a1'
    password = 'ca1d8f7f0e93fd'