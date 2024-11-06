#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: gmh
# @Desc: { 中间件模块 }
# @Date: 2024/09/05 8:18
import logging
import re

from django.db import DatabaseError
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.middleware.common import MiddlewareMixin


from django01.utils.enums.enums import StatusCodeEnum
from django01.utils.exception.exceptions import BusinessException
from django01.utils.enums.result import R
from django.conf import settings

logger = logging.getLogger(settings.LOGGER_NAME)


class ExceptionMiddleware(MiddlewareMixin):
    """统一异常处理中间件"""

    def process_request(self, request):

        if settings.NEED_LOGIN:
            if request.user.is_authenticated:
                # 每次请求都重新刷新登录时长
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)

            else:  # 没登录场景
                # | 分隔要匹配的多个url，从左到右匹配，有匹配就返回匹配值，否则返回None。
                pattern = r'^(/api/auth/login|/api/auth/logout|/api/auth/register)'

                # 如果 request.path 的开始位置能够找到这个正则样式的任意个匹配，就返回一个相应的匹配对象。
                # 如果不匹配，就返回None
                match = re.search(pattern, request.path)
                if not match:  # 如果不是url白名单，需要拦截处理
                    # 主页未登录
                    if request.path == '/':
                        return HttpResponseRedirect('/api/auth/login')
                    # ajax请求未登录
                    else:
                        return JsonResponse({'status': False, 'info': '用户未登录!'})

    def process_response(self, request, response):
        """返回结果统一处理，转成json返回中间件"""
        logger.info("response data: {}".format(response))
        if type(response) is dict:
            r = R.ok().data(obj=response)
            return JsonResponse(r)
        else:
            return response

    def process_exception(self, request, exception):
        """
        统一异常处理,先处理异常，在处理response
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
