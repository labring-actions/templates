# 在 Sealos 上部署和托管 Meilisearch

Meilisearch 是一个快速、开源的搜索引擎 API，可用于构建容错搜索体验。此模板会在 Sealos Cloud 上部署 Meilisearch v1.45.1、持久化存储和轻量 Meilisearch UI 管理界面。

![Meilisearch 截图](website-screenshot.webp)

## 关于 Meilisearch 托管

Meilisearch 以单节点 StatefulSet 运行，并将索引、任务和运行时数据保存在挂载到 `/meili_data` 的持久卷中。API 会通过 Sealos 管理的 HTTPS 入口暴露 `7700` 端口，应用和 SDK 客户端可以从集群外访问。

模板还会使用 `eyeix/meilisearch-ui:v0.15.1-lite` 部署独立的 Meilisearch UI 服务。这个 UI 提供浏览器管理界面，可管理索引、文档、搜索和设置。它不创建用户账户系统；连接时需要填写 Meilisearch API 地址和生成的 `MEILI_MASTER_KEY`。

## 常见使用场景

- **应用内搜索**：为 SaaS 产品、仪表盘和内容应用增加容错搜索能力。
- **电商搜索**：索引商品数据，支持快速关键词搜索、过滤和排序。
- **文档搜索**：为文档站、知识库和帮助中心提供搜索体验。
- **内部工具**：使用内置管理界面查看索引并测试搜索效果。
- **API 原型验证**：在接入 SDK 前创建索引、添加文档并验证查询。

## Meilisearch 托管依赖

Sealos 模板包含 Meilisearch API 容器、Meilisearch UI 容器、用于 `/meili_data` 的持久化存储、Kubernetes Service、HTTPS Ingress 和 Sealos App 链接。

### 部署依赖

