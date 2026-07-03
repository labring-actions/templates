# ELK 部署顺序与验证方案

本文基于当前目录下这 4 份文件编写：

- `elasticsearch.yaml`
- `logstash.yaml`
- `filebeat.yaml`
- `kibana.yaml`

当前约束和前提：

- 4 个组件默认 namespace 已统一为 `ns-admin`
- Filebeat 已排除 `filebeat` 和 `logstash` 自身日志
- 集群运行时为 `containerd`
- 以下流程默认你和 Elasticsearch 一样，通过当前的 `Template` 资源方式进行部署

如果你的 Elasticsearch 已经在集群中部署成功并且健康，可直接从“步骤 3. 部署 Logstash”开始。

## 1. 推荐部署顺序

推荐顺序如下：

1. Elasticsearch
2. Logstash
3. Filebeat
4. Kibana

原因：

- Logstash 依赖 Elasticsearch 的 Service、密码 Secret 和 CA Secret
- Filebeat 依赖 Logstash 的 Service
- Kibana 依赖 Elasticsearch 的 Service、密码 Secret、CA Secret 和 CA Issuer，并会在启动前为 `kibana_system` 内置用户设置密码

虽然 Kibana 也可以在 Elasticsearch 之后立即部署，但放在最后更方便一次性验证“日志链路 + UI 展示”。

## 2. 部署前检查

### 2.1 检查 namespace

```bash
kubectl get ns ns-admin
```

如果不存在，先创建：

```bash
kubectl create ns ns-admin
```

### 2.2 检查 cert-manager

```bash
kubectl get pods -n cert-manager
kubectl get crd certificates.cert-manager.io issuers.cert-manager.io
```

预期：

- `cert-manager` 命名空间下相关 Pod 为 `Running`
- `Certificate` 和 `Issuer` 两个 CRD 已存在

### 2.3 检查存储类

`elasticsearch.yaml` 默认使用 `openebs-hostpath`：

```bash
kubectl get sc
```

如果你的集群没有这个 StorageClass，需要先改 `elasticsearch.yaml` 里的默认值或在部署时覆盖参数。

## 3. 部署 Elasticsearch

### 3.1 执行部署

```bash
kubectl apply -f elasticsearch.yaml
```

### 3.2 等待资源就绪

```bash
kubectl rollout status statefulset/elasticsearch-master -n ns-admin --timeout=15m
kubectl get pods,svc,pvc -n ns-admin -l app=elasticsearch-master
kubectl get issuer,certificate -n ns-admin
```

预期：

- `elasticsearch-master-0/1/2` 为 `Running`
- StatefulSet rollout 成功
- PVC 均已 `Bound`
- `elasticsearch-ca`、`elasticsearch-master-certs` 证书状态为 `Ready=True`

### 3.3 验证 Elasticsearch 健康

先取出密码：

```bash
ES_PASS=$(kubectl get secret elasticsearch-master-credentials -n ns-admin -o jsonpath='{.data.password}' | base64 -d)
echo "$ES_PASS"
```

检查集群健康：

```bash
kubectl exec -n ns-admin elasticsearch-master-0 -- \
  curl -sk -u "elastic:${ES_PASS}" https://127.0.0.1:9200/_cluster/health?pretty
```

查看节点：

```bash
kubectl exec -n ns-admin elasticsearch-master-0 -- \
  curl -sk -u "elastic:${ES_PASS}" https://127.0.0.1:9200/_cat/nodes?v
```

预期：

- `_cluster/health` 返回 `green` 或 `yellow`
- `_cat/nodes` 能看到 3 个节点

## 4. 部署 Logstash

### 4.1 执行部署

```bash
kubectl apply -f logstash.yaml
```

### 4.2 等待资源就绪

```bash
kubectl rollout status deployment/logstash -n ns-admin --timeout=10m
kubectl get pods,svc -n ns-admin -l app=logstash
```

预期：

- `logstash` Pod 为 `Running`
- `logstash` Service 已创建
- `5044` 和 `9600` 端口可见

### 4.3 验证 Logstash 到 Elasticsearch 的连通性

查看日志：

