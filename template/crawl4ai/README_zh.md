# 在 Sealos 上部署和托管 Crawl4AI

Crawl4AI 是面向 LLM 的开源网页爬取与抓取工具。此模板在 Sealos Cloud 上部署官方 Crawl4AI API Server，并提供 Dashboard 和 Playground。

![Crawl4AI 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/crawl4ai/website-screenshot.webp)

## 关于托管 Crawl4AI

Crawl4AI 以单个 API/Web 服务运行在 `11235` 端口。部署后可通过公网 HTTPS 地址访问 Dashboard、Playground、crawl API、task API 和浏览器驱动的抓取能力。

模板为浏览器共享内存和运行时缓存路径创建持久化存储。Sealos 负责 TLS、Ingress 路由、重启管理和资源控制。

## 常见使用场景

- **LLM 内容抽取**：爬取页面并生成 markdown 或结构化内容，用于 AI 工作流。
- **抓取 API**：通过 `/crawl` 提交任务，并通过 `/task/{id}` 获取结果。
- **交互式测试**：使用 `/playground` 测试请求并生成示例代码。
- **自托管爬取后端**：把 Crawl4AI 作为内部自动化共享服务运行。

## Crawl4AI 托管依赖

Sealos 模板包含 Crawl4AI Docker Server 镜像、持久化缓存存储、公网 HTTPS Ingress 和 App 快捷入口。

### 部署依赖

- [Crawl4AI 文档](https://docs.crawl4ai.com/) - 官方文档
- [自托管指南](https://docs.crawl4ai.com/core/self-hosting/) - Docker Server 参考
- [Crawl4AI GitHub 仓库](https://github.com/unclecode/crawl4ai) - 源码与发布版本

### 实现细节

**架构组件：**

- **Crawl4AI StatefulSet**：运行 `unclecode/crawl4ai:0.8.9`，监听 `11235` 端口。
- **持久化 `/dev/shm` 卷**：通过持久卷提供浏览器共享内存空间。
- **持久化缓存卷**：保存 `/app/.cache`。
- **Ingress 与 App**：通过 HTTPS 发布 `/playground`、`/dashboard` 和 API 端点。

**配置：**

- App 快捷入口打开 `/playground`。
- API 基础地址为部署根 URL。
- 健康检查使用 `/health`。

**许可证信息：**

Crawl4AI 使用 Apache-2.0 许可证。此 Sealos 模板遵循仓库许可证。

## 为什么在 Sealos 上部署 Crawl4AI？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一从云端 IDE 到生产部署和管理的完整应用生命周期。在 Sealos 上部署 Crawl4AI 可以获得：

- **一键部署**：快速部署 Crawl4AI API Server。
- **公网 HTTPS API**：可从浏览器、脚本和 AI 工具调用 crawl API。
- **持久化运行时路径**：重启后保留运行时缓存路径。
- **便捷资源调优**：可在 Canvas 中为较重的爬取任务提高 CPU 和内存。
- **统一管理**：在 Sealos 中重启、查看日志和调整设置。

## 部署指南

1. 打开 [Crawl4AI 模板](https://sealos.io/products/app-store/crawl4ai)，点击 **Deploy Now**。
2. 查看默认资源并部署。
3. 等待部署完成。部署完成后会跳转到 Canvas。
4. 通过以下地址访问应用：
   - **Playground**：`https://<your-app-url>/playground`
   - **Dashboard**：`https://<your-app-url>/dashboard`
   - **API**：`https://<your-app-url>/crawl`

## 配置

部署后可通过以下方式配置 Crawl4AI：

- **Playground**：交互式测试爬取请求。
- **API 客户端**：向 `/crawl` 发送请求，并轮询 `/task/{id}`。
- **资源卡片**：为较大的爬取任务提高 CPU、内存或存储。

## 故障排查

### 浏览器驱动的爬取在高负载下失败

- 原因：当前部署需要更多 CPU、内存或浏览器共享内存空间。
- 解决方法：在 Canvas 中提高 StatefulSet CPU 和内存，然后用更小的爬取批次重试。

### API 请求超时

- 原因：目标站点响应慢或爬取任务较大。
- 解决方法：使用 `/task/{id}` 异步轮询，并仅为长耗时内部工作负载提高代理读取超时。

## 其他资源

- [Crawl4AI 文档](https://docs.crawl4ai.com/)
- [Docker 示例](https://github.com/unclecode/crawl4ai/blob/main/docs/examples/docker_example.py)
- [自托管指南](https://docs.crawl4ai.com/core/self-hosting/)

## 许可证

此 Sealos 模板遵循仓库许可证。Crawl4AI 本身使用 Apache-2.0 许可证。
