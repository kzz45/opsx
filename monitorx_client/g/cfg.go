package g

import (
	"encoding/json"
	"sync"

	"github.com/toolkits/file"
)

var (
	ConfigFile string              //
	config     *GlobalConfig       //
	lock       = new(sync.RWMutex) //
)

// GlobalConfig 全局配置
type GlobalConfig struct {
	Debug         bool      `json:"debug"`
	UUID          string    `json:"uuid"`
	ListenPort    int       `json:"listen_port"`
	NodePort      int       `json:"node_port"`
	CleanTime     int       `json:"clean_time"`
	ExpireTime    int       `json:"expire_time"`
	IntervalTime  int       `json:"interval_time"`
	MonitorServer string    `json:"monitor_server"`
	Logs          string    `json:"logs"`
	Magic         string    `json:"magic"`
	Plugin        string    `json:"plugin"`
	BaseNode      *Exporter `json:"base_node"`
	RedisNode     *Exporter `json:"redis_node"`
	MySQLNode     *Exporter `json:"mysql_node"`
}

// Exporter prometheus exporter
type Exporter struct {
	Port int    `json:"port"`
	Args string `json:"args"`
	Name string `json:"name"`
}

func Config() *GlobalConfig {
	lock.RLock()
	defer lock.RUnlock()
	return config
}

func ParseConfig(cfg string) {
	if cfg == "" {
		Logger.Fatalln("use -c to specify configuration file")
	}

	if !file.IsExist(cfg) {
		Logger.Fatalf("config file: %s is not exist.", cfg)
	}

	ConfigFile = cfg

	configContent, err := file.ToTrimString(cfg)
	if err != nil {
		Logger.Fatalf("read config file: %s fail: %s", cfg, err)
	}

	var c GlobalConfig
	err = json.Unmarshal([]byte(configContent), &c)
	if err != nil {
		Logger.Fatalf("parse config file: %s fail: %s", cfg, err)
	}

	lock.Lock()
	defer lock.Unlock()

	config = &c

	Logger.Infof("read config file: %s success.", cfg)
}
