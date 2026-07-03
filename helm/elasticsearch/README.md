# Elasticsearch Helm Cluster Image

基于 Helm Chart 的 Elasticsearch 集群镜像目录。

## 构建

```bash
cd /Users/shoufengxia/Desktop/Code/templates
sealos build -t <your-registry>/helm-elasticsearch:<tag> ./helm/elasticsearch
sealos push <your-registry>/helm-elasticsearch:<tag>
```

## 安装

```bash
sealos run <your-registry>/helm-elasticsearch:<tag> \
  --env NAMESPACE=ns-admin \
  --env IMAGE_TAG=7.17.28 \
  --env ELASTICSEARCH_STORAGE=100Gi \
  --env ELASTICSEARCH_STORAGE_CLASS=openebs-hostpath \
  --env ELASTICSEARCH_REQUESTS_CPU=1 \
  --env ELASTICSEARCH_LIMITS_CPU=2 \
  --env ELASTICSEARCH_REQUESTS_MEMORY=4Gi \
  --env ELASTICSEARCH_LIMITS_MEMORY=8Gi \
  --env ELASTICSEARCH_JAVA_HEAP=4g \
  --env ELASTICSEARCH_TLS_SECRET_NAME=elasticsearch-master-certs \
  --env ELASTICSEARCH_PASSWORD='<strong-password>'
```

## 环境变量

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `NAMESPACE` | `ns-admin` | 安装命名空间 |
| `IMAGE_TAG` | `7.17.28` | Elasticsearch 镜像版本 |
| `ELASTICSEARCH_STORAGE` | `100Gi` | 每个 Elasticsearch Pod 的数据卷容量 |
| `ELASTICSEARCH_STORAGE_CLASS` | `openebs-hostpath` | 数据卷 StorageClass |
| `ELASTICSEARCH_REQUESTS_CPU` | `1` | Elasticsearch 容器 CPU request |
| `ELASTICSEARCH_LIMITS_CPU` | `2` | Elasticsearch 容器 CPU limit |
| `ELASTICSEARCH_REQUESTS_MEMORY` | `4Gi` | Elasticsearch 容器内存 request |
| `ELASTICSEARCH_LIMITS_MEMORY` | `8Gi` | Elasticsearch 容器内存 limit |
| `ELASTICSEARCH_JAVA_HEAP` | `4g` | JVM heap 的 `-Xms` 和 `-Xmx` 值 |
| `ELASTICSEARCH_TLS_SECRET_NAME` | `elasticsearch-master-certs` | cert-manager 生成的节点 TLS Secret 名称 |
| `ELASTICSEARCH_PASSWORD` | `please-change-this-password` | `elastic` 用户密码，生产环境请覆盖 |
