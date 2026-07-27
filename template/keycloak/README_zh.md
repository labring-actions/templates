# 在 Sealos 上部署和托管 Keycloak

Keycloak 是一个开源身份与访问管理平台，可为应用和服务提供统一认证。这个模板会在 Sealos 上部署 Keycloak 26.7.0，并创建持久化的 KubeBlocks PostgreSQL 16.4 数据库。

![Keycloak 管理控制台](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/keycloak/website-screenshot.webp)

## 关于 Keycloak 托管

Keycloak 提供集中登录、单点登录、用户目录联邦、身份提供商代理、多因素认证，以及基于 OpenID Connect、OAuth 2.0 和 SAML 的应用集成。Realm 用于隔离一个组织或环境中的用户、客户端、角色、用户组、认证策略和会话。

这个模板会为 Keycloak 管理控制台与认证 API 创建公网 HTTPS 入口。Realm 配置和身份数据保存在 PostgreSQL 中，可在应用重启后持续保留。

## 常见使用场景

- **单点登录**：为内部应用和面向客户的应用提供统一身份入口。
- **应用认证**：为 Web 和移动应用接入 OpenID Connect、OAuth 2.0 或 SAML。
- **身份目录联邦**：连接 LDAP、Active Directory、社交账号和外部身份提供商。
- **集中权限管理**：在同一个控制台中管理用户、用户组、角色、会话和认证策略。
- **多租户身份系统**：通过独立 Realm 隔离不同组织或环境。

## Keycloak 托管依赖

这个 Sealos 模板会创建：

- Keycloak 26.7.0
- 带持久化存储的 KubeBlocks PostgreSQL 16.4
- 数据库初始化 Job
- 公网 HTTPS Ingress 和 Sealos Canvas 应用入口

### 部署依赖

