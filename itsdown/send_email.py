import configparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from itsdown import mail_config_path

config = configparser.ConfigParser()
config.read(config_path)
email_config = config["EMAIL"]


def send_email(recipient, url, status, attachment):
    sender = email_config["from"]
    email = MIMEMultipart()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = f"[itsdown]: {status}"
    body = f"""
URL : {url}
or
Check the attachment
"""
    email.attach(MIMEText(body, "plain"))
    p = MIMEBase("application", "octet-stream")
    p.set_payload(attachment)
    encoders.encode_base64(p)
    p.add_header("Content-Disposition", "attachment; filename= report.pdf")
    email.attach(p)
    s = smtplib.SMTP(email_config["smtp_server"], 587)
    s.starttls()
    s.login(email_config["smtp_user"], email_config["smtp_pass"])
    text = email.as_string()
    s.sendmail(sender, recipient, text)
    s.quit()
    print(f"Send report to {recipient}.")
