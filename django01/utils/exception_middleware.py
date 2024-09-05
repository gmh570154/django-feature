#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: gmh
# @Desc: { 中间件模块 }
# @Date: 2024/09/05 8:18
import logging

from django.db import DatabaseError
from django.http.response import JsonResponse
from django.http import HttpResponseServerError
from django.middleware.common import MiddlewareMixin


from django01.utils.enums import StatusCodeEnum
from django01.utils.exceptions import BusinessException
from django01.utils.result import R
from django.conf import settings

logger = logging.getLogger(settings.LOGGER_NAME)


class ExceptionMiddleware(MiddlewareMixin):
    """统一异常处理中间件"""

    def process_response(self, request, response):
        logger.info("response data: {}".format(response))
        if type(response) is dict:
            r = R.ok().data(obj=response)
            return JsonResponse(r)
        else:
            raise BusinessException(StatusCodeEnum.SERVER_ERR)

    def process_exception(self, request, exception):
        """
        统一异常处理
        :param request: 请求对象
        :param exception: 异常对象
        :return:
        """
        if isinstance(exception, BusinessException):
            # 业务异常处理
            data = R.set_result(exception.enum_cls).data()
            return JsonResponse(data)

        elif isinstance(exception, DatabaseError):
            # 数据库异常
            r = R.set_result(StatusCodeEnum.DB_ERR)
            logger.error(r.data(), exc_info=True)
            return HttpResponseServerError(StatusCodeEnum.SERVER_ERR.errmsg)

        elif isinstance(exception, Exception):
            # 服务器异常处理
            r = R.server_error()
            logger.error(r.data(), exc_info=True)
            return HttpResponseServerError(r.errmsg)
        return None
