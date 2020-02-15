import smtplib
from email.mime.text import MIMEText

def send_mail(customer, dealer, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '9d0e3cddc021a1'
    password = 'ca1d8f7f0e93fd'
    message = f'<h2>New Feedback Submission</h2><ul> <li>Customer: {customer}</li><li>Dealer: {dealer}</li><li>Dealer: {rating}</li><li>Dealer: {comments}</li> </ul>'

    sender_email = 'andre.williams@students.makeschool.com'
    receiver_email = f'example@gmail.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Lexas Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email 
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())