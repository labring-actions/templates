# 在 Sealos 上部署托管 New API

New API 是新一代大语言模型网关与 AI 资产管理系统，对外提供统一的 OpenAI 兼容接口。借助本模板，您可以在 Sealos 云平台上一键部署 New API，并自动配置由 KubeBlocks 托管的 PostgreSQL 和 Redis。

![New API Logo](./logo.png)

## 关于托管 New API

New API 充当应用程序与上游 AI 供应商之间的中间层，为您提供统一的 API 端点，涵盖模型路由、额度管控、渠道编排和运营监控等核心能力。团队可以通过一个 Web 控制台集中管理用户、令牌和渠道，轻松规范化多供应商接入。

本 Sealos 模板会自动配置应用运行环境、PostgreSQL、Redis、持久化存储、HTTPS 入口以及数据库初始化任务。部署完成后即可投入使用——应用数据和日志在容器重启后依然完好保存，服务通过 Sealos 托管的公网 URL 对外暴露。

## 常见应用场景

- **统一 AI 网关**：将多家模型供应商的请求统一路由到一个稳定的 OpenAI 兼容端点
- **团队额度管理**：通过中心化管理后台统一管控用户、渠道、额度和访问规则
- **供应商容灾与流量调度**：在不修改客户端集成的前提下，灵活切换和调度跨供应商流量
- **企业内部 AI 平台**：为工程、产品和运营团队提供集群内的共享 AI 网关
- **自托管模型运维**：将网关状态、凭据和路由策略完全掌控在自有基础设施中

## 托管 New API 的依赖项

Sealos 模板已包含运行 New API 所需的全部依赖：

- New API 应用容器
- KubeBlocks 托管的 PostgreSQL 16.4
- KubeBlocks 托管的 Redis 7.2.7
- 用于创建 `new-api` 数据库的 PostgreSQL 初始化任务
- Kubernetes `StatefulSet`、`Service` 和 `Ingress`
- `/data` 和 `/app/logs` 的持久化存储

### 部署依赖

