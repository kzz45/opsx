package funcs

import (
	"encoding/json"
	"fmt"
	"opsx/monitorx_proxy/g"
)

func get_alert_route() (*GlobalAlertRoute, error) {
	var result GlobalAlertRoute
	alert_route_url := fmt.Sprintf("%s%s", g.Config().Server.ServerAddr, g.ALERT_ROUTE_API)
	resp, err := do_request("GET", alert_route_url, nil)
	if err != nil {
		return nil, err
	}
	err = json.Unmarshal(resp, &result)
	if err != nil {
		return nil, err
	}
	return &result, nil
}
