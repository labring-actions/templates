# 在 Sealos 上部署和托管 Elasticsearch

Elasticsearch 是面向日志、指标、向量和应用数据的分布式搜索与分析引擎。此模板会在 Sealos Cloud 上部署固定 3 节点的 Elasticsearch 9.4.3 高可用集群，并提供带身份认证的 REST 网关。

![Elasticsearch 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/elasticsearch/website-screenshot.webp)

## 关于托管 Elasticsearch

Elasticsearch 通过 REST API 存储和检索结构化数据、非结构化数据与向量数据。三个 StatefulSet 副本均为可参与主节点选举的数据节点，并拥有稳定身份和独立持久卷。

公网 HTTPS 入口先经过轻量 NGINX 网关，并使用 HTTP Basic Auth 认证。ClusterIP REST Service 为网关提供稳定后端，headless service 负责节点发现和节点间 transport 通信；NetworkPolicy 将两条内部链路限制在网关和 Elasticsearch Pod 范围内。Sealos 通过 Canvas 管理 TLS 终止、域名路由、存储挂载和部署生命周期。

## 常见使用场景

- **应用搜索**：为商品目录、文档站点和内部内容构建全文搜索。
- **日志与事件分析**：索引运维事件，用于故障排查与趋势分析。
- **向量搜索**：存储 embedding，并通过 Elasticsearch API 执行相似度查询。
- **指标探索**：查询运维时序数据，为仪表盘和报表提供数据。

## Elasticsearch 托管依赖

此模板包含 Elasticsearch 官方镜像、三个持久卷、headless service、ClusterIP REST Service、带认证的 NGINX 网关、HTTPS ingress 和 App 入口。

### 部署依赖

- [Elasticsearch 文档](https://www.elastic.co/docs/solutions/search) - 官方产品文档
- [Elasticsearch REST API](https://www.elastic.co/docs/api/doc/elasticsearch) - REST API 参考
- [Elasticsearch GitHub 仓库](https://github.com/elastic/elasticsearch) - 源码仓库
- [Sealos 文档](https://sealos.io/docs) - Sealos 平台文档

### 实现细节

**架构组件：**

- **Elasticsearch StatefulSet**：三个 Elasticsearch 9.4.3 Pod，均为可参与主节点选举的数据节点，并具备稳定名称。
- **持久化存储**：每个节点分配一个 `1Gi` 持久卷，挂载到 `/usr/share/elasticsearch/data`。
- **Headless Service**：为节点发现、引导身份检查和 transport 通信提供稳定 Pod DNS。
- **ClusterIP REST Service**：为网关提供稳定内部端点，在 Pod 替换后继续指向当前后端。
- **REST 网关**：一个 NGINX Deployment，在请求转发至 Elasticsearch 前执行 HTTP Basic Auth 认证。
- **NetworkPolicy**：将 `9200` 端口限制给网关和集群 Pod，将 `9300` 端口限制给集群 Pod。
- **Ingress 与 App 入口**：通过 Sealos 托管的 HTTPS 域名支持 REST 客户端和浏览器访问。

**配置：**

- 副本数固定为 `3`。
- StatefulSet Pod 采用并行启动，使持久化节点在全部 Pod 重启后重新建立选举法定人数。
- 当 0 号节点的数据卷为空时，它会先检查其他节点的集群 UUID；仅在另外两个节点都明确报告没有持久化集群身份后设置 `cluster.initial_master_nodes`。
- `discovery.seed_hosts` 包含三个 StatefulSet Pod 地址。
- 每个节点分配 `500m` CPU limit、`2048Mi` memory limit 和 `512Mi` Elasticsearch heap。Sealos 实测显示，下一个更低内存档位在认证写入测试中达到 99.8%。
- 启动与就绪检查会等待集群健康状态达到 `yellow`；存活检查用于确认本地 HTTP 监听端口正常。
- 公网 REST 请求使用部署时填写的 `auth_username` 和 `auth_password`。
- 公网链路使用 Sealos TLS 与网关认证。内部 HTTP 与 transport 流量在 NetworkPolicy 边界内使用明文通信。

**许可证信息：**

Elasticsearch 由 Elastic 按 Elastic License 及相关许可条款提供。生产使用前请查阅官方许可信息。

## 为什么在 Sealos 上部署 Elasticsearch？

Sealos 是基于 Kubernetes 的 AI 云操作系统。此模板提供以下能力：

- **一键部署**：从应用商店创建完整的 3 节点集群和认证网关。
- **Kubernetes 基础能力**：使用 StatefulSet 稳定身份、服务发现、健康检查和持久卷。
- **托管 HTTPS 访问**：获得由 Sealos 管理的域名、TLS 终止和网关 Basic Auth。
- **Canvas 运维**：部署后通过 AI 对话或资源卡片调整资源。
- **按量使用资源**：从紧凑的高可用规格起步，随业务增长逐步扩容。

## 部署指南

1. 打开 [Elasticsearch 模板](https://sealos.io/products/app-store/elasticsearch)，点击 **Deploy Now**。
2. 在弹窗中设置 `auth_username` 和 `auth_password`，并将这两个值保存到密码管理器。
3. 等待部署完成，通常需要 2-3 分钟。随后 Sealos 会打开该部署的 Canvas。
4. 从 App 入口复制 HTTPS 地址，并检查集群健康状态：

   ```bash
   export ES_URL="https://<your-elasticsearch-domain>"
   curl --user '<auth_username>:<auth_password>' \
     "$ES_URL/_cluster/health?pretty"
   ```

## 登录和访问

此模板以 REST API 形式提供 Elasticsearch 服务。在浏览器中打开 App 入口时会出现 HTTP Basic Auth 提示框，请输入部署时配置的认证信息。

REST 客户端可以通过 `curl --user`、`Authorization: Basic ...` 请求头或 Elasticsearch SDK 的 Basic Auth 选项发送认证信息。缺少有效认证信息的请求会收到网关返回的 `401 Unauthorized`。

## 扩缩容

此模板使用三个副本维持小型高可用拓扑。调整计算资源的步骤如下：

1. 在 Canvas 中打开该部署。
2. 选择 Elasticsearch StatefulSet 资源卡片。
3. 更新 CPU 或内存，并将 heap 控制在 memory limit 的一半以内。
4. 通过对话框应用变更。

请保持副本数为 `3`，使节点发现和引导拓扑与模板配置保持一致。

## 故障排查

### REST API 返回 401

- 确认请求携带了部署时填写的 `auth_username` 和 `auth_password`。
- 使用 `curl --user` 时，请为包含 shell 特殊字符的认证信息加上引号。

### 集群健康状态持续为 yellow 或 red

- 在 Canvas 中检查 StatefulSet 和 Pod 资源卡片。
- 等待三个 Pod 全部 ready，再通过认证入口调用 `/_cluster/health?pretty`。

### 节点反复重启

- 在 Canvas 中检查 Pod 日志和内存使用情况。
- 提高 StatefulSet memory limit，并将 Elasticsearch heap 控制在该限制的 50% 以内。

### 获取帮助

- [Elasticsearch 文档](https://www.elastic.co/docs/solutions/search)
- [Elasticsearch REST API](https://www.elastic.co/docs/api/doc/elasticsearch)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Elasticsearch 指南](https://www.elastic.co/docs/solutions/search)
- [Elasticsearch API 参考](https://www.elastic.co/docs/api/doc/elasticsearch)
- [Sealos 应用商店](https://sealos.io/products/app-store)

## 许可证

此 Sealos 模板遵循仓库许可证提供。Elasticsearch 按 Elastic 许可条款分发。
