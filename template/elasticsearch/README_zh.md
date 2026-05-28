# 在 Sealos 上部署和托管 Elasticsearch

Elasticsearch 是一个面向日志、指标、向量和应用数据的分布式搜索与分析引擎。此模板会在 Sealos Cloud 上将 Elasticsearch 部署为固定 3 节点高可用集群。

![Elasticsearch 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/elasticsearch/website-screenshot.webp)

## 关于托管 Elasticsearch

Elasticsearch 通过 REST API 存储和搜索结构化、非结构化以及向量数据。此 Sealos 模板使用三个 StatefulSet 副本运行 Elasticsearch，使集群可以选举主节点，并在单个节点重启时继续提供查询服务。

模板会创建用于稳定节点发现的 headless service、每个节点独立的数据持久卷、用于 REST API 访问的 HTTPS ingress，以及 Kubernetes 健康检查。部署完成后，Sealos 会在 Canvas 中管理域名路由、TLS 终止、持久化存储挂载和应用生命周期。

此模板默认关闭 Elasticsearch 内置安全功能，以避免在 3 节点启动时额外生成共享 transport TLS 证书。请在可信网络中使用；如果用于生产公网访问，应在公共入口前增加带认证的网关。

## 常见使用场景

- **应用搜索**：为商品目录、文档站点和内部内容提供快速全文搜索。
- **日志与事件分析**：索引运维日志和事件，用于排障与趋势分析。
- **向量搜索原型验证**：通过 Elasticsearch API 存储 embedding 并测试相似度搜索。
- **指标探索**：查询类似时间序列的运维数据，用于仪表盘和报表。

## Elasticsearch 托管依赖

此 Sealos 模板包含自包含 Elasticsearch 部署所需的运行组件：官方 Elasticsearch 容器镜像、StatefulSet、持久卷声明、headless service、ingress 和 App 入口。

### 部署依赖

- [Elasticsearch 文档](https://www.elastic.co/docs/solutions/search) - 官方 Elasticsearch 文档
- [Elasticsearch REST API](https://www.elastic.co/docs/api/doc/elasticsearch) - API 参考
- [Elasticsearch GitHub 仓库](https://github.com/elastic/elasticsearch) - 源码仓库
- [Sealos 文档](https://sealos.run/docs) - Sealos 平台文档

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **Elasticsearch StatefulSet**：三个 Elasticsearch 9.4.1 Pod，具备稳定名称和持久化数据目录。
- **Headless Service**：为节点发现和节点间 transport 通信提供稳定 DNS 记录。
- **Ingress**：通过 Sealos 托管域名以 HTTPS 暴露 REST API。
- **App Link**：将部署后的访问入口添加到 Sealos 应用列表。

**配置：**

- `replicas` 固定为 `3`，用于高可用部署。
- `cluster.initial_master_nodes` 指向三个 StatefulSet Pod 名称。
- `discovery.seed_hosts` 使用三个 Pod 的 headless service DNS 名称。
- 每个节点分配 `500m` CPU limit、`1024Mi` memory limit、`50m` CPU request、`102Mi` memory request 和 `512Mi` Elasticsearch heap。
- 每个节点都有 `1Gi` 持久卷，挂载到 `/usr/share/elasticsearch/data`。
- 默认关闭 Elasticsearch security；部署后不需要登录。

**许可证信息：**

Elasticsearch 由 Elastic 按 Elastic License 及相关许可条款提供。生产使用前请查阅 Elastic 官方许可说明。

## 为什么在 Sealos 上部署 Elasticsearch？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一覆盖从云端 IDE 开发到生产部署和管理的完整应用生命周期。它适合运行搜索服务、AI 应用、SaaS 平台和微服务架构。在 Sealos 上部署 Elasticsearch 后，你可以获得：

- **一键部署**：直接从应用商店部署 Elasticsearch，无需手写 Kubernetes YAML。
- **Kubernetes 基础能力**：基于 Kubernetes 运行，获得 StatefulSet 调度和服务发现能力。
- **易于定制**：通过 Canvas、AI 对话或资源卡片调整资源和运行参数。
- **内置持久化存储**：通过每个节点独立的持久卷保存搜索数据，Pod 重启后数据仍可保留。
- **即时公网访问**：获得带 Sealos 托管域名和 TLS 终止的 HTTPS 入口。
- **按量使用资源**：从紧凑的 HA 资源规格开始，根据业务增长再调整资源。

在 Sealos 上部署 Elasticsearch，可以把精力放在搜索能力本身，而不是集群基础设施维护上。

## 部署指南

1. 打开 [Elasticsearch 模板](https://sealos.io/products/app-store/elasticsearch)，点击 **Deploy Now**。
2. 在弹窗中检查生成的应用名称和访问域名。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会进入 Canvas。后续如需调整，可以在 AI 对话框描述需求，或点击对应资源卡片修改配置。
4. 通过系统提供的 URL 访问 Elasticsearch：
   - **REST API**：`https://<your-elasticsearch-domain>`
   - **健康检查**：`https://<your-elasticsearch-domain>/_cluster/health?pretty`

## 登录和访问

此模板不部署 Web UI，也不需要注册或登录。Elasticsearch 会作为 REST API 服务暴露。

由于此 HA 模板默认关闭 Elasticsearch 内置安全功能，可信环境中的客户端可以直接调用 API。如果用于生产环境或公网访问，请先在网关、VPN、私有网络边界或专用安全层增加认证，再向用户暴露入口。

## 扩缩容

此模板刻意固定为 3 个副本，用于提供小型高可用集群。部署后如需调整资源：

1. 打开该部署的 Canvas。
2. 点击 Elasticsearch StatefulSet 资源卡片。
3. 根据工作负载调整 CPU、内存或存储。
4. 通过对话框应用变更。

除非同步更新 Elasticsearch 节点发现和 master 节点配置，否则请保持副本数为 `3`。

## 故障排查

### 集群健康状态为 yellow 或 red

- 原因：Pod 可能仍在启动，或某个节点尚未加入集群。
- 解决方案：在 Canvas 中检查 StatefulSet 和 Pod 资源卡片。等待三个 Pod 全部 ready 后，再访问 `/_cluster/health?pretty` 检查状态。

### API 端点无需密码即可访问

- 原因：此 HA 模板默认关闭 Elasticsearch 内置安全功能。
- 解决方案：仅在可信环境中使用该入口；生产公网访问前，请增加带认证的网关。

### 节点反复重启

- 原因：当前索引或查询负载可能需要更多内存。
- 解决方案：在 Canvas 的 StatefulSet 资源卡片中提高内存 limit，并按比例调整 Elasticsearch heap。

### 获取帮助

- [Elasticsearch 文档](https://www.elastic.co/docs/solutions/search)
- [Elasticsearch REST API](https://www.elastic.co/docs/api/doc/elasticsearch)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Elasticsearch 指南](https://www.elastic.co/docs/solutions/search)
- [Elasticsearch API 参考](https://www.elastic.co/docs/api/doc/elasticsearch)
- [Sealos 应用商店](https://sealos.run/products/app-store)

## 许可证

此 Sealos 模板遵循仓库许可证提供。Elasticsearch 本身按 Elastic 许可条款分发。
