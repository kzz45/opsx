package funcs

import (
	"encoding/json"
	"fmt"
	"opsx/monitorx_proxy/g"
)

func get_alert_rules() (*GlobalAlertRule, error) {
	var result GlobalAlertRule
	alert_rule_url := fmt.Sprintf("%s%s", g.Config().Server.ServerAddr, g.ALERT_RULE_API)
	resp, err := do_request("GET", alert_rule_url, nil)
	if err != nil {
		return nil, err
	}
	err = json.Unmarshal(resp, &result)
	if err != nil {
		return nil, err
	}
	return &result, nil
}
