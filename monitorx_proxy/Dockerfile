FROM builder-cache as builder

LABEL maintainer="kzz45@qq.com"

ENV GO111MODULE=on
ENV GOPROXY=https://goproxy.cn,direct,https://proxy.golang.com.cn,direct

RUN apk update && apk upgrade

WORKDIR /data
COPY . .

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o monitor_proxy

FROM ubuntu:20.04

RUN apt autoremove && apt clean

WORKDIR /data
COPY cfg.json cfg.json
COPY bin bin
COPY --from=builder /data/monitor_proxy .

CMD ["/data/monitor_proxy"]
