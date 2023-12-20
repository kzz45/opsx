# 实例列表(标签)
{{- range .Instances }}
- labels:
    _ip: {{ .IP }}
    _name: {{ .Name }}
    _endpoint: {{ .Endpoint }}
    {{- range $key, $value := .Labels }}
    {{ $key }}: {{ $value }}
    {{- end }}
  targets:
    - {{ .IP }}
{{- end }}