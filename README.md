# opsx

## mysql/redis/node_exporter on docker

```sh
# MySQL
docker run -d -p 3306:3306 --name mysql_local -e MYSQL_ROOT_PASSWORD=root mysql:latest

# Redis
docker run -d -p 6379:6379 --name redis_local redis:latest --requirepass 'root'

# 创建数据库 opsx
mysql -uroot -proot -h127.0.0.1 -e "create database opsx character set utf8 collate utf8_general_ci;"

# 启动一个本地的 node_exporter
docker run -d -p 9100:9100 --name node_exporter bitnami/node-exporter
```

## 后端 (monitorx_backend)

```sh
python3 -m venv venv
source venv/bin/activate
cd monitorx_backend
pip install -r requirements.txt

# 迁移数据库
python3 manage.py migrate
python3 manage.py makemigrations dops
python3 manage.py makemigrations dcmdb
python3 manage.py makemigrations dmonitor
python3 manage.py migrate

# 创建一个 admin 管理用户 用来前端登录
python3 manage.py createsuperuser

# 启动后端
python3 manage.py runserver 0.0.0.0:8000

# 启动正式环境的话 使用 gunicorn

# 下面的操作需要在前端配置好之后再运行，另外下面的脚本需要跑在 crontab 中
# 本地实践的话直接运行就好

# 生成实例任务
cd monitorx_backend/crontab
python3 instance_task.py

# 生成监控任务
cd monitorx_backend/crontab
python3 prometheus_task.py

# 同步当前告警
cd monitorx_backend/crontab
python3 current_alert.py
```

## 前端 (monitorx_frontend)

```sh
cd monitorx_frontend
rm -rf node_modules

npm cache clean --force
npm install -D

# 启动前端 运行本地开发环境
npm run dev

# 构建正式
npm run build:prod
```

## 代理端 (monitorx_proxy)

```sh
# bin 目录下的二进制文件需要下载 https://prometheus.io/download/

# 代理端需要下载 prometheus/promtool/alertmanager/amtool
cd monitorx_proxy

# 启动代理端
go run main.go

# 构建正式
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o monitor_proxy
```

## 客户端 (monitorx_client)

```sh
# bin 目录下的二进制文件需要下载 https://prometheus.io/download/

# 客户端需要下载 node_exporter
# 但是我们本地实践的话，直接用 docker 来启动一个好了 bin 目录下就不需要下载 node_exporter 了
cd monitorx_client

# 由于我 Mac 环境下 node_exporter 启动不了 暂时用 docker 方式启动一个 node_exporter
docker run -d -p 9100:9100 --name node_exporter bitnami/node-exporter

# 启动客户端
go run main.go

# 构建正式
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o monitor_client
```

## [前端配置操作步骤](./docs/README.md)
