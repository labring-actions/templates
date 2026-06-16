# 在 Sealos 上部署和托管 BillionMail

BillionMail 是开源邮件服务器、Newsletter 和邮件营销平台。这个模板会在 Sealos Cloud 上部署 BillionMail Web 控制台、邮件服务、PostgreSQL、Redis 和持久化存储。

![BillionMail 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/billionmail/website-screenshot.webp)

## 关于 BillionMail 托管

BillionMail 提供自托管控制台，用于管理域名、邮箱、邮件活动、Newsletter 运营和邮件服务配置。Sealos 模板会运行官方 BillionMail 服务组合，并提供公开 HTTPS Web 控制台和内部邮件服务协同。

部署内容包含 BillionMail Core Web/API 服务、负责 SMTP 的 Postfix、负责 IMAP/POP3 邮箱访问的 Dovecot、负责反垃圾邮件处理的 Rspamd，以及位于 `/roundcube` 的 Roundcube Webmail。Sealos 还会创建 KubeBlocks PostgreSQL、KubeBlocks Redis、持久化存储、服务发现、Ingress 和 Web 控制台 TLS。

## 常见使用场景

- **自托管邮件运营**：通过 Web 控制台管理域名、邮箱和服务端邮件设置。
- **Newsletter 发布**：在自己的基础设施上运行订阅列表和邮件活动。
- **邮件营销工作流**：在可控环境中运营外发活动，并掌握数据与配置。
- **团队邮箱管理**：创建邮箱、管理凭据，并通过 Roundcube 提供 Webmail 访问。
- **送达率测试**：调试 DNS、发信域名和邮件路由。

## BillionMail 托管依赖

Sealos 模板包含所需运行时依赖：BillionMail Core、Postfix、Dovecot、Rspamd、Roundcube、PostgreSQL 16.4、Redis 7.2 和持久化数据卷。

### 部署依赖

