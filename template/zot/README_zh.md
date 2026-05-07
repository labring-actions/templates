# 在 Sealos 上部署并托管 Zot Registry

Zot Registry 是一个 OCI 原生容器镜像仓库，用于存储和分发容器制品。这个模板会在 Sealos Cloud 上部署 Zot `v2.1.14`，默认启用基础认证，并提供两种存储后端：本地文件系统或 S3 兼容对象存储。

![Zot Logo](logo.svg)

## 关于在 Sealos 上托管 Zot Registry

Zot 是一个轻量级 OCI 仓库实现，内置 Web UI 和标准 Registry API，适合私有镜像托管、边缘分发以及企业内部 CI/CD 制品流转。它兼容 Docker/OCI 标准推拉流程，部署和运维负担相对更低。

这个 Sealos 模板提供两种运行形态。在 `filesystem` 模式下，Zot 以 StatefulSet 运行，并使用持久卷保存仓库数据；在 `objectstorage` 模式下，Zot 以 Deployment 运行，并将镜像数据写入 Sealos ObjectStorage，同时保持相同的公网 HTTPS 入口与 `/v2/` API 语义。

部署后默认启用基础认证与访问控制策略，配置了健康检查探针（`/livez`、`/readyz`、`/startupz`），并通过 Sealos 托管的 Ingress 和 TLS 对外提供访问。

## 常见使用场景

- **团队私有镜像仓库**：托管内部基础镜像和业务镜像，统一研发与生产镜像来源。
- **CI/CD 制品分发**：在 CI 阶段推送镜像，在部署阶段按版本拉取，实现流水线闭环。
- **边缘与轻量环境仓库**：在资源受限场景中运行一个足够轻量的 OCI Registry。
- **受控网络或隔离环境**：集中管理并分发已审核镜像，降低外部依赖风险。
- **OCI 制品管理中心**：除容器镜像外，也可统一托管 OCI 兼容的其他制品。

## Zot Registry 托管依赖

这个 Sealos 模板已经包含 Zot 运行所需的核心依赖：

- Zot 主服务（`ghcr.io/project-zot/zot:v2.1.14`）
- Service + Ingress（HTTPS 暴露）
- 默认启用的基础认证与仓库访问控制策略
- 可选 Sealos ObjectStorage Bucket（当 `zot_storage_backend=objectstorage`）
- 持久卷（当 `zot_storage_backend=filesystem`）

### 部署依赖

