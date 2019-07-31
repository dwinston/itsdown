# itsdown
emails you a report if a web page indicates that a service is down or has not been running


1. Supply a URL

2. Supply a function that, given a BeautifulSoup object as input, decides whether the service is down and outputs a
useful message. There are some provided in `itsdown.functions` -- you supply a function on the command line as a
dotted path.

3. If the service is down, email someone with the message, with a link to the URL, and with the page output attached to
the email.

## Installing

```bash
git clone git@github.com:dwinston/itsdown.git
cd itsdown
pip install -e .
cp itsdown/config.example.ini itsdown/config.ini
# Edit itsdown/config.ini to reflect your email service SMTP information.
```

# Usage Example

```bash
python itsdown/main.py \
    --url "https://structpred.dash.materialsproject.org/report/hours/24/" \
    --fn "itsdown.functions.fwsdash_24hr" \
    --to dwinston@lbl.gov \
    --cron-expr "0 13 * * *"
```
###<i>Note</i>

Crontab will not work if you have the normal crontab library installed. Please create a new environment or uninstall the normal crontab
and download the python-crontab. Please check the documentation right [here.](https://pypi.org/project/python-crontab/)

###Update

We removed the Celery and RabbitMQ for scheduling and instead use the python-crontab library.
One reason is because it is harder to setup. In most cases Celery and RabbitMQ
offers a lot more, though those features aren't needed in this type of application.
