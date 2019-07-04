from configparser import ConfigParser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

config = ConfigParser(Path(__file__).absolute().joinpath("config.ini"))
email_config = config["EMAIL"]


def send_email(recipient, link, status):
    sender = email_config["from"]
    email = MIMEMultipart()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = f"[itsdown]: {status}"
    body = f"""
Link : {link}
or
Check the attachment
"""
    email.attach(MIMEText(body, "plain"))
    filename = "screenshot.pdf"
    attachment = open("screenshot.pdf", "rb")
    p = MIMEBase("application", "octet-stream")
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header("Content-Disposition", "attachment; filename= %s" % filename)
    email.attach(p)
    s = smtplib.SMTP(email_config["smtp_server"], 587)
    s.starttls()
    s.login(sender, password)
    text = email.as_string()
    s.sendmail(sender, recepient, text)
    s.quit()
