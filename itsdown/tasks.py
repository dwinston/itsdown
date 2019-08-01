import re
from bs4 import BeautifulSoup
import pdfkit
import requests
from celery import Celery
import itsdown.config
from redbeat import RedBeatSchedulerEntry
from itsdown.itsdown_redbeat import ItsdownRedBeatScheduler

from itsdown.send_email import send_email

celery_app = Celery(
    'itsdown',
)
celery_app.config_from_object(itsdown.config)
scheduler = ItsdownRedBeatScheduler(app=celery_app)

@celery_app.task()
def check_page(url, mod_path, fn_name, to):
    mod = __import__(mod_path, globals(), locals(), [fn_name], 0)
    if not hasattr(mod, fn_name):
        print(f"can't find function {fn_name} in module {fn_name}")
        sys.exit(1)
    # temp
    fn_name = 'test_page_content'
    fn = getattr(mod, fn_name)
    rv = requests.get(url)
    page_as_string = rv.text
    print("Generating snapshot PDF of page in case problematic status is found...")
    snapshot_pdf = pdfkit.from_url(url, False, options={"quiet": ""})
    print(f"Done generating PDF. Analyzing page content with {fn}...")
    soup = BeautifulSoup(page_as_string, "html.parser")
    status = fn(soup)
    if status is None:
        print("No problematic status")
        return {"problematic_status": False}

    print(f"Problematic status: '{status}'. Sending report to {to}...")
    send_email(recipient=to, url=url, status=status, attachment=snapshot_pdf)
    return {"problematic_status": True}

