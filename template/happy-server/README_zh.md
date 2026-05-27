# 在 Sealos 上部署并托管 Happy Server

![Happy Server 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/happy-server/website-screenshot.webp)

## 关于 Happy Server

Happy Server 是面向 Claude Code 开源 Happy 客户端的自托管同步后端。客户端会在本地完成端到端加密，服务端只存储和转发加密后的数据，并负责认证、会话同步、HTTP API 与 WebSocket 实时连接。

此 Sealos 模板会部署一套完整的 Happy Server 后端，包括托管 PostgreSQL、Redis、S3 兼容对象存储、HTTPS Ingress 和应用启动入口。

## 使用场景

- 为需要基础设施控制权的团队自托管 Happy 同步 API。
- 将加密后的 Claude Code 客户端数据保存在自己的 Sealos 工作区。
- 通过 Redis 支撑 WebSocket 实时多设备同步。
- 使用 S3 兼容对象存储保存加密附件或产物。
- 无需手动维护 Kubernetes 清单，即可部署可复现的后端栈。

## 依赖组件

模板会创建以下资源：

- **Happy Server**：固定到 GHCR 镜像 digest 的 Node.js/Fastify 应用容器。
- **PostgreSQL 16.4**：持久化关系数据库，用于账号、会话、动态流、密钥和元数据。
- **Redis 7.2**：用于实时协同的缓存和发布订阅后端。
- **ObjectStorageBucket**：publicRead 的 S3 兼容对象存储桶，用于文件和产物 URL。
- **Ingress + Service + App**：公网 HTTPS 入口与 Sealos 应用启动项。

## 实现细节

- 运行镜像：`ghcr.io/yangchuansheng/happy-server`，按 digest 固定版本。
- 应用端口：`3005`。
- 健康检查：`/health`，会校验数据库连接。
- 数据库初始化：幂等 PostgreSQL init Job 会创建 `happy-server` 数据库和所需表结构，然后应用才进入可用状态。
- 密钥管理：数据库、Redis 和对象存储凭据均来自 Sealos 托管 Secret。
- 资源基线：部署测试后应用容器使用 `200m` CPU 和 `256Mi` 内存；`128Mi` 在启动阶段会触发 OOMKilled，因此不作为最小可用配置。

## 为什么在 Sealos 上部署

Sealos 为 Happy Server 提供了适合自托管后端的托管能力：

- 可从应用商店一键部署。
- 托管 PostgreSQL、Redis、对象存储、HTTPS Ingress 和持久化存储。
- 通过 Sealos 控制台管理域名、TLS、日志和资源配额。
- 使用 Kubernetes 原生清单，便于审计和迁移。

## 部署指南

### 步骤 1：打开模板

打开 [Sealos 应用商店中的 Happy Server 模板](https://sealos.io/products/app-store/happy-server)，然后点击 **Deploy Now**。

### 步骤 2：检查生成值

模板会生成：

- `app_name`：Kubernetes 资源名称前缀。
- `app_host`：公网访问域名前缀。
- `seed`：Happy Server 使用的随机服务端密钥。

默认生成值适合全新部署。只有在需要固定资源名或域名前缀时，才需要修改 `app_name` 或 `app_host`。

### 步骤 3：部署

点击 **Deploy**。Sealos 会创建对象存储桶、PostgreSQL 集群、Redis 集群、数据库初始化 Job、应用 Deployment、Service、Ingress 和 App 启动项。

### 步骤 4：验证服务

部署完成后，打开 Sealos 生成的应用 URL。也可以访问健康检查接口：

```bash
curl https://<你的-happy-server-域名>/health
```

健康响应示例：

```json
{"status":"ok","service":"happy-server"}
```

## 配置说明

| 配置项 | 来源 | 用途 |
| --- | --- | --- |
| `DATABASE_URL` | Sealos PostgreSQL Secret | 连接 `happy-server` 数据库。 |
| `REDIS_URL` | Sealos Redis Secret 和服务 DNS | 支撑 Redis 实时协同能力。 |
| `S3_ACCESS_KEY`、`S3_SECRET_KEY`、`S3_BUCKET`、`S3_HOST` | Sealos Object Storage Secret | 启用文件和产物存储。 |
| `PUBLIC_URL` | Sealos 生成的 HTTPS 域名 | 服务公网基础 URL。 |
| `HANDY_MASTER_SECRET` | 模板生成的 `seed` | 服务端密钥材料。 |

## 扩缩容

默认模板运行 1 个 Happy Server 副本。只有在确认 Redis 实时同步链路和客户端流量模式后，才建议增加副本数。PostgreSQL 和 Redis 使用持久化存储，并由 Sealos 提供托管服务端点。

## 故障排查

- **健康检查返回 503**：PostgreSQL 尚未就绪，或初始化 Job 尚未完成。等待 PostgreSQL 集群和 `*-pg-init` Job 完成。
- **应用启动后反复重启**：检查 Redis 服务 DNS 是否可解析，以及对象存储 Secret 是否已创建。Redis 服务名应为 `*-redis-redis-redis`。
- **启动阶段 OOMKilled**：保持应用内存限制不低于 `256Mi`。当前 Node.js 镜像在 `128Mi` 下无法稳定启动。
- **文件 URL 无法访问**：确认 ObjectStorageBucket 已创建且策略为 `publicRead`，因为 Happy Server 会返回公开对象 URL。
- **镜像拉取告警**：模板使用公开且按 digest 固定的镜像。如果工作区要求 registry 凭据，请通过 Sealos 创建生成的镜像拉取 Secret。

## 相关资源

- Happy 项目：[https://github.com/slopus/happy](https://github.com/slopus/happy)
- Happy Server 包：[https://github.com/slopus/happy/tree/main/packages/happy-server](https://github.com/slopus/happy/tree/main/packages/happy-server)
- Sealos：[https://sealos.io](https://sealos.io)
- 模板源码：[https://github.com/labring-actions/templates/tree/kb-0.9/template/happy-server](https://github.com/labring-actions/templates/tree/kb-0.9/template/happy-server)

## 许可证

Happy Server 使用 MIT License 发布。此 Sealos 模板遵循模板仓库的许可证。
