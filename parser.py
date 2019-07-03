from bs4 import BeautifulSoup
import requests, re, pdfkit
from send_email import send_email

class gettingInfo:
	page_link = ""
	while page_link == "":
		page_link = input("Link:")
	main_link = 'https://structpred.dash.materialsproject.org'
	pdfkit.from_url(page_link, 'fw_wf_report.pdf')
	page_response = requests.get(page_link, timeout=5)
	page_content = BeautifulSoup(page_response.content,"html.parser")
	imgs = page_content.find_all ("img")
	imgs = imgs[1:] ; m=1
	for image_tag in imgs:
		path = "Fireworks_Report.png" if m == 1 else "Workflows_Report.png"
		with open(path, 'wb') as handle:
			response = requests.get((main_link+image_tag.get('src')), stream=True)
			if not response.ok:
				print (response)
			for block in response.iter_content(1024):
				handle.write(block)
		m+=1

	fireworks_report = []
	workflows_report = []
	page_content = str(page_content).split("\n") ; i = 1
	for m in range (len(page_content)):
		try:
			if page_content[m][:3] == "<h3":
				if i == 1:
					fireworks_report.append("Fireworks Report")
				else:
					workflows_report.append("Workflows Report")
				while page_content[m+1][:3] != "</p":
					m+=1
					if i == 1 and page_content[m]!="<pre>":
						fireworks_report.append(page_content[m])
					elif i > 1 and page_content[m]!="<pre>":
						workflows_report.append(page_content[m])
				i+=1
		except:
			pass

status = "Down"

if status is "Down":
	send_email(gettingInfo.page_link,status)
else: 
	pass







