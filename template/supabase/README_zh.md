# 在 Sealos 上部署与托管 Supabase

Supabase 是一个开源后端平台，把 PostgreSQL、身份认证、实时订阅、对象存储和边缘函数整合在一起。该模板会在 Sealos Cloud 上部署一套可用于生产的 Supabase 全栈，并内置托管 PostgreSQL 与 API 网关路由。

![Supabase Studio](website-screenshot.webp)

## 关于在 Sealos 托管 Supabase

在这个模板里，Supabase 采用以 Kong 为入口的多服务架构。Studio 提供 Web 控制台，Auth、REST、Realtime、Storage 与 Edge Functions 通过同一个公网域名按路径统一暴露。Imgproxy 作为 sidecar 与 Storage 运行在同一个 Pod 中，本地图片转换可直接读取两者共享的持久卷。

部署时会通过 Kubeblocks 自动创建 PostgreSQL 集群，用初始化 Job 预置 Supabase 所需的 schema 与角色，再通过受控冷重启启用 logical WAL，并通过 Kubernetes Secret 完成凭据注入。Storage 服务提供两条官方后端路径：默认将文件保存到持久化卷，也可以通过 `enable_s3_storage=true` 切换到私有 Sealos `ObjectStorageBucket`。

Sealos 还会自动处理 Ingress、TLS、公网域名和 Canvas 中的生命周期运维，让你把精力集中在业务开发，而不是集群底层细节。

## 常见使用场景

- **SaaS 后端**：用一套栈快速搭建带 PostgreSQL、认证和 API 的完整后端。
- **移动应用后端**：为 iOS 和 Android 应用提供认证、数据 API 与文件存储能力。
- **实时数据看板**：通过实时频道把数据库变更推送到前端客户端。
- **内部工具平台**：基于 SQL 和角色权限快速交付管理后台与内部系统。
- **边缘 API 逻辑**：借助 Supabase Edge Functions 在靠近数据侧运行自定义 TypeScript 函数。

## Supabase 托管依赖

该 Sealos 模板来自当前 Supabase 自托管 Compose release，包含 Studio `2026.07.07-sha-a6a04f2`、Kong `3.9.1`、GoTrue `v2.189.0`、PostgREST `v14.12`、Realtime `v2.102.3`、Storage API `v1.60.4`、Imgproxy `v3.30.1`、Postgres Meta `v0.96.6`、Edge Runtime `v1.74.0`、Logflare `1.43.1`、Vector `0.53.0-alpine`、Supavisor `2.9.5`，以及托管的 PostgreSQL 16.4 集群。

### 部署依赖文档

