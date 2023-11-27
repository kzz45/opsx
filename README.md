# opsx

## mysql/redis on docker

```sh
# MySQL
docker run -d -p 3306:3306 --name mysql_local -e MYSQL_ROOT_PASSWORD=root mysql:latest

# Redis
docker run -d -p 6379:6379 --name redis_local redis:latest --requirepass 'root'

# 创建数据库 opsx
mysql -uroot -proot -h127.0.0.1 -e "create database opsx character set utf8 collate utf8_general_ci;"
```

## monitorx 后端

```sh
# 迁移数据库
python3 manage.py migrate
python3 manage.py makemigrations public
python3 manage.py makemigrations monitor
python3 manage.py migrate

# 运行
python3 manage.py runserver 0.0.0.0:8080

# 创建 admin 后台管理(非必要)
python3 manage.py createsuperuser
```

## monitorx_frontend 前端

```sh
cd monitorx_frontend

npm cache clean --force
npm install -D

# 运行开发环境
npm run dev

# 构建正式
npm run build:prod
```

## monitorx_proxy 代理端

```sh
cd monitorx_proxy

CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o monitor_proxy

# 运行
go run .
```

## monitorx_client 客户端

```sh
cd monitorx_client

CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o monitor_client

# 运行
go run .
```
