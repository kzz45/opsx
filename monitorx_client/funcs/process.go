package funcs

import (
	"fmt"
	"net/http"
	"opsx/monitorx_client/g"
	"strings"

	"github.com/shirou/gopsutil/process"
)

type UProcess struct {
	Name           string
	Cmdline        string
	Exist          int
	Num            int
	Status         string
	CPUTimePercent float64
	MemVMS         float64
	MemRSS         float64
	MemPercent     float64
}

func proc_info(proclist string) []UProcess {
	result := make([]UProcess, 0)
	args := strings.Split(proclist, "|")
	if len(args) == 0 {
		g.Logger.Errorf("no proc info in url")
		return nil
	}
	g.Logger.Infof("proc info in url: %s\n", args)
	for _, proc := range args {
		if proc != "" {
			procArgs := strings.Split(proc, ",")
			g.Logger.Infof("proc name and cmdline: %s", procArgs)
			if len(procArgs) == 2 {
				name := procArgs[0]
				cmdline := procArgs[1]
				if name != "" && cmdline != "" {
					uproc, err := get_proc_name_and_cmdline(name, cmdline)
					if err != nil {
						g.Logger.Errorf("get proc name and cmdline error: %s", err)
					}
					result = append(result, uproc)
				}
			}
		}
	}
	return result
}

func get_proc_name_and_cmdline(pname, pcml string) (UProcess, error) {
	uzp := UProcess{}
	allprocs, err := process.Processes()
	if err != nil {
		return uzp, err
	}
	for _, proc := range allprocs {
		procname, _ := proc.Name()
		procCmdline, _ := proc.Cmdline()
		if strings.EqualFold(strings.ToLower(procname), strings.ToLower(pname)) && strings.Contains(procCmdline, pcml) {
			meminfo, _ := proc.MemoryInfo()
			memrss := float64(meminfo.RSS)
			memvms := float64(meminfo.VMS)
			cpupercent, _ := proc.CPUPercent()
			mempercent, _ := proc.MemoryPercent()
			procstatus, _ := proc.Status()
			uzp.Num++
			uzp.Exist = 1
			uzp.Name = pname
			uzp.Cmdline = pcml
			uzp.Status = procstatus
			uzp.MemRSS += memrss
			uzp.MemVMS += memvms
			uzp.CPUTimePercent += cpupercent
			uzp.MemPercent += float64(mempercent)
		} else {
			uzp.Name = pname
			uzp.Cmdline = pcml
		}
	}
	return uzp, nil
}

func process_service(w http.ResponseWriter, r *http.Request) {
	params := r.URL.Query()
	paramsName := params.Get("list")
	if paramsName == "" {
		g.Logger.Errorln("no proc info in url")
		w.Write([]byte("proc_alive{} 0\n"))
	}
	var result string
	procInfos := proc_info(paramsName)
	for _, procInfo := range procInfos {
		g.Logger.Infof("%v", procInfo)
		result += fmt.Sprintf("process_num{name=\"%s\", cmdline=\"%s\", status=\"%s\"} %d\n", procInfo.Name, procInfo.Cmdline, procInfo.Status, procInfo.Num)
		result += fmt.Sprintf("process_exist{name=\"%s\", cmdline=\"%s\", status=\"%s\"} %d\n", procInfo.Name, procInfo.Cmdline, procInfo.Status, procInfo.Exist)
		result += fmt.Sprintf("process_mem_rss{name=\"%s\", cmdline=\"%s\"} %.3f\n", procInfo.Name, procInfo.Cmdline, procInfo.MemRSS)
		result += fmt.Sprintf("process_mem_vms{name=\"%s\", cmdline=\"%s\"} %.3f\n", procInfo.Name, procInfo.Cmdline, procInfo.MemVMS)
		result += fmt.Sprintf("process_mem_percent{name=\"%s\", cmdline=\"%s\"} %.3f\n", procInfo.Name, procInfo.Cmdline, procInfo.MemPercent)
		result += fmt.Sprintf("process_cpu_percent{name=\"%s\", cmdline=\"%s\"} %.3f\n", procInfo.Name, procInfo.Cmdline, procInfo.CPUTimePercent)
	}
	w.Write([]byte(result))
}
