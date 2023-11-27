package funcs

import (
	"fmt"
	"net/http"
	"opsx/monitorx_client/g"
	"strings"

	"github.com/gorilla/mux"
	"github.com/sirupsen/logrus"
)

func index(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte(`<html>
	<head><title>OMA Monitor</title></head>
	<body>
	<h1>OMA Monitor Exporter Welcome Page</h1>
	</body>
	</html>
	`))
}

func port_service(w http.ResponseWriter, r *http.Request) {
	params := r.URL.Query()
	params_name := params.Get("port")
	if params_name == "" {
		logrus.Errorln("no port infomation in url")
		w.Write([]byte("port_alive{} 0\n"))
	}
	var result, metric_value string
	var metric_list []string
	portList := strings.Split(params_name, ",")
	logrus.Infof("check ports: %s", portList)
	for _, port := range portList {
		if ok := check_port(port); ok {
			metric_value = fmt.Sprintf("port_alive{port=\"%s\"} 1\n", port)
			metric_list = append(metric_list, metric_value)
		} else {
			metric_value = fmt.Sprintf("port_alive{port=\"%s\"} 0\n", port)
			metric_list = append(metric_list, metric_value)
		}
	}
	for _, metric := range metric_list {
		result += metric
	}
	w.Write([]byte(result))
}

func exporter_service(w http.ResponseWriter, r *http.Request) {
	params := r.URL.Query()
	params_name := params.Get("name")
	if params_name == "" {
		w.Write([]byte("exporter_alive 0\n"))
	}
	if params_name == "base" {
		base_url := fmt.Sprintf("http://127.0.0.1:%d/metrics", g.Config().BaseNode.Port)
		base_result := parse_base_node(base_url)
		if base_result == "" {
			w.WriteHeader(http.StatusInternalServerError)
			w.Write([]byte("node_exporter 0\n"))
		}
		w.Write([]byte(base_result))
	}
}

func Route() *mux.Router {
	router := mux.NewRouter()
	router.HandleFunc("/", index)
	router.HandleFunc("/port/", port_service)
	router.HandleFunc("/process/", process_service)
	router.HandleFunc("/exporter/", exporter_service)
	return router
}
