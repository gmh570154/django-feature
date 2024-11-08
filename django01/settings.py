"""
Django settings for django01 project.

Generated by 'django-admin startproject' using Django 4.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
import os
from pathlib import Path

try:
    from .config.config import CONF
except ImportError:
    pass

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-js(+51#2_=7o+abk*oim887gk=_trd&yo$9z48wu@--0(+*fel'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# DEBUG = False    #关闭debug模式 这时为生产模式，在将项目部署到服务器时也需要关闭，debug模式会暴露站点的多种信息
# ALLOWED_HOSTS = ['*']  # * 为所有都可访问，部署服务器时需修改

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01.apps.App01Config',
    'django_celery_beat',
    'django_celery_results',
    'rest_framework_simplejwt'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django01.middleware.log_middleware.RequestIDMiddleware',
    'django01.middleware.exception_middleware.ExceptionMiddleware'
]

ROOT_URLCONF = 'django01.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 修改静态文件路径
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django01.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 默认
        'NAME': 'django',  # 连接的数据库
        'HOST': CONF.mysql.host,  # mysql的ip地址
        'PORT': CONF.mysql.port,  # mysql的端口
        'USER': 'root',  # mysql的用户名
        'PASSWORD': 'pass4Zentao'  # mysql的密码
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 日志配置
LOGGING = {
    'version': 1,  # 固定值，现在只有这一个版本
    'disable_existing_loggers': False,  # 设置已存在的logger不失效
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        "default": {
            "format": '%(asctime)s %(name)s  %(pathname)s:%(lineno)d %(module)s:%(funcName)s '
                      '%(levelname)s- %(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "trace": {
            'format': '%(levelname)s [%(asctime)s] [%(request_id)s] : %(message)s',
            # "format": '%(asctime)s %(name)s  %(pathname)s:%(lineno)d %(module)s:%(funcName)s '
            #           '%(levelname)s- %(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'request_id': {
            # 自定义的filter
            '()': 'django01.middleware.log_middleware.RequestIDFilter'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'when': "D",
            'interval': 1,
            # 'formatter': 'default'
            'formatter': 'trace',
            'filters': ['request_id'],
        },
        "request": {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/request.log'),
            'formatter': 'default'
        },
        "server": {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/server.log'),
            'formatter': 'default'
        },
        "root": {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/root.log'),
            'formatter': 'default'
        },

        "db_backends": {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/db_backends.log'),
            'formatter': 'default'
        },
        "autoreload": {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/autoreload.log'),
            'formatter': 'default'
        },
        "default": {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug1.log'),
            'maxBytes': 1024 * 1024 * 50,  # 日志大小50M
            'backupCount': 5,
            'formatter': 'default',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        # 应用中自定义日志记录器
        'mylogger': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': True,
        },
        "django": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            'propagate': False,   # 是否传播到django根记录器
        },
        "django.request": {
            "level": "DEBUG",
            "handlers": ["request"],
            'propagate': False,
        },
        "django.server": {
            "level": "DEBUG",
            "handlers": ["server"],
            'propagate': False,
        },
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": ["db_backends"],
            'propagate': False,
        },
        "django.utils.autoreload": {
            "level": "INFO",
            "handlers": ["autoreload"],
            'propagate': False,
        }
    },
    'root': {
        "level": "DEBUG",
        "handlers": ["root"],
    }
}

MY_HOST = CONF.DEFAULT.host
MY_PORT = CONF.DEFAULT.port

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://" + CONF.redis.host + ":" + str(CONF.redis.port) + "/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

LOGGER_NAME = "mylogger"
# 是否需要登录验证
NEED_LOGIN = False

# # session数据的序列化类
# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# 存储session数据默认使用的模块
SESSION_CACHE_ALIAS = 'default'

# # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串（默认）
# SESSION_COOKIE_NAME = 'sessionid'
# # Session的cookie保存的域名（默认）
# SESSION_COOKIE_DOMAIN = None
# # 是否Https传输cookie（默认）
# SESSION_COOKIE_SECURE = False
# SESSION_COOKIE_SECURE = False
# # Session的cookie保存的路径（默认）
# SESSION_COOKIE_PATH = '/'
# # 是否每次请求都保存Session，默认修改之后才保存（默认）
# SESSION_SAVE_EVERY_REQUEST = False
# # 是否关闭浏览器使得Session过期（默认）
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# 设置session失效时间,单位为秒
SESSION_COOKIE_AGE = 60*5
# 是否Session的cookie只支持http传输（默认）-- 配置管用
SESSION_COOKIE_HTTPONLY = True


CELERY_ENABLE_UTC = False
# 不使用国际标准时间
CELERY_TIMEZONE = 'Asia/Shanghai'
# 使用亚洲/上海时区
DJANGO_CELERY_BEAT_TZ_AWARE = False
# 解决时区问题
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
# 使用0号数据库

CELERY_BROKER_TRANSPORT = 'redis'
# 使用redis作为中间件
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# 自定义调度类，使用Django的ORM
# 任务结果，使用Django的ORM
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
# 使用mysql数据库保存结果
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
# 设置任务接收的序列化类型
CELERY_TASK_SERIALIZER = 'json'
# 设置任务序列化方式
CELERY_RESULT_SERIALIZER = 'json'
# 设置结果序列化方式

# CELERY_TASK_TIME_LIMIT = 30 * 60
# # 任务超时时间限制
# 为存储结果设置过期日期，默认1天过期。如果beat开启，Celery每天会自动清除，0表示永不清理
# 这里可以设置成0，然后自己创建清理结果的机制，比较好控制,优先级比config大
CELERY_RESULT_EXPIRES = 0

# 定时任务
CELERY_BEAT_SCHEDULE = {
    'mul_every_10_seconds': {
        # 任务路径
        'task': 'app01.rest_api.tasks.plan_task_2',
        # 每10s执行一次
        'schedule': timedelta(seconds=10),
    }
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': timedelta(seconds=300),  # Token有效期
}
