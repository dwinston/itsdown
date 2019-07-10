from celery import Celery

app = Celery(
    'itsdown',
    broker='pyamqp://guest@localhost//',
    backend='rpc://',
    include=['itsdown.tasks']
)

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
