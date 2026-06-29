# 在 Sealos 上部署和托管 OpenGist

OpenGist 是由 Git 驱动的自托管代码片段服务。此模板会在 Sealos Cloud 上部署 OpenGist，并自动创建 KubeBlocks PostgreSQL 和持久化 Git 数据存储。

![OpenGist 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/opengist/website-screenshot.webp)

## 关于托管 OpenGist

OpenGist 将代码片段保存为 Git 仓库，用户可以通过 Web 界面或 Git 工具创建、编辑、克隆、拉取和推送片段。它支持公开、私有、未列出片段、语法高亮、搜索、点赞、派生和版本历史。

此 Sealos 模板使用固定镜像 `ghcr.io/thomiceli/opengist:1.9.1`，监听 `6157` 端口。Sealos 会创建 KubeBlocks PostgreSQL `postgresql-16.4.0` 数据库、`/opengist` 持久卷、内部 Service、HTTPS Ingress 和 Sealos App 入口。

## 常见使用场景

- **私有代码片段**：托管内部笔记、脚本和示例，并保留账号控制。
- **Git 驱动的 pastebin**：用 Git 仓库保存片段历史。
- **团队知识共享**：在工程团队中共享公开或未列出的片段。
- **自托管 Gist 替代品**：运行轻量级开源 GitHub Gist 替代方案。

## OpenGist 托管依赖

此 Sealos 模板包含 OpenGist 应用容器、KubeBlocks PostgreSQL、持久化存储、Service、Ingress 和 App 资源。

### 部署依赖

- [OpenGist 文档](https://opengist.io/docs) - 官方文档
- [OpenGist GitHub 仓库](https://github.com/thomiceli/opengist) - 源码和发布版本
- [OpenGist 容器镜像](https://github.com/thomiceli/opengist/pkgs/container/opengist) - 官方 GHCR 镜像

### 实现细节

**架构组件：**

- **OpenGist**：运行在 `6157` 端口的 Web 应用和 Git-over-HTTP 服务
- **PostgreSQL**：KubeBlocks 托管的 `postgresql-16.4.0` 数据库，用于保存应用元数据
- **持久化存储**：挂载到 `/opengist` 的 `1Gi` 数据卷，用于保存 Git 仓库和索引
- **Ingress**：Sealos 托管的 HTTPS 公网入口

**配置：**

- `OG_EXTERNAL_URL` 设置为生成的 Sealos HTTPS 地址。
- `OG_DB_URI` 由 KubeBlocks PostgreSQL 连接密钥组装。
- `OG_SSH_GIT_ENABLED=false` 让公开模板聚焦 HTTPS 访问。
- 第一个注册用户会成为实例的初始账号。

**许可证信息：**

OpenGist 使用 AGPL-3.0 许可证。

## 为什么在 Sealos 上部署 OpenGist？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一部署、网络、存储和运维能力。将 OpenGist 部署到 Sealos 后，你可以获得：

- **一键部署**：通过一个模板部署 OpenGist、PostgreSQL、存储、Service、Ingress 和 App 入口。
- **托管数据库**：使用 KubeBlocks PostgreSQL 集群，降低数据库运维成本。
- **持久化 Git 数据**：用持久卷保存仓库和索引。
- **即时公网访问**：部署完成后打开自动生成的 HTTPS 地址。
- **便捷自定义**：通过 Sealos 资源卡片或 AI 对话调整资源和环境变量。

## 部署指南

1. 打开 [OpenGist 模板](https://sealos.io/products/app-store/opengist)，点击 **Deploy Now**。
2. 在弹窗中配置参数，也可以保留生成的默认值。
3. 等待部署完成，通常需要 2-4 分钟。完成后会跳转到 Canvas。
4. 从 App 卡片打开生成的 OpenGist 访问地址。
5. 注册第一个用户账号。OpenGist 会把首个注册用户作为实例初始账号。

## 配置说明

部署完成后，可以通过以下方式配置 OpenGist：

- **OpenGist 界面**：管理用户、代码片段、OAuth 提供商和可见性设置。
- **AI 对话**：描述希望 Sealos 调整的资源配置。
- **资源卡片**：点击 StatefulSet、PostgreSQL 集群、Service、Ingress 或 PVC 卡片修改设置。

## 扩容说明

OpenGist 以单副本 StatefulSet 运行，并保存持久化 Git 数据。修改副本数前，请先查阅 OpenGist 官方运行建议。

## 故障排查

### 注册页面暂时无法访问

请等待 Sealos Canvas 中的 OpenGist StatefulSet 和 PostgreSQL 集群显示 Ready。首次冷启动会创建数据库并初始化仓库存储。

### 重启后片段缺失

确认 `/opengist` 卷仍挂载在 StatefulSet 上。模板会把 Git 仓库和索引保存到该持久卷。

### 获取帮助

- [OpenGist 文档](https://opengist.io/docs)
- [OpenGist GitHub Issues](https://github.com/thomiceli/opengist/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [OpenGist 官网](https://opengist.io/)
- [OpenGist 配置](https://opengist.io/docs/configuration/configure.html)
- [OpenGist Demo](https://demo.opengist.io/)

## 许可证

此 Sealos 模板遵循仓库许可证。OpenGist 本身使用 AGPL-3.0 许可证。
