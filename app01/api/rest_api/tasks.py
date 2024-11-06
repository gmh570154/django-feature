# coding=utf-8
# Create your tasks here
from __future__ import absolute_import, unicode_literals

from django01.celeryconfig import app
import time


@app.task
def plan_task_2():
    print("任务_2已运行！")
    return {"任务_2": "success"}


@app.task(expire=60)
def xsum(numbers):
    time.sleep(5)
    return sum(numbers)
