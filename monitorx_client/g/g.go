package g

import (
	"fmt"
	"os"

	"github.com/sirupsen/logrus"
)

var (
	err       error          //
	RootDir   string         // WordDir 工作目录
	Logs_dir  string         //
	LogWriter *os.File       //
	Logger    = logrus.New() //
)

func Init() {
	Logger = logrus.New()
	RootDir, _ = os.Getwd()
	Logs_dir = fmt.Sprintf("%s/%s", RootDir, "logs")
	if _, err := os.Stat(Logs_dir); os.IsNotExist(err) {
		os.Mkdir(Logs_dir, os.ModePerm)
	}
	logfile := Logs_dir + "/monitor.log"
	LogWriter, err = os.OpenFile(logfile, os.O_APPEND|os.O_CREATE|os.O_RDWR, 0666)
	if err != nil {
		Logger.Fatalf("open log file: %s err: %s", logfile, err)
	}
	if Config().Debug {
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
}
