# 全局配置
global:
  scrape_interval: 60s
  evaluation_interval: 60s
  scrape_timeout: 50s
  external_labels:
    monitor: "gn1"

# 告警alertmanager配置
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - 127.0.0.1:9093
# 告警规则文件
rule_files:
  - alert_rule.yml

# 抓取任务配置
scrape_configs:
  {{- range .AddOns }}
  - file_sd_configs:
      - files:
          - {{ .TaskID }}_direct.yml
        refresh_interval: 10s
    job_name: {{ .Name }}
    metrics_path: {{ .Metric }}
    params:
    {{- range $key, $value := .Params }}
      {{ $key }}: {{ $value | printf "%q" }}
    {{- end }}
    scheme: {{ .Scheme }}
    scrape_interval: {{ .Interval }}s
    scrape_timeout: {{ .TimeOut }}s
    {{ end }}
