# 在 Sealos 上部署和托管 SkillHub

SkillHub 是自托管智能体技能注册中心，用于发布、发现、治理和安装可复用的智能体技能。此模板会在 Sealos Cloud 上部署官方 SkillHub web、server、scanner 容器，并自动创建 KubeBlocks PostgreSQL 和 Redis。

![SkillHub 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/skillhub/website-screenshot.webp)

## 关于托管 SkillHub

SkillHub 为团队提供私有智能体技能注册中心，支持技能、命名空间、审核、评分、下载、API token 和 CLI 安装。它适合希望在自有基础设施边界内复用和治理技能包的组织。

此 Sealos 模板遵循 `iflytek/skillhub` 官方发布拓扑：`skillhub-web`、`skillhub-server`、`skillhub-scanner`、PostgreSQL 和 Redis。默认部署使用本地持久化存储保存技能包，同时提供外部 S3 兼容对象存储选项用于生产环境。

## 常见使用场景

- **私有技能注册中心**：为 Codex、Claude 和其他智能体工作流发布内部技能。
- **团队治理**：管理命名空间、角色、审核策略、评分和审计日志。
- **CLI 分发**：让用户通过 SkillHub CLI 搜索、安装和更新技能。
- **企业自托管**：使用托管 PostgreSQL、Redis 和 HTTPS 入口运行注册中心。

## SkillHub 托管依赖

此 Sealos 模板包含独立运行 SkillHub 所需的全部运行时依赖。

### 部署依赖

- [SkillHub GitHub 仓库](https://github.com/iflytek/skillhub) - 源码和发布版本
- [SkillHub 用户指南](https://iflytek.github.io/skillhub/) - 官方用户指南
- [SkillHub 开发者文档](https://zread.ai/iflytek/skillhub) - 架构和运维文档

### 实现细节

**架构组件：**

- **SkillHub Web**：运行在 `80` 端口的 Nginx React 前端
- **SkillHub Server**：运行在 `8080` 端口的 Spring Boot API 服务
- **Skill Scanner**：运行在 `8000` 端口的安全扫描服务
- **PostgreSQL**：KubeBlocks 托管的 `postgresql-16.4.0` 数据库，用于保存应用元数据
- **Redis**：KubeBlocks Redis `redis-7.2.7`，用于 Spring session 和运行时协作
- **存储**：默认使用本地持久化存储，也可通过输入项配置外部 S3 兼容对象存储

**配置：**

- `SKILLHUB_PUBLIC_BASE_URL` 设置为生成的 Sealos HTTPS 地址。
- 模板启用直接账号密码登录，用于 bootstrap 管理员。
- `BOOTSTRAP_ADMIN_USERNAME`、`BOOTSTRAP_ADMIN_PASSWORD` 和 `BOOTSTRAP_ADMIN_EMAIL` 来自部署输入。
- 仅当 `enable_external_s3` 设置为 `true` 时显示外部 S3 字段。

**许可证信息：**

SkillHub 使用 Apache-2.0 许可证。

## 为什么在 Sealos 上部署 SkillHub？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用部署、存储、网络和运维能力。将 SkillHub 部署到 Sealos 后，你可以获得：

- **一键部署**：通过一个模板部署 SkillHub web、server、scanner、PostgreSQL、Redis、存储和 HTTPS 入口。
- **托管数据服务**：使用 KubeBlocks PostgreSQL 和 Redis，并获得可预测的资源配置。
- **即时公网访问**：部署完成后打开自动生成的 HTTPS App 地址。
- **生产存储选择**：使用默认持久卷，或连接外部 S3 兼容存储桶。
- **便捷自定义**：通过 Sealos 资源卡片或 AI 对话调整资源和环境变量。

## 部署指南

1. 打开 [SkillHub 模板](https://sealos.io/products/app-store/skillhub)，点击 **Deploy Now**。
2. 配置部署参数：
   - `admin_username`：bootstrap 管理员用户名。
   - `admin_password`：bootstrap 管理员密码。模板默认会生成随机值；打开 SkillHub 前请保存最终密码。
   - `admin_email`：bootstrap 管理员邮箱。
   - `enable_external_s3`：已有 S3 兼容存储桶和凭据时选择 `true`。
3. 等待部署完成，通常需要 4-6 分钟。完成后会跳转到 Canvas。
4. 从 App 卡片打开生成的 SkillHub 访问地址。
5. 使用 `admin_username` 和 `admin_password` 登录，然后在 SkillHub 内轮换管理员密码。

## 配置说明

部署完成后，可以通过以下方式配置 SkillHub：

- **SkillHub 界面**：管理技能、命名空间、审核、用户、API token 和注册中心设置。
- **外部 S3 输入项**：部署时设置 `enable_external_s3=true`，即可使用官方 S3 兼容存储变量。
- **AI 对话**：描述希望 Sealos 调整的资源配置。
- **资源卡片**：点击 web、server、scanner、PostgreSQL、Redis、Service、Ingress 或 PVC 卡片修改设置。

## 扩容说明

SkillHub 默认以单副本 web、server 和 scanner 组件运行。请根据真实流量和扫描负载，在对应资源卡片中调整 CPU 和内存。

## 故障排查

### 无法登录

请确认使用的是部署时配置的 `admin_username` 和 `admin_password`。bootstrap 管理员会在 server 首次启动时初始化。

### 技能上传失败

检查 server 日志和存储设置。默认配置会把包保存到 `/var/lib/skillhub/storage` 持久卷。启用外部 S3 时，请确认 endpoint、bucket、access key、secret key、region 和 path-style 模式。

### 应用仍在启动

SkillHub 冷启动时需要等待 PostgreSQL、Redis、Flyway 迁移和 scanner 服务。请在 Sealos Canvas 中等待 web、server、scanner、PostgreSQL 和 Redis 资源显示 Ready。

### 获取帮助

- [SkillHub 用户指南](https://iflytek.github.io/skillhub/)
- [SkillHub GitHub Issues](https://github.com/iflytek/skillhub/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [SkillHub GitHub 仓库](https://github.com/iflytek/skillhub)
- [SkillHub 开发者文档](https://zread.ai/iflytek/skillhub)
- [SkillHub CLI 包](https://www.npmjs.com/package/@astron-team/skillhub)

## 许可证

此 Sealos 模板遵循仓库许可证。SkillHub 本身使用 Apache-2.0 许可证。
