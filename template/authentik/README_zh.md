# 在 Sealos 上部署并托管 Authentik

Authentik 是一个开源的身份提供方（Identity Provider, IdP）与访问管理平台。该模板会在 Sealos Cloud 上部署包含独立 Worker 和托管 PostgreSQL 后端的 Authentik。

![Authentik Logo](./logo.png)

## 关于在 Sealos 托管 Authentik

Authentik 提供集中认证、单点登录（Single Sign-On, SSO）、基于策略的访问控制和身份生命周期管理能力。它支持开放授权连接（OpenID Connect, OIDC）与安全断言标记语言（Security Assertion Markup Language, SAML）等现代协议，适用于自托管应用和内部平台。

这个 Sealos 模板以多服务架构部署 Authentik：主服务负责 Web/API 流量，后台 Worker 处理异步任务，PostgreSQL 集群负责持久化数据。同时会自动创建 HTTPS Ingress 和运行时所需的持久卷。

部署完成后，你会获得一个带 TLS 的公网访问地址，并可在浏览器中完成初始化向导。后续运维可通过 Canvas 的 AI 对话或资源卡片完成。

## 常见使用场景

- **内部工具统一登录（SSO）**：将内部控制台和服务的登录统一到一个身份中心。
- **自托管应用的 OIDC/SAML 网关**：为支持联合登录的应用快速接入标准认证。
- **MFA 与无密码访问**：通过多因素认证与现代认证方式提升登录安全性。
- **团队与角色访问控制**：基于用户和用户组为 SaaS 与平台工作负载分配权限。
- **Kubernetes 应用身份入口**：以统一认证和策略能力保护应用入口。

## Authentik 托管依赖

该 Sealos 模板已包含全部必需依赖：Authentik Server、Authentik Worker、PostgreSQL 数据库、Ingress 与持久化存储。

### 部署依赖文档

