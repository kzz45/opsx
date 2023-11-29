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

# 启动后端
python3 manage.py runserver 0.0.0.0:8000

# 下面的操作需要在前端配置好之后再运行，另外下面的脚本需要跑在 crontab 中

# 生成实例任务
cd monitorx_backend/crontab
python3 instance_task.py

# 生成监控任务
cd monitorx_backend/crontab
python3 prometheus_task.py

# 同步当前告警
cd monitorx_backend/crontab
python3 current_alert.py

# 创建 admin 后台管理(非必要)
python3 manage.py createsuperuser
```

## 前端 (monitorx_frontend)

```sh
cd monitorx_frontend
rm -rf node_modules

npm cache clean --force
npm install -D

# 启动前端 运行开发环境
npm run dev

# 构建正式
npm run build:prod
```

## 代理端 (monitorx_proxy)

```sh
cd monitorx_proxy

# 启动代理端
go run main.go

# 构建正式
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o monitor_proxy
```

## 客户端 (monitorx_client)

```sh
cd monitorx_client

# 由于我 Mac 环境下 node_exporter 启动不了 暂时用 docker 方式启动一个 node_exporter
docker run -d -p 9100:9100 --name node_exporter bitnami/node-exporter

# 启动客户端
go run main.go

# 构建正式
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o monitor_client
```

## Grafana

```sh
# Mac 直接安装启动
brew install grafana
brew services start grafana

# docker 方式
docker run -d -p 3000:3000 --name=grafana grafana/grafana-enterprise

# 默认用户名密码: admin/admin
http://127.0.0.1:3000
```
