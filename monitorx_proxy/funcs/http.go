package funcs

import (
	"io"
	"io/ioutil"
	"net/http"
	"opsx/monitorx_proxy/g"
	"time"
)

func do_request(method string, url string, body io.Reader) ([]byte, error) {
	client := http.Client{Timeout: time.Duration(time.Second * 10)}
	req, err := http.NewRequest(method, url, body)
	if err != nil {
		g.Logger.Errorf("http new request error: %v", err)
		return nil, err
	}
	token := get_token()
	req.Header.Set("Authorization", token)
	req.Header.Add("Accept", "application/json")
	resp, err := client.Do(req)
	if err != nil {
		g.Logger.Errorf("http client do request error: %v", err)
		return nil, err
	}
	defer resp.Body.Close()
	result, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		g.Logger.Errorf("read http response error: %v", err)
		return nil, err
	}
	return result, nil
}
