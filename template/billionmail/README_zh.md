# BillionMail

BillionMail 是开源邮件服务器、Newsletter 和邮件营销平台。这个 Sealos 模板使用官方 BillionMail 服务镜像，并通过 KubeBlocks 提供 PostgreSQL 和 Redis。

## 在 Sealos 上部署

1. 打开 [Sealos 上的 BillionMail](https://sealos.io/products/app-store/billionmail)。
2. 点击 **Deploy Now**。
3. 填写管理员用户名、管理员密码、安全入口路径、邮件主机名、时区和日志保留天数。
4. 等待应用状态变为运行中。
5. 先访问一次 `https://<app-host>.<sealos-domain>/<safe-path>` 解锁控制台入口，再使用管理员账号登录。

## 首次登录

BillionMail 控制台使用模板输入里的安全入口路径。默认路径是 `billionmail`，首次控制台地址形如：

```text
https://<app-host>.<sealos-domain>/billionmail
```

访问该入口后，在登录页使用部署时填写的管理员用户名和密码登录。

## Webmail

Roundcube webmail 通过同一个 Web 服务的 `/roundcube/` 提供。请先在 BillionMail 控制台创建邮件域和邮箱，再使用 webmail。

## 邮件 DNS 与端口注意事项

BillionMail 在 Kubernetes Service 内提供 SMTP、SMTPS、Submission、IMAP、IMAPS、POP3 和 POP3S 服务。真实公网收发邮件还需要额外 DNS 和网络配置：

- 将 MX 记录指向部署时配置的邮件主机名。
- 为每个发信域名配置 SPF、DKIM 和 DMARC。
- 确认 SMTP 与 IMAP/POP 端口能被目标网络访问。
- 许多云环境会限制 25 端口入站或出站；认证发信优先使用 Submission 587 端口。

## 数据

模板会创建：

- KubeBlocks PostgreSQL 16.4，用于 BillionMail 应用与邮件元数据。
- KubeBlocks Redis 7.2.7，用于会话、缓存和服务协同。
- 一个持久化卷，用于邮件数据、webmail 数据、Rspamd 数据、Postfix 队列、TLS 文件、日志和可变配置。

## 源码

- [BillionMail GitHub](https://github.com/Billionmail/BillionMail)
- [BillionMail 官网](https://www.billionmail.com/)
