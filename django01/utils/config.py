# coding:utf-8
from oslo_config import cfg
# -*- coding: utf-8 -*-
# @Author: gmh
# @Desc: { 配置文件模块，读取配置文件内容 }
# @Date: 2024/09/05 8:18

# 配置组
rabbit_group = cfg.OptGroup(
    name='DEFAULT',
    title='DEFAULT options'
)

# 配置组中的多配置项模式
rabbit_Opts = [
    cfg.StrOpt('host',
               default='localhost',
               help='IP/hostname to listen on.'),
    cfg.IntOpt('port',
               default=5672,
               help='Port number to listen on.')
]

# 配置组
mysql_group = cfg.OptGroup(
    name='mysql',
    title='mysql options'
)

# 配置组中的多配置项模式
mysql_Opts = [
    cfg.StrOpt('host',
               default='localhost',
               help='mysql IP/hostname to connect.'),
    cfg.IntOpt('port',
               default=3306,
               help='Port number to connect.')
]

# 配置组
redis_group = cfg.OptGroup(
    name='redis',
    title='redis options'
)

# 配置组中的多配置项模式
redis_Opts = [
    cfg.StrOpt('host',
               default='localhost',
               help='redis IP/hostname to connect.'),
    cfg.IntOpt('port',
               default=6379,
               help='Port number to connect.')
]

# 创建对象CONF，用来充当容器
CONF = cfg.CONF

# 配置组必须在其组件被注册前注册！
CONF.register_group(rabbit_group)

# 注册配置组中含有多个配置项的模式，必须指明配置组
CONF.register_opts(rabbit_Opts, rabbit_group)


# 配置组必须在其组件被注册前注册！
CONF.register_group(mysql_group)

# 注册配置组中含有多个配置项的模式，必须指明配置组
CONF.register_opts(mysql_Opts, mysql_group)

# 配置组必须在其组件被注册前注册！
CONF.register_group(redis_group)

# 注册配置组中含有多个配置项的模式，必须指明配置组
CONF.register_opts(redis_Opts, redis_group)

# CONF(default_config_files=['local_settings.conf'])
CONF(['--config-file', 'django01/local/local_settings.conf'])
