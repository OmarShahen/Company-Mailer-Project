from email.mime.text import MIMEText
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(sender_mail, sender_password, receiver_mail, mail_subject, mail_body):

    message = MIMEMultipart("alternative")
    message['Subject'] = mail_subject
    message['To'] = receiver_mail
    message['From'] = sender_mail

    plain_text = mail_body.strip()
    html_text = mail_body.strip()

    plain_part = MIMEText(plain_text,"plain")
    html_part = MIMEText(html_text,"html")

    message.attach(plain_part)
    message.attach(html_part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as server:
        server.login(sender_mail,sender_password)
        server.sendmail(sender_mail,receiver_mail,message.as_string())

def send_mail_attachment(sender_mail, sender_password, receiver_mail, mail_subject, mail_body, file_location, file_name):

    message = MIMEMultipart()
    message['Subject'] = mail_subject
    message['To'] = receiver_mail
    message['From'] = sender_mail
    message['Bcc'] = receiver_mail

    message.attach(MIMEText(mail_body,"plain"))
    message.attach(MIMEText(mail_body,"html"))

    with open(file_location, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("content-Disposition", f"attachment; filename = {file_name}")
    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as server:
        server.login(sender_mail, sender_password)
        server.sendmail(sender_mail, receiver_mail, text)




