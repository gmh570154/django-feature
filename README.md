## 基本命令
1.创建项目不能在包含中文的目录下：django-admin startproject mysite
2.创建app： python manage.py startapp cltest
3.数据库迁移：python manage.py migrate
4.创建管理员账号：python manage.py createsuperuser

## 创建虚拟环境Creating Virtual Environments,在终端创建的步骤如下
python3 -m venv tutorial-env   创建虚拟环境
source tutorial-env/bin/activate   进入虚拟环境
deactivate   退出虚拟环境

python manage.py migrate
python manage.py runserver

# 使用daphne 部署django
pip install daphne

daphne django01.asgi:application

daphne django01.asgi:application -p 8000 -b 192.168.1.225

# 使用uvicorn部署djanog
pip install uvicorn
uvicorn django01.asgi:application --port 8000 --host 192.168.1.225

# nginx配置
~~~
upstream backend {
    server 192.168.1.225:8000;
    # There could be more than a backend here
}

server {
    listen       80;
    listen  [::]:80;
    server_name  localhost;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    location /admin {
	   proxy_pass http://backend;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
    }
}
~~~

# 添加glb-request-id的方式

request_id用一个小算法自动生成。如果请求头有 X-Request-ID，就用请求头的，这样一个请求涉及多个服务调用的时候可以把request_id带过去，标识为同一个请求的request_id.

1、在请求一开始打印请求基础信息(如 request path、get params)
2、打印日志时将 request id 带上，方便追踪请求

## 1. 定义 Middleware 和 Logging Filter
注：本示例文件路径为 dataStatistics.log_middleware.py
~~~
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import threading

from django.utils.deprecation import MiddlewareMixin

local = threading.local()
logger = logging.getLogger('mylogger')

class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = getattr(local, 'request_id', "none")
        return True


def get_current_time(format=None):
    from datetime import datetime
    dt = datetime.now()
    if format:
        result = dt.strftime(format)
    else:
        result = dt.strftime("%Y/%m/%d %H:%M:%S")
    return result


def base_n(num, b):
    return ((num == 0) and "0") or \
           (base_n(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])


def generate_sid():
    sid = get_current_time("%H%M%S%f")
    sid = int(sid)
    # 将 10 进制转为 32 进制
    sid = base_n(sid, 32)
    # 反转
    return "{}".format(sid)[::-1]


class RequestIDMiddleware(MiddlewareMixin):
    def process_request(self, request):
        local.request_id = request.META.get('HTTP_X_REQUEST_ID', generate_sid())
        request.request_id = local.request_id  # 没有glb-req-id需要添加
        logger.info("+++++ request_begin: [{}] [{}] {}".format(request.path, request.method, list(request.GET.items())))

    def process_response(self, request, response):
        logger.info("----- request_end: [{}]".format(request.path))
        if hasattr(request, 'request_id'):
            response['X-Request-ID'] = local.request_id
        try:
            del local.request_id
        except AttributeError:
            pass
        return response
~~~
## 2. 在 settings.py 中注册 自定义的 Middleware 并 使用 filter
MIDDLEWARE配置示例：
~~~
MIDDLEWARE = [
    'dataStatistics.log_middleware.RequestIDMiddleware'
]

LOGGING配置示例：

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'track': {
            'format': '%(levelname)s [%(asctime)s] [%(request_id)s] : %(message)s'  # 这里使用filter request_id里的request_id字段
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'request_id': {
            # 自定义的filter
            '()': 'dataStatistics.log_middleware.RequestIDFilter'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'track'
        },
        'tracer': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            # 对应 formatters 中 的 track
            'formatter': 'track'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'tracer': {
            # 对应 handlers 中的 tracer
            'handlers': ['tracer'],
            # change debug level as appropiate
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
~~~

## 3. 在代码中使用
~~~
首先拿到配置的 logger 对象：
logger 其实都是 settings.py 中 loggers 所定义的
logger = logging.getLogger('tracer')
然后使用时直接调用即可，如：
logger.debug("my debug demo")
logger.info("my info demo")
~~~
效果如下：
~~~
INFO [2019-11-01 16:28:12,744] [pfja6kn4] : +++++ request_begin: [/warehouse/demo/] [GET] [('parm1', 'value1'), ('parm2', 'value2')]
DEBUG [2019-11-01 16:28:12,746] [pfja6kn4] : my debug demo
INFO [2019-11-01 16:28:12,746] [pfja6kn4] : my info demo
INFO [2019-11-01 16:28:12,750] [pfja6kn4] : ----- request_end: [/warehouse/demo/]
~~~

## 增加配置文件
~~~
安装依赖
pip install oslo_config
~~~
* 增加local_setting.conf
* config.py解析conf文件
* settings.py引入全局配置

## 增加dockerfile文件和pip.conf文件使用docker进行部署
构建镜像并启动：
docker-compse up -d 

需要修改配置文件，对接mysql和redis服务：
./django01/local/local_settings.conf

tip：重新编译需要把镜像删除掉