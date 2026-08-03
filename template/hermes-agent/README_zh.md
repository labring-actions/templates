# 在 Sealos 上部署和托管 Hermes Agent

Hermes Agent 是一款开源 AI 智能体，提供持久记忆、Web 控制台和消息平台网关。此模板在 Sealos Cloud 上部署官方 Hermes Docker 运行时，并配置受保护的控制台与私有数据卷。

![Hermes Agent](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/hermes-agent/website-screenshot.webp)

## 关于托管 Hermes Agent

官方 Hermes Docker Compose 套件包含网关和控制台。此模板将两个角色放在同一个 StatefulSet Pod 中，让两个进程通过持久化存储共享官方 `/opt/data` 主目录。控制台通过端口 `9119` 提供浏览器界面；网关的认证 API 服务监听端口 `8642`，并通过 Ingress 路径 `/v1` 对外提供服务。

Hermes 将会话、配置、技能和记忆保存在 `HERMES_HOME` 下。Sealos 为 `/opt/data` 配置 1 GiB 持久卷、HTTPS Ingress 和 Canvas 应用入口。官方 Docker 套件仅依赖本地持久卷，无需数据库或对象存储服务。

## 常见使用场景

- **个人 AI 工作区**：在重启后继续保留会话、技能和记忆。
- **远程智能体控制台**：通过浏览器访问受保护的 Web 控制台。
- **消息平台网关**：连接在 Hermes 中配置的 Telegram、Discord、Slack、WhatsApp、Signal 或电子邮件频道。
- **自动化与调度**：通过 Hermes 内置网关和调度器运行周期性任务。

## Hermes Agent 托管依赖

此模板包含官方 Hermes Agent 镜像、网关容器、控制台容器、持久卷、Service、HTTPS Ingress 和 Canvas App 入口。

### 部署依赖

- [Hermes Agent 网站](https://hermes-agent.nousresearch.com/) - 产品和安装信息
- [Hermes Agent 文档](https://hermes-agent.nousresearch.com/docs) - 配置与功能指南
- [Hermes Web 控制台指南](https://github.com/NousResearch/hermes-agent/blob/v2026.8.3/website/docs/user-guide/features/web-dashboard.md) - 远程控制台认证
- [Hermes API 服务指南](https://github.com/NousResearch/hermes-agent/blob/v2026.8.3/website/docs/user-guide/features/api-server.md) - Bearer 认证 API
- [Hermes Agent 仓库](https://github.com/NousResearch/hermes-agent) - 源代码与问题追踪

## 实现细节

### 架构组件

- **网关容器**：运行官方 `gateway run` 命令，并在 `8642` 端口提供认证 API 服务。
- **控制台容器**：在 `9119` 端口运行官方 `dashboard` 命令，并提供浏览器界面。
- **持久卷**：将 `/opt/data` 挂载为 `HERMES_HOME`，用于保存会话、技能、配置和记忆。
- **Service 与 Ingress**：通过 HTTPS 将控制台路由到 `/`，将 API 服务路由到 `/v1`。

### 配置

- `dashboard_username` 和 `dashboard_password` 为非回环地址上的控制台启用官方用户名与密码认证提供程序。
- `api_server_key` 是官方 API 服务绑定任何地址时都需要的认证密钥。
- `openai_api_key` 是可选项，在选择 OpenAI 兼容提供程序时启用模型驱动的聊天操作。
- `dashboard_secret` 由 Sealos 自动生成，用于在重启后保持控制台会话稳定。

### 资源配置

| 组件 | 副本数 | CPU 上限 | 内存上限 | 存储 |
| --- | ---: | ---: | ---: | ---: |
| 网关 | 1 | `100m` | `512Mi` | - |
| 控制台 | 1 | `100m` | `256Mi` | - |
| Hermes 数据卷 | 1 | - | - | `1Gi` |

这些是官方镜像面向个人低负载场景的初始档位。观察实际模型和工具负载后，可在 Canvas 中调整资源。

### 许可证信息

Hermes Agent 采用 MIT License。

## 为什么在 Sealos 上部署 Hermes Agent？

Sealos 是基于 Kubernetes 构建的 AI 辅助云操作系统。在 Sealos 上部署 Hermes Agent 可获得一键配置、自动 HTTPS、持久存储、按量付费资源和 Canvas 运维能力。

- **一键部署**：从应用商店模板启动，无需手写 Kubernetes 清单。
- **持久化智能体状态**：在重启和升级后继续保留 Hermes 主目录。
- **安全公网访问**：通过 Sealos HTTPS 使用官方控制台凭据与 API Bearer 密钥。
- **运维控制**：通过 Canvas、AI 对话和资源卡片检查或调整部署。

## 部署指南

1. 打开 [Hermes Agent 模板](https://sealos.io/products/app-store/hermes-agent)，点击 **Deploy Now**。
2. 输入高强度的 `dashboard_username`、`dashboard_password` 和 `api_server_key`。聊天操作需要 OpenAI 兼容提供程序时，再填写 `openai_api_key`。
3. 等待部署完成。镜像与持久卷通常需要 2-3 分钟，随后 Sealos 会打开 Canvas。
4. 打开生成的 HTTPS URL。控制台登录页使用第 2 步填写的用户名和密码。

## 登录与 API 访问

### 登录控制台

打开应用 URL，在 `/login` 使用 `dashboard_username` 和 `dashboard_password` 登录。控制台通过上游基本认证提供程序保护非回环地址部署。

### API 客户端

通过 `/v1` 路径调用 API 服务时，请发送配置的 Bearer 密钥：

```bash
curl -H "Authorization: Bearer <api_server_key>" \
  "https://<your-hermes-host>/v1/models"
```

请妥善保管 API 密钥，因为 Hermes API 可以调用智能体工具，其中包括终端操作。

## 配置与扩缩容

通过 Hermes 控制台配置模型提供程序、技能、频道、计划任务和记忆。通过 Canvas 资源卡片调整 CPU、内存、存储、日志和环境变量。官方套件采用单副本部署，因为 `/opt/data` 保存智能体的本地状态。

## 故障排查

### 控制台无法打开

检查控制台容器日志，确认 `dashboard_username`、`dashboard_password` 和自动生成的控制台密钥均已注入。Sealos Ingress 要求控制台绑定到 `0.0.0.0`。

### API 请求返回 `401`

使用部署时配置的完整 `api_server_key`，并以 Bearer token 发送。API 服务缺少密钥时会默认拒绝请求。

### 聊天操作需要模型凭据

设置 `openai_api_key`，或在控制台中配置其他受支持的提供程序。模型调用完成配置后即可运行。

### 获取帮助

- [Hermes Agent 文档](https://hermes-agent.nousresearch.com/docs)
- [Hermes Agent Issues](https://github.com/NousResearch/hermes-agent/issues)
- [Sealos 文档](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Hermes Agent Docker Compose 源文件](https://github.com/NousResearch/hermes-agent/blob/v2026.8.3/docker-compose.yml)
- [Hermes Agent v2026.8.3 版本](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.3)
- [Sealos 应用商店](https://sealos.io/products/app-store)

## 许可证

此 Sealos 模板依据 templates 仓库许可证提供给 Sealos 用户。Hermes Agent 本身采用 [MIT License](https://github.com/NousResearch/hermes-agent/blob/main/LICENSE)。
