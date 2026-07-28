# 在 Sealos 上部署和托管 RSSHub

RSSHub 可将数百个网站的内容转换为标准 RSS 订阅源，供 RSS 阅读器和自动化工具使用。此模板会在 Sealos Cloud 上部署 RSSHub，并配套 Redis 缓存与独立 Browserless 服务。

![RSSHub 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/rsshub/website-screenshot.webp)

## 关于 RSSHub 托管

RSSHub 通过 HTTP 路由采集来源内容，并输出 RSS 格式数据。RSS 阅读器、通知服务和自动化系统可以通过公网应用地址订阅这些路由。

Sealos 模板会创建 RSSHub、用于共享缓存的 KubeBlocks Redis，以及为浏览器渲染型路由提供 Chrome 能力的 Browserless。Sealos 还会配置健康探针、内部服务发现、启用 TLS 的公网入口和 Redis 持久化存储。

## 常见使用场景

- **扩展 RSS 阅读器订阅源**：为原生订阅能力有限的网站生成 RSS。
- **内容更新监控**：使用统一订阅格式跟踪多个受支持网站。
- **自动化数据源**：将 RSS 条目接入工作流、通知或归档系统。
- **团队订阅服务**：搭建带集中缓存的共享 RSSHub 端点。

## 托管 RSSHub 所需的依赖

模板包含 RSSHub、KubeBlocks Redis、Browserless Chrome、内部 Service、健康探针、公网 Ingress 和 Sealos 应用入口。默认配置可直接部署，无需填写额外参数。

### 部署依赖

- [RSSHub 文档](https://docs.rsshub.app/) - 路由目录、部署与使用文档
- [RSSHub 路由](https://docs.rsshub.app/routes/) - 支持的网站与路由参数
- [RSSHub 源码](https://github.com/DIYgod/RSSHub) - 源代码、版本发布与问题跟踪
- [Browserless 文档](https://docs.browserless.io/) - 浏览器自动化服务文档

### 实现细节

**架构组件：**

- **RSSHub**：公网订阅 API，使用 `2026-07-23` 镜像并监听 1200 端口。
- **Redis**：KubeBlocks Redis 7.2.7 集群，用于共享路由缓存。
- **Browserless**：Browserless Chrome 2.55.0，通过内部服务支持浏览器渲染型路由。
- **公网入口**：由 Sealos 管理的 HTTPS Ingress，仅对外暴露 RSSHub，Redis 和 Browserless 保持集群内访问。

RSSHub 使用 Sealos 管理的数据库凭据连接 Redis，并通过 Playwright WebSocket 端点访问 Browserless。应用、浏览器服务和数据库均使用分别实测过的资源配置。RSSHub 采用 GNU Affero General Public License v3.0。

## 为什么选择在 Sealos 上部署 RSSHub？

- **一键部署**：一次创建订阅服务、缓存、浏览器运行时、存储、网络和 TLS 入口。
- **共享路由缓存**：通过内置 Redis 减少对来源网站的重复请求。
- **浏览器渲染路由**：由独立 Browserless 服务支持需要真实浏览器的路由。
- **即时 HTTPS 访问**：自动获得带托管证书的公网 RSSHub 地址。
- **Kubernetes 运维能力**：通过 Sealos Canvas、AI 对话和资源卡片分别查看与调整各组件。

## 部署指南

1. 打开 [RSSHub 模板](https://sealos.io/products/app-store/rsshub)，点击 **Deploy Now**。
2. 检查自动生成的应用名称和公网域名，然后开始部署。
3. 等待部署完成，通常需要 2-3 分钟。Redis 创建账户 Secret 和服务时可能需要更长的初始化时间。
4. 打开 Sealos 中显示的 RSSHub 应用地址。

## 使用 RSSHub 路由

根页面可用于确认 RSSHub 服务已经就绪。将文档中的路由追加到公网应用地址，即可得到订阅链接：

```text
https://<your-rsshub-domain>/<route-and-parameters>
```

例如，从 [RSSHub 路由目录](https://docs.rsshub.app/routes/) 中选择所需路由，把文档示例中的 `https://rsshub.app` 前缀替换成 Sealos 应用地址，再将结果添加到 RSS 阅读器。运维健康检查端点为 `/healthz`。

## 配置

可以通过 RSSHub Deployment 资源卡片设置受支持的环境变量，调整路由行为。`REDIS_URL` 应连接模板内置的 KubeBlocks Redis，`PLAYWRIGHT_WS_ENDPOINT` 应连接内部 Browserless 服务。

部署层面的变更可通过 Sealos Canvas AI 对话完成，也可以直接打开 RSSHub、Browserless、Redis 和网络资源卡片调整。

## 扩缩容

提高 RSSHub 的 CPU 和内存可承载更多并发请求或计算密集型路由。浏览器负载增长时可扩充 Browserless 资源，缓存规模扩大时应同步检查 Redis 容量。每次调整副本或资源后，都需要重新验证路由行为。

## 故障排查

### 路由返回错误

对照最新路由文档检查路径和必填参数。随后查看 RSSHub Pod 日志，定位来源网站、网络、限流或解析问题。

### 浏览器渲染型路由报错

确认 Browserless Pod 处于 Ready 状态，内部 Service 已生成可用端点。结合 RSSHub 与 Browserless 日志检查 Playwright 连接或页面加载错误。

### Redis 初始化时间较长

等待 KubeBlocks Redis Cluster 和账户 Secret 就绪。Redis 服务可用后，RSSHub 会自动建立连接。

### 获取帮助

- [RSSHub Issues](https://github.com/DIYgod/RSSHub/issues)
- [RSSHub 社区](https://docs.rsshub.app/community/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

此 Sealos 模板遵循 templates 仓库的许可条款。RSSHub 采用 [GNU Affero General Public License v3.0](https://github.com/DIYgod/RSSHub/blob/master/LICENSE)。
