{{- define "zookeeper.name" -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "zookeeper.headlessName" -}}
{{- printf "%s-headless" (include "zookeeper.name" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "zookeeper.image" -}}
{{- printf "%s:%s" .Values.zookeeper.image.repository .Values.zookeeper.image.tag -}}
{{- end -}}

{{- define "zookeeper.clientConnectionString" -}}
{{- $name := include "zookeeper.name" . -}}
{{- $headlessName := include "zookeeper.headlessName" . -}}
{{- $namespace := .Release.Namespace -}}
{{- $clientPort := .Values.zookeeper.service.clientPort -}}
{{- $servers := list -}}
{{- range $i := until (int .Values.zookeeper.replicas) -}}
{{- $servers = append $servers (printf "%s-%d.%s.%s.svc.cluster.local:%v" $name $i $headlessName $namespace $clientPort) -}}
{{- end -}}
{{- join "," $servers -}}
{{- end -}}
