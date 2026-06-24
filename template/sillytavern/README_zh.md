# 在 Sealos 上部署和托管 SillyTavern

SillyTavern 是功能丰富的 LLM 前端，支持角色扮演、角色聊天、提示词管理、扩展和多种 AI 服务集成。此模板在 Sealos Cloud 上将 SillyTavern 部署为单个持久化服务。

![SillyTavern 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/sillytavern/website-screenshot.webp)

## 关于托管 SillyTavern

SillyTavern 提供浏览器 UI，用于创建角色、配置提示词、连接 AI API、管理聊天和安装扩展。用户数据、配置、插件和第三方扩展会保存到持久卷。

此模板使用固定镜像 `ghcr.io/sillytavern/sillytavern:1.18.0`，通过 Sealos HTTPS Ingress 暴露 8000 端口，并启用 Docker 风格的 heartbeat 健康检查。Basic Auth 默认启用，用于满足 SillyTavern 对公网访问的安全检查。

## 常见使用场景

- **角色聊天前端**：管理角色、世界书和聊天历史。
- **多 provider LLM UI**：从界面连接 OpenAI 兼容、Anthropic、OpenRouter、Kobold 等服务。
- **提示词实验**：调整提示词、预设、上下文模板和生成参数。
- **扩展工作区**：使用第三方 UI 扩展和服务器插件。

## SillyTavern 托管依赖

Sealos 模板包含 SillyTavern、配置和用户数据持久卷、公开 HTTPS Ingress 和 App 启动入口。

### 部署依赖

- [SillyTavern 文档](https://docs.sillytavern.app/) - 官方文档
- [Docker 安装](https://docs.sillytavern.app/installation/docker/) - 容器部署参考
- [配置指南](https://docs.sillytavern.app/administration/config-yaml/) - 运行时配置
- [GitHub 仓库](https://github.com/SillyTavern/SillyTavern) - 源码和发布版本

### 实现细节

**架构组件：**

- **SillyTavern**：主 Web UI 和后端服务。
- **持久卷**：配置、数据、插件和第三方扩展目录。
- **Ingress**：通过 Sealos 提供公开 HTTPS 访问。

**配置：**

- `SILLYTAVERN_LISTEN=true` 允许服务接收 Ingress 流量。
- `SILLYTAVERN_WHITELISTMODE=false` 允许通过 Sealos URL 公开访问。
- `SILLYTAVERN_HEARTBEATINTERVAL=30` 启用内置健康检查机制。
- Basic Auth 使用部署弹窗中的 `basic_auth_username` 和 `basic_auth_password`。

**许可证信息：**

SillyTavern 来自上游项目。当前许可证信息请查看上游仓库。

## 为什么在 Sealos 上部署 SillyTavern？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用从云端开发到生产部署和运维的完整生命周期。它适合构建和扩展现代 AI 应用、SaaS 平台和复杂微服务架构。在 Sealos 上部署 SillyTavern，你可以获得：

- **一键部署**：同时部署 SillyTavern、持久存储、HTTPS Ingress 和 App 入口。
- **持久用户数据**：角色、聊天、设置、插件和扩展在重启后继续保留。
- **易于定制**：通过 Canvas 修改环境变量、资源和存储。
- **即时公开访问**：部署完成后通过 HTTPS URL 打开 SillyTavern。
- **无需 Kubernetes 专业知识**：通过简单 UI 管理容器化服务。

在 Sealos 上部署 SillyTavern，把精力放在你的 LLM 工作区上。

## 部署指南

1. 打开 [SillyTavern 模板](https://sealos.io/products/app-store/sillytavern)，点击 **Deploy Now**。
2. 保持 Basic Auth 开启用于公网访问，或在关闭前配置其他 SillyTavern 访问控制方式。默认用户名为 `user`，`basic_auth_password` 字段会预填随机密码，也可以在部署前替换。
3. 等待部署完成。部署完成后会进入 Canvas。后续变更可在对话框描述需求交给 AI 调整，或点击对应资源卡片修改配置。
4. 从 Canvas 打开 SillyTavern App URL，使用 `basic_auth_username` 和 `basic_auth_password` 登录。
5. 在 SillyTavern UI 内配置 AI provider API key、角色、提示词和扩展。

## 配置

部署后可以通过以下方式配置 SillyTavern：

- **AI 对话框**：描述资源、认证或环境变量变更，由 AI 应用更新。
- **资源卡片**：点击 StatefulSet、Service、Ingress 或存储卡片修改设置。
- **SillyTavern UI**：配置 AI provider、预设、角色、扩展和聊天设置。
- **持久配置卷**：高级配置保存在 `/home/node/app/config` 下。

## 扩展

SillyTavern 是有状态应用，活跃用户数据保存在本地持久卷。默认模板保持一个副本。模板使用 512 MiB 内存，因为首次启动会编译前端库并初始化默认用户内容。大上下文、重度扩展或多用户并发场景可提高 CPU 和内存。

## 故障排查

### 应用打开后显示访问错误

- 原因：需要 Basic Auth 凭据，或白名单相关设置被修改。
- 解决：使用配置的 `basic_auth_username` 和 `basic_auth_password`，并确认 `SILLYTAVERN_WHITELISTMODE=false`。

### 健康检查失败

- 原因：heartbeat 文件缺失或服务未启动。
- 解决：检查容器日志，并确认 `SILLYTAVERN_HEARTBEATINTERVAL=30`。

### 重启后数据缺失

- 原因：数据写入了持久化目录之外的位置。
- 解决：将配置、角色、聊天、插件和扩展保存到已挂载的 SillyTavern 目录下。

## 更多资源

- [SillyTavern Docker 指南](https://docs.sillytavern.app/installation/docker/)
- [SillyTavern 配置](https://docs.sillytavern.app/administration/config-yaml/)
- [SillyTavern 扩展](https://docs.sillytavern.app/extensions/)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

当前 SillyTavern 许可证和使用条款请查看 [上游仓库](https://github.com/SillyTavern/SillyTavern)。
