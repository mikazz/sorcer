"""
    example.py

    Run these two commands in separate terminals:

    celery -A example.celery worker
    python example.py

    curl -X GET -H "Content-Type: application/json" localhost:5000
"""

from flask import Flask
from flask_celery import Celery

app = Flask('example')
app.config['CELERY_BROKER_URL'] = 'redis://localhost'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost'
celery = Celery(app)


@celery.task()
def add_together(a, b):
    return a + b


if __name__ == '__main__':
    result = add_together.delay(23, 42)
    print(result.get())
