# Apache ZooKeeper Helm Cluster Image

基于 Helm Chart 的 Apache ZooKeeper 3.7.2 集群镜像目录，可按 Sealos Helm Charts 集群镜像流程构建和安装。

## 运行镜像

Chart 默认使用以下运行镜像：

```text
crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey/sealos:zookeeper-3.7.2
```

该镜像可通过 `registry/zookeeper/Dockerfile` 从 Dragonwell 8 + Python 3 基础镜像构建：

```bash
cd /Users/shoufengxia/Desktop/Code/templates/helm/zookeeper/registry
REGISTRY=crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey ./build-zookeeper-image.sh
```

基础镜像：

```text
crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey/sealos:base-dragonwell8-python3
```

## 构建

```bash
cd /Users/shoufengxia/Desktop/Code/templates
sealos build -t <your-registry>/helm-zookeeper:<tag> ./helm/zookeeper
sealos push <your-registry>/helm-zookeeper:<tag>
```

## 安装

```bash
sealos run <your-registry>/helm-zookeeper:<tag> \
  --env NAMESPACE=ns-admin \
  --env ZOOKEEPER_REPLICAS=3 \
  --env ZOOKEEPER_IMAGE_REPOSITORY=crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey/sealos \
  --env ZOOKEEPER_IMAGE_TAG=zookeeper-3.7.2 \
  --env ZOOKEEPER_IMAGE_PULL_POLICY=IfNotPresent \
  --env ZOOKEEPER_STORAGE_CLASS=openebs-hostpath \
  --env ZOOKEEPER_STORAGE_SIZE=5Gi \
  --env ZOOKEEPER_REQUESTS_CPU=250m \
  --env ZOOKEEPER_LIMITS_CPU=1 \
  --env ZOOKEEPER_REQUESTS_MEMORY=512Mi \
  --env ZOOKEEPER_LIMITS_MEMORY=1Gi \
  --env ZOOKEEPER_HEAP_MIN=256m \
  --env ZOOKEEPER_HEAP_MAX=512m \
  --env ZOOKEEPER_TICK_TIME=2000 \
  --env ZOOKEEPER_INIT_LIMIT=10 \
  --env ZOOKEEPER_SYNC_LIMIT=5 \
  --env ZOOKEEPER_MAX_CLIENT_CNXNS=60 \
  --env ZOOKEEPER_4LW_COMMANDS_WHITELIST=ruok,srvr,mntr,conf \
  --env ZOOKEEPER_QUORUM_LISTEN_ON_ALL_IPS=true \
  --env ZOOKEEPER_AUTOPURGE_SNAP_RETAIN_COUNT=3 \
  --env ZOOKEEPER_AUTOPURGE_PURGE_INTERVAL=1 \
  --env ZOOKEEPER_ADMIN_SERVER_ENABLED=true \
  --env SEALOS_HOST_PREFIX=zookeeper \
  --env SEALOS_CLOUD_DOMAIN=<master-ip>.nip.io \
  --env SEALOS_CERT_SECRET_NAME=wildcard-cert \
  --env SEALOS_INGRESS_CLASS_NAME=nginx \
  --env SEALOS_INGRESS_ENABLED=false \
  --env SEALOS_APP_ENABLED=false
```

ZooKeeper 默认以 3 副本 StatefulSet 运行，内部连接地址为：

```text
zookeeper.ns-admin.svc.cluster.local:2181
```

如需显式连接每个 ensemble 成员，可使用稳定 Pod DNS：

```text
zookeeper-0.zookeeper-headless.ns-admin.svc.cluster.local:2181,zookeeper-1.zookeeper-headless.ns-admin.svc.cluster.local:2181,zookeeper-2.zookeeper-headless.ns-admin.svc.cluster.local:2181
```

如需通过 Sealos Ingress 访问 ZooKeeper AdminServer，可同时设置 `SEALOS_INGRESS_ENABLED=true` 和 `SEALOS_APP_ENABLED=true`。默认不暴露外部入口，因为 ZooKeeper 的主要访问协议是内部 TCP client port `2181`。

## 卸载

```bash
helm uninstall zookeeper -n ns-admin
```

StatefulSet 的 PVC 默认会保留。确认不再需要数据后，可手动删除对应 PVC。
