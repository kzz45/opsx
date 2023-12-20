package funcs

import (
	"fmt"
	"opsx/monitorx_client/g"

	"github.com/sirupsen/logrus"
	"github.com/toolkits/file"
)

func StartBaseNode() {
	node_pid_file_dir := g.RootDir + "/" + g.Config().Logs
	node_port := g.Config().BaseNode.Port

	node_pid_file := fmt.Sprintf("%s/%d.pid", node_pid_file_dir, node_port)

	port_alive := check_port(fmt.Sprintf("%d", node_port))
	if port_alive {
		logrus.Infof("node exporter has alread started.")
	} else {
		node_bin := g.RootDir + g.Config().BaseNode.Name
		config := make([]string, 0)

		// node_args := g.Config().BaseNode.Args
		node_listen := fmt.Sprintf("--web.listen-address=127.0.0.1:%d", node_port)
		// args := strings.Split(node_args, " ")
		config = append(config, node_listen)
		fmt.Println(node_bin, config)
		pid, err := execute_with_fork(node_bin, config...)
		if err != nil {
			logrus.Errorf("start node exporter failed error: %s", err)
			return
		}
		logrus.Infof("start node exporter success with pid: %d", pid)
		file.WriteString(node_pid_file, fmt.Sprintf("%d", pid))
	}
}
