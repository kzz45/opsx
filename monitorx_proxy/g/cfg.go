package g

import (
	"encoding/json"
	"sync"

	"github.com/toolkits/file"
)

type GlobalConfig struct {
	Deubg           bool                `json:"debug"`
	UUID            string              `json:"uuid"`
	BinDir          string              `json:"bin_dir"`
	TplDir          string              `json:"tpl_dir"`
	ConfDir         string              `json:"conf_dir"`
	TempDir         string              `json:"temp_dir"`
	LogFile         string              `json:"log_file"`
	SelfHealthCheck bool                `json:"self_health_check"`
	Server          *MonitorServer      `json:"monitor_server"`
	Redis           *RedisServer        `json:"redis_server"`
	Notice          *NoticeServer       `json:"notice_server"`
	Prometheus      *PrometheusServer   `json:"prometheus_server"`
	Alertmanager    *AlertmanagerServer `json:"alertmanager_server"`
}

type MonitorServer struct {
	ServerAddr string `json:"server_addr"`
	AccessID   string `json:"access_id"`
	AccessKey  string `json:"access_key"`
	SecretKey  string `json:"secret_key"`
	TimeOut    int    `json:"timeout"`
	Interval   int    `json:"intercal"`
	HeartBeat  int    `json:"heartbeat"`
}

type RedisServer struct {
	RedisAddr string `json:"redis_addr"`
	RedisPort int    `json:"redis_port"`
	RedisPass string `json:"redis_pass"`
	RedisDB   int    `json:"redis_db"`
}

type NoticeServer struct {
	Enable bool   `json:"enable"`
	Addr   string `json:"addr"`
	Port   int    `json:"port"`
}

type PrometheusServer struct {
	Enable      bool   `json:"enable"`
	Addr        string `json:"addr"`
	Port        int    `json:"port"`
	PromDataDir string `json:"prom_data_dir"`
}

type AlertmanagerServer struct {
	Enable       bool   `json:"enable"`
	Addr         string `json:"addr"`
	Port         int    `json:"port"`
	AlertDataDir string `json:"alert_data_dir"`
}

var (
	ConfigFile string
	config     *GlobalConfig
	lock       = new(sync.RWMutex)
)

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