- [Supabase Documentation](https://supabase.com/docs) - 官方文档与产品指南
- [Supabase Self-Hosting Guide](https://supabase.com/docs/guides/self-hosting) - 自托管架构与部署说明
- [Supabase GitHub Repository](https://github.com/supabase/supabase) - 源码仓库与版本信息
- [Supabase Auth Docs](https://supabase.com/docs/guides/auth) - 身份认证与提供商配置
- [Supabase Storage Docs](https://supabase.com/docs/guides/storage) - Bucket 与对象存储使用说明
- [Supabase S3 Storage Guide](https://supabase.com/docs/guides/self-hosting/self-hosted-s3) - 本地与 S3 后端配置
- [Supabase Edge Functions Docs](https://supabase.com/docs/guides/functions) - Serverless 函数开发文档

### 实现细节

**架构组件：**

该模板会部署以下服务：

- **Supabase Studio**：项目管理与 SQL 操作的 Web 控制台（端口 `3000`）。
- **Kong Gateway**：Supabase 全部 API 的统一入口与路由层（端口 `8000` 和 `8443`）。
- **Auth（GoTrue）**：身份认证与用户管理接口（`/auth/v1/*`）。
- **REST（PostgREST）**：基于 PostgreSQL 的 REST 与 GraphQL 接口（`/rest/v1/*`、`/graphql/v1`）。
- **Realtime**：WebSocket 与实时订阅接口（`/realtime/v1/*`）。
- **Storage API**：对象与文件操作接口（`/storage/v1/*`），可使用本地持久化存储或条件式 Sealos S3 后端。
- **Imgproxy**：Storage Pod 内的图片转换 sidecar，与 Storage API 共享本地持久卷并监听 `5001` 端口。
- **Postgres Meta**：Studio 使用的元数据与管理接口（通过网关暴露 `/pg/*`）。
- **Edge Functions Runtime**：基于 Deno 的函数运行时，暴露路径为 `/functions/v1/*`。
- **Analytics（Logflare）+ Vector**：供 Studio 与平台日志使用的内部遥测链路。
- **Supavisor**：PostgreSQL 连接池服务（端口 `5432` 和 `6543`）。
- **PostgreSQL（Kubeblocks）**：持久化数据库集群，并配套初始化与重启 Job 预置 Supabase 角色、schema 和 logical WAL。

**配置项：**

- 必填输入参数：
  - `jwt_secret`：供 Auth、REST、Studio、Storage 共同使用的 JWT 签名密钥。
  - `anon_key`：由 `jwt_secret` 签发的匿名 API 密钥。
  - `service_role_key`：由 `jwt_secret` 签发的服务角色 API 密钥。
  - `dashboard_username`：Studio HTTP Basic Auth 用户名，默认值为 `supabase`。
  - `dashboard_password`：为 Studio HTTP Basic Auth 设置的密码。
- 可选存储参数：
  - `enable_s3_storage=false` 时，文件写入 Storage API 与 Imgproxy 共享的单个 1 GiB 持久化卷。
  - `enable_s3_storage=true` 时，创建私有 Sealos `ObjectStorageBucket` 并注入 S3 凭据，渲染拓扑会移除 Storage PVC。
- 默认公网访问地址为 `https://<app-name>-kong.<your-sealos-domain>`。
- Studio 控制台流量通过 Kong 的 HTTP Basic Auth 保护。登录时使用部署阶段填写的 `dashboard_username` 与 `dashboard_password`。
- 默认启用邮箱注册与自动确认，调用 `/auth/v1/signup` 后可直接获得可用 session。生产环境需要邮箱验证时，请先配置 SMTP，再设置 `GOTRUE_MAILER_AUTOCONFIRM=false`。
- SMTP、注册策略、JWT 过期时间、存储后端参数与连接池限制都可在 Canvas 里通过环境变量调整。
- PostgreSQL 数据、Storage/Imgproxy 共享文件、Studio snippets/functions、Edge Runtime 缓存都配置了持久化卷。

部署前请生成一组唯一且相互匹配的旧版 JWT 密钥。Supabase 官方 Docker 辅助脚本会把所需值写入 `docker/.env`：

```bash
git clone --depth 1 https://github.com/supabase/supabase.git
cd supabase/docker
cp .env.example .env
sh ./utils/generate-keys.sh
```

将 `.env` 中的 `JWT_SECRET`、`ANON_KEY`、`SERVICE_ROLE_KEY` 分别填入 `jwt_secret`、`anon_key`、`service_role_key`。`service_role_key` 可以绕过行级安全策略，仅应存放在可信的服务端环境中。

**许可证信息：**

Supabase 为开源项目，各组件可能采用不同许可证（Supabase 多数仓库使用 Apache-2.0）。请以各上游仓库中的许可证文件为准。

## 为什么在 Sealos 部署 Supabase？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，把开发、部署与运维整合到统一体验中。将 Supabase 部署到 Sealos，你可以获得：

- **一键部署**：无需手动拼装多服务，即可启动完整 Supabase 栈。
- **Kubernetes 级稳定性**：默认具备健康检查、服务发现和编排能力。
- **按需付费与资源效率**：可从小规格起步，按流量增长逐步扩展。
- **内置 HTTPS 访问**：自动分配公网域名并配置 SSL 证书。
- **持久化存储开箱即用**：数据库与对象数据在重启后仍可保留。
- **灵活配置**：可通过 Canvas 对话框调整环境变量、资源和副本数。
- **AI 辅助运维**：通过 AI 对话描述变更，快速完成日常运维操作。

把基础设施复杂度交给 Sealos，把时间用在交付功能上。

## 部署指南

1. 打开 [Supabase 模板](https://sealos.io/products/app-store/supabase)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - 使用上方官方脚本生成唯一密钥组。
   - 将相互匹配的 `JWT_SECRET`、`ANON_KEY`、`SERVICE_ROLE_KEY` 分别填入 `jwt_secret`、`anon_key`、`service_role_key`。
   - 为 Studio 设置易于记忆的 `dashboard_username` 与强 `dashboard_password`。
   - 其他参数无特殊需求时可保持默认值。
3. 等待部署完成（通常 2-3 分钟）。完成后会自动跳转到 Canvas。后续若需变更，可在 AI 对话中描述需求，或直接编辑资源卡片。
4. 通过系统生成的公网地址访问应用：
   - **Studio 控制台**：`https://<app-name>-kong.<your-sealos-domain>/`
   - **REST API**：`https://<app-name>-kong.<your-sealos-domain>/rest/v1/`
   - **Auth API**：`https://<app-name>-kong.<your-sealos-domain>/auth/v1/`
   - **Realtime API**：`https://<app-name>-kong.<your-sealos-domain>/realtime/v1/`
   - **Storage API**：`https://<app-name>-kong.<your-sealos-domain>/storage/v1/`
   - **Edge Functions API**：`https://<app-name>-kong.<your-sealos-domain>/functions/v1/`

### Studio 登录与首次操作

1. 打开 Studio 地址，在浏览器 Basic Auth 弹窗中输入部署时设置的 `dashboard_username` 与 `dashboard_password`。
2. 在 **Table Editor** 中创建 `notes` 表，添加文本列并插入一行数据，确认 Studio、PostgREST 和 PostgreSQL 迁移已经就绪。
3. 在 **SQL Editor** 运行 `select * from notes;`，确认查询返回刚插入的数据。
4. 在 **Storage** 中创建私有 bucket，上传小文件并下载，再核对文件内容。匿名访问测试保持 bucket 为私有状态。

启用 `enable_s3_storage=true` 后，上传与下载会经过私有 Sealos 对象存储桶。原始 bucket 地址的匿名请求保持受限，文件交付使用 Storage API 或限时签名 URL。

## 配置说明

部署完成后，你可以通过以下方式配置 Supabase：

- **AI 对话**：描述变更需求，例如调整认证策略或资源规格。
- **资源卡片**：修改各服务的环境变量、CPU/内存和副本数。
- **Studio 界面**：管理数据表、SQL、认证用户与存储 Bucket。

建议部署后优先检查：

- 如需生产邮件能力，先替换模板中的 SMTP 占位参数。
- 生产 SMTP 配置并验证完成后，再关闭邮箱自动确认。
- 根据认证策略确认 `GOTRUE_DISABLE_SIGNUP`、手机/邮箱注册开关和重定向白名单。
- 确认客户端使用 `anon_key`，服务端受信任流程使用 `service_role_key`。
- 根据边缘函数安全策略，校验 `functions_verify_jwt` 配置是否符合预期。

## 扩缩容

如需扩缩容 Supabase，可按以下步骤操作：

1. 在 Canvas 中打开当前部署。
2. 选择要扩容的服务（例如 `rest`、`realtime`、`auth`、`storage`）。
3. 先提升 CPU/内存，再对适合无状态扩展的服务增加副本数。
4. 应用变更后，持续观察 Pod 状态与接口延迟指标。

## 故障排查

### 常见问题

**问题：调用 API 时返回 401/403**
- 原因：API 密钥使用错误，或缺少 `apikey`/`Authorization` 请求头。
- 解决：客户端使用 `anon_key`，`service_role_key` 仅用于受信任的服务端路径。

**问题：无法登录或收不到验证邮件**
- 原因：SMTP 仍是占位配置，或注册策略限制过严。
- 解决：在 `auth` 部署中配置真实 SMTP 参数，并检查认证相关环境变量。

**问题：Edge Functions 返回鉴权错误**
- 原因：JWT 校验配置与请求令牌不匹配。
- 解决：检查 `functions_verify_jwt`，若已启用校验则传入合法 Bearer Token。

**问题：文件上传成功但图片转换失败**
- 原因：Storage Pod 中的 Imgproxy sidecar 不可用，或存储/图片相关环境变量被错误修改。
- 解决：检查 `storage` Pod 内的 Imgproxy 容器，并确认 `IMGPROXY_URL` 指向 `http://127.0.0.1:5001`。

**问题：部署初期 Supabase 服务启动报错**
- 原因：PostgreSQL 初始化 Job 或依赖服务尚未完全就绪。
- 解决：等待 PostgreSQL 集群与初始化 Job 完成，再复查相关 Pod 日志。

### 获取帮助

- [Supabase Docs](https://supabase.com/docs)
- [Supabase GitHub Issues](https://github.com/supabase/supabase/issues)
- [Supabase Discord](https://discord.supabase.com)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Supabase API Reference](https://supabase.com/docs/reference)
- [PostgREST Documentation](https://postgrest.org/en/stable/)
- [Kong Gateway Documentation](https://docs.konghq.com/gateway/latest/)
- [Sealos App Store](https://sealos.io/products/app-store)

## 许可证

本 Sealos 模板遵循仓库许可证条款。Supabase 及相关运行时组件遵循各自上游项目的开源许可证。
