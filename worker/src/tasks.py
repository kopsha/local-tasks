#!/usr/bin/env python3
from time import sleep
from random import random


def fake_work(url):
    fake_it = random() * 10
    print(f"faking {url} for {fake_it:.3f} seconds")
    sleep(fake_it)
    print("finished", url)
