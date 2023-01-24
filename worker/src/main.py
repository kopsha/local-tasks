#!/usr/bin/env python3
from os import environ
from itertools import chain
from flask import Flask, request, make_response, url_for, redirect, jsonify
from rq import Queue
from rq.job import Job
import redis

from worker import use_queue
from tasks import inspect_repo

redis_client = redis.from_url(environ.get("REDIS_URL"))
app = Flask(__name__)
inspector_queue = Queue(name=use_queue, connection=redis_client)


def get_recent_jobs():
    jobs = [
        (job.args[0], job.get_status())
        for job_id in chain(
            inspector_queue.failed_job_registry.get_job_ids(),
            inspector_queue.finished_job_registry.get_job_ids(),
            inspector_queue.started_job_registry.get_job_ids(),
            inspector_queue.get_job_ids(),
        )
        if (job := Job.fetch(job_id, connection=redis_client))
    ]
    return jobs


@app.route("/recent")
def recent():
    return jsonify(get_recent_jobs())


@app.route("/cloney")
def cloney():
    url = request.args.get("url")
    if not url.startswith("https://"):
        return make_response("Please provide an https url to your git repository.", 400)

    recent = dict(get_recent_jobs())
    if url in recent:
        # the url was recently inspected
        return dict(url=url, status=recent[url])

    job = inspector_queue.enqueue(inspect_repo, url)

    return dict(url=url, status=job.get_status())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=environ.get("PORT"), debug=True)
