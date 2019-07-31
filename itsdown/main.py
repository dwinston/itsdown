import argparse
import re
import sys
from tasks import check_page
from crontab import CronTab
import os ; import subprocess
dirpath = os.getcwd()
dirpath = dirpath.replace("itsdown/itsdown", "itsdown")
# pypath = subprocess.Popen(['which','python'],stdout = subprocess.PIPE).communicate()[0].decode('ascii')
# pypath = pypath.replace("/python", "")
pypath = "/Users/destrada/miniconda3/envs/itsdown/bin/python"
if __name__ == "__main__":
    cron = CronTab(user=True)

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
    mod = __import__(mod_path, globals(), locals(), [fn_name], 0)

    if not hasattr(mod, fn_name):
        print(f"can't find function {fn_name} in module {fn_name}")
        sys.exit(1)

    fn = getattr(mod, fn_name)
    if args.cron_expr:
        print("Scheduling...")
        #TODO make the python path dynamic
        sched=str(args.cron_expr).strip()
        job = cron.new(
            command=f'cd {dirpath}/itsdown/ && {pypath} '
                    f'{dirpath}/itsdown/tasks.py {url} "{fn}" {to} >> {dirpath}/itsdown/printed_out.log')
        # >> {dirpath} / itsdown / printed_out.log
        # job.setall(sched)
        job.minute.every(1)
        print(
            f"Task scheduled! Will send report to {to} when problematic status is found."
        )
        job.run()
        cron.write()

    else:
        print("Doing task now...")
        check_page(url, fn, to)