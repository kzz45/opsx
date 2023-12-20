package funcs

import (
	"bytes"
	"errors"
	"fmt"
	"io"
	"io/ioutil"
	"net"
	"net/http"
	"opsx/monitorx_proxy/g"
	"os"
	"os/exec"
	"syscall"
	"time"
)

type CmdResult struct {
	Name    string
	Content []byte
	Err     error
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

func execute_with_timeout(timeout time.Duration, name string, args ...string) (CmdResult, bool) {
	cmd := exec.Command(name, args...)
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		return CmdResult{Name: name, Err: err}, false
	}
	defer stdout.Close()
	if err := cmd.Start(); err != nil {
		return CmdResult{Name: name, Err: err}, false
	}

	done := make(chan CmdResult)
	go func() {
		var errJoin string
		content, stdOutErr := ioutil.ReadAll(stdout)
		if stdOutErr != nil {
			errJoin += stdOutErr.Error() + "\n"
		}
		if cmdWaitErr := cmd.Wait(); cmdWaitErr != nil {
			errJoin += cmdWaitErr.Error()
		}
		if errJoin != "" {
			err = errors.New(errJoin)
		}
		done <- CmdResult{Err: err, Content: content, Name: name}
		close(done)
	}()

	select {
	case <-time.After(timeout):
		errJoin := fmt.Sprintf("command name: %s with args: %v exec timeout, killed", name, args)
		if killErr := cmd.Process.Kill(); killErr != nil {
			errJoin += ", kill error: " + killErr.Error()
			return CmdResult{Err: errors.New(errJoin), Name: name}, true
		}
		if cmdResult := <-done; cmdResult.Err != nil {
			errJoin += ", wait command done error: " + cmdResult.Err.Error()
			return CmdResult{Err: errors.New(errJoin), Name: name}, true
		}
		return CmdResult{}, true
	case cmdResult := <-done:
		return cmdResult, true
	}
}

func check_conf_valid(bin_name string, filename string, role string) error {
	tool := fmt.Sprintf("%s/%s", g.BinDir, bin_name)
	args := make([]string, 0)
	if role == "prometheus" {
		args = append(args, "check", "config", filename)
	}
	if role == "alertmanager" {
		args = append(args, "check-config", filename)
	}
	result, ok := execute_with_timeout(time.Second*10, tool, args...)
	if !ok || result.Err != nil {
		return fmt.Errorf("run cmd %s with args %v error: %s", tool, args, result.Err)
	}
	g.Logger.Infof("run cmd %s with args %v success", tool, args)
	return nil
}

func start_prometheus(conf_file string) (int, error) {
	bin_tool := fmt.Sprintf("%s/prometheus", g.BinDir)
	args := make([]string, 0)
	store_data_args := fmt.Sprintf("--storage.tsdb.path=%s", g.PromDataDir)
	config_file_args := fmt.Sprintf("--config.file=%s", conf_file)
	web_listen_args := fmt.Sprintf("--web.listen-address=%s:%d", g.Config().Prometheus.Addr, g.Config().Prometheus.Port)
	args = append(args, store_data_args, config_file_args, web_listen_args, "--web.enable-lifecycle")
	pid, err := execute_with_fork(bin_tool, args...)
	if err != nil {
		g.Logger.Errorf("start prometheus error: %s", err)
		return 0, err
	}
	return pid, nil
}

func start_alertmanager(conf_file string) (int, error) {
	bin_tool := fmt.Sprintf("%s/alertmanager", g.BinDir)
	args := make([]string, 0)
	store_data_args := fmt.Sprintf("--storage.path=%s", g.AlertDataDir)
	config_file_args := fmt.Sprintf("--config.file=%s", conf_file)
	web_listen_args := fmt.Sprintf("--web.listen-address=%s:%d", g.Config().Alertmanager.Addr, g.Config().Alertmanager.Port)
	args = append(args, store_data_args, config_file_args, web_listen_args,
		"--data.retention=120h",
		"--alerts.gc-interval=30m")
	fmt.Println(args)
	pid, err := execute_with_fork(bin_tool, args...)
	if err != nil {
		g.Logger.Errorf("start alertmanager error: %s", err)
		return 0, err
	}
	return pid, nil
}

func reload(role string) error {
	var reload_url string
	if role == "prometheus" {
		reload_url = fmt.Sprintf("http://%s:%d%s", g.Config().Prometheus.Addr, g.Config().Prometheus.Port, g.PROMETHEUS_RELOAD)
	}
	if role == "alertmanager" {
		reload_url = fmt.Sprintf("http://%s:%d%s", g.Config().Alertmanager.Addr, g.Config().Alertmanager.Port, g.ALERTMANAGER_RELOAD)
	}
	client := http.Client{}
	req, err := http.NewRequest("POST", reload_url, nil)
	if err != nil {
		return err
	}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	return nil
}

func check_port(port string) bool {
	_, lerr := net.DialTimeout("tcp", "127.0.0.1:"+port, time.Duration(time.Second))
	return lerr == nil
}

func compare_file(source string, target string) bool {
	source_byte, err := ioutil.ReadFile(source)
	if err != nil {
		return false
	}
	if _, err := os.Stat(target); os.IsNotExist(err) {
		os.Create(target)
	}
	target_byte, err := ioutil.ReadFile(target)
	if err != nil {
		return false
	}
	return bytes.Equal(source_byte, target_byte)
}

func copy_file(source, target string) error {
	in, err := os.Open(source)
	if err != nil {
		return err
	}
	defer in.Close()
	out, err := os.Create(target)
	if err != nil {
		return err
	}
	defer out.Close()
	_, err = io.Copy(out, in)
	if err != nil {
		return err
	}
	return out.Close()
}
