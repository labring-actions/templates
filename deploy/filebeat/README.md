# Filebeat Cluster Image

这个目录用于构建一个“直接运行安装”的 Filebeat Sealos 集群镜像。

## 依赖

- Logstash 已部署完成
- 默认假设 Filebeat 与 Logstash 部署在同一个 namespace
- 目标节点存在 `/var/log/containers` 和 `/var/log/pods`
- 集群运行时为 `containerd`

## 构建镜像

```bash
cd /Users/shoufengxia/Desktop/Code/templates
sealos build -t <your-registry>/elk-filebeat:<tag> ./deploy/filebeat
sealos push <your-registry>/elk-filebeat:<tag>
```

## 运行安装

```bash
sealos run <your-registry>/elk-filebeat:<tag> \
  --env elasticsearchNamespace=ns-admin \
  --env filebeatRequestsCPU=100m \
  --env filebeatLimitsCPU=300m \
  --env filebeatRequestsMemory=200Mi \
  --env filebeatLimitsMemory=500Mi
```

## 验证

```bash
kubectl rollout status daemonset/filebeat -n ns-admin --timeout=10m
kubectl get pods -n ns-admin -l app=filebeat -o wide
kubectl logs -n ns-admin $(kubectl get pods -n ns-admin -l app=filebeat -o jsonpath='{.items[0].metadata.name}') --tail=100
```