- [Meilisearch 文档](https://www.meilisearch.com/docs) - 官方产品和 API 文档
- [Meilisearch REST API 参考](https://www.meilisearch.com/docs/reference/api/overview) - API 端点说明
- [Meilisearch GitHub 仓库](https://github.com/meilisearch/meilisearch) - 源码和版本发布
- [Meilisearch UI 仓库](https://github.com/eyeix/meilisearch-ui) - 此模板使用的 Web 管理界面

### 实现细节

**架构组件：**

此模板会部署以下资源：

- **Meilisearch StatefulSet**：运行 `getmeili/meilisearch:v1.45.1`，并挂载持久化 `/meili_data` 存储。
- **Meilisearch UI Deployment**：运行 `eyeix/meilisearch-ui:v0.15.1-lite`，通过 `24900` 端口提供浏览器管理界面。
- **持久卷声明**：保存索引、任务和运行时数据，避免 Pod 重启后丢失。
- **API Service 和 Ingress**：通过自动生成的 HTTPS URL 暴露 Meilisearch HTTP API。
- **UI Service 和 Ingress**：通过独立 HTTPS URL 暴露管理界面。
- **Sealos App**：在 Sealos Canvas 中打开 Meilisearch UI。

**配置：**

- `MEILI_ENV` 固定为 `production`。
- `MEILI_MASTER_KEY` 会作为 `defaults.master_key` 自动生成，并保护除 `GET /health` 以外的所有 API 路由。
- UI 会将连接信息保存在浏览器中。连接时输入 Meilisearch API URL 和生成的 master key。
- 模板不会把 master key 预置到 UI 中，因为浏览器端 singleton 配置会把 key 暴露在前端包里。
- API 资源使用经过验证的轻量规格：`100m` CPU 和 `128Mi` 内存。UI 使用 Sealos 基线规格：`200m` CPU 和 `256Mi` 内存。

**许可证信息：**

Meilisearch 使用 MIT License。此 Sealos 模板遵循 Sealos templates 仓库的许可证。Meilisearch UI 的许可证请以其上游仓库为准。

## 为什么在 Sealos 上部署 Meilisearch？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用部署、运维和管理。将 Meilisearch 部署到 Sealos 后，你可以获得：

- **一键部署**：从应用商店模板启动 Meilisearch 和管理界面，无需手写 Kubernetes 配置。
- **内置持久化存储**：在重启后保留搜索索引和任务数据。
- **即时公网访问**：部署完成后获得 API 和 Web UI 的 HTTPS 端点。
- **易于自定义**：通过 Canvas 或 AI 对话调整资源、环境变量和存储。
- **无需 Kubernetes 专业知识**：使用 Kubernetes 支撑的工作负载，而无需手动管理 Service、Ingress 或 StatefulSet。
- **按量使用资源**：先使用小规格搜索节点，后续按索引或查询负载扩容。

在 Sealos 上部署 Meilisearch，把精力放在搜索体验上，而不是基础设施配置上。

## 部署指南

1. 打开 [Meilisearch 模板](https://sealos.io/products/app-store/meilisearch)，点击 **Deploy Now**。
2. 在弹窗中检查生成的应用名称、API 域名、UI 域名和 master key。
3. 等待部署完成，通常需要 2-3 分钟。部署后会进入 Canvas。后续如需调整，可在 AI 对话中描述需求，或点击相关资源卡片修改配置。
4. 从 Sealos App 链接打开 Meilisearch UI。UI 不需要注册，也没有用户登录流程。连接实例时填写：
   - **Host**：生成的 Meilisearch API URL，例如 `https://<your-meilisearch-api-url>`
   - **API Key**：生成的 `MEILI_MASTER_KEY`
5. 如果通过 SDK 或 REST 客户端直接访问 API，受保护接口需要携带 `Authorization: Bearer <MEILI_MASTER_KEY>` 或 `X-Meili-API-Key: <MEILI_MASTER_KEY>`。

健康检查示例：

```bash
curl https://<your-meilisearch-api-url>/health
```

认证 API 调用示例：

```bash
curl   -H "Authorization: Bearer <MEILI_MASTER_KEY>"   https://<your-meilisearch-api-url>/version
```

## 配置

部署完成后，你可以通过以下方式配置 Meilisearch：

- **Meilisearch UI**：使用生成的 API URL 和 master key 连接，管理索引、文档和设置。
- **AI 对话**：描述资源或环境变量调整需求，由 Sealos 应用变更。
- **资源卡片**：打开 StatefulSet、Deployment、Service、Ingress、PVC 或 App 卡片，查看和修改部署设置。
- **API 客户端**：结合生成的公网 URL 和 `MEILI_MASTER_KEY` 使用 Meilisearch SDK 或 REST 请求。

## 扩容

如需纵向扩容：

1. 打开当前部署的 Canvas。
2. 点击 Meilisearch StatefulSet 资源卡片。
3. 根据索引和查询负载调整 CPU 与内存资源。
4. 应用变更并等待 Pod 滚动更新完成。

内置 UI 是无状态服务，可独立重新部署。此模板中的 Meilisearch 是单节点部署；对于更大的生产搜索负载，在提升流量或索引规模前，请先参考 Meilisearch 官方建议。

## 故障排查

### UI 要求填写 host 和 API key

- 原因：轻量 UI 会把连接信息保存在浏览器中，不会预置 master key。
- 解决方法：使用生成的 Meilisearch API URL 作为 host，使用生成的 `MEILI_MASTER_KEY` 作为 API key。

### API 请求返回未授权错误

- 原因：Meilisearch 以 production 模式运行，并使用生成的 master key。
- 解决方法：在受保护 API 请求中加入 `Authorization: Bearer <MEILI_MASTER_KEY>` 或 `X-Meili-API-Key: <MEILI_MASTER_KEY>`。

### UI 无法连接 API

- 原因：UI 在浏览器中运行，必须访问公网 Meilisearch API URL。
- 解决方法：使用此模板生成的 HTTPS API URL，不要使用内部 Kubernetes Service 名称。

### 索引任务占用过多内存

- 原因：大批量文档或复杂索引任务可能需要超过轻量默认值的内存。
- 解决方法：在 Canvas 中提高 StatefulSet 内存限制后再执行大批量导入。

### 获取帮助

- [官方文档](https://www.meilisearch.com/docs)
- [GitHub Issues](https://github.com/meilisearch/meilisearch/issues)
- [Meilisearch UI Issues](https://github.com/eyeix/meilisearch-ui/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Meilisearch 快速开始](https://www.meilisearch.com/docs/learn/getting_started/quick_start)
- [API Keys](https://www.meilisearch.com/docs/learn/security/master_api_keys)
- [索引文档](https://www.meilisearch.com/docs/learn/getting_started/indexing)
- [搜索 API](https://www.meilisearch.com/docs/reference/api/search)

## 许可证

此 Sealos 模板遵循 Sealos templates 仓库的许可证。Meilisearch 本身使用 MIT License。
