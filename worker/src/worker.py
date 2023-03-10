#!/usr/bin/env python3
from os import environ
import redis
from rq import Worker, Queue, Connection


use_redis = redis.from_url(environ.get("REDIS_URL"))
use_queue = "inspector"


if __name__ == "__main__":
    with Connection(use_redis):
        worker = Worker(Queue(use_queue))
        worker.work()
