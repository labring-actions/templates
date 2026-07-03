# Apache HDFS Helm Cluster Image

基于 Helm Chart 的 Apache HDFS 3.3.6 集群镜像目录，可按 Sealos Helm Charts 集群镜像流程构建和安装。

## 运行镜像

Chart 默认使用以下运行镜像：

```text
crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey/sealos:hdfs-3.3.6
```

镜像需要包含 `/opt/hadoop`、`/opt/java`、`bash` 和 `python3`，默认通过该镜像启动 HDFS NameNode 与 DataNode。

## 构建

```bash
cd /Users/shoufengxia/Desktop/Code/templates
sealos build -t <your-registry>/helm-hdfs:<tag> ./helm/hdfs
sealos save -o hdfs-v3.3.6.tar <your-registry>/helm-hdfs:<tag>
```

## 安装

```bash
sealos run -f hdfs-v3.3.6.tar \
  --env NAMESPACE=ns-admin \
  --env HDFS_IMAGE_REPOSITORY=crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey/sealos \
  --env HDFS_IMAGE_TAG=hdfs-3.3.6 \
  --env HDFS_IMAGE_PULL_POLICY=IfNotPresent \
  --env HDFS_NAMENODE_REPLICAS=1 \
  --env HDFS_DATANODE_REPLICAS=1 \
  --env HDFS_DFS_REPLICATION=1 \
  --env HDFS_PERMISSIONS_ENABLED=false \
  --env HDFS_NAMENODE_STORAGE_CLASS=openebs-hostpath \
  --env HDFS_NAMENODE_STORAGE_SIZE=10Gi \
  --env HDFS_DATANODE_STORAGE_CLASS=openebs-hostpath \
  --env HDFS_DATANODE_STORAGE_SIZE=20Gi \
  --env HDFS_NAMENODE_REQUESTS_CPU=500m \
  --env HDFS_NAMENODE_LIMITS_CPU=2 \
  --env HDFS_NAMENODE_REQUESTS_MEMORY=1Gi \
  --env HDFS_NAMENODE_LIMITS_MEMORY=2Gi \
  --env HDFS_DATANODE_REQUESTS_CPU=500m \
  --env HDFS_DATANODE_LIMITS_CPU=2 \
  --env HDFS_DATANODE_REQUESTS_MEMORY=1Gi \
  --env HDFS_DATANODE_LIMITS_MEMORY=2Gi \
  --env SEALOS_CLOUD_DOMAIN=192.168.10.70.nip.io \
  --env SEALOS_CERT_SECRET_NAME=wildcard-cert \
  --env SEALOS_INGRESS_CLASS_NAME=nginx \
  --env SEALOS_INGRESS_ENABLED=true \
  --env SEALOS_APP_ENABLED=true \
  --env SEALOS_HOST_PREFIX=hdfs
```

部署完成后，Sealos 桌面默认会显示 NameNode UI 入口：

```text
https://hdfs.<domain>/
```

内部 HDFS 地址：

```text
hdfs://hdfs-namenode.ns-admin.svc.cluster.local:8020
```

## 常用参数

生产环境可按副本数同步调整 DataNode 和 HDFS 副本数：

```bash
--env HDFS_DATANODE_REPLICAS=3
--env HDFS_DFS_REPLICATION=3
--env HDFS_DATANODE_STORAGE_SIZE=100Gi
```

## 卸载

```bash
helm uninstall hdfs -n ns-admin
```

StatefulSet 的 PVC 默认会保留。确认不再需要数据后，可手动删除对应 PVC。
