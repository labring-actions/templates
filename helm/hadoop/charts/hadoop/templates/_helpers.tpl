{{- define "hadoop.name" -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hadoop.configName" -}}
{{- printf "%s-config" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hadoop.nameNodeName" -}}
{{- printf "%s-namenode" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hadoop.dataNodeName" -}}
{{- printf "%s-datanode" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hadoop.resourceManagerName" -}}
{{- printf "%s-resourcemanager" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hadoop.nodeManagerName" -}}
{{- printf "%s-nodemanager" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hadoop.nameNodeHost" -}}
{{- printf "%s.%s.svc.cluster.local" (include "hadoop.nameNodeName" .) .Release.Namespace -}}
{{- end -}}

{{- define "hadoop.resourceManagerHost" -}}
{{- printf "%s.%s.svc.cluster.local" (include "hadoop.resourceManagerName" .) .Release.Namespace -}}
{{- end -}}

{{- define "hadoop.image" -}}
{{- printf "%s:%s" .Values.hadoop.image.repository .Values.hadoop.image.tag -}}
{{- end -}}
