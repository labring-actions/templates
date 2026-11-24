# 在 Sealos 上部署和托管 Qdrant

Qdrant 是高性能向量数据库与相似度搜索引擎，适用于嵌入向量、推荐系统和检索增强 AI 应用。

![Qdrant 官网](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/qdrant/website-screenshot.webp)

## 关于 Qdrant 托管

本模板以单副本 StatefulSet 运行 Qdrant 官方镜像，将 1 GiB 持久卷挂载到 `/qdrant/storage`。公网 HTTPS 地址提供 REST API，集群内部可通过 6334 端口访问 gRPC API。

访问 `/dashboard` 可使用仪表盘，创建集合、查看数据点并执行相似度查询。客户端库可通过 `/collections` 等 REST 端点接入。

## 常见使用场景

- 为 RAG 和语义搜索应用存储并检索嵌入向量。
- 构建推荐系统和相似度匹配服务。
- 通过 Qdrant 仪表盘和 REST API 验证向量搜索方案。
- 为 AI Agent 和聊天机器人提供独立向量存储。
- 在扩展到生产流量前评估集合结构。

## Qdrant 托管依赖

- 具备 CPU、内存和存储配额的 Sealos 工作空间。
- 用于集合和索引的 1 GiB 持久卷。
- 用于生成写入向量的嵌入模型或服务。
- 面向不可信客户端时所需的 API Key 配置。

## 为什么在 Sealos 上部署 Qdrant？

- 一键部署即可获得公网 HTTPS REST 端点。
- 由 Kubernetes 提供健康探针、调度和 Pod 自动恢复。
- 持久化存储保留集合、负载数据和索引。
- 按量计费的资源卡适配开发环境和小型生产数据集。
- 通过 Canvas 查看 StatefulSet、Service、Ingress 和 PVC。
- 在 Sealos 桌面中通过 AI 对话了解部署情况。

## 部署指南

1. 打开 [Qdrant 模板](https://sealos.io/products/app-store/qdrant)，点击 **Deploy Now**。
2. 保留自动生成的应用名称，确认 1 GiB 存储规格后提交部署。
3. 等待 2-3 分钟让 StatefulSet 就绪，然后打开公网地址并追加 `/dashboard`。
4. 创建一个集合，写入几条测试向量，并在仪表盘中执行相似度查询。
5. 在向生产客户端开放前，在 Qdrant 配置中启用 API Key。

## 许可证

Qdrant 使用 [Apache License 2.0](https://github.com/qdrant/qdrant/blob/master/LICENSE) 许可证。