```bash
kubectl logs -n ns-admin deployment/logstash --tail=100
```

重点关注是否出现以下错误：

- Elasticsearch 认证失败
- SSL 证书校验失败
- 无法解析 `elasticsearch-master.ns-admin.svc`

可选验证 API：

```bash
kubectl port-forward -n ns-admin svc/logstash 9600:9600
```

本地另开一个终端执行：

```bash
curl http://127.0.0.1:9600/?pretty
curl http://127.0.0.1:9600/_node/pipelines?pretty
```

预期：

- 能返回 Logstash 节点和 pipeline 信息
- `logstash.conf` 已被加载

## 5. 部署 Filebeat

### 5.1 执行部署

```bash
kubectl apply -f filebeat.yaml
```

### 5.2 等待资源就绪

```bash
kubectl rollout status daemonset/filebeat -n ns-admin --timeout=10m
kubectl get pods -n ns-admin -l app=filebeat -o wide
```

预期：

- 每个需要采集日志的节点上都有一个 Filebeat Pod
- Pod 状态为 `Running`

### 5.3 验证 Filebeat 到 Logstash 的链路

先挑一个 Pod 看日志：

```bash
kubectl get pods -n ns-admin -l app=filebeat
kubectl logs -n ns-admin <任意一个-filebeat-pod-name> --tail=100
```

重点关注是否出现以下错误：

- 连接 `logstash.ns-admin.svc:5044` 失败
- 权限不足，无法读取 `/var/log/containers`
- 采集器初始化失败

### 5.4 造一条测试日志

部署一个测试 Pod 持续打印日志：

```bash
kubectl run log-producer -n ns-admin \
  --image=busybox:1.36 \
  --restart=Never \
  -- sh -c 'i=0; while true; do echo "$(date) elk smoke test $i"; i=$((i+1)); sleep 5; done'
```

确认测试 Pod 已启动：

```bash
kubectl get pod log-producer -n ns-admin
kubectl logs -n ns-admin log-producer --tail=5
```

### 5.5 验证日志已进入 Elasticsearch

查看是否已生成 `logstash-*` 索引：

```bash
kubectl exec -n ns-admin elasticsearch-master-0 -- \
  curl -sk -u "elastic:${ES_PASS}" https://127.0.0.1:9200/_cat/indices/logstash-*?v
```

查询测试日志：

```bash
kubectl exec -n ns-admin elasticsearch-master-0 -- \
  curl -sk -u "elastic:${ES_PASS}" \
  -H 'Content-Type: application/json' \
  https://127.0.0.1:9200/logstash-*/_search \
  -d '{"size":5,"sort":[{"@timestamp":"desc"}],"query":{"match_phrase":{"message":"elk smoke test"}}}'
```

预期：

- 能看到 `logstash-YYYY.MM.dd` 索引
- 搜索结果里能查到 `elk smoke test`

### 5.6 验证 Filebeat 已排除自身和 Logstash 日志

检查最近 10 分钟内是否还写入了 `filebeat` 或 `logstash` 自身日志：

```bash
kubectl exec -n ns-admin elasticsearch-master-0 -- \
  curl -sk -u "elastic:${ES_PASS}" \
  -H 'Content-Type: application/json' \
  https://127.0.0.1:9200/logstash-*/_count \
  -d '{"query":{"bool":{"filter":[{"terms":{"kubernetes.container.name":["filebeat","logstash"]}},{"range":{"@timestamp":{"gte":"now-10m"}}}]}}}'
```

预期：

- `count` 为 `0`

说明：

- 这个检查只看最近 10 分钟，避免被历史旧数据干扰
- 如果刚好在变更前已经写入过旧日志，不影响这个验证结论

## 6. 部署 Kibana

### 6.1 执行部署

```bash
kubectl apply -f kibana.yaml
```

### 6.2 等待资源就绪

```bash
kubectl rollout status deployment/kibana -n ns-admin --timeout=10m
kubectl get pods,svc -n ns-admin -l app=kibana
kubectl get configmap kibana-access-info -n ns-admin -o yaml
```

预期：

