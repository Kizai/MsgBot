# 钉钉消息机器人构建成docker镜像的操作步骤

### 1. 创建存放API服务代码的文件夹
```powershell
# 创建存放dockerfile文件夹
$ mkdir -p Ding_Msg_Bot

# 创建appw文件夹存放api服务代码
$ cd Ding_Msg_Bot
```
### 2. 编写dockefile文件
```dockerfile
$ vim Dockerfile
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

CMD ["app/main.py"]

```
### 3. 存放主代码和配置文件到`app`目录下
```powershell
$ mkdir -p app && cd app
# 拷贝api服务代码到app文件夹下
$ ls
config.json main.py
# 请修改配置文件中ws下钉钉机器人的wedhook和secret改成你个人的
```
### 4. 构建镜像
```powershell
$ docker build -f Dockerfile -t dingmsgbot:1.0 .
```

### 5. 运行镜像测试
```powershell
$ docker run -it -d -p 6656:6656 --restart always --name dingmsgbot-api dingmsgbot:1.0

$ docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED         STATUS         PORTS                                       NAMES
01ea3396e757   866af2b13613   "python3 app/main.py"   4 seconds ago   Up 3 seconds                    0.0.0.0:6656->6656/tcp, :::6656->6656/tcp   dingmsgbot-api
```
### 使用Postman测试API服务是否开启
经过测试，API接口服务是正常运行的。

![](https://s2.loli.net/2022/06/19/mr5vUiSNnyfDpQl.png)

### 上传自定义镜像到DockerHub
* 注册账号

访问: https://hub.docker.com/ 注册账号

* 登录帐号
```powershell
docker login -u username
```
* Tag镜像
```powershell
# 新建一个tag，名字必须跟注册账号一样
docker tag dingmsgbot:0.1 username/dingmsgbot:0.1
```
* 推送镜像到DockerHub
```powershell
docker push username/dingmsgbot:0.1
```
* 拉取镜像
```powershell
docker pull username/dingmsgbot:0.1
```
* 部署镜像测试
```powershell
docker run -it -d -p --restart always --name dingmsgbot-api 6656:6656 username/dingmsgbot:0.1
```
