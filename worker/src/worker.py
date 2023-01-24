#!/usr/bin/env python3
from os import environ
import redis
from rq import Worker, Queue, Connection

listen = ("default",)
use_redis = redis.from_url(environ.get("REDIS_URL"))


if __name__ == "__main__":
    with Connection(use_redis):
        worker = Worker(map(Queue, listen))
        worker.work()
