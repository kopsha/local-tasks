#!/usr/bin/env python3
from os import environ
from flask import Flask, jsonify, request
from rq import Queue
from rq.job import Job

from worker import use_redis
from tasks import fake_work


app = Flask(__name__)
taskq = Queue(connection=use_redis)


@app.route("/")
def all_jobs():
    jobs = dict(
        pending=dict(),
        current=dict(),
        finished=dict(),
        failed=dict(),
    )
    for job in taskq.jobs:
        jobs["pending"][job.id] = job.args[0]

    for job_id in taskq.started_job_registry.get_job_ids():
        job = Job.fetch(job_id, connection=use_redis)
        jobs["current"][job_id] = job.args[0]

    for job_id in taskq.finished_job_registry.get_job_ids():
        job = Job.fetch(job_id, connection=use_redis)
        jobs["finished"][job_id] = job.args[0]

    for job_id in taskq.failed_job_registry.get_job_ids():
        job = Job.fetch(job_id, connection=use_redis)
        jobs["failed"][job_id] = job.args[0]

    return jsonify(jobs)


@app.route("/fakey")
def fakey():
    url = request.args.get("url")
    print("starting", url, flush=True)
    result = taskq.enqueue(fake_work, url)
    return jsonify(dict(url=url, description=result.description))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=environ.get("PORT"), debug=True)
