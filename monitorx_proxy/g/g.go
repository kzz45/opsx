package g

import (
	"fmt"
	"os"

	"github.com/sirupsen/logrus"
)

const (
	TASKS_API            = "/api/monitor/get_tasks/"       //
	SERVERS_API          = "/api/monitor/server/"          //
	SILENCE_API          = "/api/monitor/get_silence/"     //
	INSTANCE_API         = "/api/monitor/instance/"        //
	USERGROUP_API        = "/api/monitor/user_group/"      //
	ALERT_RULE_API       = "/api/monitor/get_alert_rule/"  //
	ALERT_ROUTE_API      = "/api/monitor/get_alert_route/" //
	PROMETHEUS_RELOAD    = "/-/reload"                     //
	ALERTMANAGER_RELOAD  = "/-/reload"                     //
	ALERTMANAGER_SILENCE = "/api/v2/silences/"             //
)

var (
	err               error          //
	BinDir            string         //
	TplDir            string         //
	TempDir           string         //
	ConfDir           string         //
	RootDir           string         //
	PromDataDir       string         //
	AlertDataDir      string         //
	LogWriter         *os.File       //
	Logger            = logrus.New() //
	local_redis_queue RedisHandler   //
)

func Init() {
	Logger = logrus.New()
	RootDir, _ = os.Getwd()
	BinDir = fmt.Sprintf("%s/%s", RootDir, Config().BinDir)
	TplDir = fmt.Sprintf("%s/%s", RootDir, Config().TplDir)
	TempDir = fmt.Sprintf("%s/%s", RootDir, Config().TempDir)
	ConfDir = fmt.Sprintf("%s/%s", RootDir, Config().ConfDir)
	PromDataDir = fmt.Sprintf("%s/%s", RootDir, Config().Prometheus.PromDataDir)
	AlertDataDir = fmt.Sprintf("%s/%s", RootDir, Config().Alertmanager.AlertDataDir)
	if _, err := os.Stat(BinDir); os.IsNotExist(err) {
		os.Mkdir(BinDir, os.ModePerm)
	}
	if _, err := os.Stat(TplDir); os.IsNotExist(err) {
		os.Mkdir(TplDir, os.ModePerm)
	}
	if _, err := os.Stat(TempDir); os.IsNotExist(err) {
		os.Mkdir(TempDir, os.ModePerm)
	}
	if _, err := os.Stat(ConfDir); os.IsNotExist(err) {
		os.Mkdir(ConfDir, os.ModePerm)
	}
	if _, err := os.Stat(PromDataDir); os.IsNotExist(err) {
		os.Mkdir(PromDataDir, os.ModePerm)
	}
	if _, err := os.Stat(AlertDataDir); os.IsNotExist(err) {
		os.Mkdir(AlertDataDir, os.ModePerm)
	}
	logfile_dir := RootDir + "/" + Config().LogFile
	LogWriter, err = os.OpenFile(logfile_dir, os.O_APPEND|os.O_CREATE|os.O_RDWR, 0666)
	if err != nil {
		Logger.Fatalf("open log file: %s err: %s", logfile_dir, err)
	}
	if Config().Deubg {
		Logger.SetFormatter(
			&logrus.TextFormatter{
				ForceColors:     true,
				FullTimestamp:   true,
				TimestampFormat: "2006-01-02 15:04:05",
			},
		)
		Logger.SetLevel(logrus.DebugLevel)
		Logger.SetOutput(os.Stdout)
	} else {
		Logger.SetFormatter(
			&logrus.TextFormatter{
				ForceColors:     false,
				FullTimestamp:   true,
				TimestampFormat: "2006-01-02 15:04:05",
			},
		)
		Logger.SetOutput(LogWriter)
	}
	local_redis_conn := RedisConn{
		DB:       Config().Redis.RedisDB,
		Port:     Config().Redis.RedisPort,
		Queue:    "",
		Addr:     Config().Redis.RedisAddr,
		Password: Config().Redis.RedisPass,
	}
	local_redis_queue = RedisSetUP(local_redis_conn)
}
