# Kibana Helm Cluster Image

基于 Helm Chart 的 Kibana 集群镜像目录。

## 构建

```bash
cd /Users/shoufengxia/Desktop/Code/templates
sealos build -t <your-registry>/helm-kibana:<tag> ./helm/kibana
sealos push <your-registry>/helm-kibana:<tag>
```

## 安装

```bash
sealos run <your-registry>/helm-kibana:<tag> \
  --env NAMESPACE=ns-admin \
  --env KIBANA_REPLICAS=1 \
  --env KIBANA_REQUESTS_CPU=500m \
  --env KIBANA_LIMITS_CPU=1 \
  --env KIBANA_REQUESTS_MEMORY=1Gi \
  --env KIBANA_LIMITS_MEMORY=2Gi \
  --env KIBANA_TLS_SECRET_NAME=kibana-certs \
  --env ELASTICSEARCH_CA_SECRET_NAME=elasticsearch-ca-secret \
  --env SEALOS_CLOUD_DOMAIN=<master-ip>.nip.io \
  --env SEALOS_CERT_SECRET_NAME=wildcard-cert
```

部署完成后，桌面会显示 Kibana 图标，点击进入：

```text
https://kibana.<master-ip>.nip.io/login
```
