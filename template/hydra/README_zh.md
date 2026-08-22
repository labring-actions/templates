# 在 Sealos 上部署和托管 Ory Hydra

Ory Hydra 是 OAuth 2.0 和 OpenID Connect 提供程序。此模板会在 Sealos Cloud 上部署 Hydra、KubeBlocks PostgreSQL 数据库，并暴露公开 OAuth/OIDC 端点。

![Ory Hydra 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/hydra/website-screenshot.webp)

## 关于托管 Ory Hydra

Hydra 提供符合标准的 OAuth 2.0 和 OpenID Connect 端点，用于委托授权、令牌签发和发现元数据。模板运行官方 Hydra 容器，在启动前执行 SQL 迁移，并将运行状态保存在 PostgreSQL 中。

Hydra 会把用户登录和授权同意页面交给你自己的身份 UI。部署时配置 `login_url` 和 `consent_url`，OAuth 流程会把用户重定向到这些页面。

## 常见使用场景

- **OAuth 提供程序**：为 API 签发访问令牌和刷新令牌。
- **OpenID Connect 发现**：发布 issuer 元数据和 JWKS 端点。
- **集中授权层**：让多个服务接入统一 OAuth/OIDC 提供程序。
- **开发者身份实验环境**：用自托管 Hydra 测试 OAuth 客户端。

## Ory Hydra 托管依赖

Sealos 模板包含 Hydra 和 KubeBlocks PostgreSQL。

### 部署依赖

- [Ory Hydra 文档](https://www.ory.sh/docs/hydra) - 官方文档
- [Hydra GitHub 仓库](https://github.com/ory/hydra) - 源码和发布版本
- [OAuth 2.0 与 OIDC 概念](https://www.ory.sh/docs/hydra/concepts) - 核心概念

### 实现细节

**架构组件：**

- **Hydra**：使用官方 `oryd/hydra:v2.3.0` 镜像的公开 OAuth/OIDC 服务
- **PostgreSQL**：用于保存 Hydra 状态的 KubeBlocks PostgreSQL 16.4 集群
- **迁移 init container**：Hydra 启动前执行 `hydra migrate sql up -e --yes`
- **Ingress**：通过自动 HTTPS 暴露公开端口

**配置：**

公开 issuer URL 由 Sealos 应用域名生成。Hydra 需要外部登录和授权同意 URL，因此部署时请填写身份 UI 或授权同意应用的公开地址。

**许可证信息：**

Ory Hydra 使用 Apache License 2.0。

## 为什么在 Sealos 上部署 Ory Hydra？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署、存储、网络和生命周期管理。部署 Ory Hydra 到 Sealos 后，你可以获得：

- **一键部署**：从应用商店模板启动 Hydra 和 PostgreSQL。
- **托管数据库**：KubeBlocks 为 Hydra 状态提供 PostgreSQL。
- **即时公网访问**：Sealos 为 OAuth/OIDC 元数据和 API 创建 HTTPS 端点。
- **易于定制**：在部署表单中配置登录和授权同意 URL。
- **Kubernetes 运维能力**：在 Sealos 控制台管理资源、日志和扩缩容。

## 部署指南

1. 打开 [Ory Hydra 模板](https://sealos.io/products/app-store/hydra)，点击 **Deploy Now**。
2. 使用外部身份 UI 端点配置 `login_url` 和 `consent_url`。
3. 等待部署完成。Hydra 会先执行数据库迁移，然后服务进入就绪状态。
4. 通过生成的地址访问公开端点：
   - **OIDC Discovery**：`https://[your-app-url]/.well-known/openid-configuration`
   - **JWKS**：`https://[your-app-url]/.well-known/jwks.json`
   - **健康检查**：`https://[your-app-url]/health/ready`

## 配置

部署后，可通过内部网络中的 Hydra admin API 配置 OAuth 客户端，或添加内部管理流程。公开 Sealos URL 用于 OAuth/OIDC 客户端流量。

## 扩缩容

如需扩缩容 Hydra，打开部署对应 Canvas，点击 Deployment 资源卡，调整副本数或资源后应用变更。请根据令牌和授权同意流量调整 PostgreSQL 资源。

## 故障排查

### 登录或授权同意跳转失败

- 原因：`login_url` 或 `consent_url` 仍为占位地址，或身份 UI 无法访问。
- 解决：将部署输入更新为登录和授权同意应用的公开 URL。

### Discovery 元数据中的 Issuer 异常

- 原因：issuer 需要匹配 Sealos 公开 URL。
- 解决：检查 App URL，并保留生成的 host 设置重新部署。

## 其他资源

- [Hydra CLI 参考](https://www.ory.sh/docs/hydra/cli)
- [OAuth2 流程](https://www.ory.sh/docs/hydra/oauth2)
- [Ory 社区](https://www.ory.sh/docs/ecosystem/community)

## 许可证

此 Sealos 模板遵循仓库许可证。Ory Hydra 本身使用 Apache License 2.0。
