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
    --to dwinston@lbl.gov
```
