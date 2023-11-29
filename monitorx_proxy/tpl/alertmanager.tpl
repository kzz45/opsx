# 告警配置
global:
  resolve_timeout: 5m

route:
  group_by: ["alertname", "level", "_product_id"]
  receiver: 1000
  routes:
    {{- range .Routes }}
    - receiver: {{ .Receiver }}
      continue: true
      group_wait: {{ .GroupWait }}s
      group_interval: {{ .GroupInterval }}s
      repeat_interval: {{ .RepeatInterval }}s
      match:
        {{- range $key, $value := .Match }}
        {{ $key }}: {{ $value }}
        {{- end }}
    {{- range .SubRoute }}
    - receiver: {{ .Receiver }}
      continue: true
      group_wait: {{ .GroupWait }}s
      group_interval: {{ .GroupInterval }}s
      repeat_interval: {{ .RepeatInterval }}s
      match:
        {{- range $key, $value := .Match }}
        {{ $key }}: {{ $value }}
        {{- end }}
    {{- end }}
    {{- end }}

receivers:
  - name: 1000
    webhook_configs:
      - url: http://127.0.0.1:5454/api/v1/notice/
{{- range .Receivers }}
  - name: {{ .Name }}
    webhook_configs:
      - url: {{ .WebhookConfigs }}
{{- end }}

inhibit_rules:
  - source_match:
      severity: "crit"
    target_match:
      severity: "warn"
    equal: ["alertname", "level", "_product_id"]
