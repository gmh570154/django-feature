import logging
import time

from django.conf import settings

logger = logging.getLogger(settings.LOGGER_NAME)

'''函数执行时间统计，装饰器功能'''


def exec_time_util(func):
    def inner(*args, **kw):
        start = time.time()
        data = func(*args, **kw)
        logger.info("function exec time: {:.6f}s".format(time.time() - start))
        return data

    return inner
