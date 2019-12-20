from celery import Celery

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@celery.task
def add(x, y):
    return x + y


@celery.task
def hello():
    return 'hello world'
