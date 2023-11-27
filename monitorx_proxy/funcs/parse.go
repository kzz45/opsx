package funcs

import (
	"fmt"
	"opsx/monitorx_proxy/g"
	"os"
	"text/template"
)

func render_alert_rule_conf(tmpl_path string, conf_path string) error {
	conf_file := fmt.Sprintf("%s/alert_rule.yml", conf_path)
	fs, err := os.Create(conf_file)
	if err != nil {
		return err
	}
	global_alert_rule, err := get_alert_rules()
	if err != nil {
		return err
	}
	tpl := template.Must(template.ParseFiles(tmpl_path))
	err = tpl.Execute(fs, global_alert_rule)
	if err != nil {
		return err
	}
	return nil
}

func RenderAlertRoute(tmpl_path string, conf_path string) error {
	return nil
}

func render_alertmanager_conf(tmpl_path string, conf_path string) error {
	alert_manager_conf_file := fmt.Sprintf("%s/alertmanager.yml", conf_path)
	am_fs, err := os.Create(alert_manager_conf_file)
	if err != nil {
		g.Logger.Errorf("create prometheus conf file error: %v", err)
		return err
	}
	global_alert_route, err := get_alert_route()
	if err != nil {
		return err
	}
	tpl := template.Must(template.ParseFiles(tmpl_path))
	err = tpl.Execute(am_fs, global_alert_route)
	if err != nil {
		return err
	}
	return nil
}

func render_prometheus_conf(prom_tmpl_path string, ins_tmpl_path string, conf_path string) ([]int, error) {
	prometheus_conf_file := fmt.Sprintf("%s/prometheus.yml", conf_path)
	prom_fs, err := os.Create(prometheus_conf_file)
	if err != nil {
		g.Logger.Errorf("create prometheus conf file error: %v", err)
		return nil, err
	}
	job_tasks, err := get_job_tasks()
	if err != nil {
		return nil, err
	}
	tpl_prom := template.Must(template.ParseFiles(prom_tmpl_path))
	add_ons := make([]JobAddOn, 0)
	var jobs JobTask
	for _, job_task := range job_tasks {
		add_ons = append(add_ons, job_task.AddOns...)
	}
	jobs.AddOns = add_ons
	err = tpl_prom.Execute(prom_fs, jobs)
	if err != nil {
		return nil, err
	}

	task_ids := make([]int, 0)
	tpl_ins := template.Must(template.ParseFiles(ins_tmpl_path))
	for _, job_task := range job_tasks {
		task_ids = append(task_ids, job_task.TaskID)
		ins_conf_file := fmt.Sprintf("%s/%d_direct.yml", conf_path, job_task.TaskID)
		ins_fs, err := os.Create(ins_conf_file)
		if err != nil {
			g.Logger.Errorf("create instance conf file error: %v", err)
			return nil, err
		}
		err = tpl_ins.Execute(ins_fs, job_task)
		if err != nil {
			return nil, err
		}
	}
	return task_ids, nil
}
