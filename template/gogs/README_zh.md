# 在 Sealos 上部署和托管 Gogs

Gogs 是轻量级自托管 Git 服务，支持仓库、用户、组织、议题和项目协作。此模板在 Sealos Cloud 上部署 Gogs，并配置 KubeBlocks PostgreSQL、持久化 Git 数据、公开 HTTPS 访问和首次注册流程。

![Gogs 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/gogs/website-screenshot.webp)

## 关于托管 Gogs

Gogs 作为单个 Web 服务运行，使用 PostgreSQL 保存应用元数据，并使用持久化存储保存仓库、SSH 密钥、日志和自定义配置。模板会在启动前生成生产用 `app.ini`，将公开根 URL 设置为 Sealos 域名，并通过 Sealos Ingress 暴露 HTTP 服务。

Sealos 会自动创建 PostgreSQL、持久化卷、HTTPS Ingress 和应用入口。Gogs 负责浏览器中的用户、仓库、组织、议题和 Git 协作流程。

## 常见使用场景

- **个人 Git 托管**：用轻量服务托管私有仓库。
- **团队代码协作**：管理用户、组织、仓库、议题和合并请求。
- **内部工具链**：为自托管 CI、自动化和部署流程提供私有 Git 服务。
- **教学和实验环境**：为课程、工作坊和小团队提供隔离的 Git 托管。

## Gogs 托管依赖

此 Sealos 模板包含所有必需依赖：Gogs Web 应用、KubeBlocks PostgreSQL、持久化仓库存储、ClusterIP Service、HTTPS Ingress 和 Sealos App 入口。

### 部署依赖

- [官方网站](https://gogs.io/) - Gogs 产品网站
- [GitHub 仓库](https://github.com/gogs/gogs) - 源码和版本发布
- [Docker 文档](https://github.com/gogs/gogs/tree/main/docker) - 官方容器说明
- [配置入门](https://gogs.io/fine-tuning/configuration-primer) - Gogs 配置参考

### 实现细节

**架构组件：**

此模板部署以下服务：

- **Gogs Web 服务**：提供 Web UI、Git HTTP 端点、注册、登录和仓库工作流。
- **PostgreSQL**：存储用户、仓库元数据、议题、组织和设置。
- **持久化存储**：在 `/data` 下保存 Git 仓库、自定义配置、日志和运行数据。
- **Sealos Ingress**：通过生成的 Sealos 域名提供 HTTPS 访问。

**配置：**

模板通过 ConfigMap 写入 `/data/gogs/conf/app.ini`，并从 KubeBlocks 连接 Secret 注入 PostgreSQL 凭据。模板默认关闭注册验证码，便于完成首次初始化；全新部署中的第一个注册用户会成为管理员。

**许可证信息：**

Gogs 使用 MIT License。此 Sealos 模板遵循 Sealos templates 仓库许可证。

## 为什么在 Sealos 上部署 Gogs？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署和日常运维生命周期。部署 Gogs 到 Sealos 后，你可以获得：

- **一键部署**：从应用商店启动 Gogs，无需手写 Kubernetes YAML。
- **托管数据库创建**：通过 KubeBlocks 创建 PostgreSQL 并自动连接到应用。
- **持久化存储**：仓库和应用数据可在重启和升级后保留。
- **即时 HTTPS 访问**：Sealos 为 Gogs Web UI 提供公开域名和 TLS 证书。
- **Canvas 运维**：通过 Canvas、AI 对话和资源卡调整资源、查看日志和更新设置。
- **按量资源效率**：从轻量资源起步，并随仓库使用量增长扩容。

## 部署指南

1. 打开 [Gogs 模板](https://sealos.io/products/app-store/gogs)，点击 **Deploy Now**。
2. 在弹窗中配置参数。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续变更可以在对话框中描述需求让 AI 应用更新，也可以点击资源卡修改设置。
4. 通过提供的 URL 访问 Gogs，并点击 **Register**。
5. 创建第一个账号。Gogs 会将全新部署中的第一个注册用户设为管理员。
6. 使用该账号登录并创建第一个仓库。

## 登录和注册

Gogs 在全新部署中启用自助注册，并默认关闭注册验证码以便首次初始化。第一个注册用户会成为管理员，因此请在分享 URL 前先创建管理员账号。

管理员存在后，其他用户仍可从同一登录页注册，除非你在 Gogs 管理后台关闭注册。

## 配置

部署后可以通过以下方式配置 Gogs：

- **Gogs 管理后台**：管理用户、组织、仓库、认证源和应用设置。
- **Canvas 资源卡**：修改 CPU、内存、存储或环境值。
- **AI 对话**：描述运维变更，并让 Sealos 应用到模板资源。

## 扩容

扩容部署：

1. 打开部署对应的 Canvas。
2. 点击 Gogs StatefulSet 或 PostgreSQL 资源卡。
3. 调整 CPU、内存、存储或副本相关设置。
4. 应用变更并观察 rollout 状态。

## 故障排查

### 注册页面无法访问

- 原因：应用仍在启动，或 PostgreSQL 正在完成初始化。
- 解决：等待 Gogs StatefulSet 和 PostgreSQL Cluster 就绪，然后刷新 App URL。

### 登录成功但仓库操作失败

- 原因：持久化卷或数据库可能仍在启动后预热。
- 解决：在 Canvas 中检查 Gogs Pod 日志和 PostgreSQL 状态。

### 获取帮助

- [Gogs 文档](https://gogs.io/docs)
- [GitHub Issues](https://github.com/gogs/gogs/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [Gogs 配置入门](https://gogs.io/fine-tuning/configuration-primer)
- [Gogs Docker 指南](https://github.com/gogs/gogs/tree/main/docker)
- [Gogs 版本发布](https://github.com/gogs/gogs/releases)

## License

此 Sealos 模板遵循 Sealos templates 仓库许可证。Gogs 本身使用 MIT License。
