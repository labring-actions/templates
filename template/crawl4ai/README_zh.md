# 在 Sealos 上部署和托管 Crawl4AI

Crawl4AI 是面向 LLM 的开源网页爬取与抓取工具。此模板在 Sealos Cloud 上部署官方 Crawl4AI API Server，并提供 Dashboard 和 Playground。

![Crawl4AI 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/crawl4ai/website-screenshot.webp)

## 关于托管 Crawl4AI

Crawl4AI 以单个 API/Web 服务运行在 `11235` 端口。部署后可通过公网 HTTPS 地址访问 Dashboard、Playground、crawl API 和浏览器驱动的抓取能力，`CRAWL4AI_API_TOKEN` 为这些公开入口提供访问保护。

模板会提供 1 GiB 持久化 Playwright 浏览器缓存、1 GiB 的 `/dev/shm` 浏览器共享内存，并在 `/var/lib/crawl4ai/outputs` 保存截图和 PDF 等抓取产物。初始化容器会把镜像兼容的 Chromium revision 安装到缓存中，Sealos 负责 TLS、Ingress 路由、重启管理和资源控制。

## 常见使用场景

- **LLM 内容抽取**：爬取页面并生成 markdown 或结构化内容，用于 AI 工作流。
- **抓取 API**：通过 `/crawl` 执行同步爬取，或通过 `/crawl/job` 提交异步任务，再从 `/crawl/job/{task_id}` 获取结果。
- **交互式测试**：使用 `/playground` 测试请求并生成示例代码。
- **自托管爬取后端**：把 Crawl4AI 作为内部自动化共享服务运行。

## Crawl4AI 托管依赖

Sealos 模板包含 Crawl4AI Docker Server 镜像、持久化输出存储、浏览器共享内存、公网 HTTPS Ingress 和 App 快捷入口。

### 部署依赖

- [Crawl4AI 文档](https://docs.crawl4ai.com/) - 官方文档
- [自托管指南](https://docs.crawl4ai.com/core/self-hosting/) - Docker Server 参考
- [Crawl4AI GitHub 仓库](https://github.com/unclecode/crawl4ai) - 源码与发布版本

### 实现细节

**架构组件：**

- **Crawl4AI StatefulSet**：运行 `unclecode/crawl4ai:0.9.1`，监听 `11235` 端口并启用令牌认证。
- **持久化 Playwright 缓存**：安装并保留镜像所需的精确 Chromium revision。
- **持久化 `/dev/shm` 卷**：通过兼容 Sealos 的持久卷提供 1 GiB 浏览器共享内存空间。
- **持久化输出卷**：将生成的爬取产物保存到 `/var/lib/crawl4ai/outputs`，重启后继续保留。
- **Ingress 与 App**：通过 HTTPS 发布 `/playground/`、`/dashboard/` 和 API 端点。

**配置：**

- App 快捷入口打开 `/playground/`，访问 `/` 时会重定向到该页面。
- API 基础地址为部署根 URL。
- Playground、Dashboard 和受保护的 API 端点使用部署时设置的 `CRAWL4AI_API_TOKEN`。
- 公网 Ingress 会关闭访问日志，避免 Dashboard WebSocket 的令牌查询参数写入入口请求日志。
- 模板会生成稳定的 `SECRET_KEY`，使 Pod 重启后的会话凭据保持有效。
- 健康检查使用公开的 `/health` 端点。

**许可证信息：**

Crawl4AI 使用 Apache-2.0 许可证。此 Sealos 模板遵循仓库许可证。

## 为什么在 Sealos 上部署 Crawl4AI？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一从云端 IDE 到生产部署和管理的完整应用生命周期。在 Sealos 上部署 Crawl4AI 可以获得：

- **一键部署**：快速部署 Crawl4AI API Server。
- **公网 HTTPS API**：可从浏览器、脚本和 AI 工具调用 crawl API。
- **公开入口保护**：Playground、Dashboard 和爬取请求均需使用部署令牌。
- **爬取产物持久化**：重启后继续保留生成的爬取产物。
- **便捷资源调优**：可在 Canvas 中为较重的爬取任务提高 CPU 和内存。
- **统一管理**：在 Sealos 中重启、查看日志和调整设置。

## 部署指南

1. 打开 [Crawl4AI 模板](https://sealos.io/products/app-store/crawl4ai)，点击 **Deploy Now**。
2. 保留自动生成的 **API 令牌**，或替换为自定义的高强度令牌，然后开始部署。请妥善保存该值，Playground、Dashboard 和 API 客户端都会使用它。
3. 等待 2-3 分钟完成部署。部署完成后会跳转到 Canvas，后续可通过 AI 对话框和资源卡片调整配置。
4. 通过以下地址访问应用：
   - **Playground**：打开 `https://<your-app-url>/playground/`，页面提示时在 API Token 输入框中填写部署令牌。
   - **Dashboard**：打开 `https://<your-app-url>/dashboard/`，页面提示时在 API Token 输入框中填写同一个部署令牌。
   - **API**：向 `https://<your-app-url>/crawl` 发送请求，并设置 `Authorization: Bearer <CRAWL4AI_API_TOKEN>`。
   - **健康检查**：访问公开端点 `https://<your-app-url>/health`。

## 配置

部署后可通过以下方式配置 Crawl4AI：

- **Playground 与 Dashboard**：在两个界面的 API Token 输入框中填写部署时选定的 `CRAWL4AI_API_TOKEN`。
- **API 客户端**：向 `/crawl` 发送同步请求，或在 `/crawl/job` 创建异步任务，再携带 Bearer Token 轮询 `/crawl/job/{task_id}`。
- **持久化输出**：生成的产物保存在 StatefulSet 内的 `/var/lib/crawl4ai/outputs`。
- **资源卡片**：为较大的爬取任务提高 CPU、内存或存储。

## 故障排查

### 浏览器驱动的爬取在高负载下失败

- 原因：当前部署需要更多 CPU、内存或浏览器共享内存空间。
- 解决方法：在 Canvas 中提高 StatefulSet CPU 和内存，然后用更小的爬取批次重试。

### Playground、Dashboard 或 API 返回鉴权错误

- 原因：提交的令牌与部署环境中的 `CRAWL4AI_API_TOKEN` 值存在差异。
- 解决方法：在 Playground 或 Dashboard 的 API Token 输入框中填写部署令牌，API 客户端则通过 Bearer Token 发送该值。

### API 请求超时

- 原因：目标站点响应慢或爬取任务较大。
- 解决方法：通过 `/crawl/job` 提交异步任务，轮询 `/crawl/job/{task_id}`，并为长耗时内部工作负载调整代理读取超时。

## 其他资源

- [Crawl4AI 文档](https://docs.crawl4ai.com/)
- [Docker 示例](https://github.com/unclecode/crawl4ai/blob/main/docs/examples/docker_example.py)
- [自托管指南](https://docs.crawl4ai.com/core/self-hosting/)

## 许可证

此 Sealos 模板遵循仓库许可证。Crawl4AI 本身使用 Apache-2.0 许可证。
