package main

import (
	"flag"
	"opsx/monitorx_proxy/funcs"
	"opsx/monitorx_proxy/g"
	"time"
)

func main() {

	cfg := flag.String("c", "cfg.json", "configuration file")
	flag.Parse()

	g.ParseConfig(*cfg)
	g.Init()

	go func() {
		for {
			funcs.RunPrometheus()
			time.Sleep(time.Minute)
		}
	}()

	go func() {
		for {
			funcs.RunAlertManager()
			time.Sleep(time.Minute)
		}
	}()

	go func() {
		for {
			funcs.RunSilence()
			time.Sleep(time.Minute)
		}
	}()

	go funcs.NoticeServer()

	select {}
}
