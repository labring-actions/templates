# 在 Sealos 上部署和托管 Cal.com

Cal.com 是一个开源预约排期平台，适合管理会议预约、可用时间和团队排班。这个模板会在 Sealos Cloud 上部署一套自托管的 Cal.com Web 应用，并配套托管 PostgreSQL。

## 关于在 Sealos 上托管 Cal.com

Cal.com 把公开预约页、团队排班、嵌入式预约、路由表单和工作流自动化整合在同一个 Web 应用里。这个 Sealos 模板遵循上游默认的自托管路径，也就是一个 Cal.com Web 运行时加一个 PostgreSQL 后端。

Sealos 会自动创建 PostgreSQL 集群、在首次启动前准备好 `calendso` 数据库、配置带 TLS 的公网 Ingress，并注入 Cal.com 运行所需的认证与加密密钥。当前模板还会在对外暴露 Web 进程前等待 PostgreSQL 就绪，并对 Prisma 迁移做重试，避免数据库慢几秒时出现“应用起来了，但初始化没完成”的半成品状态。

这个模板默认只聚焦 Cal.com 的核心预约能力。Prisma Studio，以及可选的 API v2 与 Redis 组件，都不在默认部署路径里。

## 常见使用场景

- **个人预约页面**：用于分享咨询、演示、办公时间或教练服务的预约链接。
- **团队排班**：适合销售、支持或客户成功团队使用轮询、共享或集体预约。
- **嵌入式预约**：把 Cal.com 预约组件嵌入你自己的产品、官网或客户门户。
- **内部流程预约**：可用于候选人面试、入职安排、合作伙伴沟通和内部协作排期。
- **面向客户的预约流程**：把手工来回确认时间的流程改成自助预约。

## Cal.com 托管依赖

这个 Sealos 模板已经包含默认自托管部署所需的核心运行依赖：

- **Cal.com Web 运行时**：`calcom.docker.scarf.sh/calcom/cal.com:v6.2.0`
- **PostgreSQL 集群**：Kubeblocks 托管的 `postgresql-16.4.0`
- **数据库初始化任务**：使用 `public.ecr.aws/docker/library/postgres:16.4-alpine` 在首次 Web 启动前创建 `calendso` 数据库
- **Service 与 Ingress**：内部服务监听 `3000` 端口，并通过 Sealos 提供公网 HTTPS 访问

### 部署相关资源

