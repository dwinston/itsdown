import argparse
import sys
from functools import partial
import re

from bs4 import BeautifulSoup
import requests
import pdfkit
#from .send_email import send_email


def fwsdash_24hr(soup, threshold_pct=0):
	"""given bs node as input, decides whether the service is down and returns a useful message"""
	fw_report_text = soup.find("pre").get_text()
	total_fws = sum(int(n) for n in re.findall(f"\ntotal\s*:\s*(\d+)", fw_report_text))
	completed_fws = sum(int(n) for n in re.findall(f"\nCOMPLETED\s*:\s*(\d+)", fw_report_text))
	if total_fws:
		pct_complete = 100 * completed_fws / total_fws
		if pct_complete <= threshold_pct:
			return f"{total_fws} submitted, but {completed_fws} completed (under {threshold_pct}% threshold)"


fwsdash_24hr_10 = partial(fwsdash_24hr, threshold_pct=10)
fwsdash_24hr_50 = partial(fwsdash_24hr, threshold_pct=50)
fwsdash_24hr_100 = partial(fwsdash_24hr, threshold_pct=100)


# 3. If the service is down, email someone with the message, with a link to the URL, and with the page output attached to the email.

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Evaluate if it is down.')
	parser.add_argument('url', type=str, help='The page of interest')
	parser.add_argument('evaluator', type=str, help='Dotted path to evaluate URL')
	parser.add_argument('recipient', type=str, help='Email address to send report, if any')
	args = parser.parse_args()

	rv = requests.get(args.url)
	soup = BeautifulSoup(rv.text, "html.parser")
	modname = ".".join(args.evaluator.split('.')[:-1])
	fnname = args.evaluator.split('.')[-1]
	mod = __import__(modname, globals(), locals(), [fnname], 0)

	if not hasattr(mod, fnname):
		print(f"can't find function {fnname} in module {modname}")
		sys.exit(1)

	fn = getattr(mod, fnname)
	result = fn(soup)
	if result is None:
		print("No problem")
		sys.exit(0)



