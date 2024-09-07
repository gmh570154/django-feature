# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import threading
from django.conf import settings

from django.utils.deprecation import MiddlewareMixin

local = threading.local()
logger = logging.getLogger(settings.LOGGER_NAME)


class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = getattr(local, 'request_id', "none")
        return True


def get_current_time(format=None):  # 需要优化，每次生成唯一的请求id

    from datetime import datetime
    dt = datetime.now()
    if format:
        result = dt.strftime(format)
    else:
        result = dt.strftime("%Y/%m/%d %H:%M:%S")
    return result


def base_n(num, b):
    return ((num == 0) and "0") or \
           (base_n(num // b, b).lstrip("0") +
            "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])


def generate_sid():
    sid = get_current_time("%H%M%S%f")
    sid = int(sid)
    # 将 10 进制转为 32 进制
    sid = base_n(sid, 32)
    # 反转
    return "{}".format(sid)[::-1]


class RequestIDMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # import pdb;pdb.set_trace()
        local.request_id = request.META.get(
            'HTTP_X_REQUEST_ID', generate_sid())
        request.request_id = local.request_id  # 没有glb-req-id需要添加
        logger.info("+++++ request_begin: [{}] [{}] {}".format(
            request.path, request.method, list(request.GET.items())))

    def process_response(self, request, response):
        logger.info("----- request_end: [{}]".format(request.path))
        # import pdb;pdb.set_trace()
        if hasattr(request, 'request_id'):
            response['X-Request-ID'] = local.request_id
        try:
            del local.request_id
        except AttributeError:
            pass
        return response