- [Authentik Documentation](https://docs.goauthentik.io/) - 官方文档与部署指南
- [Authentik GitHub Repository](https://github.com/goauthentik/authentik) - 源码、版本发布与问题跟踪
- [Authentik Providers Guide](https://docs.goauthentik.io/docs/providers/) - OIDC、SAML 与代理提供方集成指南
- [Sealos Platform](https://sealos.io) - 部署与运维平台

## 实现细节

### 架构组件

该模板会部署以下资源：

- **Authentik Server（StatefulSet）**：运行 `ghcr.io/goauthentik/server:2025.12.3` 的 `server` 模式，对外提供 `9000` 端口 Web UI/API，并在集群内暴露 `9443`。
- **Authentik Worker（StatefulSet）**：使用相同镜像运行 `worker` 模式，处理后台与定时任务。
- **PostgreSQL 集群（KubeBlocks）**：部署 PostgreSQL `16.4.0`，提供持久化存储和基于 Secret 的凭据注入。
- **PostgreSQL 初始化任务（Init Job）**：等待数据库就绪后，若不存在则创建 `authentik` 数据库。
- **Service + Ingress**：通过 Sealos 自动 TLS 证书集成，将 Authentik 以 HTTPS 暴露到公网。
- **App 资源**：将访问 URL 发布到 Sealos 应用卡片，便于在 Canvas 一键进入。

### 默认资源与存储

| 组件 | CPU 请求 | CPU 上限 | 内存请求 | 内存上限 | 存储 |
|---|---:|---:|---:|---:|---|
| Authentik Server | 20m | 200m | 51Mi | 512Mi | `/data` 1Gi, `/templates` 1Gi |
| Authentik Worker | 20m | 200m | 51Mi | 512Mi | `/data` 1Gi, `/certs` 1Gi, `/templates` 1Gi |
| PostgreSQL | 50m | 500m | 51Mi | 512Mi | `data` 1Gi |

### 配置说明

部署时模板会使用以下核心参数：

- `app_host`：Ingress 使用的公网域名前缀。
- `app_name`：本次部署的资源命名前缀。
- `authentik_secret_key`：运行时密钥（默认自动生成）。

数据库主机、端口、用户名和密码会从 Kubernetes 自动生成的 Secret 注入。Authentik Server 与 Worker 共享同一个 PostgreSQL 后端和密钥，以保证运行行为一致。

### 许可证信息

Authentik 为开源项目，采用上游维护的许可证条款。请参考 [Authentik LICENSE](https://github.com/goauthentik/authentik/blob/main/LICENSE) 获取最新信息。

## 为什么在 Sealos 上部署 Authentik？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，覆盖从部署到运维的完整应用生命周期。将 Authentik 部署到 Sealos，你可以获得：

- **一键部署**：无需手写 Kubernetes 清单，即可启动多服务身份系统。
- **数据库自动托管**：PostgreSQL 会自动创建、连接并初始化。
- **易于自定义**：可在 Canvas 对话框中调整环境变量、存储和计算资源。
- **安全公网访问**：默认提供自动 HTTPS Ingress 与证书集成。
- **持久化存储内置**：重启后仍可保留身份和配置数据。
- **按量计费更高效**：可按工作负载弹性调整，避免长期过度预留。
- **AI 辅助运维**：可通过 AI 对话完成部署后的配置变更。

将 Authentik 部署到 Sealos 后，你可以把精力聚焦在身份架构本身，而不是底层基础设施编排。

## 部署指南

1. 打开 [Authentik 模板](https://sealos.io/appstore/authentik)，点击 **Deploy Now**。
2. 配置部署参数：
   - **App Host**：公网域名前缀。
   - **App Name**：部署资源前缀。
   - **Authentik Secret Key**：可使用默认生成值，或提供你自己的高强度密钥。
3. 等待部署完成（通常 2-3 分钟）。部署后会自动跳转到 Canvas。后续变更可在对话框中描述需求由 AI 自动应用，或点击资源卡片手动修改。
4. 打开生成的访问地址，完成 Authentik 初始化流程并创建首个管理员账号。

## 配置

部署完成后，可通过以下方式配置 Authentik：

- **AI 对话框**：用自然语言描述变更需求，由 AI 自动落地。
- **资源卡片**：在 Canvas 中调整 StatefulSet 资源、环境变量与存储。
- **Authentik 管理后台**：管理提供方、应用、流程、策略、用户组与品牌设置。

典型的部署后配置任务包括：

1. 在初始化向导中创建首个管理员账号。
2. 按需接入外部身份源。
3. 添加 OIDC/SAML 提供方并映射应用。
4. 为高权限用户启用 MFA 策略。

## 扩缩容

扩展运行容量时可按以下步骤操作：

1. 在 Canvas 打开当前部署。
2. 选择 Server 或 Worker 的 StatefulSet 资源卡片。
3. 根据负载提高 CPU 和内存资源。
4. 应用变更并确认健康检查恢复正常。

多数场景建议先进行垂直扩容。若需横向扩展，请结合你的业务负载与上游 Authentik 指南调整架构。

## 故障排查

### 常见问题

**问题：初始化页面不可访问**
- 原因：Server 容器仍在启动，或依赖组件尚未就绪。
- 解决：等待 Authentik Server 探针状态健康后，再刷新公网访问地址。

**问题：启动时出现数据库连接错误**
- 原因：PostgreSQL 尚未就绪，或初始化任务尚未完成。
- 解决：检查 PostgreSQL 集群状态，并确认 Init Job 成功完成后再重启 Authentik Pod。

**问题：Worker 报告健康检查失败**
- 原因：密钥不一致或后端连接临时异常。
- 解决：确认 Server 与 Worker 使用相同的 `AUTHENTIK_SECRET_KEY` 和 PostgreSQL 凭据，然后重启 Worker Pod。

**问题：无法通过 HTTPS 访问 Authentik**
- 原因：Ingress 或证书签发流程仍在进行中。
- 解决：检查 Ingress 域名配置，并在 Sealos 中等待 TLS 证书就绪。

### 获取帮助

- [Authentik Documentation](https://docs.goauthentik.io/)
- [Authentik GitHub Issues](https://github.com/goauthentik/authentik/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Authentik User Guides](https://docs.goauthentik.io/docs/)
- [Authentik Release Notes](https://github.com/goauthentik/authentik/releases)
- [Sealos Documentation](https://sealos.io/docs)

## 许可证

该 Sealos 模板遵循仓库许可证条款。Authentik 本身遵循上游项目许可证；请以官方仓库中的最新许可证信息为准。
