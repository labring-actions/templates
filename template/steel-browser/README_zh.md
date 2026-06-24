# 在 Sealos 上部署和托管 Steel Browser

Steel Browser 是面向 AI Agent 和应用的开源浏览器 API。此模板会在 Sealos Cloud 上部署 Steel Browser API 与 UI 合并容器，并配置持久化浏览器文件与缓存存储。

![应用截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/steel-browser/website-screenshot.webp)

## 关于托管 Steel Browser

Steel Browser 提供 REST API、Swagger 文档、会话调试 UI，以及用于浏览器自动化的 Chrome DevTools Protocol 连接能力。此模板运行官方合并镜像，API 和 Web UI 由同一个工作负载提供。

Sealos 会自动创建 HTTPS Ingress、用于生成文件和浏览器缓存数据的持久化卷，以及公网访问地址。浏览器调试端口保留在 Kubernetes 内部服务边界内。

## 常见使用场景

- **AI Web Agent**：为 Agent 提供可控制的浏览器会话。
- **网页抓取与提取**：通过 API 获取截图、PDF、Markdown 和可读正文内容。
- **自动化调试**：通过内置 UI 和 API 文档检查浏览器会话。
- **SDK 集成**：让 Node.js、Python、Playwright、Puppeteer 或 Selenium 客户端连接到自托管端点。

## Steel Browser 托管依赖

此 Sealos 模板包含 Steel Browser 运行时容器、持久化卷、内部服务发现和 HTTPS Ingress。

### 部署依赖

- [官方文档](https://docs.steel.dev/) - Steel 文档
- [API 参考](https://docs.steel.dev/api-reference) - REST API 参考
- [GitHub 仓库](https://github.com/steel-dev/steel-browser) - 源代码和发布标签

### 实现细节

**架构组件：**

- **Steel Browser**：使用模板中固定的 `ghcr.io/steel-dev/steel-browser` 镜像 digest 提供 API 与 UI 合并服务。由于每个 session 都会启动真实 Chromium 运行时，工作负载内存上限按官方 4 GB 建议配置。
- **持久化文件卷**：保存 `/files` 下的浏览器生成文件。
- **浏览器缓存卷**：保存 `/app/.cache` 下的 Chromium 和 Puppeteer 缓存数据。
- **Ingress**：通过 Sealos 托管 TLS 暴露 `3000` 端口上的 Web UI 和 API。

**配置：**

公网端点通过 `/ui` 提供 UI，生成的 Sealos 基础 URL 提供健康检查响应，`/v1/sessions` 提供 API session 元数据，`/documentation/` 提供 Swagger 文档。容器也暴露内部调试端口，用户流量通过 HTTPS Ingress 访问。

模板默认设置 `SKIP_FINGERPRINT_INJECTION=true`。当上游 fingerprint generator 无法为捆绑浏览器运行时生成匹配的桌面 Chrome 指纹时，这个设置可以保持 Sealos 自托管 session 稳定创建。Session 创建、截图、PDF 导出和自动化 API 会继续使用浏览器原生指纹运行。

**许可证信息：**

Steel Browser 使用 Apache License 2.0。

## 为什么在 Sealos 上部署 Steel Browser？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一覆盖从云端 IDE 开发到生产部署与运维的完整应用生命周期。它非常适合构建和扩展现代 AI 应用、SaaS 平台和复杂微服务架构。在 Sealos 上部署 Steel Browser，你可以获得：

- **一键部署**：一次点击即可部署浏览器自动化基础设施。
- **易于自定义**：通过 Sealos UI 配置资源和环境变量。
- **无需 Kubernetes 专业知识**：无需手动维护清单即可运行浏览器 API。
- **内置持久化存储**：重启后保留生成文件和浏览器缓存数据。
- **即时公网访问**：自动获得 API 和 UI 的 HTTPS 端点。

在 Sealos 上部署 Steel Browser，把精力放在 Agent 工作流上。

## 部署指南

1. 打开 [Steel Browser 模板](https://sealos.io/products/app-store/steel-browser)，点击 **Deploy Now**。
2. 在弹窗中配置参数。
3. 等待部署完成。部署完成后会跳转到 Canvas。
4. 通过提供的 URL 访问应用：
   - **Steel UI**：在生成的 URL 后打开 `/ui`。
   - **API 端点**：将生成的 URL 作为 SDK 的 `baseURL`。
   - **API 文档**：在生成的 URL 后打开 `/documentation/`，或查看上游 [API 参考](https://docs.steel.dev/api-reference)。

## 配置

Steel Browser 无需初始管理员账号。API 客户端可以把生成的 Sealos URL 作为 `baseURL`。公网部署时，先通过私有网络、网关或带认证的反向代理增加访问控制，再把端点分享给其他用户。模板默认关闭 fingerprint injection，以保证自托管浏览器稳定启动；高级用户确认目标镜像支持所需指纹配置后，可在 StatefulSet 环境变量中重新启用。

## 扩缩容

Steel Browser 使用本地持久化卷保存浏览器会话和文件输出，因此默认按单副本运行。随着 session 并发和生成文件增加，可提高 CPU、内存或卷容量。

## 故障排查

### 浏览器会话启动较慢

- 原因：Chromium 和 Xvfb 需要内存和启动时间。
- 解决办法：提高 Steel Browser 工作负载内存，并等待启动探针完成。

### 创建 session 返回 fingerprint generation 错误

- 原因：捆绑的 fingerprint generator 可能无法为当前镜像和请求尺寸生成一致的 Chrome 指纹。
- 解决办法：保留 `SKIP_FINGERPRINT_INJECTION=true`，然后通过 API 或 UI 创建 session。

### API 客户端无法直接连接 CDP

- 原因：调试端口保留在模板内部。
- 解决办法：使用公网 Sealos URL 提供的 Steel API 和 SDK 端点。

## 更多资源

- [Steel 文档](https://docs.steel.dev/)
- [Steel API 参考](https://docs.steel.dev/api-reference)
- [Steel Cookbook](https://github.com/steel-dev/steel-cookbook)

## 许可证

此 Sealos 模板使用 Apache License 2.0。Steel Browser 本身使用 Apache License 2.0。
