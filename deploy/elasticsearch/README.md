# Elasticsearch Cluster Image

这个目录用于构建一个“直接运行安装”的 Sealos 集群镜像。

## 目录结构

- `Kubefile`: 集群镜像构建文件
- `manifests/elasticsearch.yaml.tmpl`: 基于 go-template 的 Elasticsearch 安装清单
- `registry/`: Sealos 构建时使用的目录，占位即可

## 前置条件

- 集群已安装 `cert-manager`
- 目标集群存在可用的 StorageClass，默认是 `openebs-hostpath`
- 目标集群允许 Elasticsearch 使用特权 initContainer 设置 `vm.max_map_count`

## 构建镜像

在 `templates` 仓库根目录执行：

```bash
cd /Users/shoufengxia/Desktop/Code/templates
sealos build -t <your-registry>/elk-elasticsearch:<tag> ./deploy/elasticsearch
sealos push <your-registry>/elk-elasticsearch:<tag>
```

## 运行安装

```bash
sealos run <your-registry>/elk-elasticsearch:<tag> \
  --env elasticsearchNamespace=ns-admin \
  --env elasticsearchStorage=100 \
  --env elasticsearchStorageClass=openebs-hostpath \
  --env elasticsearchRequestsCPU=1 \
  --env elasticsearchLimitsCPU=2 \
  --env elasticsearchRequestsMemory=4Gi \
  --env elasticsearchLimitsMemory=8Gi \
  --env elasticsearchJavaHeap=4g \
  --env elasticsearchTLSSecretName=elasticsearch-master-certs \
  --env elasticsearchPassword='<strong-password>'
```

## 默认参数

`Kubefile` 中已经内置以下默认值，不传 `--env` 时会使用它们：

- `elasticsearchNamespace=ns-admin`
- `elasticsearchStorage=100`
- `elasticsearchStorageClass=openebs-hostpath`
- `elasticsearchRequestsCPU=1`
- `elasticsearchLimitsCPU=2`
- `elasticsearchRequestsMemory=4Gi`
- `elasticsearchLimitsMemory=8Gi`
- `elasticsearchJavaHeap=4g`
- `elasticsearchTLSSecretName=elasticsearch-master-certs`
- `elasticsearchPassword=please-change-this-password`

## 验证

```bash
kubectl get pods,svc,pvc -n ns-admin -l app=elasticsearch-master
kubectl get issuer,certificate -n ns-admin
kubectl get secret elasticsearch-master-credentials -n ns-admin
```

取出密码并验证集群健康：

```bash
ES_PASS=$(kubectl get secret elasticsearch-master-credentials -n ns-admin -o jsonpath='{.data.password}' | base64 -d)
kubectl exec -n ns-admin elasticsearch-master-0 -- \
  curl -sk -u "elastic:${ES_PASS}" https://127.0.0.1:9200/_cluster/health?pretty
```
