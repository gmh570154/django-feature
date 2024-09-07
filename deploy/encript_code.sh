# pyarmor gen -O dist .  # 普通加密
# pyarmor gen --enable jit --obf-code 1 --private dist .  # 参数多点
pyarmor gen -O dist --enable jit --obf-code 1   -b '172.30.42.44' .   # 绑定到设备信息，网卡/mac，ip地址等
# pyarmor gen --enable jit --obf-code 0 dist .
# pyarmor gen --enable jit --obf-code 1 dist .
cp -r logs templates dist/
cp django01/local/local_settings.conf dist/django01/local 