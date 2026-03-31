# 在 Sealos 上部署 RustFS

RustFS 是一个使用 Rust 构建的高性能分布式对象存储系统。该 Sealos 模板会将 RustFS 部署为一个 4 副本的分布式集群，并自动配置持久化存储、用于副本发现的 headless Service，以及对外暴露的 HTTPS 控制台入口。

## 关于 RustFS 托管

RustFS 面向分布式对象存储场景，提供兼容 S3 的访问接口。在这个模板中，每个副本都会挂载 4 个数据卷，并通过 `RUSTFS_VOLUMES` 组成统一的分布式存储拓扑。同时，模板也会启用一个 Web 控制台，方便你通过浏览器进行管理。

如果你希望在 Sealos 上快速部署一个自托管对象存储，而不想手动编排 StatefulSet 网络、持久卷和 Ingress，这个模板会比较合适。

## 模板会部署哪些资源

- 一个包含 4 个 RustFS 副本的 `StatefulSet`
- 一个用于保存 RustFS Access Key 和 Secret Key 的 `Secret`
- 一个用于保存 RustFS 共享运行参数的 `ConfigMap`
- 一个用于副本发现的 headless `Service`
- 一个暴露 `9000` 和 `9001` 端口的集群内 `Service`
- 一个用于 RustFS 控制台的 HTTPS `Ingress`
- 一个用于 Sealos UI 展示和跳转的 `App` 资源
- 每个 Pod 会创建 5 个持久化卷：
  - 4 个数据卷，挂载到 `/data/rustfs0` 到 `/data/rustfs3`
  - 1 个日志卷，挂载到 `/logs`
- 默认 4 副本部署一共会创建 20 个 PVC：
  - 16 个数据 PVC
  - 4 个日志 PVC

## 默认运行配置

- 镜像：`rustfs/rustfs:1.0.0-alpha.85`
- 副本数：`4`
- S3 接口端口：`9000`
- 控制台端口：`9001`
- 默认区域：`us-east-1`
- 纠删码驱动数量：`16`
- 存储类：`openebs-hostpath`

## 模板参数

| 参数 | 说明 | 必填 | 默认值 |
| --- | --- | --- | --- |
| `access_key` | RustFS 使用的 S3 Access Key | 是 | `''` |
| `secret_key` | RustFS 使用的 S3 Secret Key | 是 | `''` |
| `data_volume_size` | 每个数据卷 PVC 的大小，单位 GiB。固定 4 副本时总共会创建 16 个数据 PVC。 | 否 | `1` |
| `logs_volume_size` | 每个日志卷 PVC 的大小，单位 GiB。固定 4 副本时总共会创建 4 个日志 PVC。 | 否 | `1` |

## 部署指南

1. 在 Sealos 模板市场中打开 RustFS 模板。
2. 填写必填参数：
   - `access_key`
   - `secret_key`
3. 按需调整可选参数，例如数据卷和日志卷大小。
4. 点击 **Deploy** 并等待 StatefulSet 全部就绪。
5. 部署完成后，打开生成的应用地址，通过 HTTPS 访问 RustFS 控制台。

## 访问信息

- 控制台地址：`https://<app_host>.<SEALOS_CLOUD_DOMAIN>`
- 集群内 S3 服务：`<app_name>:9000`
- 集群内控制台服务：`<app_name>:9001`

这个模板默认只对外暴露了 `9001` 控制台端口。S3 API 端口 `9000` 仍然通过集群内 Service 提供访问。

## 运维说明

- 模板中的 RustFS 以 4 副本分布式 StatefulSet 方式运行。
- 每个 Pod 都会创建独立的一组 PVC，因此总存储消耗会随副本数增长。
- 使用默认值时，整个集群总共会申请 20Gi 持久化存储：
  - 16 个数据 PVC x `1Gi`
  - 4 个日志 PVC x `1Gi`
- 删除 StatefulSet 或缩容时，PVC 会被保留。
- 健康检查使用 `/health` 作为存活探针，`/health/ready` 作为就绪探针。

## 常见使用场景

- 自托管 S3 兼容对象存储
- 内部应用文件和制品存储
- 对象存储相关开发与测试环境
- 在 Sealos 上快速搭建轻量分布式存储

## 故障排查

### 控制台无法访问

- 确认应用在 Sealos 中已经进入 `Running` 状态。
- 检查 Ingress 是否已经完成创建和生效。
- 检查 4 副本集群创建出来的 20 个 PVC 是否都已成功绑定。

### Pod 一直无法就绪

- 检查每个 Pod 创建的 5 个 PVC 是否都已成功绑定。
- 确认当前存储类支持所需容量和访问模式。
- 查看 Pod 日志，确认是否存在 RustFS 启动失败或凭据配置错误。

### 集群外无法连接 S3 API

- 这个模板默认只公开暴露控制台。
- 如果你需要集群外访问 `9000` 端口，可以额外增加 Ingress 或其他 Service 暴露方式。

## 相关资源

- [RustFS GitHub 仓库](https://github.com/rustfs/rustfs)
- [RustFS 官方网站](https://rustfs.com/)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

该模板遵循当前 templates 仓库的许可证策略。RustFS 项目本身的许可证请以其上游仓库为准。
