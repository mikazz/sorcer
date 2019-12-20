"""
RabbitMQ :  amqp://localhost
Redis:      redis://localhost


Run Celery
celery -A tasks worker --loglevel=info

"""

from celery import Celery

# first argument to Celery is the name of the current module
celery = Celery('tasks', broker='amqp://guest@localhost//')


@celery.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@celery.task
def add(x, y):
    return x + y


@celery.task
def hello():
    return 'hello world'
