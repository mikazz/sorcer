from __future__ import absolute_import
from os import path, environ
import json
from flask import Flask, Blueprint, abort, jsonify, request, session
from celery import Celery

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
PORT = 5000
HOST = "127.0.0.1"


def make_celery(app):
    """
        celery = make_celery(flask_app)
    """
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


celery = make_celery(app)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls reverse_messages every 10 seconds.
    sender.add_periodic_task(10.0, reverse_messages, name='reverse every 10')

    # Calls log('Logging Stuff') every 30 seconds
    sender.add_periodic_task(30.0, log.s(('Logging Stuff')), name='Log every 30')

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        log.s('Monday morning log!'),
    )


@celery.task(name="tasks.add")
def add(x, y):
    return x + y


@app.route("/test")
def hello_world(x=16, y=16):
    x = int(request.args.get("x", x))
    y = int(request.args.get("y", y))
    res = add.apply_async((x, y))
    context = {"id": res.task_id, "x": x, "y": y}
    result = "add((x){}, (y){})".format(context['x'], context['y'])
    goto = "{}".format(context['id'])
    return jsonify(result=result, goto=goto)


@app.route("/test/result/<task_id>")
def show_result(task_id):
    retval = add.AsyncResult(task_id).get(timeout=1.0)
    return repr(retval)


if __name__ == "__main__":
    print("\n", f"http://{HOST}:{PORT}/test", "\n")
    app.run(host=HOST, port=PORT, debug=True)
