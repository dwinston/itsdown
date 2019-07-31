from os import environ
from flask import Flask
from celery import Celery


flask_app = Flask(__name__)


# Configs

def make_celery(app):
    # create context tasks in celery
    celery_app = Celery(
        flask_app.import_name,
    )
    TaskBase = celery_app.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery

celery = make_celery(app)


@app.route('/')
def view():
    return "Hello, Flask is up and running!"


if __name__ == "__main__":
    app.run()