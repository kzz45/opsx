package funcs

import (
	"fmt"
	"opsx/monitorx_proxy/g"
	"time"
)

func RunPrometheus() {
	if g.Config().Prometheus.Enable {
		instance_tpl := fmt.Sprintf("%s/instance.tpl", g.TplDir)
		promtheus_tpl := fmt.Sprintf("%s/prometheus.tpl", g.TplDir)
		task_ids, err := render_prometheus_conf(promtheus_tpl, instance_tpl, g.TempDir)
		if err != nil {
			g.Logger.Errorf("render prom conf or instance conf error: %s", err)
			return
		}
		alert_rules_tpl := fmt.Sprintf("%s/alert_rules.tpl", g.TplDir)
		if err := render_alert_rule_conf(alert_rules_tpl, g.TempDir); err != nil {
			g.Logger.Errorf("render alert rule conf error: %s", err)
			return
		}
		alert_rule_temp_conf := fmt.Sprintf("%s/alert_rule.yml", g.TempDir)
		alert_rule_conf := fmt.Sprintf("%s/alert_rule.yml", g.ConfDir)
		diff_alert_rule := compare_file(alert_rule_temp_conf, alert_rule_conf)
		if !diff_alert_rule {
			g.Logger.Warnf("temp alert_rule conf: %s diff with target real conf: %s", alert_rule_temp_conf, alert_rule_conf)
			err := copy_file(alert_rule_temp_conf, alert_rule_conf)
			if err != nil {
				g.Logger.Errorf("copy source alert_rule conf: %s to target real conf: %s with error: %s", alert_rule_temp_conf, alert_rule_conf, err)
				return
			} else {
				reload("prometheus")
				g.Logger.Warnf("reload prometheus because prometheus alert_rule config file change")
			}
		}
		g.Logger.Infoln("render prometheus config success")

		prometheus_temp_conf := fmt.Sprintf("%s/prometheus.yml", g.TempDir)
		if err := check_conf_valid("promtool", prometheus_temp_conf, "prometheus"); err != nil {
			g.Logger.Errorf("check config %s error: %s", prometheus_temp_conf, err)
			return
		}
		g.Logger.Infoln("check prometheus config success")

		for _, task_id := range task_ids {
			instance_temp_conf := fmt.Sprintf("%s/%d_direct.yml", g.TempDir, task_id)
			instance_conf := fmt.Sprintf("%s/%d_direct.yml", g.ConfDir, task_id)
			diff := compare_file(instance_temp_conf, instance_conf)
			if !diff {
				g.Logger.Warnf("temp instance conf: diff with target real conf: %s", instance_temp_conf, instance_conf)
				err := copy_file(instance_temp_conf, instance_conf)
				if err != nil {
					g.Logger.Errorf("copy source instance conf: %s to target real conf: %s with error: %s", instance_temp_conf, instance_conf, err)
				}
			}
		}
		prometheus_conf := fmt.Sprintf("%s/prometheus.yml", g.ConfDir)
		diff := compare_file(prometheus_temp_conf, prometheus_conf)
		if !diff {
			g.Logger.Warnf("source temp conf: %s diff with target real conf: %s", prometheus_temp_conf, prometheus_conf)
			err := copy_file(prometheus_temp_conf, prometheus_conf)
			if err != nil {
				g.Logger.Errorf("copy source temp conf: %s to target real conf: %s with error: %s", prometheus_temp_conf, prometheus_conf, err)
				return
			} else {
				reload("prometheus")
				g.Logger.Warnf("reload prometheus because prometheus config file change")
			}
		} else {
			g.Logger.Infof("source temp conf: %s same with target real conf: %s", prometheus_temp_conf, prometheus_conf)
		}
		prometheus_alive := check_port("9090")
		if prometheus_alive {
			g.Logger.Infof("prometheus already running")
			return
		}
		pid, err := start_prometheus(prometheus_conf)
		if err != nil {
			g.Logger.Errorf("start prometheus error: %s", err)
			return
		}
		g.Logger.Infof("start prometheus with pid: %d", pid)
	}
}

