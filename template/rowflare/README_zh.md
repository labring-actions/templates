# 在 Sealos 上部署和托管 Rowflare

Rowflare 是开源的 Airtable 替代品，提供表格、看板、日历、时间线、画廊和表单视图，支持公式、自动化、REST API 和 MCP 服务器。此模板在 Sealos Cloud 上部署 Rowflare 官方 Docker 镜像，并配置持久化存储和公网 HTTPS 地址。

![Rowflare 官网](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/rowflare/website-screenshot.webp)

## 关于 Rowflare 托管

Rowflare 是电子表格形式的数据库：每个 base 包含相互关联的数据表和带类型的字段，支持 Airtable 公式语言、汇总与查找字段，并可用多种视图查看同一批记录。团队可以实时协作，集成方面可使用仿照 Airtable Web API 设计的 REST API，或通过内置 MCP 服务器连接 AI 客户端。

Docker 镜像在 workerd（Cloudflare 开源的 Workers 运行时）中运行与 Cloudflare 部署相同的 Worker 代码。账号数据、每个 base 各自的 SQLite 数据库以及附件都保存在 `/data` 下，因此此模板只运行一个带持久卷的 StatefulSet，不需要外部数据库或对象存储。

上方截图为官方产品网站。部署完成后，App 地址会打开 Rowflare 登录页。

## 常见使用场景

- **项目与任务管理**：在表格、看板、日历和时间线视图中规划工作，并用汇总字段跟踪进度。
- **轻量级 CRM**：通过关联记录和公式字段管理公司、联系人和商机。
- **从 Airtable 迁移**：从 Airtable 或 CSV 导入 base，把数据保存在自己的工作空间中。
- **内部数据收集**：发布表单，提交内容直接写入数据表。
- **自动化与 AI 工作流**：在记录变化时触发自动化、调用 REST API，或通过 MCP 连接 AI 客户端。

## Rowflare 托管依赖

官方镜像已包含 Web 应用、API 服务和存储引擎，不需要数据库集群、缓存或对象存储。

### 部署依赖链接

- [Rowflare 官网](https://rowflare.com) - 产品介绍
- [Rowflare GitHub 仓库](https://github.com/rowflare/rowflare) - 源码和问题追踪
- [自托管指南](https://github.com/rowflare/rowflare/blob/main/docs/self-hosting.md) - Docker 镜像、配置项和备份
- [REST API 文档](https://github.com/rowflare/rowflare/blob/main/docs/api.md) - 供脚本和集成使用的 API

### 实现细节

- **镜像**：`rowflare/rowflare:0.1.0`，并用多架构 index digest 固定。
- **运行时**：一个 StatefulSet 副本，监听 `8787` 端口，配有 Service、HTTPS Ingress 和 Sealos App 入口。
- **存储**：挂载在 `/data` 的 1 GiB 持久卷保存账号数据库、所有 base 和全部附件。数据增长后可在资源卡片中扩容。
- **配置**：`MODE=selfhost` 且 `ALLOW_SIGNUP=false`，第一个注册的账号成为所有者，之后的用户通过邀请加入。`SECRET_KEY` 在部署时自动生成，用于加密工作空间所有者保存的 AI 服务密钥以及 SMTP 或 Resend 凭据。`APP_URL` 设置为生成的 HTTPS 地址，用于邮件和自动化中的绝对链接。
- **健康检查**：启动、就绪和存活探针均调用 `/api/config`。
- **安全**：容器以用户和用户组 `1000` 运行，移除全部 Linux capabilities，并关闭 ServiceAccount Token 挂载。
- **资源**：限制为 `500m` CPU 和 `512Mi` 内存，请求为 `50m` CPU 和 `51Mi` 内存。

## 为什么在 Sealos 上部署 Rowflare？

Sealos 基于 Kubernetes 一键部署 Rowflare，无需编写清单或配置反向代理即可获得可用的实例。

- **一键部署**：模板同时创建工作负载、持久卷、Service、Ingress 和 App 入口。
- **Kubernetes 基础**：容器无响应时，健康检查会自动重启它。
- **按量付费**：只为实例实际使用的 CPU、内存和存储付费。
- **持久化存储**：base 和附件在重启和重新部署后依然保留。
- **公网 HTTPS**：Sealos 自动分配域名和 TLS 证书。
- **Canvas 与 AI 对话**：部署后可在 Canvas 的 AI 对话中描述配置修改，或打开 StatefulSet、Service 和 Ingress 资源卡片调整资源、存储或环境变量等设置。

## 部署指南

1. 打开 [Rowflare 模板](https://sealos.io/products/app-store/rowflare)，点击 **Deploy Now**。
2. 检查生成的应用名称和资源设置，然后开始部署。
3. 等待部署完成，通常需要 **2-3 分钟**。随后 Sealos 会打开该部署的 Canvas。
4. 打开 Rowflare 的 App 地址并立即点击 **Sign up**。第一个账号成为实例所有者，之后注册通道关闭。
5. 从 **Project tracker** 等模板创建 base，或导入 CSV 文件或 Airtable base。
6. 在工作空间设置中邀请同事。每个邀请链接有效期为 7 天。

## 配置

在 StatefulSet 资源卡片中修改以下环境变量，容器会使用新值重启。

- `ALLOW_SIGNUP`：设为 `true` 后，任何能访问该实例的人都可以注册账号。
- `MAIL_PROVIDER`、`MAIL_FROM`、`RESEND_API_KEY` 或 `SMTP_HOST`、`SMTP_PORT`、`SMTP_SECURITY`、`SMTP_USERNAME`、`SMTP_PASSWORD`：启用邮箱确认、密码重置等账号邮件。
- `AUTOMATION_MONTHLY_RUNS`：每个 base 每月的自动化运行次数（默认 `10000`，`0` 表示不限制）。
- `APP_URL`：绑定自定义域名后同步更新。

请勿修改 `SECRET_KEY`。修改后已保存的 AI 和邮件凭据将无法读取，所有者需要重新填写。

## 故障排查

- **注册提示仅限邀请**：第一个账号已经存在。请向所有者索取邀请链接，或设置 `ALLOW_SIGNUP=true`。
- **忘记所有者密码**：未配置账号邮件时没有重置链接。请先配置 `MAIL_PROVIDER`，再在登录页使用 **Forgot password?**。
- **存储空间已满**：在 StatefulSet 资源卡片中扩容 `/data` 卷。

## 许可证

Rowflare 采用 [AGPL-3.0 许可证](https://github.com/rowflare/rowflare/blob/main/LICENSE) 发布。
