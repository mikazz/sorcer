#!/usr/bin/python3

from sys import platform
import sys
import time
from rq import Connection

if platform == "linux" or platform == "linux2":
    from rq import Worker  # best worker (has fork)
elif platform == "darwin":
    raise NotImplemented("Unknown rq job queue Worker for OS X")
elif platform == "win32":
    from rq_win import WindowsWorker as Worker  # Windows Worker (limited)

from redis import Redis
import multiprocessing

redis = Redis(host='localhost')


def need_burst_workers():
    # check database or redis key to determine whether burst worker army is required
    return True


def num_burst_workers_needed():
    # check the number, maybe divide the number of pending tasks by n
    return 10  # int


def main(qs):
    with Connection(connection=redis):
        if need_burst_workers():
            for i in range(num_burst_workers_needed()):
                # Wrap work method call into multiprocessing
                multiprocessing.Process(target=Worker(qs).work(), kwargs={'burst': True}).start()
        else:
            time.sleep(10)


if __name__ == '__main__':
    qs = sys.argv[1:] or ['default']
    main(qs)
