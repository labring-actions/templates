{{- define "yarn.name" -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "yarn.configName" -}}
{{- printf "%s-config" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "yarn.resourceManagerName" -}}
{{- printf "%s-resourcemanager" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "yarn.nodeManagerName" -}}
{{- printf "%s-nodemanager" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "yarn.resourceManagerHost" -}}
{{- printf "%s.%s.svc.cluster.local" (include "yarn.resourceManagerName" .) .Release.Namespace -}}
{{- end -}}

{{- define "yarn.image" -}}
{{- printf "%s:%s" .Values.yarn.image.repository .Values.yarn.image.tag -}}
{{- end -}}
