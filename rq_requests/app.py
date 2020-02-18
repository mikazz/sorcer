from redis import Redis
from rq import Queue, Connection, Worker
import requests


def enqueue_urls(urls=[]):
    if len(urls) == 0: # load from file
        with open('urls.txt', 'r') as file:
            for url in file:
                urls.append(url.strip())
    with Connection():
        q = Queue('test')
        for url in urls:
            q.enqueue(count_words_at_url, url)


def count_words_at_url(url):
    resp = requests.get(url, timeout=3)
    return len(resp.text.split())

def custom_worker():
    # using requests before forking
    print count_words_at_url('http://python-rq.org/') # causes the problem

    with Connection():
        q = Queue('test')
        w = Worker([q])
        w.work()

