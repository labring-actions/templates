# 在 Sealos 上部署和托管 Sub2API

Sub2API 是一个面向上游 AI 服务订阅额度分发与管理的 API 网关平台。这个模板会在 Sealos Cloud 上一并部署 Sub2API、PostgreSQL、Redis、持久化存储和公网 HTTPS 入口。

## 关于在 Sealos 上托管 Sub2API

Sub2API 可以作为一套自托管控制平面，统一承接 AI 流量转发、API 密钥发放、额度管控、计费编排和上游账号管理。借助 Sealos 模板，你不需要手动拼装数据库、Redis、存储卷或 Ingress，部署完成后就能得到一套开箱即用的运行环境。

这个部署方案以 PostgreSQL 保存核心业务数据，用 Redis 承担高速状态与协调能力，并为 `/app/data` 挂载独立持久卷。Sealos 还会自动准备 HTTPS 访问地址、JWT 与 TOTP 所需的运行时密钥，并在控制台展示应用入口，等 Pod 全部健康后即可开始首轮初始化。

## 常见使用场景

- **统一 AI 网关入口**：把内部工具或客户应用的请求汇总到一个网关地址，避免直接暴露多家上游服务凭据。
- **额度与成本治理**：按团队或业务线分配订阅额度，追踪消耗情况，控制共享上游资源的使用节奏。
- **多账号统一运营**：接入多个上游 AI 账号，在同一管理面板中处理分流、切换、密钥发放和容量调度。
- **团队安全协作**：为运营或内部用户提供可控的 Web 管理界面，用于账号管理、计费策略和访问控制。
- **特定厂商集成**：按需配置 Gemini OAuth 等授权参数，适配带有特殊鉴权流程的上游服务。

## Sub2API 托管依赖

这个 Sealos 模板已经包含运行所需的核心组件：Sub2API `0.1.104`、PostgreSQL `16.4.0`、Redis `7.2.7`、持久化存储、HTTPS Ingress，以及会显示在 Sealos Canvas 中的应用入口。

### 部署依赖与参考资料

