# Apache Hadoop Helm Cluster Image

基于 Helm Chart 的 Apache Hadoop 3.3.6 集群镜像目录，可按 Sealos Helm Charts 集群镜像流程构建和安装。

## 运行镜像

Chart 默认使用以下运行镜像：

```text
crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey/sealos:hadoop-3.3.6
```

镜像需要包含 `/opt/hadoop`、`/opt/java`、`bash` 和 `python3`，默认通过该镜像启动 HDFS NameNode/DataNode 与 YARN ResourceManager/NodeManager。

## 构建

```bash
cd /Users/shoufengxia/Desktop/Code/templates
sealos build -t <your-registry>/helm-hadoop:<tag> ./helm/hadoop
sealos save -o hadoop-v3.3.6.tar <your-registry>/helm-hadoop:<tag>
```

## 安装

```bash
sealos run -f hadoop-v3.3.6.tar \
  --env NAMESPACE=ns-admin \
  --env HADOOP_IMAGE_REPOSITORY=crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey/sealos \
  --env HADOOP_IMAGE_TAG=hadoop-3.3.6 \
  --env HADOOP_IMAGE_PULL_POLICY=IfNotPresent \
  --env HADOOP_NAMENODE_REPLICAS=1 \
  --env HADOOP_DATANODE_REPLICAS=1 \
  --env HADOOP_RESOURCEMANAGER_REPLICAS=1 \
  --env HADOOP_NODEMANAGER_REPLICAS=1 \
  --env HADOOP_DFS_REPLICATION=1 \
  --env HADOOP_NAMENODE_STORAGE_CLASS=openebs-hostpath \
  --env HADOOP_NAMENODE_STORAGE_SIZE=10Gi \
  --env HADOOP_DATANODE_STORAGE_CLASS=openebs-hostpath \
  --env HADOOP_DATANODE_STORAGE_SIZE=20Gi \
  --env HADOOP_RM_STORAGE_CLASS=openebs-hostpath \
  --env HADOOP_RM_STORAGE_SIZE=5Gi \
  --env HADOOP_NM_STORAGE_CLASS=openebs-hostpath \
  --env HADOOP_NM_STORAGE_SIZE=20Gi \
  --env HADOOP_NAMENODE_REQUESTS_CPU=500m \
  --env HADOOP_NAMENODE_LIMITS_CPU=2 \
  --env HADOOP_NAMENODE_REQUESTS_MEMORY=1Gi \
  --env HADOOP_NAMENODE_LIMITS_MEMORY=2Gi \
  --env HADOOP_DATANODE_REQUESTS_CPU=500m \
  --env HADOOP_DATANODE_LIMITS_CPU=2 \
  --env HADOOP_DATANODE_REQUESTS_MEMORY=1Gi \
  --env HADOOP_DATANODE_LIMITS_MEMORY=2Gi \
  --env HADOOP_RM_REQUESTS_CPU=500m \
  --env HADOOP_RM_LIMITS_CPU=2 \
  --env HADOOP_RM_REQUESTS_MEMORY=1Gi \
  --env HADOOP_RM_LIMITS_MEMORY=2Gi \
  --env HADOOP_NM_REQUESTS_CPU=500m \
  --env HADOOP_NM_LIMITS_CPU=2 \
  --env HADOOP_NM_REQUESTS_MEMORY=2Gi \
  --env HADOOP_NM_LIMITS_MEMORY=4Gi \
  --env HADOOP_NODEMANAGER_MEMORY_MB=4096 \
  --env HADOOP_NODEMANAGER_VCORES=2 \
  --env HADOOP_SCHEDULER_MINIMUM_ALLOCATION_MB=128 \
  --env HADOOP_SCHEDULER_MAXIMUM_ALLOCATION_MB=4096 \
  --env HADOOP_LOG_AGGREGATION_ENABLED=false \
  --env SEALOS_CLOUD_DOMAIN=192.168.10.70.nip.io \
  --env SEALOS_CERT_SECRET_NAME=wildcard-cert \
  --env SEALOS_INGRESS_CLASS_NAME=nginx \
  --env SEALOS_INGRESS_ENABLED=true \
  --env SEALOS_APP_ENABLED=true \
  --env SEALOS_RESOURCEMANAGER_HOST_PREFIX=hadoop \
  --env SEALOS_NAMENODE_HOST_PREFIX=hadoop-namenode
```

部署完成后，Sealos 桌面默认会显示两个入口：

```text
https://hadoop.<domain>/
https://hadoop-namenode.<domain>/
```

内部服务地址：

```text
HDFS: hdfs://hadoop-namenode.ns-admin.svc.cluster.local:8020
YARN ResourceManager: hadoop-resourcemanager.ns-admin.svc.cluster.local:8088
```

## 常用参数

默认会创建 4 个 StatefulSet：NameNode、DataNode、ResourceManager、NodeManager。生产环境可以调整以下参数：

```bash
--env HADOOP_DATANODE_REPLICAS=3
--env HADOOP_NODEMANAGER_REPLICAS=3
--env HADOOP_DFS_REPLICATION=3
--env HADOOP_DATANODE_STORAGE_SIZE=100Gi
--env HADOOP_NM_STORAGE_SIZE=100Gi
--env SEALOS_RESOURCEMANAGER_HOST_PREFIX=hadoop
--env SEALOS_NAMENODE_HOST_PREFIX=hadoop-namenode
```

## 卸载

```bash
helm uninstall hadoop -n ns-admin
```

StatefulSet 的 PVC 默认会保留。确认不再需要数据后，可手动删除对应 PVC。
