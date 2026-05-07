# 在 Sealos 上部署并托管 ZITADEL

ZITADEL 是一个开源的身份与访问管理（Identity and Access Management, IAM）平台，提供认证与授权能力。该模板会在 Sealos Cloud 上部署带托管 PostgreSQL 后端的 ZITADEL。

![ZITADEL Logo](./logo.png)

## 关于在 Sealos 托管 ZITADEL

ZITADEL 提供集中式身份服务，包括单点登录（Single Sign-On, SSO）、OAuth 2.0、开放授权连接（OpenID Connect, OIDC）、安全断言标记语言（Security Assertion Markup Language, SAML）、用户与组织管理，以及基于策略的访问控制。它常用于为 SaaS 平台、内部工具和 API 生态构建统一身份层。

该 Sealos 模板以面向生产的方式部署 ZITADEL：通过 KubeBlocks 提供持久化 PostgreSQL 存储，并通过 HTTPS Ingress 暴露公网入口。应用数据库凭据会从托管的 Kubernetes Secret 自动注入。

在首次启动阶段，模板会根据部署参数创建首个人类用户。根据 ZITADEL 官方 Kubernetes 文档中的 first-instance 模型，登录名格式应为 `<username>@zitadel.<domain>`。

## 常见使用场景

- **企业内部 SSO**：为内部控制台、管理系统和企业工具统一登录入口。
- **客户身份管理（CIAM）**：管理 SaaS 终端用户的注册、登录与账号生命周期。
- **API 与服务认证**：为后端服务和机器到机器流程签发并校验令牌。
- **B2B 多组织权限隔离**：在组织/租户维度隔离用户、角色和权限。
- **策略驱动的访问控制**：通过可配置身份策略强化安全访问路径。

## ZITADEL 托管依赖

该 Sealos 模板已包含运行所需全部依赖：ZITADEL 应用服务、托管 PostgreSQL 集群、Ingress、Service 暴露和持久化存储。

### 部署依赖文档

