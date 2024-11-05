import uuid

from django.conf import settings
from app01.rest_api.tasks import plan_task_2, xsum
from django01.core.base_view import BaseView
from django01.utils.time_util import exec_time_util
from celery import group
from django_celery_results.models import GroupResult

import logging
logger = logging.getLogger(settings.LOGGER_NAME)
# Create your views here.
# Function based view，使用装饰器功能处理返回json数据


@exec_time_util
def myView(request):
    data = {
        "name": "Vaibhav",
        "age": 20,
        "hobbies": ["Coding", "Art", "Gaming", "Cricket", "Piano"],
    }
    return data


# Class based view
class MyView(BaseView):
    def get(self, request):
        self.action = "get json"
        self.resource_id_name = "null"

        data = {
            "name": "Vaibhav",
            "age": 20,
            "hobbies": ["Coding", "Art", "Gaming", "Cricket", "Piano"],
        }
        for i in range(10):
            task_result = plan_task_2.delay()  # celery 异步后台执行

        res = group(xsum.s([i, i]) for i in range(10))()
        ts = GroupResult(group_id=uuid.uuid1().int, result="success")
        ts.save()  # 保存groupResult结果
        # print(res.get())  # 阻塞任务直接结束

        logger.info("id: %s, state: %s, ready: %s, successful: %s".format(
            task_result.id, task_result.state, task_result.ready(), task_result.successful))

        self.result = "success"
        self.save_operation_log(request)
        return data
