# PolarDB-X Helm Cluster Image

基于 PolarDB-X Operator 官方安装文档与官方 Helm 仓库打包的 Sealos 集群镜像目录。

当前目录延续了 `helm/` 目录现有服务的组织形式，并且已经将 upstream `polardbx-operator` chart 完整 vendored 到本仓库：

- `Kubefile` 负责执行 `helm upgrade --install`
- `charts/polardbx-operator/` 保存官方 chart、CRD 与模板
- 安装时直接使用仓库内置 chart，不再依赖运行时下载

参考文档：

- https://doc.polardbx.com/operator/deployment/1-installation.html
- https://polardbx-charts.oss-cn-beijing.aliyuncs.com/index.yaml

## 构建

```bash
cd /Users/shoufengxia/Desktop/Code/templates
sealos build -t <your-registry>/helm-polardb-x:<tag> ./helm/polardb-x
sealos push <your-registry>/helm-polardb-x:<tag>
```

## 安装

```bash
sealos run <your-registry>/helm-polardb-x:<tag> \
  --env NAMESPACE=ns-admin \
  --env POLARDBX_RELEASE_NAME=polardbx-operator \
  --env POLARDBX_IMAGE_REPO=polardbx-opensource-registry.cn-beijing.cr.aliyuncs.com/polardbx \
  --env POLARDBX_IMAGE_TAG=v1.7.0 \
  --env POLARDBX_VERSION=v1.7.0 \
  --env POLARDBX_CLUSTER_VERSION=latest \
  --env POLARDBX_NODE_VOLUME_DATA=/data \
  --env POLARDBX_NODE_VOLUME_LOG=/data-log \
  --env POLARDBX_NODE_VOLUME_FILESTREAM=/filestream \
  --env POLARDBX_ALLOW_SCHEDULE_ON_MASTER=true \
  --env POLARDBX_ENABLE_EXPORTERS=true
```

## 常用环境变量

- `NAMESPACE`: Operator 安装命名空间，默认 `ns-admin`
- `POLARDBX_RELEASE_NAME`: Helm release 名称，默认 `polardbx-operator`
- `POLARDBX_IMAGE_REPO`: Operator 及默认集群镜像仓库
- `POLARDBX_IMAGE_TAG`: Operator 组件镜像标签
- `POLARDBX_VERSION`: 写入 PolarDB-X Cluster 与 XStore 注解的版本值
- `POLARDBX_CLUSTER_VERSION`: `clusterDefaults.version`，默认 `latest`
- `POLARDBX_NODE_VOLUME_DATA`: 节点数据目录
- `POLARDBX_NODE_VOLUME_LOG`: 节点日志目录
- `POLARDBX_NODE_VOLUME_FILESTREAM`: 节点文件流目录
- `POLARDBX_ALLOW_SCHEDULE_ON_MASTER`: 是否允许调度到 master 节点
- `POLARDBX_ENABLE_ACK_RESOURCE_CONTROLLER`: 是否启用 ACK 资源控制器
- `POLARDBX_ENABLE_EXPORTERS`: 是否为 PolarDB-X Pod 创建 exporter sidecar

## 说明

- `charts/polardbx-operator` 直接来自官方 Helm 仓库中的 `polardbx-operator` `1.7.0` 包。
- 当前镜像使用 vendored chart，本地构建完成后，`sealos run` 不再依赖外部网络去下载 upstream chart。
- 如果后续需要覆盖更多官方 values，可以直接编辑 [values.yaml](/Users/shoufengxia/Desktop/Code/templates/helm/polardb-x/charts/polardbx-operator/values.yaml) 或继续在 `Kubefile` 里追加 `--set` 参数。
