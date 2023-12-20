package main

import (
	"context"
	"crypto/tls"
	"flag"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"

	"k8s.io/klog/v2"
)

func main() {
	var params WhsParams

	flag.IntVar(&params.port, "port", 443, "")
	flag.StringVar(&params.certFile, "tlsCertFile", "", "")
	flag.StringVar(&params.keyFile, "tlsKeyFile", "", "")
	flag.Parse()

	cert, err := tls.LoadX509KeyPair(params.certFile, params.keyFile)
	if err != nil {
		klog.Errorf("falild to load key pair: %v", err)
	}

	whs := &Whs{
		server: &http.Server{
			Addr:      fmt.Sprintf(":%v", params.port),
			TLSConfig: &tls.Config{Certificates: []tls.Certificate{cert}},
		},
	}

	mux := http.NewServeMux()
	mux.HandleFunc("/mutate", whs.serve)
	mux.HandleFunc("/validate", whs.serve)
	whs.server.Handler = mux

	go func() {
		if err := whs.server.ListenAndServeTLS("", ""); err != nil {
			klog.Errorf("failed to listen and serve webhook: %v", err)
		}
	}()

	klog.Info("server start")

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
	<-sig

	klog.Infof("shutdown webhook server gracefully")
	whs.server.Shutdown(context.Background())
}
