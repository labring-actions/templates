# 在 Sealos 上部署和托管 Logto

[Logto](https://logto.io/) 是一个开源身份平台，适合为现代应用构建登录注册、用户管理、OIDC/OAuth 2.0、SAML、多租户和授权能力。

## 模板内容

- 使用固定镜像 `svhd/logto:1.40.1` 部署 Logto `1.40.1`。
- 自动创建并初始化专用 PostgreSQL 数据库。
- 提供两个公开 HTTPS 地址：一个用于应用认证流量，一个用于 Admin Console。
- 首次启动时自动创建数据库、写入种子数据并执行数据库变更。

## 使用要求

- 一个 [Sealos](https://sealos.io/) 账号。
- 不需要外部数据库；模板会自动创建 PostgreSQL。

## 在 Sealos 上部署

1. 打开 [Sealos Logto 模板](https://sealos.io/products/app-store/logto)。
2. 点击 **Deploy Now**，可以使用自动生成的应用名和域名，也可以在部署前自定义。
3. 等待 Logto 应用和 PostgreSQL 数据库都进入运行状态。
4. 在 Sealos 应用详情中打开 Admin Console 地址。

## 首次注册与登录

Logto 会提供两个地址：

- **Admin Console**：`https://${{ defaults.app_host }}-admin.${{ SEALOS_CLOUD_DOMAIN }}`
- **Core/Auth 端点**：`https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`

首次启动后，请打开 **Admin Console** 地址。欢迎页会显示 **Create account** 入口，可用用户名和密码创建初始管理员账号。开源版只允许创建一次初始管理员账号；创建完成后，再回到 Admin Console 使用 **Sign in** 登录。

将 **Core/Auth 端点** 作为连接业务应用时的 issuer 和重定向地址基础域名，用于 OIDC/OAuth 登录流程。

## 部署后检查

- 在 Admin Console 创建第一个管理员账号。
- 在 Logto 中配置业务应用的 redirect URI。
- 确认 Core/Auth 端点和 Admin Console 端点都使用 HTTPS。
- 在启用生产身份流程前，先阅读 Logto 官方文档。

## 参考链接

- [Logto 文档](https://docs.logto.io/)
- [Logto GitHub 仓库](https://github.com/logto-io/logto)
- [Sealos 文档](https://sealos.io/docs/)
