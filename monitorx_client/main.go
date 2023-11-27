package main

import (
	"flag"
	"fmt"
	"net/http"
	"opsx/monitorx_client/funcs"
	"opsx/monitorx_client/g"
	"time"

	"github.com/sirupsen/logrus"
)

func main() {
	cfg := flag.String("c", "cfg.json", "config file")
	flag.Parse()
	g.ParseConfig(*cfg)
	g.Init()

	go func() {
		for {
			funcs.StartBaseNode()
			time.Sleep(time.Minute * 1)
		}
	}()

	route := funcs.Route()
	addr := fmt.Sprintf("0.0.0.0:%d", g.Config().ListenPort)
	err := http.ListenAndServe(addr, route)
	if err != nil {
		logrus.Errorf("oma monitor start faild: %s", err)
	}
	logrus.Infof("oma monitor start with: %d", addr)

	select {}
}
