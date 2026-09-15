# 在 Sealos 上部署并托管 ZITADEL

ZITADEL 是一个开源身份与访问管理平台，支持单点登录（SSO）、OAuth 2.0、OpenID Connect、SAML、用户管理和策略授权。该模板会在 Sealos Cloud 上部署 ZITADEL v4.16.2，并自动创建托管 PostgreSQL 数据库。

![ZITADEL 管理控制台](./website-screenshot.webp)

## 关于在 Sealos 托管 ZITADEL

ZITADEL 为应用、API、员工和客户提供统一身份层。管理员可以在管理控制台中集中维护用户、项目、应用、角色、登录策略和身份提供商。

该模板保留精简的单 ZITADEL 拓扑，并通过 KubeBlocks 部署 PostgreSQL 16.4。Sealos 会准备数据库持久化存储、TLS 公网入口、服务发现和应用访问链接。启动门会等待 PostgreSQL 就绪后再初始化 ZITADEL，从源头解决首次部署时的数据库竞争问题。

## 常见使用场景

- **企业 SSO**：为内部控制台和业务应用提供统一认证。
- **客户身份管理（CIAM）**：管理客户登录、账号生命周期、多因素认证和账号恢复流程。
- **应用认证**：为 Web、原生和移动应用接入 OAuth 2.0 与 OpenID Connect。
- **API 授权**：为 API 和机器间工作负载签发并校验令牌。
- **B2B 组织管理**：按客户组织隔离用户、角色和访问策略。

## ZITADEL 托管依赖

模板已包含 ZITADEL 服务、托管 PostgreSQL 集群、数据库持久化存储、HTTPS Ingress 和 Sealos App 资源。

### 部署参考

- [ZITADEL Kubernetes 指南](https://zitadel.com/docs/self-hosting/deploy/kubernetes) - 官方 Kubernetes 部署说明
- [ZITADEL 配置参考](https://zitadel.com/docs/self-hosting/manage/configure/configure) - 运行时与首实例配置
- [ZITADEL GitHub 仓库](https://github.com/zitadel/zitadel) - 源码与版本发布

## 实现细节

### 架构组件

- **ZITADEL StatefulSet**：运行 `ghcr.io/zitadel/zitadel:v4.16.2`，并使用官方 `start-from-init` 启动命令。
- **PostgreSQL 就绪门**：使用 `postgres:16.4-alpine` 和 `pg_isready`，确认数据库可用后再启动 ZITADEL。
- **PostgreSQL 集群**：通过 KubeBlocks 运行 PostgreSQL 16.4，并挂载 1 GiB 持久化卷。
- **Service 与 Ingress**：将 8080 端口通过公网 HTTPS 地址暴露。
- **App 资源**：把 ZITADEL 入口地址添加到 Sealos 部署 Canvas。

数据库主机、端口、用户名和密码均来自 KubeBlocks 连接 Secret。模板会根据必填部署参数创建首个组织及其 IAM 所有者。

### 已验证的最低资源

下列配置通过了空数据库初始化、管理员登录、Organization 与 Users 控制台操作，以及 222 秒稳定性测试；整个过程重启数为 0：

| 组件 | CPU 请求 | CPU 上限 | 内存请求 | 内存上限 | 存储 |
|---|---:|---:|---:|---:|---:|
| ZITADEL | 10m | 100m | 25Mi | 256Mi | - |
| PostgreSQL 就绪门 | 10m | 100m | 12Mi | 128Mi | - |
| PostgreSQL | 50m | 500m | 51Mi | 512Mi | 1Gi |

ZITADEL 使用 128 MiB 内存时，在首次初始化阶段触发了 `OOMKilled`。应用内存上限应保持在 256 MiB 或更高档位。

## 为什么在 Sealos 上部署 ZITADEL？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统。该模板提供以下能力：

- **一键部署**：一次完成应用、数据库、网络和存储资源创建。
- **托管 PostgreSQL**：自动创建 KubeBlocks 数据库并完成连接配置。
- **安全公网访问**：自动获得 HTTPS 地址，由 Ingress 负责 TLS 终止。
- **资源高效利用**：从经过验证的低负载规格起步，按实际资源用量付费。
- **AI 辅助运维**：通过 Canvas AI 对话或资源卡片调整部署。

## 部署指南

1. 打开 [ZITADEL 模板](https://sealos.io/products/app-store/zitadel)，点击 **Deploy Now**。
2. 填写首个管理员的必填参数：
   - `admin_username`：首个 IAM 所有者账号的用户名部分。
   - `admin_password`：至少 8 个字符，并包含大小写字母、数字和特殊字符。
3. 启动部署，等待 PostgreSQL 与 ZITADEL 就绪。全新部署通常需要 2-3 分钟，完成后 Sealos 会打开 Canvas。
4. 打开 ZITADEL App 地址。根地址会进入登录流程，管理控制台位于 `/ui/console/`。
5. 使用生成的登录名和部署时填写的密码登录：
   - **登录名**：`<admin_username>@zitadel.<deployed-domain>`
   - **密码**：`admin_password` 对应的值
6. 首次登录时，可配置双因素认证，或点击 **跳过** 进入管理控制台。

例如，`admin_username` 为 `admin`，部署域名为 `zitadel-ab12cd34.usw-1.sealos.app` 时，登录名如下：

```text
admin@zitadel.zitadel-ab12cd34.usw-1.sealos.app
```

请使用上方完整登录名。ZITADEL 会通过其中的组织后缀识别账号。

## 配置

登录后，可在 ZITADEL 控制台中创建项目和应用、添加用户、配置身份提供商并管理策略。生产应用接入前，建议完成以下安全设置：

1. 为管理员账号配置 MFA。
2. 检查组织级和实例级登录策略。
3. 为每个接入服务创建独立项目和应用。
4. 将客户端凭据与回调地址记录在安全系统中。

系统生成的 32 字符主密钥用于保护 ZITADEL 加密数据。数据库整个生命周期应持续使用同一个主密钥。

后续资源调整可通过 Sealos Canvas 的 AI 对话或资源卡片完成。该模板保持单副本 StatefulSet；高可用架构需要结合官方生产指南统一规划 ZITADEL 与 PostgreSQL。

## 故障排查

### 登录页提示找不到用户

请使用 `<admin_username>@zitadel.<deployed-domain>`。组织域名会在公网部署域名前增加 `zitadel.` 前缀。

### 应用仍在启动

就绪门会先等待托管 PostgreSQL 端点，再执行 ZITADEL 首实例迁移。全新部署可预留 2-3 分钟，并在 Canvas 中查看 PostgreSQL 与 StatefulSet 资源卡片的状态。

### ZITADEL 因 `OOMKilled` 重启

请将 ZITADEL 内存上限设置为至少 256 MiB。实测 128 MiB 档位在首次初始化期间资源不足。

### 获取帮助

- [ZITADEL 文档](https://zitadel.com/docs)
- [ZITADEL GitHub Issues](https://github.com/zitadel/zitadel/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

该 Sealos 模板遵循仓库许可证。ZITADEL 采用 [GNU Affero General Public License v3.0](https://github.com/zitadel/zitadel/blob/main/LICENSE)。
