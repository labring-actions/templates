# 在 Sealos 上部署和托管 listmonk

listmonk 是一个快速的自托管 Newsletter 与邮件列表管理平台。此模板会在 Sealos Cloud 上部署 listmonk、Kubeblocks 托管的 PostgreSQL 数据库，以及持久化媒体存储。

## 关于托管 listmonk

listmonk 提供 Web 管理后台，用于管理订阅者、列表、邮件活动、模板和事务邮件。它以单个 Go 应用运行，并使用 PostgreSQL 保存数据，因此部署轻量，同时能在重启后保留邮件列表数据。

Sealos 模板会创建 PostgreSQL、`/listmonk/uploads` 持久化卷、内部服务、HTTPS Ingress 和仪表盘 App 入口。首次启动时，listmonk 会先执行幂等安装和升级流程，然后启动管理后台。

## 常见使用场景

- **Newsletter 发布**：向产品、社区或内容读者定期发送更新。
- **邮件列表管理**：细分订阅者，管理订阅确认，并维护可复用邮件列表。
- **邮件活动分析**：在同一后台查看投递、打开、点击和归档页面。
- **事务邮件模板**：在营销邮件之外管理可复用的事务邮件模板。

## listmonk 托管依赖

此 Sealos 模板包含运行所需依赖：listmonk 容器镜像、PostgreSQL、持久化上传存储、服务发现和 HTTPS Ingress。

### 部署依赖

- [listmonk 文档](https://listmonk.app/docs/) - 官方安装与配置指南
- [listmonk GitHub 仓库](https://github.com/knadh/listmonk) - 源码与版本发布
- [Sealos 应用商店](https://sealos.io/products/app-store/listmonk) - 一键部署模板

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **listmonk StatefulSet**：运行 `listmonk/listmonk:v6.1.0`，通过 `9000` 端口提供管理后台和公开的邮件活动/订阅页面。
- **PostgreSQL Cluster**：由 Kubeblocks 托管的 PostgreSQL `postgresql-16.4.0`，保存用户、列表、邮件活动、设置和分析数据。
- **持久化上传卷**：将上传媒体保存到 `/listmonk/uploads`，重启后文件仍会保留。
- **Ingress 与 App 入口**：通过 Sealos 托管的 HTTPS URL 暴露 listmonk。

**配置方式：**

应用使用 listmonk 环境变量，并以 `--config ''` 启动，符合官方容器使用环境变量配置的建议。PostgreSQL 连接信息来自 Kubeblocks 管理的 Secret。模板还会把 `app.root_url` 更新为生成的 Sealos 公网 URL，让邮件活动链接和公开页面使用实际部署域名。

**首次管理员：**

部署时可以填写 `admin_username` 和 `admin_password`。如果两者都填写，listmonk 会在首次安装时创建该 Super Admin 账户。如果任一字段留空，请打开部署后的 URL，并在 `/admin/login` 的首次设置表单中创建 Super Admin；密码至少需要 8 个字符。

**许可证信息：**

listmonk 使用 AGPL-3.0 许可证。此 Sealos 模板用于在 Sealos Cloud 上部署 listmonk。

## 为什么在 Sealos 上部署 listmonk？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用从开发、部署到运维的完整生命周期。在 Sealos 上部署 listmonk 可以获得：

- **一键部署**：打开模板页面，点击 **Deploy Now**，Sealos 会创建应用、数据库、存储、网络和公网 URL。
- **默认持久化数据**：PostgreSQL 和上传存储都会使用持久化卷。
- **即时 HTTPS 访问**：每次部署都会获得由 Sealos 管理的公网 HTTPS 入口。
- **易于调整**：可在 Canvas 中通过 AI 对话或资源卡片调整资源、环境变量和运维设置。
- **Kubernetes 基础能力**：无需手动管理 YAML、Ingress、证书或数据库 Operator，即可运行在 Kubernetes 上。

## 部署指南

1. 打开 [listmonk 模板](https://sealos.io/products/app-store/listmonk)，点击 **Deploy Now**。
2. 配置部署参数。如需预创建 Super Admin，请填写 `admin_username` 和 `admin_password`；否则留空，并在 Web 首次设置页面创建管理员。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续如需调整，可在 AI 对话中描述需求，或点击相关资源卡片修改配置。
4. 通过提供的 URL 访问 listmonk：
   - **管理后台**：打开 `/admin/login`。使用部署时配置的 Super Admin 凭据登录；如果未提供凭据，则先完成首次设置表单。
   - **公开页面**：订阅、归档和邮件活动链接使用同一个生成的 HTTPS 域名。

## 配置

部署完成后，可以通过以下方式配置 listmonk：

- **管理后台**：管理 SMTP、模板、列表、订阅者、媒体上传、隐私设置和邮件活动默认值。
- **Canvas AI 对话**：描述需要的运维变更，让 Sealos 帮助应用更新。
- **资源卡片**：在 Canvas 中调整 CPU、内存、存储和环境变量。

在生产环境发送邮件前，请先在 listmonk 管理设置中配置 SMTP 或其他支持的发送器。

## 扩缩容

listmonk 以单副本 StatefulSet 部署，因为它在挂载的持久化卷中保存媒体，并由单个应用进程协调邮件活动。调整资源的步骤：

1. 打开当前部署的 Canvas。
2. 点击 listmonk StatefulSet 资源卡片。
3. 调整 CPU 或内存资源。
4. 应用修改并等待 Pod 重新就绪。

## 故障排查

### 管理登录页显示设置表单

如果部署时 `admin_username` 或 `admin_password` 留空，这是正常现象。填写邮箱、用户名和密码即可创建第一个 Super Admin 账户。

### 填写部署凭据后无法登录

确认 `admin_username` 至少 3 个字符，`admin_password` 至少 8 个字符。如果首次启动时提供了无效值，请重新部署；如果还没有创建用户，也可以从设置页面创建第一个 Super Admin。

### 邮件活动没有发送

请在 **Admin → Settings** 中配置 SMTP 或其他发送器。模板只部署 listmonk 本身，不包含邮件中继服务。

### 获取帮助

- [listmonk 文档](https://listmonk.app/docs/)
- [listmonk GitHub Issues](https://github.com/knadh/listmonk/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [配置参考](https://listmonk.app/docs/configuration/)
- [API 文档](https://listmonk.app/docs/apis/)
- [角色和权限](https://listmonk.app/docs/roles-and-permissions/)

## 许可证

此 Sealos 模板遵循仓库许可证。listmonk 本身使用 AGPL-3.0 许可证。