- [Sub2API GitHub 仓库](https://github.com/Wei-Shaw/sub2api) - 上游源码与项目说明
- [Sub2API 在线演示](https://demo.sub2api.org/) - 官方演示环境
- [Sub2API Issues](https://github.com/Wei-Shaw/sub2api/issues) - 问题反馈与功能讨论
- [PostgreSQL 文档](https://www.postgresql.org/docs/) - PostgreSQL 官方参考
- [Redis 文档](https://redis.io/docs/latest/) - Redis 官方参考
- [Sealos 文档](https://sealos.run/docs) - 平台使用文档
- [Sealos Discord](https://discord.gg/wdUn538zVP) - 社区支持

## 实现细节

### 架构组件

这个模板会部署以下服务：

- **Sub2API 应用**：以 `StatefulSet` 方式运行 `weishaw/sub2api:0.1.104`，对外提供 `8080` 端口，并将运行时文件写入 `/app/data`。
- **PostgreSQL**：基于 KubeBlocks 的 PostgreSQL `16.4.0` 集群，附带 `1Gi` 持久卷，用来保存业务数据。
- **PostgreSQL 初始化 Job**：在数据库就绪后自动执行，若 `sub2api` 数据库不存在则创建，重复执行也不会破坏已有数据。
- **Redis**：基于 KubeBlocks 的 Redis `7.2.7` 部署，使用 replication 拓扑，并带有 Sentinel 组件，用于集群内部协调与高可用支持。
- **Ingress 与 App 资源**：Sealos 会自动创建公网 HTTPS 入口，并通过 `App` 资源把访问地址展示在 Canvas 中。

### 配置项

模板把最常用的运行参数暴露成了 Sealos 表单输入：

- `admin_email`：初始管理员邮箱
- `admin_password`：初始管理员密码；留空时会在首次启动时自动生成一次性密码
- `timezone`：应用时区，默认值为 `Asia/Shanghai`
- `run_mode`：可选 `standard` 或 `simple`
- `gemini_oauth_client_id`、`gemini_oauth_client_secret`、`gemini_oauth_scopes`、`gemini_quota_policy`
- `gemini_cli_oauth_client_secret`、`antigravity_oauth_client_secret`
- `security_url_allowlist_enabled`、`security_url_allowlist_allow_insecure_http`、`security_url_allowlist_allow_private_hosts`、`security_url_allowlist_upstream_hosts`
- `update_proxy_url`：更新检查或访问 GitHub 时使用的可选代理地址

下面这些安全密钥会由模板自动生成：

- `JWT_SECRET`
- `TOTP_ENCRYPTION_KEY`

### 运行特性

- 健康检查走 `GET /health`，服务端口为 `8080`。
- 应用默认启用 `AUTO_SETUP=true`，方便首次启动时自动完成初始化。
- 数据库连接信息来自 KubeBlocks 生成的 PostgreSQL 连接 Secret。
- Redis 凭据来自 KubeBlocks 生成的 Redis Secret。
- 公网访问地址形如 `https://<app-host>.<your-sealos-domain>`。

### 许可证说明

Sub2API 的许可证以其上游项目为准。若要用于生产环境或二次分发，建议先在上游仓库中核对当前许可证条款。

## 为什么要在 Sealos 上部署 Sub2API？

Sealos 是一个构建在 Kubernetes 之上的 AI 助手式云操作系统，能够把应用部署与运维这套流程大幅简化。把 Sub2API 部署到 Sealos 上，你可以获得：

- **一键部署**：网关、PostgreSQL、Redis、存储和 Ingress 一次拉起，无需自己写 Kubernetes 清单。
- **基础设施内建**：数据库、密钥、存储、网络和 SSL 都由模板统一编排。
- **部署后易于调整**：后续变更可以通过 AI 对话框或 Canvas 里的资源卡片完成，不必手改 YAML。
- **持久化存储现成可用**：应用数据、PostgreSQL 数据和 Redis 数据在重启或常规维护后都能保留下来。
- **公网 HTTPS 开箱即用**：每次部署都会自动拿到带 TLS 的公开访问地址。
- **按量计费更灵活**：可以先小规模启动，等流量上来后再逐步扩容。
- **享受 Kubernetes 的可靠性**：既保留 Kubernetes 的调度与生命周期管理优势，又不用自己维护底层平台。

把 Sub2API 交给 Sealos 托管后，你可以把精力放在 API 治理和服务接入上，而不是基础设施拼装上。

## 部署指南

1. 打开 [Sub2API 模板页面](https://sealos.io/products/app-store/sub2api)，点击 **Deploy Now**。
2. 在弹出的配置窗口中填写参数。
   - 设置 `admin_email` 作为首个管理员账号邮箱。
   - 可以手动填写 `admin_password`，也可以留空，让 Sub2API 在首次启动时自动生成一次性密码。
   - 按需选择 `timezone` 和 `run_mode`。
   - 只有在你的部署确实需要时，才填写 Gemini OAuth 和 allowlist 相关参数。
   - 如果访问 GitHub 或更新接口必须经过代理，请设置 `update_proxy_url`。
3. 等待部署完成，通常需要 2-3 分钟。部署结束后会自动跳转到 Canvas。后续如需调整配置，可以直接在 AI 对话框中描述需求，或点击对应资源卡片进行修改。
4. 通过提供的地址访问应用。
   - **管理界面**：打开 `https://<app-host>.<your-sealos-domain>`，使用已配置的管理员账号登录。
   - **网关入口**：同一个公网基础地址也可以作为 API 访问入口，具体路径以你的 Sub2API 路由配置为准。

如果 `admin_password` 为空，请在首次启动后查看应用日志，取回自动生成的管理员密码。

## 配置说明

部署完成后，你可以通过以下方式管理 Sub2API：

- **AI 对话框**：直接描述你想变更的内容，例如调整环境变量、资源规格或其他部署参数。
- **资源卡片**：在 Canvas 中打开 Sub2API、PostgreSQL、Redis、Job 或 Ingress 卡片，查看状态或修改配置。
- **应用后台**：登录 Sub2API Web 控制台后，可以继续管理上游账号、额度策略、计费逻辑、路由规则和 API 密钥分发。

## 扩缩容

这个模板默认只部署 1 个 Sub2API 应用副本。大多数场景下，建议先从 CPU、内存和存储容量调整开始：

1. 在 Canvas 中打开你的部署。
2. 点击需要调整的 `StatefulSet`、PostgreSQL 或 Redis 资源卡片。
3. 根据实际负载提升 CPU、内存或存储容量。
4. 在对话框中应用修改，并观察更新后的健康状态。

如果你准备把应用副本数扩到 1 以上，建议先结合自身环境验证 Sub2API 的会话、存储和协同行为，再决定是否横向扩展。

## 故障排查

### 常见问题

**问题 1：部署完成后登录页打不开**
- 原因：某个依赖组件可能还没有完全就绪。
- 解决办法：先确认 PostgreSQL 初始化 Job 是否执行成功，再检查 Sub2API `StatefulSet`、PostgreSQL 集群和 Redis 集群在 Canvas 中是否都处于健康状态。

**问题 2：我把 `admin_password` 留空了，现在无法登录**
- 原因：系统在首次启动时自动生成了管理员密码。
- 解决办法：打开 Sub2API 容器日志，搜索初始化阶段输出的管理员密码。

**问题 3：上游 API 请求被拦截**
- 原因：URL allowlist 限制与你当前环境不匹配。
- 解决办法：检查 `security_url_allowlist_enabled`、`security_url_allowlist_allow_insecure_http`、`security_url_allowlist_allow_private_hosts` 和 `security_url_allowlist_upstream_hosts`。

**问题 4：在线更新检查无法访问 GitHub**
- 原因：当前运行环境需要出站代理。
- 解决办法：设置 `update_proxy_url`，然后重新部署，或更新现有应用的环境变量配置。

**问题 5：应用启动后一直不健康**
- 原因：PostgreSQL、Redis 可能尚未就绪，或者初始化流程还没有跑完。
- 解决办法：等待依赖 Pod 和 PostgreSQL 初始化 Job 完成，再回到 Canvas 查看应用状态，确认 `/health` 检查是否恢复正常。

### 获取帮助

- [Sub2API GitHub 仓库](https://github.com/Wei-Shaw/sub2api)
- [Sub2API Issues](https://github.com/Wei-Shaw/sub2api/issues)
- [Sealos 文档](https://sealos.run/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

这个 Sealos 模板由当前 templates 仓库提供。Sub2API 本身的许可证以后续上游项目说明为准，使用前请在上游仓库中确认最新条款。
