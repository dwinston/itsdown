import re
from bs4 import BeautifulSoup
import pdfkit
import requests
from celery import Celery
import itsdown.celeryconfig
from celery.schedules import crontab

from itsdown.send_email import send_email

app = Celery(
    'itsdown',
)
app.config_from_object('celeryconfig')

# Optional configuration, see the application user guide.
# app.conf.update(
#     result_expires=3600,
# )

@app.task()
def check_page(url, mod_path, fn_name, to):
    mod = __import__(mod_path, globals(), locals(), [fn_name], 0)
    if not hasattr(mod, fn_name):
        print(f"can't find function {fn_name} in module {fn_name}")
        sys.exit(1)
    fn = getattr(mod, fn_name)
    rv = requests.get(url)
    page_as_string = rv.text
    print("Generating snapshot PDF of page in case problematic status is found...")
    snapshot_pdf = pdfkit.from_url(url, False, options={"quiet": ""})
    print(f"Done generating PDF. Analyzing page content with {fn}...")
    soup = BeautifulSoup(page_as_string, "html.parser")
    status = fn(soup)
    if not status is None:
        print("No problematic status")
        return {"problematic_status": False}

    print(f"Problematic status: '{status}'. Sending report to {to}...")
    send_email(recipient=to, url=url, status=status, attachment=snapshot_pdf)
    return {"problematic_status": True}

