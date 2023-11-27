package funcs

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"opsx/monitorx_proxy/g"
)

func get_silence_from_server() ([]SilenceData, error) {
	silence_url := fmt.Sprintf("%s%s", g.Config().Server.ServerAddr, g.SILENCE_API)
	resp, err := do_request("GET", silence_url, nil)
	if err != nil {
		g.Logger.Errorf("get silence from: %s error: %v", silence_url, err)
		return nil, err
	}
	var silence Silence
	err = json.Unmarshal(resp, &silence)
	if err != nil {
		return nil, err
	}
	return silence.Data, nil
}

func am_current_silence() ([]AmSilence, error) {
	amsilence_url := fmt.Sprintf("http://127.0.0.1:9093%s", g.ALERTMANAGER_SILENCE)
	resp, err := http.Get(amsilence_url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	var am_silence []AmSilence
	am_silence_bytes, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	err = json.Unmarshal(am_silence_bytes, &am_silence)
	if err != nil {
		return nil, err
	}
	var result []AmSilence
	for _, item := range am_silence {
		if item.Status.State != "expired" {
			result = append(result, item)
		}
	}
	return result, nil
}

func create_or_update_silence(data CRUDSilenceData) bool {
	amsilence_url := fmt.Sprintf("http://127.0.0.1:9093%s", g.ALERTMANAGER_SILENCE)
	data_bytes, err := json.Marshal(data)
	if err != nil {
		return false
	}
	req, err := http.NewRequest("POST", amsilence_url, bytes.NewBuffer(data_bytes))
	req.Header.Set("Content-Type", "application/json")
	if err != nil {
		return false
	}
	client := http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return false
	}
	defer resp.Body.Close()
	return true
}
