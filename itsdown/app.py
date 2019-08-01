import pprint
import redis
import time
from itsdown import tasks
from celery.schedules import crontab
from flask import Flask, request
from celery import Celery
from redbeat import RedBeatScheduler, RedBeatSchedulerEntry
from tasks import celery_app
from itsdown.config import redis_host, redis_port, redbeat_redis_index

pp = pprint.PrettyPrinter(indent=4)

flask_app = Flask(__name__)
r = redis.Redis(
    host=redis_host,
    port=redis_port,
    db=redbeat_redis_index
)

@flask_app.route('/')
def view():
    return "Hello, Flask is up and running!"

@flask_app.route('/add_periodic_task')
def add_periodic_task():
    kwargs = dict(request.args)

    cron_expr = "* * * * *"
    minute, hour, day_of_month, month_of_year, day_of_week = (
        kwargs['cron_expr'].strip().split()
    )
    kwargs.pop('cron_expr')
    schedule = crontab(
        minute=minute,
        hour=hour,
        day_of_month=day_of_month,
        month_of_year=month_of_year,
        day_of_week=day_of_week,
    )
    entry = RedBeatSchedulerEntry(
        name=kwargs['fn_name'],
        task='tasks.check_page',
        schedule=schedule,
        kwargs=kwargs,
        app=celery_app
    )
    entry.save()
    return 'Task Added!'

@flask_app.route('/add_task_trivial')
def add_task_trivial():

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
    entry = RedBeatSchedulerEntry('print_arg_task', 'tasks.print_arg',
                                  schedule, args=['Print Me!'],
                                  app=celery_app)
    entry.save()
    return 'Task Added!'

@flask_app.route('/drop_all_periodic_tasks')
def drop_all_periodic_tasks():
    print('RedBeat schedule before clearing:')
    periodics = tasks.scheduler.get_periodic_tasks()
    keys = list(periodics.keys())
    for k in keys:
        print(f'Removing task: {k}')
        # RedBeatSchedulerEntry(k, app=tasks.celery_app).delete()
        tasks.scheduler.remove_periodic_task(k)

    print('RedBeat schedule after clearing:')
    print(tasks.scheduler.get_periodic_tasks())

    return 'All tasks dropped!'

@flask_app.route('/pretty_print_periodic_tasks')
def pretty_print_periodic_tasks():
    periodics = tasks.scheduler.get_periodic_tasks()
    task_names = list(periodics.keys())
    width = 70
    s = '\n'
    s += ('-' * width + '\n')
    s += ('PERIODIC TASK DEFINITIONS\n')
    s += ('-' * width + '\n')
    if not periodics:
        s += 'No periodic tasks defined.'
    else:
        for n in task_names:
            s += f'Task Name (Redis key): "{n}"\n\n'
            s += f'Definition: \n\n'
            s += f'{pp.pformat(periodics[n])}\n'
        #     s += f'Periodic Task: "{n}"\n'
        #     for k in periodics[n].keys():
    s += ('-' * width + '\n')
    print(s)
    return(s)

if __name__ == "__main__":
    flask_app.run(debug=True)
