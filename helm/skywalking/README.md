# SkyWalking Helm Cluster Image

基于 Helm Chart 的 Apache SkyWalking 10.4.0 集群镜像目录。

默认部署组件：

- SkyWalking OAP Server
- SkyWalking UI
- 单节点 BanyanDB 存储
- UI Ingress 和 Sealos 桌面入口

OAP 和 UI 默认使用基于 Dragonwell 21 重新打包的镜像；BanyanDB 是 Go 服务，不需要 Dragonwell 基础镜像。

## 构建 Dragonwell 运行镜像

先构建并推送 OAP/UI 的 Dragonwell 版镜像。即使只在本地打包，也需要一个本地 registry 作为 `sealos build` 保存镜像时的读取源。

启动本地 registry：

```bash
docker run -d --restart=always -p 5000:5000 --name local-registry registry:2
```

构建并推送到本地 registry。脚本会在推送成功后自动把 chart 默认镜像仓库更新为 `localhost:5000/...`：

```bash
cd /Users/shoufengxia/Desktop/Code/templates/helm/skywalking/registry
REGISTRY=localhost:5000 ./build-dragonwell-images.sh
```

默认构建结果：

```text
localhost:5000/skywalking-oap-server-dragonwell:10.4.0-dragonwell21
localhost:5000/skywalking-ui-dragonwell:10.4.0-dragonwell21
```

`REGISTRY` 必须是完整镜像仓库前缀。本地构建填 `localhost:5000`；远端构建可填 `registry.cn-hangzhou.aliyuncs.com/<namespace>`。不要使用未带 registry 的本地镜像名，否则 `sealos build` 会把它解析成 `docker.io/library/...` 并尝试从 Docker Hub 拉取。

执行 `sealos build` 前可以先确认渲染结果：

```bash
cd /Users/shoufengxia/Desktop/Code/templates
helm template skywalking helm/skywalking/charts/skywalking --namespace ns-admin | grep 'image:'
```

OAP/UI 必须显示为完整仓库地址，例如：

```text
image: "crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey/skywalking-oap-server-dragonwell:10.4.0-dragonwell21"
image: "crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey/skywalking-ui-dragonwell:10.4.0-dragonwell21"
```

如果 OAP/UI 镜像在本地机器构建并推送，但 `sealos build` 在另一台服务器上执行，需要把 chart 镜像地址同步到服务器。两种方式任选一种：

```bash
# 方式一：把本地更新后的 helm/skywalking 目录同步到服务器
rsync -av /Users/shoufengxia/Desktop/Code/templates/helm/skywalking/ <user>@<server>:/path/to/templates/helm/skywalking/
```

```bash
# 方式二：在服务器上的仓库目录只更新 chart 镜像地址，不构建镜像
cd /path/to/templates
REGISTRY=crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey \
  ./helm/skywalking/registry/update-chart-images.sh

helm template skywalking helm/skywalking/charts/skywalking --namespace ns-admin | grep 'image:'
sealos build -t <your-registry>/helm-skywalking:<tag> ./helm/skywalking
```

## 构建

```bash
cd /Users/shoufengxia/Desktop/Code/templates
sealos build -t <your-registry>/helm-skywalking:<tag> ./helm/skywalking
sealos push <your-registry>/helm-skywalking:<tag>
```

## 安装

```bash
sealos run <your-registry>/helm-skywalking:<tag> \
  --env NAMESPACE=ns-admin \
  --env SKYWALKING_OAP_REPLICAS=1 \
  --env SKYWALKING_UI_REPLICAS=1 \
  --env SKYWALKING_OAP_IMAGE_REPOSITORY=localhost:5000/skywalking-oap-server-dragonwell \
  --env SKYWALKING_UI_IMAGE_REPOSITORY=localhost:5000/skywalking-ui-dragonwell \
  --env SKYWALKING_IMAGE_TAG=10.4.0-dragonwell21 \
  --env SKYWALKING_IMAGE_PULL_POLICY=IfNotPresent \
  --env SKYWALKING_UI_OAP_ADDRESS=http://skywalking-oap:12800 \
  --env SKYWALKING_UI_ZIPKIN_ADDRESS=http://skywalking-oap:9412 \
  --env SKYWALKING_STORAGE_TYPE=banyandb \
  --env SKYWALKING_BANYANDB_TARGETS=skywalking-banyandb:17912 \
  --env SKYWALKING_BANYANDB_ENABLED=true \
  --env SKYWALKING_BANYANDB_IMAGE_REPOSITORY=apache/skywalking-banyandb \
  --env SKYWALKING_BANYANDB_IMAGE_TAG=0.10.1 \
  --env SKYWALKING_BANYANDB_STORAGE_CLASS=openebs-hostpath \
  --env SKYWALKING_BANYANDB_STORAGE_SIZE=20Gi \
  --env SKYWALKING_OAP_REQUESTS_CPU=500m \
  --env SKYWALKING_OAP_LIMITS_CPU=2 \
  --env SKYWALKING_OAP_REQUESTS_MEMORY=1Gi \
  --env SKYWALKING_OAP_LIMITS_MEMORY=2Gi \
  --env SKYWALKING_UI_REQUESTS_CPU=100m \
  --env SKYWALKING_UI_LIMITS_CPU=500m \
  --env SKYWALKING_UI_REQUESTS_MEMORY=256Mi \
  --env SKYWALKING_UI_LIMITS_MEMORY=1Gi \
  --env SKYWALKING_BANYANDB_REQUESTS_CPU=500m \
  --env SKYWALKING_BANYANDB_LIMITS_CPU=2 \
  --env SKYWALKING_BANYANDB_REQUESTS_MEMORY=1Gi \
  --env SKYWALKING_BANYANDB_LIMITS_MEMORY=4Gi \
  --env SEALOS_HOST_PREFIX=skywalking \
  --env SEALOS_CLOUD_DOMAIN=<master-ip>.nip.io \
  --env SEALOS_CERT_SECRET_NAME=wildcard-cert \
  --env SEALOS_INGRESS_CLASS_NAME=nginx \
  --env SEALOS_APP_ENABLED=true
```

部署完成后，桌面会显示 SkyWalking 图标，点击进入：

```text
https://skywalking.<master-ip>.nip.io/
```

应用接入 SkyWalking OAP 时，集群内默认地址为：

```text
skywalking-oap.ns-admin.svc.cluster.local:11800
```

如果要使用外部 BanyanDB，可设置：

```bash
--env SKYWALKING_BANYANDB_ENABLED=false \
--env SKYWALKING_BANYANDB_TARGETS=<banyandb-host>:17912
```

默认 chart 只对外暴露 UI。OAP 的 gRPC、HTTP 和 Zipkin 端口通过 `skywalking-oap` Service 在集群内访问。

SkyWalking OAP 10.4.0 要求 BanyanDB server API 版本为 `0.10`。如果使用 `apache/skywalking-banyandb:0.9.0`，OAP 会因为 `Incompatible BanyanDB server API version: 0.9. But accepted versions: 0.10` 直接退出。

如需换 Dragonwell 基础镜像，可在构建 OAP/UI 镜像时覆盖：

```bash
DRAGONWELL_IMAGE=alibabadragonwell/dragonwell:21-alinux \
REGISTRY=localhost:5000 ./build-dragonwell-images.sh
```