- [ZITADEL Kubernetes Installation](https://zitadel.com/docs/self-hosting/deploy/kubernetes/installation) - 官方安装流程与前置要求
- [ZITADEL Kubernetes Configuration](https://zitadel.com/docs/self-hosting/deploy/kubernetes/configuration) - first-instance 与运行时配置参考
- [ZITADEL Helm Values](https://github.com/zitadel/zitadel-charts/blob/main/charts/zitadel/values.yaml) - 上游 Helm 参数参考
- [ZITADEL GitHub Repository](https://github.com/zitadel/zitadel) - 源码、版本发布与问题跟踪
- [Sealos Platform](https://sealos.io) - 部署与运维平台

## 实现细节

### 架构组件

该模板会部署以下资源：

- **ZITADEL（StatefulSet）**：运行 `ghcr.io/zitadel/zitadel:v4.10.1`，启动命令为 `start-from-init`。
- **PostgreSQL 集群（KubeBlocks）**：部署 PostgreSQL `16.4.0`，提供持久化存储和托管凭据。
- **Service + Ingress**：通过 NGINX Ingress 注解与 TLS 集成，将 ZITADEL 以 HTTPS 暴露到公网。
- **App 资源**：将外部访问地址发布到 Sealos 应用卡片。

### 运行时配置

核心部署参数：

- `admin_username`：首个实例的人类管理员用户名。
- `admin_password`：首个实例的人类管理员密码。

数据库连接字段（`host`、`port`、`username`、`password`）由 KubeBlocks 生成的 Secret `${{ defaults.app_name }}-pg-conn-credential` 注入。

### 默认资源与存储

| 组件 | CPU 请求 | CPU 上限 | 内存请求 | 内存上限 | 存储 |
|---|---:|---:|---:|---:|---|
| ZITADEL | 20m | 200m | 25Mi | 256Mi | 由运行时管理 + 数据库持久化 |
| PostgreSQL | 50m | 500m | 51Mi | 512Mi | `data` 1Gi |

### 许可证信息

ZITADEL 采用 [GNU AGPL v3](https://github.com/zitadel/zitadel/blob/main/LICENSE) 许可证。

## 为什么在 Sealos 上部署 ZITADEL？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，可显著简化部署和运维流程。将 ZITADEL 部署到 Sealos，你可以获得：

- **一键部署**：无需手写 Kubernetes YAML 即可启动 IAM 基础设施。
- **数据库自动托管**：PostgreSQL 自动创建并完成连接配置。
- **易于自定义**：通过 Canvas 调整环境变量与计算/存储资源。
- **安全公网访问**：开箱即用的 HTTPS Ingress 与 TLS 支持。
- **持久化存储内置**：数据库状态可持续保存。
- **AI 辅助运维**：可通过 AI 对话或资源卡片更新配置。
- **按量计费更高效**：资源按实际负载弹性调整，避免过度预留。

将 ZITADEL 部署在 Sealos 上，你可以把精力聚焦在身份体系设计，而不是基础设施编排。

## 部署指南

1. 打开 [ZITADEL 模板](https://sealos.io/appstore/zitadel)，点击 **Deploy Now**。
2. 配置部署参数：
   - **App Host** 与 **App Name**
   - **Admin Username** 与 **Admin Password**
   - **Master Key** 建议使用系统默认生成值，除非你有明确自定义需求
3. 等待部署完成（通常 2-3 分钟）。部署后会自动跳转到 Canvas。后续变更可在对话框中描述需求由 AI 自动应用，或点击资源卡片手动修改。
4. 访问 ZITADEL 控制台并登录：
   - **Console URL**：`https://<domain>/ui/console`
   - **Login Name**：`<username>@zitadel.<domain>`
   - **Password**：你配置的 `admin_password`

其中 `<domain>` 是部署后的公网域名（通常为 `${app_host}.${SEALOS_CLOUD_DOMAIN}`）。

示例：

- Domain: `zitadel-ab12cd34.usw-1.sealos.app`
- Username: `zitadel-admin`
- Login Name: `zitadel-admin@zitadel.zitadel-ab12cd34.usw-1.sealos.app`

## 配置

部署完成后，你可以通过以下方式配置 ZITADEL：

- **AI Dialog**：描述你希望的变更，由 AI 自动落地。
- **Resource Cards**：调整 StatefulSet 资源、环境变量和 Ingress 配置。
- **ZITADEL Console**：管理组织、用户、应用与身份流程。

建议在部署后执行以下操作：

1. 验证首个管理员可正常登录。
2. 按安全策略轮换或重置初始凭据。
3. 配置 OIDC/SAML 应用与令牌策略。
4. 启用 MFA 与额外安全策略。

## 扩缩容

扩展部署容量时可按以下步骤操作：

1. 打开部署对应的 Canvas。
2. 选择 ZITADEL StatefulSet 资源卡片。
3. 根据负载提升 CPU/内存配置。
4. 应用变更并确认 readiness/liveness 探针保持健康。

若要获得更高可用性和性能，还应结合实际流量与数据保留策略规划 PostgreSQL 的规格与备份方案。

## 故障排查

### 常见问题

**问题：初始化阶段 Pod 进入 CrashLoopBackOff**
- 原因：初始管理员密码不满足密码策略要求。
- 解决：使用包含大小写字母、数字和特殊字符的强密码。

**问题：密码正确但仍无法登录**
- 原因：登录名格式错误。
- 解决：使用 `Login Name = <username>@zitadel.<domain>`。

**问题：无法访问 `/ui/console`**
- 原因：Ingress/TLS 仍在创建或签发中。
- 解决：等待 Ingress 和证书就绪后重试。

**问题：启动时报数据库连接错误**
- 原因：PostgreSQL 尚未就绪，或启动时出现临时依赖竞争。
- 解决：确认 PostgreSQL 集群健康后重试。

### 获取帮助

- [ZITADEL Documentation](https://zitadel.com/docs)
- [ZITADEL GitHub Issues](https://github.com/zitadel/zitadel/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [ZITADEL Self-Hosting Overview](https://zitadel.com/docs/self-hosting/deploy/overview)
- [ZITADEL Kubernetes Deployment Docs](https://zitadel.com/docs/self-hosting/deploy/kubernetes)
- [Sealos Documentation](https://sealos.io/docs)

## 许可证

该 Sealos 模板遵循仓库许可证条款。ZITADEL 本身采用 [GNU AGPL v3](https://github.com/zitadel/zitadel/blob/main/LICENSE)。
