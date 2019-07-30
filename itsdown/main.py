import argparse
import re
import sys
from celery.schedules import crontab
from redbeat import RedBeatSchedulerEntry
from itsdown import tasks

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
    )
    parser.add_argument(
        "--to",
        type=str,
        help="Email address to send report, if any",
        default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--cron-expr", type=str, help='Cron expression, e.g. "0 13 * * 1"', default=None
    )
    args = parser.parse_args()

    url, fn_path, to, cron_expr = args.url, args.fn, args.to, args.cron_expr
    mod_path, fn_name = re.match(r"(.+)\.(.+)", fn_path).groups()



    if args.cron_expr:
        print("Scheduling...")
        minute, hour, day_of_month, month_of_year, day_of_week = (
            args.cron_expr.strip().split()
        )

        schedule = crontab(
            minute=minute,
            hour=hour,
            day_of_month=day_of_month,
            month_of_year=month_of_year,
            day_of_week=day_of_week,
        )
        entry = RedBeatSchedulerEntry('check_page', 'tasks.check_page',
                                      schedule, args=[url, mod_path, fn_name, to],
                                      app=tasks.app)

        entry.save()
        # print(entry.key)

        # remove periodic task
        # RedBeatSchedulerEntry('check_page', app=tasks.app).delete()

        print(
            f"Task scheduled! Will send report to {to} "
            "when problematic status is found."
        )

    else:
        print("Doing task now...")
        tasks.check_page(url, mod_path, fn_name, to)