- [BillionMail 官网](https://www.billionmail.com/) - 官方网站
- [BillionMail GitHub](https://github.com/Billionmail/BillionMail) - 源码与上游文档
- [Sealos 上的 BillionMail 模板](https://sealos.io/products/app-store/billionmail) - Sealos 一键部署入口
- [Sealos Discord](https://discord.gg/wdUn538zVP) - Sealos 社区支持

### 实现细节

**架构组件：**

这个模板会部署以下服务：

- **BillionMail Core**：主 Web 控制台和 API 服务，通过 Sealos App URL 访问。
- **Postfix**：提供 SMTP、SMTPS 和 Submission 发信服务。
- **Dovecot**：提供 IMAP、IMAPS、POP3 和 POP3S 邮箱访问服务。
- **Rspamd**：提供反垃圾邮件和邮件过滤能力。
- **Roundcube**：位于 `/roundcube` 的 Webmail 界面。
- **PostgreSQL**：KubeBlocks PostgreSQL 16.4 集群，用于 BillionMail 和 Webmail 数据。
- **Redis**：KubeBlocks Redis 7.2 集群，用于缓存、会话和服务协同。
- **持久化卷**：存储邮件数据、可变配置、TLS 文件、日志、Webmail 数据和邮件服务状态。

**配置：**

- Sealos App URL 会在根路径打开 BillionMail，例如 `https://<app-host>.<sealos-domain>`。
- 初始管理员账号来自部署参数 `admin_username` 和 `admin_password`。
- `mail_hostname` 用于 Postfix 和 DNS 配置指引，例如 `mail.example.com`。
- `timezone` 配置容器时区，`retention_days` 控制 BillionMail 日志备份保留天数。

**许可证信息：**

此 Sealos 模板遵循 templates 仓库许可证。生产使用前请查看 BillionMail 上游仓库中的当前应用许可证条款。

## 为什么在 Sealos 上部署 BillionMail？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署、运维和资源管理。在 Sealos 上部署 BillionMail 可以获得：

- **一键部署**：通过模板化流程启动完整 BillionMail 服务栈。
- **托管云资源**：在同一平台使用 KubeBlocks PostgreSQL、KubeBlocks Redis、持久化存储、Ingress 和 TLS。
- **Canvas 运维**：部署后可通过 Canvas、AI 对话和资源卡片调整资源、查看工作负载和更新设置。
- **资源效率**：按量使用资源，并随着业务增长调整 CPU、内存和存储。
- **Kubernetes 基础**：保留 Kubernetes 的可移植性和可观测性，同时简化日常集群操作。

## 部署指南

1. 打开 [BillionMail 模板](https://sealos.io/products/app-store/billionmail)，点击 **Deploy Now**。
2. 在弹窗中配置部署参数：
   - **Admin Username**：初始 BillionMail 管理员用户名，默认值为 `billion`。
   - **Admin Password**：初始 BillionMail 管理员密码。部署前请设置强密码。
   - **Mail Hostname**：邮件服务和 DNS 指引使用的主机名，例如 `mail.example.com`。
   - **Timezone**：容器时区，例如 `Etc/UTC`。
   - **Retention Days**：BillionMail 日志备份保留天数。
3. 等待部署完成，通常需要 2-3 分钟。部署后 Sealos 会跳转到 Canvas。后续变更可以在 AI 对话中描述需求，或点击对应资源卡片修改。
4. 打开 Sealos 提供的 BillionMail App URL。控制台位于根路径，例如 `https://<app-host>.<sealos-domain>`。
5. 使用第 2 步配置的管理员用户名和密码登录。初始管理员账号会在部署期间创建，首次访问直接使用这些部署凭据。
6. 登录后先创建邮件域名和邮箱，再使用邮件投递或 Roundcube Webmail。

## 首次登录与 Webmail

在 BillionMail 登录页使用部署参数中的管理员用户名和密码。请把密码保存在自己的密码管理器中，因为模板输入就是初始管理员凭据来源。

Roundcube Webmail 地址为：

```text
https://<app-host>.<sealos-domain>/roundcube
```

请先在 BillionMail 控制台创建域名和邮箱，再登录 Roundcube。

## 邮件 DNS 与端口

BillionMail 会在 Kubernetes 内提供 SMTP、SMTPS、Submission、IMAP、IMAPS、POP3 和 POP3S 服务。公网邮件投递还需要 DNS 与网络规划：

- 将 MX 记录指向配置的 `mail_hostname`。
- 为每个发信域名配置 SPF、DKIM 和 DMARC。
- 确认目标收发网络可以访问所需 SMTP 与 IMAP/POP 端口。
- 当环境限制 `25` 端口时，认证发信使用 Submission `587` 端口。

## 扩缩容

如需调整资源，打开部署 Canvas，在对应工作负载、数据库或存储卷资源卡片中修改 CPU、内存和存储。邮件存储与投递服务属于有状态组件，修改副本或存储配置后请验证邮件流。

## 故障排查

### 管理员登录失败

- 确认正在打开 Sealos 提供的根路径 App URL。
- 使用部署时配置的 `admin_username` 和 `admin_password`。
- 等待 BillionMail 工作负载、PostgreSQL 集群、Redis 集群和初始化 Job 完成后重试。

### 邮件投递失败

- 检查发信域名的 MX、SPF、DKIM 和 DMARC 记录。
- 确认 `mail_hostname` 指向预期邮件主机。
- 检查云厂商或网络环境对 SMTP `25` 端口的限制。

### Webmail 登录失败

- 先在 BillionMail 中创建域名和邮箱。
- 打开 `/roundcube`，使用邮箱凭据登录。

## 其他资源

- [BillionMail 官网](https://www.billionmail.com/)
- [BillionMail GitHub](https://github.com/Billionmail/BillionMail)
- [Sealos 上的 BillionMail 模板](https://sealos.io/products/app-store/billionmail)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

此 Sealos 模板遵循 templates 仓库许可证。BillionMail 由上游项目分发，请查看 [BillionMail GitHub 仓库](https://github.com/Billionmail/BillionMail) 获取当前许可证条款。
