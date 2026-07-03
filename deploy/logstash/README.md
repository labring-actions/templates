# Logstash Cluster Image

这个目录用于构建一个“直接运行安装”的 Logstash Sealos 集群镜像。

## 依赖

- Elasticsearch 已部署完成
- `elasticsearch-master-credentials` Secret 已存在
- `elasticsearch-ca-secret` Secret 已存在
- 默认假设 Logstash 与 Elasticsearch 部署在同一个 namespace

## 构建镜像

```bash
cd /Users/shoufengxia/Desktop/Code/templates
sealos build -t <your-registry>/elk-logstash:<tag> ./deploy/logstash
sealos push <your-registry>/elk-logstash:<tag>
```

## 运行安装

```bash
sealos run <your-registry>/elk-logstash:<tag> \
  --env elasticsearchNamespace=ns-admin \
  --env logstashReplicas=1 \
  --env logstashRequestsCPU=1 \
  --env logstashLimitsCPU=2 \
  --env logstashRequestsMemory=2Gi \
  --env logstashLimitsMemory=4Gi \
  --env logstashJavaHeap=1g \
  --env elasticsearchCASecretName=elasticsearch-ca-secret
```

## 验证

```bash
kubectl rollout status deployment/logstash -n ns-admin --timeout=10m
kubectl get pods,svc -n ns-admin -l app=logstash
kubectl logs -n ns-admin deployment/logstash --tail=100
```
