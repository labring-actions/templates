# Logstash Helm Cluster Image

基于 Helm Chart 的 Logstash 集群镜像目录。

## 构建

```bash
cd /Users/shoufengxia/Desktop/Code/templates
sealos build -t <your-registry>/helm-logstash:<tag> ./helm/logstash
sealos push <your-registry>/helm-logstash:<tag>
```

## 安装

```bash
sealos run <your-registry>/helm-logstash:<tag> \
  --env NAMESPACE=ns-admin \
  --env LOGSTASH_REPLICAS=1 \
  --env LOGSTASH_REQUESTS_CPU=1 \
  --env LOGSTASH_LIMITS_CPU=2 \
  --env LOGSTASH_REQUESTS_MEMORY=2Gi \
  --env LOGSTASH_LIMITS_MEMORY=4Gi \
  --env LOGSTASH_JAVA_HEAP=1g \
  --env ELASTICSEARCH_CA_SECRET_NAME=elasticsearch-ca-secret
```
