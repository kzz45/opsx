告警状态: {{ if eq .MergeStatus  "崩盘" }}<font color ="warning">{{ .MergeStatus }}</font>{{- end }}{{ if eq .MergeStatus  "恢复" }}<font color ="info">{{ .MergeStatus }}</font>{{- end }}
告警名称: {{ range $key, $value := .CommonLabels }}{{ if eq $key "alertname" }}{{ $value }}{{ end }}{{- end }}
告警时间: {{ .StartsAt }}
告警描述: {{ range $key, $value := .CommonAnnotations }}{{ if eq $key "summary" }}{{ $value }}{{ end }}{{- end }}
告警产品: {{ range $key, $value := .CommonLabels }}{{ if eq $key "_product_name" }}{{ $value }}{{ end }}{{- end }}
产品聚合: {{ range $key, $value := .AlertProduct }}产品: {{ $key }} 聚合: {{ $value }}次{{- end }}
状态聚合: {{ range $key, $value := .AlertStatus }}告警状态: {{ $key }} 聚合: {{ $value }}次{{- end }}