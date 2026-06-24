# 在 Sealos 上部署和托管 cobalt

cobalt 是注重隐私的媒体处理 API，可从受支持的社交和视频服务保存媒体内容。本模板会在 Sealos Cloud 上部署 cobalt API 容器，并配置 HTTPS Ingress 和可选认证控制。

![cobalt 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/cobalt/website-screenshot.webp)

## 关于 cobalt 托管

cobalt 作为轻量 API 服务运行。它接收媒体处理请求，应用速率限制，并为受支持服务返回结构化响应。官方容器要求配置 `API_URL`，本模板会将它设置为 Sealos 公网 HTTPS 地址。

Sealos 模板会以 Kubernetes Deployment 部署 cobalt，监听 `9000` 端口。默认单实例模式不需要数据库。上游 cobalt 只有在 `API_INSTANCE_COUNT` 大于 `1` 时才需要 Redis，因此本模板保持默认单实例模式，并避免创建多余数据库资源。

Sealos 会负责公网 HTTPS 访问、服务发现、资源配置和应用入口管理。

## 常见使用场景

- **媒体处理 API**：为受支持的媒体提取流程提供自托管 API。
- **私有工具后端**：为内部工具运行可控的 cobalt 实例。
- **带限流的公网入口**：使用内置限流环境变量支撑公网部署。
- **机器人防护**：公开暴露时可配置 Cloudflare Turnstile 会话认证。

## cobalt 托管依赖

本 Sealos 模板包含以下运行依赖：

- cobalt 镜像 `ghcr.io/imputnet/cobalt:7.13.3`
- HTTPS Ingress 和 Sealos App 入口

### 部署依赖

- [cobalt GitHub 仓库](https://github.com/imputnet/cobalt) - 源码和版本发布
- [cobalt 实例运行指南](https://github.com/imputnet/cobalt/blob/main/docs/run-an-instance.md) - 运行部署参考
- [cobalt API 环境变量](https://github.com/imputnet/cobalt/blob/main/docs/api-env-variables.md) - 配置参考

## 实现细节

**架构组件：**

- **cobalt Deployment**：使用 `ghcr.io/imputnet/cobalt:7.13.3` 镜像运行，监听 `9000` 端口。
- **Service 和 Ingress**：通过公网 HTTPS 地址暴露 cobalt。
- **Sealos App Resource**：把 cobalt 加入 Sealos 应用界面。

**配置：**

模板会设置：

- `API_URL` 为带尾部斜杠的 Sealos 公网地址。
- `API_PORT=9000`
- 与上游文档一致的保守限流默认值。
- 可选 `TURNSTILE_SITEKEY` 和 `TURNSTILE_SECRET`。
- 可选 `API_AUTH_REQUIRED`。
- 可选逗号分隔的 `DISABLED_SERVICES`。

cobalt 没有登录或注册流程。默认情况下 API 直接开放。需要让 API 请求通过 Turnstile 会话校验时，请启用 `api_auth_required` 并配置 Turnstile。

**默认资源：**

- App CPU limit：`200m`
- App Memory limit：`256Mi`
- App CPU request：`20m`
- App Memory request：`25Mi`

**健康检查：**

模板在 cobalt API 端口上使用 TCP 启动、就绪和存活探针。

**许可信息：**

cobalt 使用 GNU AGPL v3.0。

## 为什么在 Sealos 上部署 cobalt？

Sealos 是基于 Kubernetes 构建的 AI 辅助云操作系统，统一应用部署、存储、网络和运维。在 Sealos 上部署 cobalt 可以获得：

- **一键部署**：通过一个模板部署 cobalt 和 HTTPS 访问。
- **无数据库负担**：默认单实例部署不需要 PostgreSQL、Redis 或对象存储。
- **即时公网访问**：Sealos 自动分配公网 HTTPS 入口。
- **易于自定义**：可在 Sealos Canvas 调整限流、禁用服务和认证设置。
- **AI 辅助运维**：可通过 Sealos AI 对话或资源卡片修改部署。

## 部署指南

1. 打开 [cobalt 模板](https://sealos.io/products/app-store/cobalt)，点击 **Deploy Now**。
2. 配置部署参数：
   - **api_auth_required**：需要请求通过 Turnstile 会话校验时启用。
   - **disabled_services**：可选的逗号分隔禁用服务列表。
   - **turnstile_sitekey** 和 **turnstile_secret**：可选 Cloudflare Turnstile 设置。
3. 等待部署完成，通常需要 1-2 分钟。部署完成后，你会进入 Canvas。后续如需修改配置，可以在对话框中描述需求，让 AI 自动应用变更；也可以点击对应资源卡片手动调整设置。
4. 通过提供的 URL 访问 cobalt：
   - **API Base URL**：使用 Sealos 提供的公网 HTTPS 地址。
   - **Server Info**：打开 `/` 查看 cobalt 元数据。

## 配置

部署后可通过以下方式配置 cobalt：

- **环境变量**：通过 Deployment 资源卡片调整限流、禁用服务、Turnstile、API 认证、代理和 YouTube session 设置。
- **AI 对话**：在 Sealos 中描述想要变更的配置，让 AI 应用到对应资源。
- **Ingress 设置**：媒体流程需要更长请求时间时，可调整上传和超时设置。

## 故障排查

### 容器启动后立即退出

- **原因**：`API_URL` 缺失或格式错误。
- **解决方法**：保留模板生成的 `API_URL`，包含 `https://` 协议和尾部斜杠。

### 公网请求需要 Turnstile 会话校验

- **原因**：cobalt 默认开放 API。
- **解决方法**：启用 `api_auth_required`，并配置 `turnstile_sitekey` 和 `turnstile_secret`。

### 部分服务处理失败

- **原因**：某些 provider 可能需要 cookies、代理或 YouTube session 设置。
- **解决方法**：在 Deployment 资源卡片中按 cobalt 文档添加对应上游环境变量。

## 更多资源

- [cobalt 文档](https://github.com/imputnet/cobalt/tree/main/docs)
- [cobalt API 参考](https://github.com/imputnet/cobalt/blob/main/docs/api.md)
- [Sealos 应用商店](https://sealos.io/products/app-store)

## 许可证

本 Sealos 模板提供在 Sealos 上运行 cobalt 的部署配置。cobalt 本身使用 GNU AGPL v3.0。
