# Apache Hadoop YARN Helm Cluster Image

基于 Helm Chart 的 Apache Hadoop YARN 3.3.6 集群镜像目录，可按 Sealos Helm Charts 集群镜像流程构建和安装。

## 运行镜像

Chart 默认使用以下运行镜像：

```text
crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey/sealos:yarn-3.3.6
```

镜像需要包含 `/opt/hadoop`、`/opt/java`、`bash` 和 `python3`，默认通过该镜像启动 YARN ResourceManager 与 NodeManager。

## 构建

```bash
cd /Users/shoufengxia/Desktop/Code/templates
sealos build -t <your-registry>/helm-yarn:<tag> ./helm/yarn
sealos save -o yarn-v3.3.6.tar <your-registry>/helm-yarn:<tag>
```

## 安装

```bash
sealos run -f yarn-v3.3.6.tar \
  --env NAMESPACE=ns-admin \
  --env YARN_IMAGE_REPOSITORY=crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey/sealos \
  --env YARN_IMAGE_TAG=yarn-3.3.6 \
  --env YARN_IMAGE_PULL_POLICY=IfNotPresent \
  --env YARN_RESOURCEMANAGER_REPLICAS=1 \
  --env YARN_NODEMANAGER_REPLICAS=1 \
  --env YARN_FS_DEFAULT_URI=file:/// \
  --env YARN_RM_STORAGE_CLASS=openebs-hostpath \
  --env YARN_RM_STORAGE_SIZE=5Gi \
  --env YARN_NM_STORAGE_CLASS=openebs-hostpath \
  --env YARN_NM_STORAGE_SIZE=20Gi \
  --env YARN_RM_REQUESTS_CPU=500m \
  --env YARN_RM_LIMITS_CPU=2 \
  --env YARN_RM_REQUESTS_MEMORY=1Gi \
  --env YARN_RM_LIMITS_MEMORY=2Gi \
  --env YARN_NM_REQUESTS_CPU=500m \
  --env YARN_NM_LIMITS_CPU=2 \
  --env YARN_NM_REQUESTS_MEMORY=2Gi \
  --env YARN_NM_LIMITS_MEMORY=4Gi \
  --env YARN_NODEMANAGER_MEMORY_MB=4096 \
  --env YARN_NODEMANAGER_VCORES=2 \
  --env YARN_SCHEDULER_MINIMUM_ALLOCATION_MB=128 \
  --env YARN_SCHEDULER_MAXIMUM_ALLOCATION_MB=4096 \
  --env YARN_LOG_AGGREGATION_ENABLED=false \
  --env SEALOS_CLOUD_DOMAIN=192.168.10.70.nip.io \
  --env SEALOS_CERT_SECRET_NAME=wildcard-cert \
  --env SEALOS_INGRESS_CLASS_NAME=nginx \
  --env SEALOS_INGRESS_ENABLED=true \
  --env SEALOS_APP_ENABLED=true \
  --env SEALOS_HOST_PREFIX=yarn
```

部署完成后，Sealos 桌面默认会显示 ResourceManager UI 入口：

```text
https://yarn.<domain>/
```

内部 ResourceManager 地址：

```text
yarn-resourcemanager.ns-admin.svc.cluster.local:8088
```

默认 `YARN_FS_DEFAULT_URI=file:///`，适合独立启动 YARN。若要连接前面打包的 HDFS，可设置：

```bash
--env YARN_FS_DEFAULT_URI=hdfs://hdfs-namenode.ns-admin.svc.cluster.local:8020
```

## 卸载

```bash
helm uninstall yarn -n ns-admin
```

StatefulSet 的 PVC 默认会保留。确认不再需要数据后，可手动删除对应 PVC。