- [New API 官方文档](https://docs.newapi.pro/) - 产品概述与使用指南
- [环境变量参考](https://docs.newapi.pro/en/docs/installation/config-maintenance/environment-variables) - 运行时配置参考
- [API 文档](https://docs.newapi.pro/en/docs/api) - OpenAI 兼容接口与供应商专属接口文档
- [New API GitHub 仓库](https://github.com/QuantumNous/new-api) - 源代码与问题追踪
- [社区交流](https://docs.newapi.pro/en/docs/support/community-interaction) - 社区与技术支持渠道

### 实现细节

**架构组件：**

本模板部署以下服务：

- **New API StatefulSet**（`calciumion/new-api:v0.11.4`）：在 `3000` 端口提供 Web 管理界面和 OpenAI 兼容 API
- **PostgreSQL 集群**：存储用户、渠道、额度及应用配置数据
- **Redis 集群**：提供缓存和基于 Redis 的运行时状态存储
- **PostgreSQL 初始化任务**：等待数据库就绪后幂等创建 `new-api` 数据库
- **Service、Ingress 和 App 资源**：通过 Sealos 托管的 HTTPS 发布应用

**配置方式：**

- `SQL_DSN` 由 KubeBlocks Secret `${{ defaults.app_name }}-pg-conn-credential` 自动组装
- `REDIS_CONN_STRING` 由 `${{ defaults.app_name }}-redis-redis-account-default` 和 Redis 内部服务 DNS 自动构建
- `SESSION_SECRET` 和 `CRYPTO_SECRET` 默认自动生成，确保部署即拥有稳定的运行时密钥
- 健康检查指向 `/api/status`，持久卷分别挂载在 `/data` 和 `/app/logs`
- 当前模板为每个应用 PVC 分配 `103Mi` 存储空间

**许可证信息：**

New API 采用 [GNU Affero 通用公共许可证 v3.0](https://github.com/QuantumNous/new-api/blob/main/LICENSE) 开源。上游项目同时提供商业授权方案，有需要的组织可直接联系维护者。

## 为什么选择在 Sealos 上部署 New API？

Sealos 是一个基于 Kubernetes 构建的 AI 赋能云操作系统，让您无需自行维护配置文件和运维管线，即可享受 Kubernetes 级别的部署能力。对于 New API 而言，网关、数据库、缓存、存储和公网 HTTPS 入口全部封装在一个模板中，开箱即用。

在 Sealos 上部署 New API，您将获得：

- **一键部署**：从模板直接启动全套技术栈，无需手动拼装 PostgreSQL、Redis、Ingress 和存储
- **托管 Kubernetes 基础**：运行在标准 Kubernetes 资源之上，自带服务发现、稳定存储和可控发布
- **灵活定制**：后续可通过 Canvas、AI 对话框和资源卡随时调整资源和配置
- **内置持久化存储**：应用数据和日志在 Pod 重启和升级过程中始终安全持久
- **即时公网 HTTPS**：通过 Sealos 托管的 Ingress 自动启用 TLS，UI 和 API 即刻对外可达
- **按需付费**：从小规模起步，仅在流量或数据量增长时扩展资源

## 部署指南

1. 打开 [New API 模板页面](https://sealos.io/products/app-store/new-api)，点击 **Deploy Now**。
2. 在弹窗中配置以下参数：
   - `app_host`
   - `app_name`
   - `session_secret`
   - `crypto_secret`
3. 等待部署完成（通常 2-3 分钟）。部署成功后会自动跳转到 Canvas。后续修改可在 AI 对话框描述需求，或点击对应资源卡调整配置。
4. 通过 `https://<app_host>.<SEALOS_CLOUD_DOMAIN>` 访问 New API，在 Web 界面完成初始设置。

## 配置说明

部署完成后，您可以通过以下方式配置 New API：

- **Web 管理界面**：在控制面板中添加供应商、渠道、额度、分组和运行时设置
- **AI 对话框**：向 Sealos AI 助手描述资源调整或配置变更需求
- **资源卡**：打开应用、PostgreSQL、Redis、Ingress 或存储资源卡进行精确调整

### 模板参数

| 参数 | 说明 | 默认值 |
| --- | --- | --- |
| `app_host` | New API Ingress 的公网主机名前缀 | `new-api-<random>` |
| `app_name` | Kubernetes 资源名称前缀 | `new-api-<random>` |
| `session_secret` | New API 使用的会话密钥 | 随机 32 位字符串 |
| `crypto_secret` | 用于 Redis 加密状态的加密密钥 | 随机 32 位字符串 |

### 运维注意事项

- 复用同一部署状态时，请保持 `session_secret` 不变
- 已有 Redis 加密数据的环境中，请保持 `crypto_secret` 不变
- 初始化任务仅在 `new-api` 数据库不存在时才会创建
- 模板默认为单副本部署，扩展副本数前请先验证会话管理和运行时行为

## 扩展指南

在 Sealos 上扩展 New API：

1. 在 Canvas 中打开对应部署
2. 点击 New API `StatefulSet` 资源卡
3. 按需调整 CPU 和内存的请求值或限制值
4. 应用更改并观察发布进度

对于有状态组件（PostgreSQL 和 Redis），可根据业务需要在各自的资源卡中单独扩展。除非已验证多副本策略，否则建议将应用副本数保持为 `1`。

## 故障排除

### 常见问题

**问题：重新部署后登录或初始设置异常**
- 原因：`SESSION_SECRET` 在首次部署后发生了变更
- 解决方案：恢复原始密钥值并重启应用 Pod

**问题：Redis 加密数据无法解密**
- 原因：在已有加密数据的情况下变更了 `CRYPTO_SECRET`
- 解决方案：在重启工作负载前恢复原始 `crypto_secret` 值

**问题：应用启动成功但数据库初始化失败**
- 原因：应用首次启动时 PostgreSQL 尚未就绪，或初始化任务未成功完成
- 解决方案：在 Canvas 中检查 `${{ defaults.app_name }}-pg-init` 任务状态和 PostgreSQL 集群健康状态，必要时重新触发应用发布

### 获取帮助

- [New API 官方文档](https://docs.newapi.pro/)
- [New API GitHub Issues](https://github.com/QuantumNous/new-api/issues)
- [常见问题](https://docs.newapi.pro/en/docs/support/faq)
- [Sealos 文档](https://sealos.io/docs)
- [Sealos Discord 社区](https://discord.gg/wdUn538zVP)

## 额外资源

- [New API 项目概述](https://docs.newapi.pro/en/docs/introduction)
- [安装文档](https://docs.newapi.pro/en/docs/installation)
- [API 文档](https://docs.newapi.pro/en/docs/api)
- [环境变量参考](https://docs.newapi.pro/en/docs/installation/config-maintenance/environment-variables)

## 许可证

本 Sealos 模板遵循 Sealos 模板仓库的许可政策。New API 本身采用 [GNU Affero 通用公共许可证 v3.0](https://github.com/QuantumNous/new-api/blob/main/LICENSE) 开源。
