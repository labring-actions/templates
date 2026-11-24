# 在 Sealos 上部署和托管 SearXNG

SearXNG 是注重隐私的元搜索引擎，可聚合多个来源的结果，并避免构建用户画像。

![SearXNG 搜索结果](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/searxng/website-screenshot.webp)

## 关于 SearXNG 托管

本模板以 StatefulSet 运行 SearXNG，并配套一个 KubeBlocks Redis Cluster 用于缓存和限流。Web 界面通过公网 HTTPS 发布，自动生成的密钥用于保护会话数据。

内置配置启用了 `360search` 引擎，其余引擎保持关闭。可在 SearXNG 设置中添加工作空间网络可达的引擎，然后重启工作负载使配置生效。

## 架构组件

- **SearXNG StatefulSet**：提供搜索界面并聚合各引擎结果。
- **KubeBlocks Redis Cluster**：提供单副本 Redis 服务和单 Sentinel，用于缓存与限流状态。
- **Service 与 Ingress**：通过公网 HTTPS 暴露 Web 界面。
- **ConfigMap**：保存 SearXNG 设置、启用引擎和超时参数。

## 常见使用场景

- 为团队或家庭提供私有元搜索前端。
- 在单一界面中查询多个搜索引擎。
- 在共享网络中减少搜索画像。
- 为内部工具增加自托管搜索端点。
- 在向用户开放前验证引擎覆盖情况。

## SearXNG 托管依赖

- 具备 CPU、内存和存储配额的 Sealos 工作空间。
- 由本模板创建的 KubeBlocks Redis Cluster。
- 到每个启用搜索引擎的出站 HTTPS 访问。
- 用于 Redis 数据卷的存储。

## 为什么在 Sealos 上部署 SearXNG？

- 一键部署 SearXNG 及其 Redis 依赖。
- 由 Kubernetes 提供健康探针、调度和 Pod 自动恢复。
- 通过 KubeBlocks 提供持久化缓存存储。
- Web 与数据库组件均使用按量计费的资源卡。
- 通过 Canvas 查看 StatefulSet、Redis Cluster、Service 和 Ingress。
- 在 Sealos 桌面中通过 AI 对话获取部署指导。

## 部署指南

1. 打开 [SearXNG 模板](https://sealos.io/products/app-store/searxng)，点击 **Deploy Now**。
2. 保留自动生成的应用名称，确认资源规格后提交部署。
3. 等待 2-3 分钟让 SearXNG Pod 和 Redis Cluster 就绪，然后从 App 卡片打开公网地址。
4. 执行一次搜索，确认已启用引擎能够返回结果。
5. 编辑 ConfigMap，添加工作空间网络可达的其他引擎，然后重启 Pod。

## 许可证

SearXNG 使用 [GNU Affero General Public License v3.0](https://github.com/searxng/searxng/blob/master/LICENSE) 许可证。
