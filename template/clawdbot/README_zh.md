# 在 Sealos 上部署托管 Openclaw

Openclaw 是一款 AI 智能体网关，支持 WhatsApp、Telegram、Discord 等多渠道集成。借助本模板，您可以在 Sealos 云平台上快速部署一个生产就绪的 Openclaw 实例，并自动配置持久化存储。

## 关于托管 Openclaw

Openclaw 以单节点 AI 智能体网关服务的形式运行，为跨多个消息平台部署和管理 AI 智能体提供统一接口。Sealos 模板会自动为您的智能体配置、工作空间数据以及 WhatsApp 会话文件配置持久化存储，确保数据安全可靠，即使服务重启也能完好保存。

这套网关架构让您能够将兼容 OpenAI 的 AI 模型（如 Claude、GPT-4 等）连接到 Telegram、Discord、WhatsApp 和 Slack 等热门消息平台。部署完成后，系统会自动配置 SSL 证书、域名管理，并通过 Sealos 控制面板提供一体化监控能力。

## 常见应用场景

- **跨平台 AI 助手**：在 Telegram、Discord、WhatsApp 和 Slack 上同时部署同一个 AI 助手
- **客服自动化**：构建能够跨多个渠道处理客户咨询的智能聊天机器人
- **团队协作**：为团队沟通平台打造 AI 驱动的生产力机器人
- **社区管理**：利用 AI 智能体自动管理社区内容和用户互动
- **个人 AI 助手**：运行专属的个人 AI 助手，可从任何消息平台访问

## 托管 Openclaw 的依赖项

Sealos 模板已包含所有必需的依赖：运行时环境、用于配置和工作空间数据的持久化存储卷。

### 部署依赖

