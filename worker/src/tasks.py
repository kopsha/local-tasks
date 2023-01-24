#!/usr/bin/env python3
import subprocess
from tempfile import TemporaryDirectory


def exec(cmd, cwd):
    completed = subprocess.run(cmd, shell=True, capture_output=True, cwd=cwd)
    completed.check_returncode()
    result = (
        completed.stdout.decode("utf-8").strip(),
        completed.stderr.decode("utf-8").strip(),
    )
    return result


def inspect_repo(url):
    with TemporaryDirectory() as area51:
        cmd = f"git clone {url} {area51}"
        out, err = exec(cmd, area51)
        print("finished", url)
