"""
RabbitMQ :  amqp://localhost
            amqp://test:test@localhost:5672/test

Redis:      redis://localhost
            redis://localhost:6379/0

Run Celery
celery -A tasks worker --loglevel=info
"""

from urllib.request import urlopen
from celery import Celery

celery = Celery('demo',
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)


@celery.task
def fetch(url):
    print(f'GET: {url}')
    return urlopen(url).read()


@celery.task(rate_limit='1/s')
def fetch_rate(url):
    """
        Can use /h /m
    """
    print(f'GET: {url}')
    return urlopen(url).read()


if __name__ == '__main__':
    result = fetch.delay("http://python.org/")
    print(type(result), result)
    #print(result.get())
