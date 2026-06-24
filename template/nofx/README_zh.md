# 在 Sealos 上部署和托管 NOFX

NOFX 是开源 AI 交易终端，用于市场研究、策略生成、执行和监控。本模板在 Sealos Cloud 上部署 NOFX 后端、前端和 KubeBlocks PostgreSQL。

![应用截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/nofx/website-screenshot.webp)

## 关于托管 NOFX

NOFX 提供面向加密货币、美股、外汇和大宗商品的 AI 辅助交易工作台。Sealos 模板分别部署前端和后端工作负载，把 `/api` 流量路由到后端，并使用外接 PostgreSQL 保存应用状态。

上游 Docker Compose 默认使用本地存储，同时应用文档也提供 PostgreSQL 配置。本模板选择 KubeBlocks PostgreSQL，用于更适合生产的部署形态。

## 常见使用场景

- **AI 交易工作台**：研究市场、构建策略并监控交易员。
- **交易所配置**：保存交易所账号和交易设置。
- **策略测试**：管理 AI 模型、市场标的和策略逻辑。
- **竞赛看板**：查看交易员表现和公开竞赛数据。

## NOFX 托管依赖

Sealos 模板包含 NOFX 前端、NOFX 后端、KubeBlocks PostgreSQL、HTTPS Ingress、生成的 JWT/加密配置和健康检查。

### 部署依赖

- [VergeX 官方网站](https://vergex.trade) - 产品主页
- [NOFX GitHub 仓库](https://github.com/NoFxAiOS/nofx) - 源码与部署文档
- [NOFX API 文档](https://github.com/NoFxAiOS/nofx/tree/main/docs/api) - API 文档
- [NOFX Docker Compose](https://github.com/NoFxAiOS/nofx/blob/main/docker-compose.prod.yml) - 上游容器拓扑

### 实现细节

**架构组件：**

- **前端**：由 `ghcr.io/nofxaios/nofx/nofx-frontend` 提供静态 Web 界面
- **后端**：由 `ghcr.io/nofxaios/nofx/nofx-backend` 提供 Go API 服务
- **PostgreSQL**：KubeBlocks PostgreSQL `postgresql-16.4.0`
- **Ingress**：根路径路由到前端，`/api` 路由到后端

**配置：**

模板设置 `DB_TYPE=postgres`，注入 KubeBlocks 数据库凭据，生成 JWT secret，配置数据加密，并默认关闭匿名体验改进遥测。后端健康检查使用 `/api/health`，前端健康检查使用 `/health`。

**许可证：**

NOFX 使用 GNU Affero General Public License v3.0。

## 为什么在 Sealos 上部署 NOFX？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用从开发到生产部署和管理的完整生命周期。在 Sealos 上部署 NOFX 可以获得：

- **一键部署**：一次部署前端、后端、数据库、Ingress 和 SSL。
- **托管 PostgreSQL**：使用 KubeBlocks PostgreSQL 替代本地 SQLite 文件。
- **即时公网访问**：部署完成后打开生成的 HTTPS URL。
- **安全默认配置**：使用生成的 JWT 和数据加密配置。
- **简化运维**：在 Sealos Canvas 中调整资源和环境变量。

在 Sealos 上部署 NOFX，以托管基础设施运行交易终端。

## 部署指南

1. 打开 [NOFX 模板](https://sealos.io/products/app-store/nofx)，点击 **Deploy Now**。
2. 在弹窗中配置参数。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续修改可在对话框中描述需求让 AI 执行，或点击对应资源卡片调整配置。
4. 通过提供的 URL 访问 NOFX。
5. 在 Web 界面注册第一个用户。NOFX 会在首次注册时显示 Google Authenticator 二维码和 OTP secret。
6. 使用认证器应用扫描二维码，输入当前 6 位 OTP，完成注册。
7. 后续登录时，先输入邮箱和密码，再输入当前 Google Authenticator 动态验证码。

## 配置

NOFX 通过 Web 界面和后端认证 API 开放首次注册。第一个用户初始化完成后，系统会关闭额外公网注册，用于单用户部署模型。注册和后续登录都需要 Google Authenticator/TOTP 验证。

本模板将应用文件处理保留在 NOFX 工作负载内，并为 Sealos 模板选择 PostgreSQL 替代 SQLite。

## 扩缩容

调整 NOFX 资源：

1. 打开当前部署的 Canvas。
2. 点击前端、后端或 PostgreSQL 资源卡片。
3. 调整 CPU、内存、副本数或存储。
4. 在对话框中应用变更。

## 故障排查

**注册或登录失败**

- 原因：后端可能仍在等待 PostgreSQL 或 JWT/加密配置。
- 解决：等待后端 readiness probe 通过后重试注册。

**OTP 验证失败**

- 原因：认证器应用验证码可能已过期，或设备时间存在偏差。
- 解决：等待下一个 30 秒 OTP 窗口，确认设备时间，然后使用最新验证码重试。

**前端已加载但 API 请求失败**

- 原因：`/api` 路由或后端启动状态需要检查。
- 解决：查看后端工作负载日志，并确认 `/api/health` 已就绪。

## 更多资源

- [NOFX README](https://github.com/NoFxAiOS/nofx)
- [NOFX API Reference](https://github.com/NoFxAiOS/nofx/tree/main/docs/api)
- [NOFX Security Notes](https://github.com/NoFxAiOS/nofx/blob/main/SECURITY.md)

## 许可证

本 Sealos 模板遵循仓库许可证。NOFX 本身使用 AGPL-3.0。
