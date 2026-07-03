{{- define "hdfs.name" -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hdfs.configName" -}}
{{- printf "%s-config" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hdfs.nameNodeName" -}}
{{- printf "%s-namenode" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hdfs.dataNodeName" -}}
{{- printf "%s-datanode" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hdfs.nameNodeHost" -}}
{{- printf "%s.%s.svc.cluster.local" (include "hdfs.nameNodeName" .) .Release.Namespace -}}
{{- end -}}

{{- define "hdfs.image" -}}
{{- printf "%s:%s" .Values.hdfs.image.repository .Values.hdfs.image.tag -}}
{{- end -}}
