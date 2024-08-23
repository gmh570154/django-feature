# 基础镜像
FROM python:3.9-alpine as base
 
# 将 pip 源设置为国内的源
COPY pip.conf /root/.pip/pip.conf

# 在容器中创建项目目录
RUN mkdir /code

# 设置工作目录
WORKDIR /code
 
# 将当前目录下的所有文件复制到容器中的 /code 目录
COPY . /code/
 
# 安装项目依赖
RUN pip install -r requirements.txt

# # 在新镜像中创建数据卷，防止代码数据丢失
# VOLUME /code

# 运行 Django 的 migrate 命令
RUN python manage.py migrate

# 暴露端口
EXPOSE 8000

# 设置 CMD 指令，以便在容器中运行 Django 服务器
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]