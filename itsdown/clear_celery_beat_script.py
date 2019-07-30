from itsdown import tasks
from redbeat import RedBeatSchedulerEntry, RedBeatScheduler

def main():

    s = RedBeatScheduler(app=tasks.app, lock_key='redbeat:lock')
    print(s.schedule)
    print(tasks.app.conf)

    # entry = RedBeatSchedulerEntry(k, app=tasks.app).delete()



if __name__ == '__main__':
    main()
