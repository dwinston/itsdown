import smtplib, getpass
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
   

def send_email(link,status):
	sender = input("From:")
	try: 
	    password = getpass.getpass() 
	except Exception as error: 
	    print('ERROR', error) 
	recepient = input("To:")

	email = MIMEMultipart() 

	email['From'] = sender
	email['To'] = recepient 
	email['Subject'] = f'Fireworks Report : Status \"{status}\"'
	body = f"""
	Link : {link}
	or
	Check the attachment below:"""
	email.attach(MIMEText(body, 'plain')) 
	filename = "fw_wf_report.pdf"
	attachment = open("fw_wf_report.pdf", "rb") 
	p = MIMEBase('application', 'octet-stream') 
	p.set_payload((attachment).read()) 
	encoders.encode_base64(p) 
	p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
	email.attach(p) 
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	s.starttls() 
	s.login(sender, password) 
	text = email.as_string() 
	s.sendmail(sender, recepient, text) 
	s.quit() 