- [Keycloak 文档](https://www.keycloak.org/documentation) - 服务端和管理指南
- [Keycloak GitHub 仓库](https://github.com/keycloak/keycloak) - 源码和版本信息
- [Sealos 应用市场](https://sealos.io/products/app-store) - 一键部署应用

## 实现细节

### 架构组件

- **Keycloak StatefulSet**：运行身份服务、管理控制台、认证端点和账户控制台。
- **PostgreSQL Cluster**：保存 Realm、用户、客户端、角色、凭据、会话和配置。
- **数据库初始化 Job**：等待 PostgreSQL 就绪，并以幂等方式创建 `keycloak` 数据库。
- **Ingress 和 App 资源**：通过 HTTPS 发布 Keycloak，并在 Sealos Canvas 中创建入口。

Keycloak 使用 KubeBlocks 生成的凭据连接 PostgreSQL。健康检查通过 Keycloak 管理端口访问官方 `/health/started`、`/health/ready` 和 `/health/live` 端点。

### 资源规格

模板经过真实部署测试，并调整到以下最小资源规格：

| 组件 | CPU 上限 | 内存上限 | 存储 |
| --- | ---: | ---: | ---: |
| Keycloak | 200m | 1024Mi | - |
| PostgreSQL | 500m | 512Mi | 1Gi |
| 初始化容器和 Job | 100m | 128Mi | - |

Keycloak 使用 100m CPU 冷启动时出现了持续的阻塞线程告警。200m / 1024Mi 规格完成了数据库迁移、管理员登录、Realm 创建、用户创建、随机 404 请求和稳定日志窗口，所有容器保持零重启。Realm 数量与认证流量增长后，应提高 Keycloak CPU 和 PostgreSQL 容量。

### 许可信息

Keycloak 使用 Apache License 2.0。这个 Sealos 模板负责封装部署配置，并保持上游许可证。

## 为什么在 Sealos 上部署 Keycloak？

- **一键部署**：从应用市场同时创建 Keycloak 和 PostgreSQL。
- **托管数据库**：KubeBlocks 管理 PostgreSQL 凭据、存储和生命周期资源。
- **身份数据持久化**：Realm 和用户数据可在 Keycloak 重启后持续保留。
- **公网 HTTPS 访问**：Sealos 自动为管理控制台和认证端点创建 Ingress 与 TLS。
- **健康感知启动**：数据库启动门禁和官方健康端点会在 Keycloak 就绪后接入流量。
- **简化运维**：可以从 Sealos Canvas 查看日志、调整资源和管理部署。

## 部署指南

1. 打开 [Keycloak 模板](https://sealos.io/products/app-store/keycloak)，点击 **Deploy Now**。
2. 输入初始管理员用户名和高强度管理员密码，并把这组凭据保存在密码管理器中。
3. 点击 **Deploy**，等待 PostgreSQL 初始化和 Keycloak 冷启动。首次部署通常需要几分钟。
4. 从 Sealos Canvas 打开 **Keycloak** 入口。
5. 选择 **Administration Console**，使用部署时填写的管理员凭据登录。

## 登录和用户注册

### 初始管理员登录

部署参数 `admin_username` 和 `admin_password` 会在 `master` Realm 中创建临时引导管理员。打开 `https://<app-host>/admin/`，使用这组凭据登录。

使用引导账号创建长期管理员：

1. 选择 `master` Realm。
2. 打开 **Users**，点击 **Add user**，创建长期管理员。
3. 打开新用户的 **Credentials** 标签页，设置长期密码。
4. 打开 **Role mapping**，分配 `admin` Realm 角色，并在新的浏览器会话中验证该账号。
5. 长期账号验证通过后，删除临时引导管理员。

`master` Realm 用于管理 Keycloak 服务。业务应用的用户和客户端应放在单独创建的 Realm 中。

### 应用用户

在目标 Realm 的 **Users** 页面创建用户。Realm 管理员可以通过 **Realm settings** > **Login** > **User registration** 管理自助注册。每个应用都通过对应 Realm 中创建的客户端接入，并使用该 Realm 的 OpenID Connect、OAuth 2.0 或 SAML 端点。

## 配置参数

| 参数 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| `admin_username` | 部署时填写 | 是 | `master` Realm 的初始引导管理员用户名。 |
| `admin_password` | 部署时填写 | 是 | 初始引导管理员密码。请安全保存，并在首次登录后迁移到长期管理员账号。 |

Sealos 会生成公网应用地址，并将它配置为 Keycloak 主机名。PostgreSQL 连接信息来自 KubeBlocks 创建的凭据 Secret。

## 扩缩容

1. 在 Sealos Canvas 中打开 Keycloak 部署。
2. 提高 Keycloak CPU，改善启动速度和登录吞吐量。
3. Realm、缓存或扩展提供商增长后，提高 Keycloak 内存。
4. 身份数据和会话量增长后，提高 PostgreSQL 资源与存储容量。

这个模板使用一个 Keycloak 副本和一个 PostgreSQL 副本。具有严格可用性目标的生产环境应规划经过验证的多副本 Keycloak 与高可用 PostgreSQL 拓扑。

## 故障排查

### 管理控制台仍在启动

- 等待 Keycloak 资源卡片显示 Ready；冷启动过程包含服务构建优化和数据库迁移。
- 在 Sealos Canvas 中查看 Keycloak 启动日志。
- 确认 PostgreSQL 资源卡片处于 Running 状态。

### 管理员登录失败

- 使用部署时填写的 `admin_username` 和 `admin_password`。
- 确认登录页使用 `master` Realm。
- 创建长期管理员后，确认该账号已经获得 `admin` Realm 角色。

### 应用回调地址或签发者地址异常

- 使用 Sealos Canvas 中显示的 Keycloak 公网 HTTPS 地址配置客户端。
- 在客户端设置中填写应用的重定向 URI 和 Web Origin。
- Realm 签发者地址为 `https://<app-host>/realms/<realm-name>`。

### Realm 用户无法自助注册

- 打开目标 Realm，启用 **Realm settings** > **Login** > **User registration**。
- 检查该 Realm 的邮箱验证、密码策略和必需操作配置。

### 启动时出现数据库错误

- 确认 KubeBlocks PostgreSQL Cluster 处于 Running 状态。
- 查看数据库初始化 Job 和 Keycloak init container 日志。
- 确认 PostgreSQL 持久卷具有可用容量。

## 相关资源

- [Keycloak 官网](https://www.keycloak.org/)
- [Keycloak 服务管理指南](https://www.keycloak.org/docs/latest/server_admin/)
- [Keycloak 服务端指南](https://www.keycloak.org/guides#server)
- [Keycloak GitHub](https://github.com/keycloak/keycloak)
- [Sealos 文档](https://sealos.io/docs)

## 许可

这个 Sealos 模板遵循模板仓库许可证。Keycloak 使用 Apache License 2.0。
