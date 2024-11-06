#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: gmh
# @Desc: { 中间件模块 }
# @Date: 2024/09/05 8:18

class CommonException(Exception):
    """公共异常类"""

    def __init__(self, enum_cls):
        self.code = enum_cls.code
        self.errmsg = enum_cls.errmsg
        self.enum_cls = enum_cls
        super().__init__()


class BusinessException(CommonException):
    """业务异常类"""
    pass


class APIException(CommonException):
    """接口异常类"""
    pass
