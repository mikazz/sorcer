import os
import random
import time

from flask import Flask
from celery import Celery

# Flask configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'
HOST = "127.0.0.1"
PORT = 5000

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


if __name__ == '__main__':
    print("\n", f"http://{HOST}:{PORT}", "\n")
    app.run(host=HOST, port=PORT, debug=True)
