import redis
import time
from itsdown import tasks
from celery.schedules import crontab
from flask import Flask
from celery import Celery
from redbeat import RedBeatScheduler, RedBeatSchedulerEntry
from tasks import celery_app
from itsdown.celeryconfig import redbeat_redis_url, redis_host, redis_port

flask_app = Flask(__name__)
r = redis.Redis(
    host=redis_host,
    port=redis_port,
    db=7
)

for key in r.scan_iter("redbeat:*_task"):
    print(key)
rv = r.delete(b'redbeat:print_arg_task')
print(rv)
print(r.hgetall(b'redbeat:print_arg_task'))
exit()

@flask_app.route('/')
def view():
    return "Hello, Flask is up and running!"

@flask_app.route('/add_task')
def add_task():

    cron_expr = "* * * * *"
    minute, hour, day_of_month, month_of_year, day_of_week = (
        cron_expr.strip().split()
    )

    schedule = crontab(
        minute=minute,
        hour=hour,
        day_of_month=day_of_month,
        month_of_year=month_of_year,
        day_of_week=day_of_week,
    )
    print('BEFORE')
    print(tasks.scheduler.schedule)

    entry = RedBeatSchedulerEntry('print_arg_task', 'tasks.print_arg',
                                  schedule, args=['Print Me!'],
                                  app=celery_app)

    entry.save()
    print('Immediately after')
    print(celery_app.conf.beat_schedule)
    print(tasks.scheduler.schedule)
    # for i in range(120):
    #     time.sleep(1)
    #     print(f'Seconds: {i}')
    #     print(scheduler.schedule)
    #     if 'check_page' in scheduler.schedule:
    #         exit()

    return 'Task Added!'
@flask_app.route('/drop_all_tasks')
def drop_tasks():
    print('RedBeat schedule before clearing:')
    rv = r.hget('redbeat:print_arg_task', 'definition')
    print(str(rv))

    print(celery_app.redbeat_conf.schedule)
    s = tasks.scheduler
    keys = list(tasks.scheduler.schedule.keys())
    print(keys)
    if keys:
        for k in keys:
            print(f'Removing task: {k}')
            RedBeatSchedulerEntry(k, app=tasks.celery_app).delete()

    print('RedBeat schedule after clearing:')
    print(tasks.scheduler.schedule)

    return 'All tasks dropped!'



if __name__ == "__main__":
    flask_app.run(debug=True)
