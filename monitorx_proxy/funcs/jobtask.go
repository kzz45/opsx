package funcs

import (
	"encoding/json"
	"fmt"
	"opsx/monitorx_proxy/g"
)

func get_job_tasks() ([]JobTask, error) {
	var result []JobTask
	servers, err := get_server()
	if err != nil {
		return nil, err
	}
	for _, server := range servers {
		job_tasks_url := fmt.Sprintf("%s%s?uuid=%s", g.Config().Server.ServerAddr, g.TASKS_API, server.UUID)
		var job_tasks []JobTask
		resp, err := do_request("GET", job_tasks_url, nil)
		if err != nil {
			continue
		}
		err = json.Unmarshal(resp, &job_tasks)
		if err != nil {
			continue
		}
		result = append(result, job_tasks...)
	}
	return result, nil
}
