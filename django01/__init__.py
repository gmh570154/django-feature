import pymysql

from django01.celeryconfig import app as celery_app

__all__ = ('celery_app',)

pymysql.install_as_MySQLdb()  # 替换默认的引擎
