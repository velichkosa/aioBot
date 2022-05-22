import smtplib
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email_validate import validate


import db_operator as db

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


def check_exists_email(user_id):
    email_len = db.to_mongo(user_id, None, 'email_len')
    if email_len == 0:
        return False, email_len
    elif email_len > 0:
        return True, email_len


def validate_email(email):
    valid = validate(
        email_address=email,
        check_format=True,
        check_blacklist=False,
        check_dns=True,
        dns_timeout=10,
        check_smtp=True,
        smtp_debug=False)
    return valid


def to_email(src, data, to, chat_id):
    msg = MIMEMultipart()

    # setup the parameters of the message
    password = config['email_pwd']
    msg['From'] = "textrecognition.bot@gmail.com"
    msg['To'] = to
    msg['Subject'] = "txtr bot result"

    # add in the message body
    msg.attach(MIMEText(data, 'plain'))

    # attach image to message body
    with open(src, 'rb') as fp:
        img = MIMEImage(fp.read())
    msg.attach(img)
    # create server
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()