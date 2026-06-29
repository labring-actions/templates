# 在 Sealos 上部署和托管 AstrBot

AstrBot 是一个 AI Agent 助手和聊天机器人框架，提供 WebUI、插件市场、消息平台适配器和大模型服务接入能力。此模板会在 Sealos Cloud 上将 AstrBot 部署为带持久化存储的单节点服务。

![AstrBot 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/astrbot/website-screenshot.webp)

## 关于 AstrBot 托管

AstrBot 在 6185 端口提供 Web 管理控制台，并将运行数据、插件、模型服务配置和机器人配置保存在持久化存储中。Sealos 模板会自动创建容器、持久化卷、服务、HTTPS Ingress 和仪表盘 App 入口。

此部署遵循官方 Docker 运行方式，并固定使用 `soulter/astrbot:v4.26.2`。部署完成后，你可以在 WebUI 中接入 Telegram、Discord、QQ、飞书、钉钉、企微以及 OneBot 兼容网关等消息平台。

## 常见使用场景

- **AI 聊天机器人运营**：用一个机器人框架管理多个消息渠道。
- **大模型服务编排**：在 WebUI 中配置 OpenAI 兼容接口、Gemini、Ollama 等模型服务。
- **插件化自动化**：安装 AstrBot 插件，用于工作流、指令、搜索、沙箱和集成。
- **Agent 实验环境**：测试 Agent Runner、MCP 工具和网页搜索能力。

## AstrBot 托管依赖

Sealos 模板包含 AstrBot、持久化存储、公开 HTTPS 访问，以及同一工作负载内的可选 OneBot WebSocket 服务端口。

### 部署依赖

- [官方网站](https://astrbot.app) - 产品主页
- [Docker 部署指南](https://docs.astrbot.app/deploy/astrbot/docker.html) - 官方 Docker 部署文档
- [GitHub 仓库](https://github.com/AstrBotDevs/AstrBot) - 源码和版本发布
- [Docker 镜像](https://hub.docker.com/r/soulter/astrbot) - 官方容器镜像

### 实现细节

**架构组件：**

- **AstrBot WebUI**：面向浏览器的管理控制台，服务端口为 6185。
- **OneBot WebSocket 端口**：内部服务端口 6199，用于 OneBot 兼容适配器。
- **持久化存储**：挂载到 `/AstrBot/data`，用于保存插件、配置和运行状态。

**配置：**

- App URL 会直接打开 AstrBot WebUI。
- 模板将 `/AstrBot/data` 放在持久化卷中，配置可在重启后保留。
- 消息平台适配器和模型服务在部署后通过 WebUI 配置。

**许可证信息：**

AstrBot 使用 GNU Affero General Public License v3.0 许可证。此 Sealos 模板遵循仓库许可证提供。

## 为什么在 Sealos 上部署 AstrBot？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用从开发、部署到运维的生命周期。在 Sealos 上部署 AstrBot 可以获得：

- **一键部署**：从 App Store 部署 AstrBot，无需编写 Kubernetes 清单。
- **内置持久化存储**：保存 AstrBot 插件、模型服务配置和机器人数据。
- **即时公网访问**：自动获得带 HTTPS 的 WebUI App URL。
- **便捷自定义**：从 Sealos Canvas 调整资源和环境变量。
- **集中运维**：在一个仪表盘查看发布状态、日志、存储和入口。

## 部署指南

1. 打开 [AstrBot 模板](https://sealos.io/products/app-store/astrbot)，点击 **Deploy Now**。
2. 在弹窗中确认部署参数。
3. 等待部署完成。部署完成后，你会被重定向到 Canvas。
4. 从 Canvas 打开 AstrBot App URL。
5. 按 AstrBot 首次启动页面完成设置或登录。如果页面要求凭据，请在 Sealos 中查看 AstrBot 工作负载日志，使用应用打印的初始登录信息。

## 登录和首次启动说明

AstrBot 会在 App URL 暴露 WebUI。首次启动时，根据页面提示完成初始化或登录，然后在控制台中配置模型服务、消息平台适配器和插件。

如果 AstrBot 在容器日志中打印了初始登录信息，请保存到密码管理器中。首次成功登录后，建议在 WebUI 中轮换凭据。

## 配置

部署完成后，可以通过以下方式配置 AstrBot：

- **AstrBot WebUI**：添加模型服务、消息平台、插件和机器人行为。
- **AI Dialog**：在 Sealos 中描述资源或环境变量调整需求。
- **资源卡片**：打开 StatefulSet、Service、Ingress 或存储卡片进行直接编辑。

## 扩缩容

AstrBot 将状态保存在单个持久化卷中，建议保持 1 个副本，直到你验证了外部状态方案。插件负载或模型调用流量增长时，可以从 StatefulSet 卡片增加 CPU 或内存。

## 故障排查

### WebUI 没有显示登录或初始化页面

- 原因：AstrBot 可能仍在初始化插件和运行数据。
- 解决：等待 StatefulSet 就绪，然后在 Sealos Canvas 中查看工作负载日志。

### 适配器无法连接到 AstrBot

- 原因：消息平台回调或 OneBot 网关配置可能指向了错误的公网 URL 或端口。
- 解决：浏览器回调使用 HTTPS App URL，并按 AstrBot 官方适配器文档配置 OneBot 兼容集成。

## 其他资源

- [AstrBot 文档](https://docs.astrbot.app/what-is-astrbot.html)
- [插件使用](https://docs.astrbot.app/use/plugin.html)
- [HTTP API](https://docs.astrbot.app/scalar.html)
- [社区](https://docs.astrbot.app/community.html)

## 许可证

此 Sealos 模板遵循仓库许可证提供。AstrBot 本身使用 GNU Affero General Public License v3.0 许可证。
