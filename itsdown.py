#!/usr/bin/env python

import time
import argparse
import re
import sys
from celery.schedules import crontab
from redbeat import RedBeatSchedulerEntry
from itsdown import tasks
from itsdown.config import flask_url
from urllib.parse import urlencode
import requests

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate if it is down.")
    parser.add_argument(
        "--url", type=str, help="The page of interest", default=argparse.SUPPRESS
    )
    parser.add_argument(
        "--fn",
        type=str,
        help="Dotted path to function to evaluate URL",
        default=argparse.SUPPRESS,
        required=True,
    )
    parser.add_argument(
        "--to",
        type=str,
        help="Email address to send report, if any",
        default=argparse.SUPPRESS,
        required=True,
    )
    parser.add_argument(
        "--cron-expr",
        type=str,
        help='Cron expression, e.g. "0 13 * * 1"',
        default=None
    )
    args = parser.parse_args()

    url, fn_path, to, cron_expr = args.url, args.fn, args.to, args.cron_expr
    mod_path, fn_name = re.match(r"(.+)\.(.+)", fn_path).groups()



    if args.cron_expr:
        endpoint = 'add_periodic_task'
        query_string = urlencode({
            'url': url,
            'to': to,
            'cron_expr': cron_expr,
            'mod_path': mod_path,
            'fn_name': fn_name
        })
        req_url = f'http://{flask_url}/{endpoint}?{query_string}'
        rv = requests.get(req_url)
        print(rv)
        print("Scheduling...")
        print(
            f"Periodic task scheduled! Will send report to {to} "
            "when problematic status is found."
        )

    else:
        print("Doing task now...")
        tasks.check_page(url, mod_path, fn_name, to)
