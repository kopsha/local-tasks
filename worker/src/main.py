#!/usr/bin/env python3
from flask import Flask
from tasks import fake_add
from threading import Thread


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h3>Hello, World!</h3>"


def xxx(name):
    print("started", name)
    fake_add.delay(10, 100)


@app.route("/fakey")
def fakey():
    print("wtf")
    ntz = Thread(target=xxx, args=(1,))
    ntz.start()
    # no need to wait for completion
    print(f"<pre>Started {ntz.native_id}</pre>")
    return f"<pre>Started {ntz.native_id}</pre>"
