# 在 Sealos 上部署并托管 Pocket ID

Pocket ID 是一个简洁的开放授权连接（OpenID Connect, OIDC）提供方，使用通行密钥（Passkey）而非密码进行身份认证。该模板会在 Sealos Cloud 上部署一个可用于生产环境、具备持久化能力的 Pocket ID 服务。

## 关于在 Sealos 托管 Pocket ID

Pocket ID 面向希望使用轻量级、自托管身份系统的团队和个人，核心特点是基于 Passkey 的现代认证体验。它提供标准 OIDC 端点，可为你的内部或公网应用提供统一登录能力。

该 Sealos 模板以单 StatefulSet 方式部署 Pocket ID，并将持久化存储挂载到 `/app/data`，确保身份数据在 Pod 重启或升级后仍可保留。公网访问通过 Sealos 托管的 HTTPS Ingress 暴露，并默认启用 TLS；运行参数通过模板输入与环境变量注入。

## 常见使用场景

- **内部工具自托管 SSO**：将仪表盘、管理后台和工程工具统一接入 Pocket ID。
- **Passkey 优先认证**：以抗钓鱼能力更强的 Passkey 替代传统密码登录流程。
- **Homelab 或中小团队身份网关**：为多个自托管服务集中管理认证能力，降低维护复杂度。
- **开发与测试环境认证统一**：在测试集群中提供一致的 OIDC 登录体验。

## Pocket ID 托管依赖

该 Sealos 模板已包含 Pocket ID 所需的全部运行时依赖：

- Pocket ID 应用容器
- 用于稳定实例与存储绑定的 Kubernetes `StatefulSet`
- 用于集群内流量转发的 Kubernetes `Service`
- 提供公网 HTTPS 访问并启用 TLS 的 Kubernetes `Ingress`
- 挂载到 `/app/data` 的持久卷声明（Persistent Volume Claim, PVC）

### 部署依赖文档

- [Pocket ID Website](https://pocket-id.org) - 产品概览与版本信息
- [Pocket ID Documentation](https://docs.pocket-id.org) - 安装与配置文档
- [Pocket ID GitHub Repository](https://github.com/pocket-id/pocket-id) - 源码与问题跟踪
- [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html) - OIDC 协议参考

### 实现细节

**架构组件：**

该模板会部署以下资源：

- **Pocket ID StatefulSet**（`ghcr.io/pocket-id/pocket-id:v2.2.0`）：主身份服务（1 副本）
- **Service**：将容器端口 `1411` 暴露到集群网络
- **Ingress**：通过 `https://<app_host>.<SEALOS_CLOUD_DOMAIN>` 对外提供 TLS 访问
- **Persistent Storage**：`1Gi` PVC 挂载到 `/app/data`，用于持久化应用状态

**配置说明：**

- `APP_URL` 根据 `app_host` 与 Sealos 域名自动生成。
- `ENCRYPTION_KEY` 由模板变量注入（默认随机生成）。
- `TRUST_PROXY` 默认为 `false`。
- 单 Pod 默认资源配置：
  - **limits**：`cpu: 200m`，`memory: 256Mi`
  - **requests**：`cpu: 20m`，`memory: 25Mi`

**许可证信息：**

Pocket ID 采用 [BSD 2-Clause License](https://github.com/pocket-id/pocket-id/blob/main/LICENSE)。

## 为什么在 Sealos 上部署 Pocket ID？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，在统一工作空间中覆盖部署、运维和迭代。将 Pocket ID 部署到 Sealos，你可以获得：

- **一键部署**：无需手写 Kubernetes 清单即可快速上线 Pocket ID。
- **Kubernetes 级可靠性**：基于成熟的 StatefulSet、Service 与 Ingress 原语运行。
- **便捷的 Day-2 运维**：通过 Canvas 资源卡片和 AI 对话调整参数与资源。
- **内置持久化存储**：重启和更新后仍可保留身份数据。
- **即开即用的公网 HTTPS**：默认获得带托管 TLS 的公网访问地址。
- **按量计费的弹性成本**：计算与存储按实际使用规模扩展。

## 部署指南

1. 打开 [Pocket ID 模板](https://sealos.io/appstore/pocket-id)，点击 **Deploy Now**。
2. 配置部署参数：
   - `app_host`
   - `app_name`
   - `encryption_key`
3. 等待部署完成（通常 2-3 分钟）。部署后会自动跳转到 Canvas。
4. 在 Canvas 打开生成的 Pocket ID 访问地址，完成初始化配置。

## 配置

部署完成后，可通过以下方式管理 Pocket ID：

- **AI Dialog**：用自然语言描述变更需求，让 AI 自动应用配置。
- **Resource Cards**：点击 StatefulSet、Service、Ingress 或存储卡片进行调整。

### 模板参数

| Parameter | Description | Default |
| --- | --- | --- |
| `app_host` | Pocket ID 公网地址使用的域名前缀 | `pocket-id-<random>` |
| `app_name` | 本次部署的 Kubernetes 资源名前缀 | `pocket-id-<random>` |
| `encryption_key` | Pocket ID 使用的应用加密密钥 | 随机 32 字符值 |

### 运维说明

- 首次部署后请保持 `encryption_key` 稳定，避免出现加解密或会话问题。
- 该模板默认采用单副本 StatefulSet，以保证有状态数据一致性。

## 扩缩容

在 Sealos 上扩展 Pocket ID 可按以下步骤操作：

1. 在 Canvas 打开 Pocket ID 部署。
2. 点击 StatefulSet 资源卡片。
3. 按需调整 CPU/内存 requests 与 limits。
4. 应用变更并观察发布状态。

若需扩展存储，可通过存储相关资源卡片调整 PVC 容量。多数场景建议维持 `1` 个副本，除非你已经验证适用于该身份服务的高可用方案。

## 故障排查

### 常见问题

**问题：OIDC 回调失败或重定向地址异常**
- 原因：`APP_URL` 与实际公网访问地址不一致。
- 解决：检查 `app_host` 与 Ingress Host 配置，然后重新部署或更新配置。

**问题：更新后用户数据无法解密或会话失效**
- 原因：初始化后 `encryption_key` 被修改。
- 解决：恢复原始密钥值并重启 Pod。

**问题：部署后短时间内无法访问服务 URL**
- 原因：DNS 与 Ingress 仍在传播或生效中。
- 解决：等待数分钟后从 Canvas 再次访问。

### 获取帮助

- [Pocket ID Documentation](https://docs.pocket-id.org)
- [Pocket ID GitHub Issues](https://github.com/pocket-id/pocket-id/issues)
- [Sealos Documentation](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Pocket ID Demo](https://demo.pocket-id.org)
- [Pocket ID Project Site](https://pocket-id.org)
- [OIDC Discovery Endpoint Basics](https://openid.net/specs/openid-connect-discovery-1_0.html)

## 许可证

该 Sealos 模板遵循 Sealos templates 仓库的许可证策略。Pocket ID 本身采用 [BSD 2-Clause License](https://github.com/pocket-id/pocket-id/blob/main/LICENSE)。
