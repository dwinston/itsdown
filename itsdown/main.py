import argparse
import sys
from functools import partial
import re

from bs4 import BeautifulSoup
import pdfkit
import requests

from itsdown.send_email import send_email


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Evaluate if it is down.')
	parser.add_argument('--url', type=str, help='The page of interest', default=argparse.SUPPRESS)
	parser.add_argument('--fn', type=str, help='Dotted path to function to evaluate URL', default=argparse.SUPPRESS)
	parser.add_argument('--to', type=str, help='Email address to send report, if any', default=argparse.SUPPRESS)
	args = parser.parse_args()

	rv = requests.get(args.url)
	page_as_string = rv.text
	print("Generating snapshot PDF of page in case problematic status is found...")
	snapshot_pdf = pdfkit.from_url(args.url, False, options={"quiet": True})
	print(f"Done generating PDF. Analyzing page content with {args.fn}...")
	soup = BeautifulSoup(page_as_string, "html.parser")
	mod_name, fn_name = re.match(r"(.+)\.(.+)", args.fn).groups()
	mod = __import__(mod_name, globals(), locals(), [fn_name], 0)

	if not hasattr(mod, fn_name):
		print(f"can't find function {fn_name} in module {fn_name}")
		sys.exit(1)

	fn = getattr(mod, fn_name)
	status = fn(soup)
	if status is None:
		print("No problematic status")
		sys.exit(0)

	print(f"Problematic status: '{status}'. Sending report to {args.to}...")
	send_email(recipient=args.to, url=args.url, status=status, attachment=snapshot_pdf)