- `kibana` Pod 为 `Running`
- `kibana` Service 已创建
- `kibana-system-credentials` Secret 已存在
- `kibana-access-info` 中能看到集群内访问地址

说明：

- `kibana.yaml` 现在新增了 `kibana_service_type` 输入项，默认值为 `ClusterIP`
- 当 `kibana_service_type=ClusterIP` 时，Kibana 只在集群内可访问
- 集群内访问地址可参考 `kibana-access-info` ConfigMap 中的 `internal_url` 和 `internal_fqdn_url`

### 6.3 验证 Kibana 页面和 Elasticsearch 连接

先建立本地转发：

```bash
kubectl port-forward -n ns-admin svc/kibana 5601:5601
```

浏览器访问：

```text
https://127.0.0.1:5601
```

登录账号：

- 用户名：`elastic`
- 密码：`elasticsearch-master-credentials` Secret 中的 password

如果只做命令行验证：

```bash
curl -k -I https://127.0.0.1:5601/login
```

如果要从集群内其他 Pod 访问 Kibana，可使用：

```bash
curl -k -I https://kibana.ns-admin.svc:5601/login
curl -k -I https://kibana.ns-admin.svc.cluster.local:5601/login
```

预期：

- 返回 `200` 或 `302`
- Kibana 页面可以正常打开
- 登录后没有 “Kibana server is not ready yet” 或 Elasticsearch 连接失败提示

### 6.4 验证 Kibana 中的数据展示

在 Kibana 中创建 Data View：

- 名称：`logstash-*`
- 时间字段：`@timestamp`

进入 Discover：

- 搜索 `elk smoke test`
- 预期能看到测试 Pod 打出来的日志

## 7. 一次性总体验证清单

按顺序完成后，建议再做一遍总体验证：

1. `kubectl get pods -n ns-admin`
2. `kubectl get svc -n ns-admin`
3. `kubectl get pvc -n ns-admin`
4. `kubectl get certificate,issuer -n ns-admin`
5. Elasticsearch 健康检查返回 `green` 或 `yellow`
6. Logstash 日志中没有认证或 TLS 报错
7. Filebeat DaemonSet 在目标节点全部就绪
8. `logstash-*` 索引已创建
9. Kibana 可以登录并检索到测试日志
10. 最近 10 分钟内 `filebeat` 和 `logstash` 自身日志计数为 `0`

## 8. 常见失败点与排查顺序

### 8.1 Kibana 起不来

优先检查：

```bash
kubectl describe pod -n ns-admin -l app=kibana
kubectl logs -n ns-admin deployment/kibana --tail=100
kubectl get secret kibana-certs kibana-system-credentials elasticsearch-master-credentials elasticsearch-ca-secret -n ns-admin
kubectl get issuer elasticsearch-ca-issuer -n ns-admin
```

重点看：

- `kibana-certs` 是否已签发
- `kibana-system-credentials` 是否存在
- `elasticsearch-ca-issuer` 是否存在
- Elasticsearch 密码 Secret 是否存在

### 8.2 Logstash 起不来

优先检查：

```bash
kubectl describe pod -n ns-admin -l app=logstash
kubectl logs -n ns-admin deployment/logstash --tail=100
```

重点看：

- Elasticsearch 用户名密码是否正确
- `elasticsearch-ca-secret` 是否存在
- DNS `elasticsearch-master.ns-admin.svc` 是否可解析

### 8.3 Filebeat 没有把日志送进来

优先检查：

```bash
kubectl describe pod -n ns-admin -l app=filebeat
kubectl logs -n ns-admin <任意一个-filebeat-pod-name> --tail=100
kubectl get svc logstash -n ns-admin
```

重点看：

- 是否能连到 `logstash.ns-admin.svc:5044`
- 节点上是否存在 `/var/log/containers`
- DaemonSet 是否在所有目标节点调度成功

## 9. 验证完成后的清理

如果你用了测试日志 Pod，验证完成后可以删除：

```bash
kubectl delete pod log-producer -n ns-admin
```

如果你只是增量部署 Logstash、Filebeat、Kibana，而不重建 Elasticsearch，这份文档可以直接复用。
