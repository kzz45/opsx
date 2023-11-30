package funcs

import (
	"encoding/json"
	"fmt"
	"opsx/monitorx_proxy/g"
	"strings"
)

func get_user_group_webhook(reciver string) (UserGroup, error) {
	var user_group UserGroupResp
	group_ids := strings.Split(reciver, "-")
	user_group_url := fmt.Sprintf("%s%s?id__in=%s", g.Config().Server.ServerAddr, g.USERGROUP_API, strings.Join(group_ids, ","))
	// g.Logger.Debugf("user_group_url: %v\n", user_group_url)
	resp, err := do_request("GET", user_group_url, nil)
	if err != nil {
		// return "", err
		return UserGroup{}, err
	}
	err = json.Unmarshal(resp, &user_group)
	if err != nil {
		// return "", err
		return UserGroup{}, err
	}
	// return user_group.Results[len(user_group.Results)-1].WebHook, nil
	return user_group.Results[len(user_group.Results)-1], nil
}
