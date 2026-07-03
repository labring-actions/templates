# Kibana Cluster Image

这个目录用于构建一个“直接运行安装”的 Kibana Sealos 集群镜像。

## 依赖

- Elasticsearch 已部署完成
- `elasticsearch-master-credentials` Secret 已存在
- `elasticsearch-ca-secret` Secret 已存在
- `elasticsearch-ca-issuer` Issuer 已存在
- 集群存在可用的 Ingress Controller
- 集群存在 TLS Secret，默认使用 `wildcard-cert`

## 构建镜像

```bash
cd /Users/shoufengxia/Desktop/Code/templates
sealos build -t <your-registry>/elk-kibana:<tag> ./deploy/kibana
sealos push <your-registry>/elk-kibana:<tag>
```

## 运行安装

```bash
sealos run <your-registry>/elk-kibana:<tag> \
  --env elasticsearchNamespace=ns-admin \
  --env kibanaReplicas=1 \
  --env kibanaRequestsCPU=500m \
  --env kibanaLimitsCPU=1 \
  --env kibanaRequestsMemory=1Gi \
  --env kibanaLimitsMemory=2Gi \
  --env kibanaTLSSecretName=kibana-certs \
  --env elasticsearchCASecretName=elasticsearch-ca-secret \
  --env kibanaSystemPassword='<strong-password>' \
  --env SEALOS_CLOUD_DOMAIN=<master-ip>.nip.io \
  --env SEALOS_CERT_SECRET_NAME=wildcard-cert
```

默认公网访问地址：

```text
https://kibana.<master-ip>.nip.io/login
```

## 验证

```bash
kubectl rollout status deployment/kibana -n ns-admin --timeout=10m
kubectl get pods,svc,ingress -n ns-admin -l app=kibana
kubectl logs -n ns-admin deployment/kibana -c configure-kibana-system-user --tail=100
kubectl logs -n ns-admin deployment/kibana -c kibana --tail=100
```
