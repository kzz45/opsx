package funcs

import (
	"encoding/json"
	"fmt"
	"opsx/monitorx_proxy/g"
)

func get_server() ([]Server, error) {
	g.Logger.Infof("get server list from: %s%s", g.Config().Server.ServerAddr, g.SERVERS_API)
	server_url := fmt.Sprintf("%s%s?uuid=%s", g.Config().Server.ServerAddr, g.SERVERS_API, g.Config().UUID)
	resp, err := do_request("GET", server_url, nil)
	if err != nil {
		g.Logger.Errorf("get server list from: %s%s error: %v", g.Config().Server.ServerAddr, g.SERVERS_API, err)
		return nil, err
	}
	server := Servers{}
	err = json.Unmarshal(resp, &server)
	if err != nil {
		g.Logger.Errorf("json unmarshal server struct error: %v", err)
		return nil, err
	}
	return server.Results, nil
}
