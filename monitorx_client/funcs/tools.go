package funcs

import (
	"bufio"
	"fmt"
	"net"
	"net/http"
	"opsx/monitorx_client/g"
	"os/exec"
	"strings"
	"syscall"
	"time"

	"github.com/sirupsen/logrus"
)

func local_addr() string {
	addrs, err := net.InterfaceAddrs()
	if err != nil {
		return fmt.Sprintf("%s", err)
	}

	for _, addr := range addrs {
		if ipnet, ok := addr.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
			if ipnet.IP.To4() != nil {
				if strings.HasPrefix(ipnet.IP.String(), "10") ||
					strings.HasPrefix(ipnet.IP.String(), "192") ||
					strings.HasPrefix(ipnet.IP.String(), "172") {
					return ipnet.IP.String()
				}
			}
		}
	}
	return ""
}

func check_port(port string) bool {
	localIP := local_addr()
	_, rerr := net.DialTimeout("tcp", localIP+":"+port, time.Duration(time.Second))
	_, lerr := net.DialTimeout("tcp", "127.0.0.1:"+port, time.Duration(time.Second))
	if lerr == nil || rerr == nil {
		return true
	}
	return false
}

func execute_with_fork(name string, args ...string) (int, error) {
	cmd := exec.Command(name, args...)
	cmd.SysProcAttr = &syscall.SysProcAttr{Setpgid: true}
	if err := cmd.Start(); err != nil {
		g.Logger.Errorf("fork sub process error: %s", err)
		return 0, err
	}
	go func() {
		cmd.Wait()
	}()
	return cmd.Process.Pid, nil
}

func parse_base_node(url string) string {
	var result string
	client := http.Client{
		Timeout: time.Duration(time.Second * time.Duration(g.Config().IntervalTime)),
	}
	resp, err := client.Get(url)
	if err != nil {
		logrus.Errorf("read url: %s error: %s", url, err)
		return result
	}
	defer resp.Body.Close()
	scaner := bufio.NewScanner(resp.Body)
	for scaner.Scan() {
		if !strings.Contains(scaner.Text(), "go_") && !strings.Contains(scaner.Text(), "http_") {
			if !strings.HasPrefix(scaner.Text(), "#") {
				result += scaner.Text() + "\n"
			}
		}
	}
	return result
}