func RunAlertManager() {
	if g.Config().Alertmanager.Enable {
		alertmanager_tpl := fmt.Sprintf("%s/alertmanager.tpl", g.TplDir)
		if err := render_alertmanager_conf(alertmanager_tpl, g.TempDir); err != nil {
			g.Logger.Errorf("render alertmanager conf error: %s", err)
			return
		}
		g.Logger.Infoln("render alertmanager config success")
		alertmanager_temp_conf := fmt.Sprintf("%s/alertmanager.yml", g.TempDir)
		if err := check_conf_valid("amtool", alertmanager_temp_conf, "alertmanager"); err != nil {
			g.Logger.Errorf("check config %s error: %s", alertmanager_temp_conf, err)
			return
		}
		g.Logger.Infoln("check alertmanager config success")

		alertmanager_conf := fmt.Sprintf("%s/alertmanager.yml", g.ConfDir)
		diff := compare_file(alertmanager_temp_conf, alertmanager_conf)
		if !diff {
			g.Logger.Warnf("source temp conf: %s diff with target real conf: %s", alertmanager_temp_conf, alertmanager_conf)
			err := copy_file(alertmanager_temp_conf, alertmanager_conf)
			if err != nil {
				g.Logger.Errorf("copy source temp conf: %s to target real conf: %s with error: %s", alertmanager_temp_conf, alertmanager_conf, err)
				return
			} else {
				reload("alertmanager")
			}
		} else {
			g.Logger.Infof("source temp conf: %s same with target real conf: %s", alertmanager_temp_conf, alertmanager_conf)
		}

		alertmanager_alive := check_port("9093")
		if alertmanager_alive {
			g.Logger.Infof("alertmanager already running")
			return
		}
		pid, err := start_alertmanager(alertmanager_conf)
		if err != nil {
			g.Logger.Errorf("start alertmanager error: %s", err)
			return
		}
		g.Logger.Infof("start alertmanager with pid: %d", pid)
	}
}

func RunSilence() {
	if g.Config().Alertmanager.Enable {
		server_silence_data, err := get_silence_from_server()
		if err != nil {
			g.Logger.Errorf("get silence from server error: %v", err)
			return
		}
		am_silence_data, err := am_current_silence()
		if err != nil {
			g.Logger.Errorf("get silence from alertmanager error: %v", err)
			return
		}
		server_silence := make(map[string]CRUDSilenceData)
		if len(server_silence_data) > 0 {
			for _, x := range server_silence_data {
				xd := CRUDSilenceData{
					CreatedBy: x.CreatedBy,
					EndsAt:    time.Unix(x.EndsAt, 10).UTC().Format(time.RFC3339),
					StartsAt:  time.Unix(x.StartsAt, 10).UTC().Format(time.RFC3339),
					Comment:   x.Comment,
					Matchers:  x.Matchers,
				}
				server_silence[x.CreatedBy] = xd
			}
		}
		am_silence := make(map[string]CRUDSilenceData)
		if len(am_silence_data) > 0 {
			for _, y := range am_silence_data {
				yd := CRUDSilenceData{
					ID:        y.ID,
					Comment:   y.Comment,
					Matchers:  y.Matchers,
					CreatedBy: y.CreatedBy,
					EndsAt:    y.EndsAt.Format(time.RFC3339),
					StartsAt:  y.StartsAt.Format(time.RFC3339),
				}
				am_silence[y.CreatedBy] = yd
			}
		}
		if len(server_silence) > 0 && len(am_silence) > 0 {
			for sk, sv := range server_silence {
				for ak, av := range am_silence {
					if sk == ak {
						if sv.EndsAt == av.EndsAt {
							sv.ID = av.ID
							g.Logger.Infof("exists silence: %s end_time: %v", sv.ID, sv.EndsAt)
							continue
						} else {
							sv.ID = av.ID
							g.Logger.Infof("update silence: %s end_time: %v", sv.ID, sv.EndsAt)
							if ok := create_or_update_silence(sv); ok {
								g.Logger.Infof("update silence %s success", sv.ID)
							}
						}
					}
				}
			}
		}
		if len(server_silence) > 0 && len(am_silence) == 0 {
			for _, silence := range server_silence {
				g.Logger.Infof("create silence: %s end_time: %v", silence.ID, silence.EndsAt)
				if ok := create_or_update_silence(silence); ok {
					g.Logger.Infof("create silence: %s success", silence.ID)
				}
			}
		}
	}
}
