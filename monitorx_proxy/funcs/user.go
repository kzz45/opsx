package funcs

import (
	"encoding/json"
	"fmt"
	"opsx/monitorx_proxy/g"
	"strings"
)

func get_user_group_webhook(reciver string) (string, error) {
	var user_group UserGroupResp
	group_ids := strings.Split(reciver, "-")
	user_group_url := fmt.Sprintf("%s%s?id__in=%s", g.Config().Server.ServerAddr, g.USERGROUP_API, strings.Join(group_ids, ","))
	resp, err := do_request("GET", user_group_url, nil)
	if err != nil {
		return "", err
	}
	err = json.Unmarshal(resp, &user_group)
	if err != nil {
		return "", err
	}
	return user_group.Results[len(user_group.Results)-1].WebHook, nil

}
