groups:
  - name: GlobalAlertRules
    rules:
    {{- range .Rules }}
      - alert: {{ .Alert }}
        expr: {{ .Expr }}
        for: {{ .For }}
        labels:
          level: {{ .Labels.Level }}
          {{- if .Labels.AlertID }}
          alert_id: {{ .Labels.AlertID }}
          {{- end }}
          {{- if .Labels.AdjustID  }}
          adjust_id: {{ .Labels.AdjustID }}
          {{- end }}
        annotations:
          summary: {{ .Annotations.Summary }}
          description: {{ .Annotations.Description }}
    {{- end }}