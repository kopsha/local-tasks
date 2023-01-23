#!/usr/bin/env python3
from celery import Celery
from time import sleep
from random import random


app = Celery("inspector", broker="pyamqp://guest:guest@amqp//")


@app.task
def fake_add(x, y):
    fake_it = random()
    print(f"faking {x} + {y} for {fake_it:.3f}")
    sleep(fake_it)
    print("finished, result:", x + y)
    return x + y


if __name__ == "__main__":
    print("attempt to execute main worker app")