- [官方网站](https://clawd.bot) - Openclaw 官方网站
- [GitHub 仓库](https://github.com/moltbot/moltbot) - 源代码和文档
- [快速入门指南](https://clawd.bot) - 快速上手和配置说明

### 实现细节

**架构组件：**

本模板部署以下服务：

- **Openclaw 网关**：运行在 18789 端口的主 AI 智能体网关服务
- **持久化存储**：自动配置两个持久卷：
  - 配置存储（1Gi）：存储智能体配置、模型设置和渠道凭据
  - 工作空间存储（1Gi）：存储智能体工作空间数据和生成的文件

**配置方式：**

Openclaw 网关通过环境变量和初始化时生成的配置文件进行配置：

- **Base URL**：兼容 OpenAI 的 API 端点（默认为 Sealos AI Proxy）
- **API Key**：AI 模型提供商的认证密钥
- **Model**：使用的默认 AI 模型（例如 claude-opus-4-5-20251101）
- **Gateway Token**：访问网关控制 UI 的认证令牌
- **Channel Tokens**：Discord、Telegram、WhatsApp 和 Slack 的可选令牌

控制 UI 默认启用，可通过网关 URL 加上网关令牌参数访问。该 UI 让您能够管理智能体、配置渠道、监控活动，无需手动修改配置文件。

**渠道支持：**

- **Telegram**：完全支持，默认启用
- **Discord**：添加 Discord 机器人令牌即可启用
- **WhatsApp**：会话数据存储在持久化存储中
- **Slack**：使用机器人令牌和应用令牌进行配置

**许可证信息：**

Openclaw 是开源软件。具体许可条款请查阅 [GitHub 仓库](https://github.com/moltbot/moltbot)。

## 为什么选择在 Sealos 上部署 Openclaw？

Sealos 是一个基于 Kubernetes 构建的 AI 赋能云操作系统，将整个应用生命周期——从云端 IDE 开发到生产部署和管理——融为一体。它非常适合构建和扩展现代 AI 应用、SaaS 平台和复杂的微服务架构。在 Sealos 上部署 Openclaw，您将获得：

- **一键部署**：只需点击一下即可部署 Openclaw。无需编写 YAML 配置，无需处理容器编排的复杂性——只需点击、部署即可完成。
- **内置自动扩展**：您的 AI 智能体会根据需求自动扩展和收缩。从容应对来自多个消息平台的流量峰值，无需人工干预。
- **轻松定制**：通过直观的表单配置 AI 模型、API 密钥和渠道连接。无需修改一行代码即可完成个性化配置。
- **零门槛 Kubernetes**：无需成为 Kubernetes 专家即可享受 Kubernetes 的所有优势——高可用性、服务发现、容器编排。
- **内置持久化存储**：内置的持久化存储方案确保您的智能体配置、工作空间数据和 WhatsApp 会话在部署和扩展过程中始终安全可访问。
- **即时公网访问**：每次部署都会自动获得带 SSL 证书的公网 URL。无需复杂的网络配置即可立即分享您的 AI 智能体网关。
- **集成 AI 代理**：无缝连接 Sealos AI Proxy，轻松访问 Claude、GPT-4 等兼容 OpenAI 的模型。

在 Sealos 上部署 Openclaw，专注于打造智能 AI 智能体，让基础设施管理交给我们。

## 部署指南

1. 访问 [Sealos Cloud](https://cloud.sealos.run)
2. 在桌面界面点击"应用商店"
3. 在应用商店中搜索"Openclaw"
4. 点击"部署应用"并配置以下参数：
   - **Base URL**：您的兼容 OpenAI 的 API 端点（默认：https://aiproxy.usw-1.sealos.io/v1）
   - **API Key**：您的 AI 模型提供商的 API 密钥
   - **Model**：使用的默认模型 ID（例如 claude-opus-4-5-20251101）
   - **Auth Token**：网关认证的 JWT 密钥（默认自动生成）
5. 等待部署完成（通常 1-3 分钟）
6. 通过提供的 URL 访问您的 Openclaw 网关

## 配置说明

部署完成后，您可以通过多种方式配置 Openclaw：

### 控制界面

通过以下地址访问控制界面：
```
https://[您的应用地址]/?token=[gateway-token]
```

网关令牌在部署后会自动生成并显示在应用启动器中。该界面提供基于 Web 的管理功能：
- 管理 AI 智能体
- 配置消息渠道（Telegram、Discord、WhatsApp、Slack）
- 监控智能体活动
- 调整模型设置

### 环境变量

在应用启动器中更新部署以修改应用设置：

- **DISCORD_BOT_TOKEN**：您的 Discord 机器人令牌
- **TELEGRAM_BOT_TOKEN**：您的 Telegram 机器人令牌
- **SLACK_BOT_TOKEN**：您的 Slack 机器人令牌
- **SLACK_APP_TOKEN**：您的 Slack 应用令牌（用于 socket 模式）

### 渠道设置

每个消息平台都需要特定的设置：

**Telegram：**
1. 通过 Telegram 的 [@BotFather](https://t.me/botfather) 创建机器人
2. 复制机器人令牌
3. 将令牌添加到 TELEGRAM_BOT_TOKEN 环境变量或通过控制界面添加
4. 与您的机器人开始对话

**Discord：**
1. 在 [Discord 开发者门户](https://discord.com/developers/applications) 创建 Discord 应用
2. 创建机器人用户并复制令牌
3. 将令牌添加到 DISCORD_BOT_TOKEN 环境变量或通过控制界面添加
4. 邀请机器人加入您的服务器

**WhatsApp：**
1. WhatsApp 会话数据存储在持久化存储的 `/home/openclaw/.openclaw/whatsapp` 路径
2. 通过控制界面按照 WhatsApp Web 二维码认证流程操作
3. 会话数据在容器重启后依然保存

**Slack：**
1. 在 [Slack API](https://api.slack.com/apps) 创建 Slack 应用
2. 启用机器人作用域并将应用安装到您的工作区
3. 通过环境变量或控制界面添加机器人令牌和应用令牌（用于 socket 模式）

## 扩展指南

扩展您的 Openclaw 部署：

1. 打开应用启动器
2. 选择您的 Openclaw 部署
3. 调整 CPU/内存资源：
   - 最小：100m CPU，204Mi 内存
   - 最大：1000m CPU，2Gi 内存
4. 如有需要，增加副本数量（当前设置为 1）
5. 点击"更新"应用更改

**注意：**Openclaw 使用 StatefulSet 进行部署。对于高流量的生产环境，建议在负载均衡器后部署多个实例。

## 故障排除

### 常见问题

**问题：消息平台上的智能体无响应**
- 原因：平台的机器人令牌缺失或错误
- 解决方案：验证环境变量或控制界面中配置了正确的机器人令牌

**问题：AI 模型错误**
- 原因：API 密钥无效、基础 URL 错误或模型名称错误
- 解决方案：检查您的 API 密钥是否有效、基础 URL 是否正确，以及模型 ID 是否被您的提供商支持

**问题：重启后 WhatsApp 会话丢失**
- 原因：会话数据未正确持久化
- 解决方案：模板已为 WhatsApp 会话配置持久化存储。确保存储卷正确挂载

**问题：无法访问控制界面**
- 原因：网关令牌或 URL 错误
- 解决方案：从应用启动器复制网关令牌，使用 `?token=[网关令牌]` 参数访问 URL

### 获取帮助

- [官方文档](https://clawd.bot)
- [GitHub 问题追踪](https://github.com/moltbot/moltbot/issues)
- [Sealos Discord 社区](https://discord.gg/sealos)

## 额外资源

- [Openclaw 官网](https://clawd.bot) - 官方网站和文档
- [GitHub 仓库](https://github.com/moltbot/moltbot) - 源代码、问题和贡献
- [Sealos 文档](https://sealos.io/docs) - 了解在 Sealos 上部署应用的更多信息
- [AI 代理配置](https://aiproxy.usw-1.sealos.io) - Sealos AI 代理，用于访问兼容 OpenAI 的模型

## 许可证

本 Sealos 模板采用与 Openclaw 相同的许可证提供。具体许可条款请参阅 [Openclaw GitHub 仓库](https://github.com/moltbot/moltbot)。
