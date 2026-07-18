{{- define "fastapi-chart.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "fastapi-chart.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end }}