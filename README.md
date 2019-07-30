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

You will also need to install [wkhtmltopdf](https://wkhtmltopdf.org/) 
which is required for generating the
PDF report that are emailed to specified recipients:
```
# Ubuntu/Debian?
sudo apt-get install wkhtmltopdf

# Homebrew
brew install Caskroom/cask/wkhtmltopdf
```

# Usage Example

```bash
python itsdown/main.py \
    --url "https://structpred.dash.materialsproject.org/report/hours/24/" \
    --fn "itsdown.functions.fwsdash_24hr" \
    --to dwinston@lbl.gov
```

## Advanced installation

In addition to the above, you can use [Celery](http://www.celeryproject.org/) to run reports in a crontab-like manner.

You'll need to install [RabbitMQ](https://www.rabbitmq.com/) (Celery's recommended so-called "data broker"):
```
# Ubuntu/Debian?
sudo apt-get install rabbitmq-server
# Docker?
docker run -d -p 5462:5462 rabbitmq
# Homebrew?
brew install rabbitmq
```

# Usage Example

Start the RabbitMQ server:

```
# For example, if you use `brew install` on a Mac, this will ensure rabbitmq starts now and on system restarts.
brew services start rabbitmq
```

Start the Celery server:

```
celery -A itsdown.tasks worker -l info
```

Schedule a periodic itsdown task with a 
[crontab expression](https://www.adminschoice.com/crontab-quick-reference)
```bash
python itsdown/main.py \
    --url "https://structpred.dash.materialsproject.org/report/hours/24/" \
    --fn "itsdown.functions.fwsdash_24hr" \
    --to tylerhuntington222@lbl.gov \
    --cron-expr "* * * * *"
```

(Under construction) Use `celery.schedules.crontab` to do great things! 
