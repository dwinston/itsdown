from bs4 import BeautifulSoup
import pdfkit
import requests
from itsdown.send_email import send_email
import sys

def check_page(url, fn, to):
    rv = requests.get(url)
    page_as_string = rv.text
    print("Generating snapshot PDF of page in case problematic status is found...")
    snapshot_pdf = pdfkit.from_url(url, False, options={"quiet": ''})
    print("Normal")
    print(f"Done generating PDF. Analyzing page content with {fn}...")
    soup = BeautifulSoup(page_as_string, "html.parser")
    status = fn(soup)
    if status is None:
        print("No problematic status")
        return {"problematic_status": False}

    print(f"Problematic status: '{status}'. Sending report to {to}...")
    send_email(recipient=to, url=url, status=status, attachment=snapshot_pdf)
    return {"problematic_status": True}

if __name__ == "__main__":
    url, fn, to = sys.argv[1:]
    if url:
        check_page(url,fn,to)