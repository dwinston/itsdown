import tasks
from redbeat import RedBeatSchedulerEntry, RedBeatScheduler

def main():

    print('RedBeat schedule before clearing:')
    print(tasks.scheduler.schedule)
    keys = list(tasks.scheduler.schedule.keys())
    print(keys)
    if keys:
        for k in keys:
            print(f'Removing task: {k}')
            RedBeatSchedulerEntry(k, app=tasks.celery_app).delete()

    print('RedBeat schedule after clearing:')
    print(tasks.scheduler.schedule)



if __name__ == '__main__':
    main()
