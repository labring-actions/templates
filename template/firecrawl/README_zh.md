# 在 Sealos 上部署和托管 Firecrawl

Firecrawl 是自托管网页爬取和抓取 API，可将网站转换为干净、适合大模型使用的数据。此模板会在 Sealos Cloud 上部署 Firecrawl，并包含托管 PostgreSQL、托管 Redis、RabbitMQ、Playwright 渲染服务和公网 HTTPS 访问。

![Firecrawl 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/firecrawl/website-screenshot.webp)

## 关于托管 Firecrawl

Firecrawl 提供页面抓取、站点爬取和内容提取 API，适合 AI 工作流使用。API 服务运行 Firecrawl 的自托管 API 和 worker harness，Redis 保存队列和限流状态，RabbitMQ 承载后台任务，PostgreSQL 保存 Firecrawl 和 NUQ 数据，Playwright 处理需要浏览器渲染的页面。

此 Sealos 模板遵循官方自托管拓扑，并使用 Kubernetes 原生 Service 和托管数据库资源。模板默认关闭 API 认证，匹配 Firecrawl 关于自托管 SDK 可选 API key 的说明。

## 常见使用场景

- **LLM 数据摄取**：将网页转换为干净的 Markdown 或结构化数据。
- **研究型爬虫**：爬取文档、市场资料和内容站点。
- **浏览器渲染抓取**：用 Playwright 处理 JavaScript 较重的页面。
- **私有抓取 API**：在自己的 Sealos 工作空间运行可控的 Firecrawl 端点。

## Firecrawl 托管依赖

此模板包含 Firecrawl API 与 worker harness 容器、Playwright 服务、PostgreSQL 16、Redis 7、RabbitMQ、内部 Service、HTTPS Ingress 和 App 资源。

### 部署依赖

- [Firecrawl 官网](https://firecrawl.dev/) - 产品介绍
- [Firecrawl 文档](https://docs.firecrawl.dev/) - API 和 SDK 参考
- [Firecrawl 自托管指南](https://github.com/firecrawl/firecrawl/blob/main/SELF_HOST.md) - 官方自托管运行说明
- [Firecrawl GitHub 仓库](https://github.com/firecrawl/firecrawl) - 源码和问题反馈

### 实现细节

**架构组件：**

- **Firecrawl API 和 Worker Harness**：通过 `3002` 端口提供公网 API，并以适合 Sealos 的低并发配置运行官方自托管 harness。
- **Playwright Service**：内部渲染服务，用于浏览器抓取。
- **PostgreSQL Cluster**：保存 Firecrawl 应用数据和 NUQ 队列 schema。
- **Redis Cluster**：由 KubeBlocks 托管的 Redis 保存队列和限流状态。
- **RabbitMQ StatefulSet**：提供 Firecrawl job harness 所需的 AMQP broker。
- **Ingress 和 App 入口**：通过 Sealos 生成的 HTTPS URL 暴露 Firecrawl API。

**配置：**

- 可选 `openai_api_key`、`openai_base_url` 和 `model_name` 输入用于启用 AI 提取能力。
- 模板自动生成 `BULL_AUTH_KEY`，用于队列管理路径。
- PostgreSQL、Redis、RabbitMQ 和 Playwright URL 由模板内部连接，并使用托管凭据。
- PostgreSQL 初始化步骤会创建 Firecrawl 自托管队列 worker 所需的 NUQ schema。
- Firecrawl API 使用 `NUQ_WORKER_COUNT=1`、`1` CPU 上限和 `2048Mi` 内存上限，这是根据线上 Sealos 验证和 Sealos 资源阶梯确定的配置。
- 对象存储未内置，因为 Firecrawl 官方自托管 Docker 与 Kubernetes 部署文档没有定义必需的 S3 兼容运行配置。

**许可证信息：**

Firecrawl 使用 AGPL-3.0 License。此 Sealos 模板提供在 Sealos Cloud 上运行 Firecrawl 的部署配置。

## 为什么在 Sealos 上部署 Firecrawl？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一部署和运维流程。在 Sealos 上部署 Firecrawl，可以获得一键部署、自动 HTTPS、托管数据服务、持久化存储、资源控制和基于 Canvas 的更新能力。

## 部署指南

1. 打开 [Firecrawl 模板](https://sealos.io/products/app-store/firecrawl)，点击 **Deploy Now**。
2. 如需 AI 提取能力，配置可选 OpenAI 兼容模型参数。
3. 等待部署完成，通常需要 3-5 分钟，期间 PostgreSQL、Redis、RabbitMQ 和 Playwright 会依次就绪。部署完成后会跳转到 Canvas。后续修改可以在 AI 对话中描述需求，或点击相关资源卡片调整设置。
4. 将生成的公网 URL 作为 Firecrawl API base URL 使用。
5. 从客户端发送 `/v1/scrape` 或 `/v1/crawl` 请求验证 API 可用性。默认模板会关闭 API 认证，因此自托管 SDK 可以省略 API key；后续启用数据库认证后再配置 API key。

## 配置

部署后可以通过以下方式配置 Firecrawl：

- **API 客户端**：将 SDK 或 HTTP 客户端指向生成的 URL。
- **AI 对话**：更新模型设置或并发相关环境变量。
- **资源卡片**：在 Canvas 中调整 API、Playwright、RabbitMQ、Redis 或 PostgreSQL 资源。
- **队列管理路径**：需要查看 Bull 队列时使用生成的 `BULL_AUTH_KEY`。
- **登录和 API key**：此模板里的 Firecrawl 是 API 优先服务，没有浏览器登录界面；`USE_DB_AUTHENTICATION=false` 时，自托管 SDK 可以省略 API key。

## 扩缩容

默认从单个 API 和 Playwright 副本开始。爬取量增长时先增加 API 的 CPU 与内存，再检查 Playwright、Redis、RabbitMQ 和 PostgreSQL 的就绪状态与存储容量。

## 故障排查

### API 请求超时

- 原因：API 可能仍在等待 Redis、RabbitMQ、PostgreSQL 或 Playwright。
- 解决方法：先在 Canvas 中检查所有工作负载日志和数据库就绪状态。

### API 日志出现 worker load 警告

- 原因：Firecrawl 内置 queue worker 在爬取突发时接近 CPU 上限。
- 解决方法：先在 Canvas 中提高 Firecrawl API CPU 上限，再提高 worker 并发。

### 浏览器渲染页面失败

- 原因：Playwright 服务不可用或资源不足。
- 解决方法：查看 Playwright Deployment 日志，并为浏览器密集型任务增加 CPU 或内存。

### AI 提取失败

- 原因：OpenAI 兼容模型凭据缺失或无效。
- 解决方法：设置 `openai_api_key`、`openai_base_url` 和 `model_name`，然后重启 API Deployment。

## 更多资源

- [Firecrawl API 文档](https://docs.firecrawl.dev/)
- [Firecrawl 自托管指南](https://github.com/firecrawl/firecrawl/blob/main/SELF_HOST.md)
- [Firecrawl GitHub Issues](https://github.com/firecrawl/firecrawl/issues)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板作为部署配置提供给 Sealos 用户使用。Firecrawl 本身基于 [AGPL-3.0 License](https://github.com/firecrawl/firecrawl/blob/main/LICENSE) 授权。