- [Cal.com GitHub 仓库](https://github.com/calcom/cal.com) - 源码、发布信息和上游部署资源
- [Cal.com Docker 说明](https://github.com/calcom/cal.com#docker) - 上游 Docker 与自托管入口说明
- [Cal.com Self-Hosting 文档](https://github.com/calcom/cal.com/tree/main/docs/self-hosting) - 更完整的自托管文档与指南
- [Sealos Discord](https://discord.gg/wdUn538zVP) - Sealos 社区支持渠道

## 实现细节

### 架构组件

这个模板会部署以下组件：

- **Cal.com Web Deployment**：运行 Next.js 应用，执行 Prisma 迁移、应用市场种子任务，并提供预约界面
- **PostgreSQL Cluster**：存储用户、预约、事件类型、工作流和应用配置
- **PostgreSQL Init Job**：等待 PostgreSQL 就绪后，以幂等方式创建 `calendso` 数据库
- **Ingress**：通过 `https://<app-host>.<domain>` 对外暴露 Cal.com，并由 Sealos 处理 TLS

### 配置说明

- `NEXT_PUBLIC_WEBAPP_URL`、`NEXTAUTH_URL`、`NEXT_PUBLIC_WEBSITE_URL` 和 `NEXT_PUBLIC_EMBED_LIB_URL` 都已预先绑定到 Sealos 分配的公网域名
- `NEXTAUTH_SECRET`、`CALENDSO_ENCRYPTION_KEY`、`CRON_API_KEY` 和 `CRON_SECRET` 会在部署时自动生成
- SMTP 输入项是可选的。不填写也能启动应用，但邮件验证和通知功能可能不可用
- `CALCOM_LICENSE_KEY` 为可选项，仅在你需要 Cal.com 付费能力时才需要填写
- 由于 Cal.com 启动时会执行迁移、种子任务和应用服务启动，这个模板默认把内存上限设为 `2Gi`，以避免常见的启动阶段 OOM

### 许可证信息

Cal.com 采用 [AGPLv3](https://github.com/calcom/cal.com/blob/main/LICENSE) 许可证。若组织需要不同的商业条款，可直接联系 Cal.com 获取商业授权。

## 为什么在 Sealos 上部署 Cal.com？

Sealos 是一个基于 Kubernetes 的云操作系统，能把数据库、Ingress、存储和应用工作负载打包成一个可直接部署的模板。把 Cal.com 部署到 Sealos 后，你可以获得：

- **一键部署**：无需手工编排 Kubernetes 资源，就能同时启动 Cal.com 和 PostgreSQL
- **托管数据库能力**：直接使用 Kubeblocks 托管 PostgreSQL，密钥和服务发现都已接好
- **易于定制**：后续可以通过 Canvas 里的 AI 对话框或资源卡片修改环境变量、资源配置和运行参数
- **默认公网 HTTPS**：每次部署都会自动得到一个带 TLS 的公网访问地址
- **不用手写 Kubernetes**：继续享受 Kubernetes 的可靠性和编排能力，但不必自己维护大量 YAML
- **资源使用更灵活**：按实际负载调整资源，按需使用、按量付费

把 Cal.com 部署到 Sealos 后，你可以把精力放在预约流程和业务配置上，而不是基础设施拼装上。

## 部署指南

1. 打开 [Cal.com 模板页面](https://sealos.io/products/app-store/calcom)，点击 **Deploy Now**。
2. 如果你需要 SMTP 或 License 配置，请在弹窗里填写对应参数。
3. 等待部署完成，通常需要 2 到 3 分钟。部署结束后你会被带到 Canvas。后续如果要修改配置，可以直接在对话框里描述需求让 AI 代你调整，或者点击对应资源卡片手动修改。
4. 通过系统生成的公网地址访问你的应用。
   - **Cal.com Web 界面**：完成初始化向导并创建第一个管理员账号
   - **预约页面**：初始化完成后即可发布个人或团队预约链接

## 配置

部署完成后，你可以通过以下方式继续调整 Cal.com：

- **AI 对话框**：直接描述你想改的基础设施或运行配置，让 Sealos 自动处理
- **资源卡片**：在 Canvas 中打开 Deployment、PostgreSQL 或 Ingress 卡片，修改资源和设置
- **Cal.com 管理界面**：首次登录后可继续配置品牌、用户、可用时间、事件类型、团队与工作流

## 故障排查

### 首次启动时间偏长

Cal.com 在第一次启动时会执行数据库迁移和应用市场种子写入。首次部署比普通 Web 应用慢一些是正常现象，建议先等待几分钟再判断是否异常。

### 应用能启动，但访问时报数据库或初始化错误

这通常说明 PostgreSQL 在启动阶段比 Web 进程慢。当前模板已经在启动前增加了更长的数据库等待时间，并对 Prisma 迁移做了重试。如果你后续自定义了启动命令，记得保留这套迁移重试逻辑。

### 启动阶段出现 OOMKilled

Cal.com 启动时的内存需求高于普通轻量 Web 应用。模板默认把内存上限设为 `2Gi`；如果你后续手动调低，迁移或 seed 步骤可能再次失败。

### 邮件功能不可用

请在部署参数里补充 `EMAIL_FROM`、`EMAIL_FROM_NAME`、`EMAIL_SERVER_HOST`、`EMAIL_SERVER_PORT`、`EMAIL_SERVER_USER` 和 `EMAIL_SERVER_PASSWORD`，或者在部署完成后通过 Canvas 更新。

### 自定义域名下认证回调异常

请确认你的公网域名仍然和 `NEXTAUTH_URL` 以及 Ingress 当前使用的 Host 保持一致。

## 更多资源

- [Cal.com 官网](https://cal.com/)
- [Cal.com GitHub Releases](https://github.com/calcom/cal.com/releases)
- [Cal.com Self-Hosting 文档](https://github.com/calcom/cal.com/tree/main/docs/self-hosting)
- [Sealos App Store](https://sealos.io/products/app-store)

## License

本文档对应的是 Cal.com 的 Sealos 应用模板。Cal.com 本身采用 AGPLv3 许可证，完整的授权信息和商业授权选项请以其上游仓库说明为准。
