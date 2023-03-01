# 基于哪个镜像
FROM ubuntu:20.04

# 维护者信息
MAINTAINER kizai<kizai@foxmail.com>
# 设置工作空间，后续命令会在此目录下执行
WORKDIR /app
# 添加文件到容器中
ADD . /app/
# 安装运行环境
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip install flask==2.1.2 
RUN pip install flask_json==0.3.4
RUN pip install requests

VOLUME ["/app"]

# 开放6656端口
EXPOSE 6656

CMD echo "----end----"

# 配置容器启动后执行的命令
ENTRYPOINT ["python3"]

CMD ["app/lemumsg_api.py"]
