# coding:utf-8
from oslo_config import cfg
from oslo_config import types


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

# 创建对象CONF，用来充当容器
CONF = cfg.CONF

# 配置组必须在其组件被注册前注册！
CONF.register_group(rabbit_group)

# 注册配置组中含有多个配置项的模式，必须指明配置组
CONF.register_opts(rabbit_Opts, rabbit_group)

# CONF(default_config_files=['local_settings.conf'])
CONF(['--config-file', 'django01/local/local_settings.conf'])

print("rabbit.host: " + CONF.DEFAULT.host)
print("rabbit.port: " + str(CONF.DEFAULT.port))