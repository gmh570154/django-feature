import logging

from django.http import JsonResponse
from django.conf import settings

from django01.utils.result import R
from django01.utils.enums import StatusCodeEnum
from django01.utils.exceptions import BusinessException

logger = logging.getLogger(settings.LOGGER_NAME)


def json_util(func):
    def inner(*args, **kw):
        logger.info("request data: {},{}".format(str(*args), str(**kw)))
        data = func(*args, **kw)
        logger.info("response data: {}".format(data))
        if type(data) is dict:
            r = R.ok().data(obj=data)
            return JsonResponse(r)
        else:
            raise BusinessException(StatusCodeEnum.SERVER_ERR)

    return inner
