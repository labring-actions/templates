# Filebeat Helm Cluster Image

基于 Helm Chart 的 Filebeat 集群镜像目录。

## 构建

```bash
cd /Users/shoufengxia/Desktop/Code/templates
sealos build -t <your-registry>/helm-filebeat:<tag> ./helm/filebeat
sealos push <your-registry>/helm-filebeat:<tag>
```

## 安装

```bash
sealos run <your-registry>/helm-filebeat:<tag> \
  --env NAMESPACE=ns-admin \
  --env FILEBEAT_REQUESTS_CPU=100m \
  --env FILEBEAT_LIMITS_CPU=300m \
  --env FILEBEAT_REQUESTS_MEMORY=200Mi \
  --env FILEBEAT_LIMITS_MEMORY=500Mi
```
