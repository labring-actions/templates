# 在 Sealos 上部署托管 OpenClaw（2026-03 更新）

OpenClaw 是一个本地优先（local-first）的 AI Agent Gateway，可统一接入 WhatsApp、Telegram、Discord、Slack 等多渠道，并通过一个控制平面管理会话、工具与自动化能力。借助 Sealos 模板，你可以快速部署一个带持久化存储的 OpenClaw 实例。

## 关于托管 OpenClaw

OpenClaw 网关默认运行在 `18789` 端口，提供控制 UI、WebChat、渠道接入与 Agent 路由能力。  
Sealos 模板会自动准备持久化存储，用于保存：

- 网关配置与令牌
- 工作空间数据
- 渠道会话数据（如 WhatsApp 会话）

这样即使容器重建或重启，核心状态也能保留。

## 最新版本信息（截至 2026-03-02）

- OpenClaw 最新稳定版本：`v2026.3.1`（发布于 2026-03-02）
- 最新版本新增了容器/Kubernetes 友好的健康检查端点：  
  `/health`、`/healthz`、`/ready`、`/readyz`

这意味着在 Sealos/K8s 中可以更标准地配置 liveness/readiness probe。

## 适用场景

- 跨平台 AI 助手（同一助手覆盖 Telegram / Discord / WhatsApp / Slack）
- 多渠道客服自动化
- 团队协作机器人（知识检索、流程自动化）
- 社区运营与内容自动化
- 个人 AI 助手（统一消息入口）

## 依赖与组件

Sealos 模板通常已包含运行所需基础依赖，核心是：

- OpenClaw 网关服务
- 持久化存储卷（配置与工作空间）
- 公网访问入口（域名与 TLS 由平台托管能力提供）

> 注：不同 Sealos 集群模板的资源默认值可能不同，建议以应用表单中的实时参数为准。

## 推荐部署参数

在应用商店部署 OpenClaw 时，建议重点确认以下参数：

- **Base URL**：兼容 OpenAI API 的模型网关地址  
  例如：`https://aiproxy.usw-1.sealos.io/v1`
- **API Key**：模型提供商密钥
- **Model**：默认模型 ID（建议使用你当前 provider 实际可用模型）
- **Gateway/Auth Token**：网关访问令牌（请使用强随机值）
- 可选渠道令牌：
  - `TELEGRAM_BOT_TOKEN`
  - `DISCORD_BOT_TOKEN`
  - `SLACK_BOT_TOKEN`
  - `SLACK_APP_TOKEN`

## 部署步骤（Sealos）

1. 打开 [Sealos Cloud](https://cloud.sealos.run)
2. 进入应用商店并搜索 **OpenClaw**
3. 点击部署，填写模型与鉴权参数
4. 等待服务启动（通常数分钟）
5. 打开应用提供的公网地址，使用网关令牌登录控制 UI

## 控制 UI 与安全建议（重要）

旧文档常见 `/?token=...` 方式访问控制 UI。  
最新实践建议：

- 不在 URL 中长期携带敏感 token
- 首次登录后在 UI 内进行会话管理
- 定期轮换 Gateway Token
- 对第三方 skills 做最小信任与代码审查

## 渠道接入

### Telegram
1. 通过 [@BotFather](https://t.me/botfather) 创建机器人
2. 获取 token 并填入 `TELEGRAM_BOT_TOKEN`
3. 在控制 UI 中完成路由与会话策略配置

### Discord
1. 在 [Discord Developer Portal](https://discord.com/developers/applications) 创建应用与机器人
2. 将 token 写入 `DISCORD_BOT_TOKEN`
3. 邀请机器人进目标服务器并配置权限

### Slack
1. 在 [Slack API](https://api.slack.com/apps) 创建应用
2. 配置 bot token 与 app token
3. 分别填入 `SLACK_BOT_TOKEN`、`SLACK_APP_TOKEN`

### WhatsApp
- 会话数据建议持久化到 OpenClaw 数据目录
- 按控制 UI 引导进行二维码配对

## 扩展与运维建议

- 根据流量调节 CPU/内存与副本
- 使用健康检查端点配置探针：`/healthz`、`/readyz`
- 通过对象存储做定时备份（配置/工作区/关键会话）
- 对外服务建议配合平台监控与告警

## 故障排查

- **渠道不回复**：检查对应 Bot Token 是否有效、权限是否完整
- **模型调用失败**：检查 Base URL、API Key、模型 ID 是否匹配
- **控制台无法访问**：确认网关 URL 与 token；检查 Ingress/证书状态
- **重启后状态丢失**：确认 PVC 正常绑定且挂载路径正确

## 参考链接

- OpenClaw 官网：<https://openclaw.ai>
- OpenClaw 文档：<https://docs.openclaw.ai>
- OpenClaw GitHub：<https://github.com/openclaw/openclaw>
- OpenClaw Releases：<https://github.com/openclaw/openclaw/releases>
- Sealos OpenClaw 模板页：<https://sealos.io/products/app-store/openclaw/>
- Sealos Cloud：<https://cloud.sealos.run>
