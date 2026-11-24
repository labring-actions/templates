# 在 Sealos 上部署和托管 OmniRoute

OmniRoute 是自托管的 OpenAI 兼容 AI 网关，提供模型路由、供应商故障回退、API Key 和管理面板。

![OmniRoute 管理面板](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/omniroute/website-screenshot.webp)

## 关于 OmniRoute 托管

本模板以 StatefulSet 运行 OmniRoute，为 `/app/data` 挂载 1 GiB 持久卷，并配套一个 KubeBlocks Redis Cluster 保存运行状态。管理面板密码在部署时提供，网关请求需要 API Key。

打开公网地址并使用初始密码登录。在管理面板中添加供应商凭据、配置模型路由与故障回退，并为客户端创建 API Key。OpenAI 兼容端点通过同一域名提供。

## 架构组件

- **OmniRoute StatefulSet**：运行管理面板、路由引擎和 OpenAI 兼容 API。
- **KubeBlocks Redis Cluster**：提供单副本 Redis 服务，用于运行状态和缓存。
- **持久卷**：保存 OmniRoute 配置、供应商元数据和 API Key。
- **Service 与 Ingress**：通过公网 HTTPS 发布管理面板和 API。

## 常见使用场景

- 在多个模型供应商前提供统一的 OpenAI 兼容端点。
- 按模型、成本或可用性路由请求并自动回退。
- 集中管理供应商凭据，并向应用签发限定范围的 API Key。
- 统计助手、Agent 和内部工具的使用情况。
- 在生产推广前验证多供应商 AI 路由方案。

## OmniRoute 托管依赖

- 具备 CPU、内存和存储配额的 Sealos 工作空间。
- 由本模板创建的 KubeBlocks Redis Cluster。
- 至少一个上游 AI 供应商账号和 API Key。
- 通过模板 input 提供的初始管理面板密码。
- 到已配置模型供应商的出站 HTTPS 访问。

## 为什么在 Sealos 上部署 OmniRoute？

- 一键部署网关及其 Redis 依赖。
- 由 Kubernetes 提供健康探针、调度和 Pod 自动恢复。
- 持久化存储保留路由、供应商设置和 API Key。
- 按量计费的资源卡适配网关负载。
- 通过 Canvas 查看 StatefulSet、Redis Cluster、Service 和 Ingress。
- 在 Sealos 桌面中通过 AI 对话获取部署指导。

## 部署指南

1. 打开 [OmniRoute 模板](https://sealos.io/products/app-store/omniroute)，点击 **Deploy Now**。
2. 输入初始管理面板密码，保留自动生成的应用名称，并确认资源规格。
3. 等待 2-3 分钟让 StatefulSet 和 Redis Cluster 就绪，然后从 App 卡片打开公网地址。
4. 使用第 2 步的密码登录，添加供应商凭据并创建 API Key。
5. 使用该 Key 向 OpenAI 兼容端点发送一次测试聊天请求，再打开 Canvas 查看全部资源。

## 许可证

OmniRoute 使用 [MIT License](https://github.com/cheaper-inference/OmniRoute/blob/main/LICENSE) 许可证。
