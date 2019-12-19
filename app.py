from celery import Celery

celery = Celery('hello', broker='amqp://guest@localhost//')


@celery.task
def hello():
    return 'hello world'