- [Zot 官方网站](https://zotregistry.dev/) - 项目概览与文档入口
- [Zot GitHub 仓库](https://github.com/project-zot/zot) - 源码与版本发布
- [Zot 示例配置](https://github.com/project-zot/zot/tree/main/examples) - 官方参考配置
- [Sealos 文档](https://sealos.io/docs) - 平台使用与运维说明

### 实现细节

**架构组件：**

此模板会部署以下资源：

- **Zot 工作负载**：
  - `filesystem` 模式使用 `StatefulSet`
  - `objectstorage` 模式使用 `Deployment`
- **Service**：暴露 `5000` 端口，承载 Zot API 与 UI
- **Ingress**：公网 HTTPS 入口，由 Sealos 托管 TLS
- **ObjectStorageBucket**（可选）：仅在对象存储模式下创建
- **ConfigMap**（对象存储模式）：保存 Zot 配置与 htpasswd 内容

**配置说明：**

- 自动生成默认值：
  - `app_name`、`app_host`
- 运行存储模式：
  - `filesystem`：本地持久化仓库数据（`1Gi` PVC）
  - `objectstorage`：使用 Sealos ObjectStorage 凭据接入 S3 兼容后端
- 认证与权限：
  - 默认启用基础认证
  - 管理员策略为配置的 admin 用户授予 `read/create/update/delete`
- 公网入口：
  - `https://<app_host>.<SEALOS_CLOUD_DOMAIN>`
- API 入口：
  - `https://<app_host>.<SEALOS_CLOUD_DOMAIN>/v2/`

**许可证信息：**

Zot 使用 [Apache License 2.0](https://github.com/project-zot/zot/blob/main/LICENSE)。

## 为什么在 Sealos 上部署 Zot Registry？

Sealos 是构建在 Kubernetes 之上的 AI 驱动云操作系统，能显著降低应用交付和运维复杂度。在 Sealos 上部署 Zot，你可以获得：

- **一键部署**：无需手写 Kubernetes YAML，即可快速上线可用的私有镜像仓库。
- **Kubernetes 原生运行时**：基于 Service、Ingress、StatefulSet/Deployment 等成熟能力稳定运行。
- **灵活存储策略**：按业务特性选择本地持久化或 S3 兼容对象存储。
- **自动 HTTPS 访问**：平台自动分配公网域名并处理 TLS 证书。
- **便捷 Day-2 运维**：通过 Canvas 的 AI 对话和资源卡片持续调整配置。
- **按量计费更高效**：先小规模启动，再按流量和负载弹性调整资源。

在 Sealos 上部署 Zot，你可以把精力集中在制品管理和交付，而不是基础设施细节。

## 部署指南

1. 打开 [Zot 模板](https://sealos.io/products/app-store/zot)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - `zot_storage_backend`：`filesystem` 或 `objectstorage`
   - `zot_admin_user`
   - 若使用 `filesystem`：填写 `zot_admin_password`
   - 若使用 `objectstorage`：填写 `zot_admin_htpasswd_hash`，可选配置 `zot_s3_region`
3. 等待部署完成（通常 2-3 分钟）。部署后会自动跳转到 Canvas。后续变更可通过 AI 对话描述需求，或在资源卡片中直接修改。
4. 访问 Zot：
   - **Web UI**：`https://<app_host>.<SEALOS_CLOUD_DOMAIN>/`
   - **Registry API**：`https://<app_host>.<SEALOS_CLOUD_DOMAIN>/v2/`
5. 使用你配置的管理员凭据进行仓库认证操作。

## 配置

部署完成后，你可以通过以下方式管理 Zot：

- **AI 对话**：用自然语言描述改动目标，由 AI 自动生成并应用变更。
- **资源卡片**：直接修改工作负载、Ingress 和存储配置。
- **Registry 客户端**：通过 Docker/Podman/Skopeo 登录并执行推送与拉取。

### 模板参数

| 参数 | 说明 | 是否必填 |
| --- | --- | --- |
| `zot_storage_backend` | 存储后端（`filesystem` 或 `objectstorage`） | 是 |
| `zot_admin_user` | 基础认证管理员用户名 | 是 |
| `zot_admin_password` | 管理员密码（仅 `filesystem` 模式） | 条件必填 |
| `zot_admin_htpasswd_hash` | 管理员 htpasswd 哈希（仅 `objectstorage` 模式，不能填明文） | 条件必填 |
| `zot_s3_region` | 对象存储模式的 S3 区域 | 条件必填 |

## 扩缩容

如需调整 Zot 资源：

1. 打开 Canvas 中对应部署。
2. 选择 Zot 工作负载资源卡片（StatefulSet 或 Deployment）。
3. 调整 CPU/内存后应用变更。
4. 对象存储模式可按需调整 Deployment 副本数，并验证客户端访问行为。

## 故障排查

### 常见问题

**问题：对象存储模式下 Pod 启动后反复重启**
- 原因：对象存储相关配置不兼容，或 S3 后端参数无效。
- 解决：确认对象存储模式使用兼容的搜索扩展配置，并检查模板参数与默认值是否正确下发。

**问题：访问 `/v2/` 返回 `UNAUTHORIZED`**
- 原因：未携带认证信息或认证信息错误。
- 解决：核对管理员凭据，并在客户端重新执行 registry 登录。

**问题：文件系统模式认证正常，但对象存储模式认证失败**
- 原因：`zot_admin_htpasswd_hash` 填了明文密码，而不是哈希。
- 解决：填写 bcrypt 或 SHA-crypt 格式哈希（例如使用 `htpasswd -nB <user>` 生成）。

**问题：推送大镜像层失败**
- 原因：工作负载资源不足，或客户端侧限制导致上传中断。
- 解决：在 Canvas 中提升工作负载资源后重试。

### 获取帮助

- [Zot 文档](https://zotregistry.dev/)
- [Zot GitHub Issues](https://github.com/project-zot/zot/issues)
- [Sealos 文档](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Zot 配置示例](https://github.com/project-zot/zot/tree/main/examples)
- [OCI Distribution 规范](https://github.com/opencontainers/distribution-spec)
- [Skopeo 文档](https://github.com/containers/skopeo)

## 许可证

本 Sealos 模板遵循 templates 仓库的许可证策略。Zot 项目本身使用 [Apache License 2.0](https://github.com/project-zot/zot/blob/main/LICENSE)。
