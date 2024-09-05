import json
import logging

from django.http import HttpResponse
from django.conf import settings

from django01.utils.enums import StatusCodeEnum
from django01.utils.exceptions import BusinessException

logger = logging.getLogger(settings.LOGGER_NAME)


def json_util(func):
    def inner(*args, **kw):
        logger.info("request data: {},{}".format(str(*args), str(**kw)))
        data = func(*args, **kw)
        logger.info("response data: {}".format(data))
        if type(data) is dict:
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            raise BusinessException(StatusCodeEnum.SERVER_ERR)

    return inner
