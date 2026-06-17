# 在 Sealos 上部署和托管 Loki

Loki 是 Grafana 开源的日志聚合系统，用 Prometheus 风格的标签存储和查询日志。此模板会在 Sealos Cloud 上部署一个带持久化存储和公网 HTTPS 入口的单节点 Loki 实例。

## 关于 Loki 托管

Loki 存储压缩后的日志流，并只索引元数据标签，而不是索引完整日志文本，因此适合轻量级应用和基础设施日志采集。Sealos 模板会以 StatefulSet 运行 Loki，将 `/loki` 数据持久化到 1 GiB 存储卷，并通过 `3100` 端口暴露 HTTP API。

此部署适用于开发、测试、小型可观测性栈和轻量日志采集场景。模板不包含 Grafana 或日志采集器，部署后可以自行连接 Grafana、Promtail、Grafana Alloy 或其他兼容客户端。

## 常见使用场景

- **应用日志采集**：通过 Loki push API 存储应用、Worker 和服务日志。
- **Grafana 日志检索**：将 Loki 入口添加为 Grafana 数据源，并使用 LogQL 查询日志。
- **轻量 DevOps 监控**：为开发和预发环境保留一个小型持久化日志后端。
- **排障流水线**：将 CI、Job 或批处理日志发送到可搜索的后端。

## Loki 托管依赖

Sealos 模板包含启动 Loki 所需的运行时依赖：官方 Loki 容器镜像、Kubernetes StatefulSet、ClusterIP Service、Ingress 和持久化存储。

### 部署依赖

- [Loki 文档](https://grafana.com/docs/loki/latest/) - 官方 Loki 文档
- [Loki HTTP API](https://grafana.com/docs/loki/latest/reference/loki-http-api/) - readiness、写入和查询 API 参考
- [LogQL 文档](https://grafana.com/docs/loki/latest/query/) - 查询语言参考
- [Grafana Loki GitHub](https://github.com/grafana/loki) - 源代码和版本发布

### 实现细节

**架构组件：**

此模板会部署以下资源：

- **Loki StatefulSet**：运行 `docker.io/grafana/loki:3.7.2`，使用内置本地文件系统配置。
- **持久化存储卷**：挂载 `/loki`，用于保存 chunks、索引和规则数据。
- **Service**：在集群内通过 `3100` 端口暴露 Loki。
- **Ingress 与应用入口**：提供 Loki HTTP API 的 HTTPS 访问地址。

**配置说明：**

Loki 使用默认 single-binary 本地配置启动。上游本地配置默认关闭认证，因此在发送敏感日志前，应根据你的工作区和网络策略保护入口。模板不会创建用户、密码或初始化流程。

**许可证信息：**

Loki 使用 GNU Affero General Public License v3.0 许可证。此 Sealos 模板遵循模板仓库的许可证条款。

## 为什么在 Sealos 上部署 Loki？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用部署、网络、存储和运维能力。在 Sealos 上部署 Loki，你可以获得：

- **一键部署**：从应用商店部署 Loki，无需手写 Kubernetes YAML。
- **内置持久化存储**：通过托管持久卷在重启后保留日志数据。
- **即时公网访问**：使用自动生成的 HTTPS 入口配置 API 客户端和 Grafana 数据源。
- **资源可控**：当日志量增长时，可在 Sealos Canvas 中调整 CPU、内存和存储。
- **Kubernetes 运维基础**：无需直接管理集群底层资源，也能运行在托管 Kubernetes 基础之上。

## 部署指南

1. 打开 [Loki 模板](https://sealos.io/products/app-store/loki)，点击 **Deploy Now**。
2. 保留默认参数，或在弹窗中调整生成的应用名称和访问域名。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续如需修改，可在 AI 对话框中描述需求，或点击 StatefulSet、Service、Ingress、存储等资源卡片调整配置。
4. 通过生成的 URL 访问 Loki：
   - **就绪检查**：`https://[your-loki-url]/ready`
   - **构建信息**：`https://[your-loki-url]/loki/api/v1/status/buildinfo`
   - **写入 API**：`https://[your-loki-url]/loki/api/v1/push`
   - **查询 API**：`https://[your-loki-url]/loki/api/v1/query_range`

## API 访问方式

此模板中的 Loki 不提供独立 Web UI。请使用 HTTP API，或将生成的 URL 连接到 Grafana 作为 Loki 数据源。

API 检查示例：

```bash
curl https://[your-loki-url]/ready
curl https://[your-loki-url]/loki/api/v1/status/buildinfo
```

日志写入示例：

```bash
NOW=$(date +%s)000000000
curl -X POST "https://[your-loki-url]/loki/api/v1/push" \
  -H 'Content-Type: application/json' \
  --data "{\"streams\":[{\"stream\":{\"job\":\"demo\"},\"values\":[[\"$NOW\",\"hello from Sealos Loki\"]]}]}"
```

## 配置说明

部署后，你可以通过以下方式配置 Loki：

- **AI 对话框**：描述资源或运行时配置调整，让 Sealos 应用变更。
- **资源卡片**：在 Canvas 中点击 StatefulSet、Service、Ingress 或存储资源卡片。
- **客户端配置**：将 Grafana、Promtail、Grafana Alloy 或兼容客户端指向生成的 HTTPS 入口。

## 扩缩容

此模板是面向轻量负载的单节点 Loki 部署。调整资源时：

1. 打开当前部署的 Canvas。
2. 点击 Loki StatefulSet 资源卡片。
3. 根据日志写入量调整 CPU、内存或存储。
4. 应用变更并等待 Pod 重新就绪。

如果需要高吞吐或高可用生产日志系统，请使用 Loki 分布式部署模式和对象存储架构，而不是此单节点模板。

## 故障排查

### Loki 查询没有返回日志

- 原因：Loki 中没有匹配 LogQL 查询的日志流，或查询时间范围过窄。
- 解决：先通过 `/loki/api/v1/push` 写入测试日志，再用 `/loki/api/v1/query_range` 和 `{job="demo"}` 这类标签选择器查询。

### Grafana 无法连接

- 原因：数据源 URL 配置错误，或 Loki Pod 仍在启动。
- 解决：确认 `https://[your-loki-url]/ready` 返回 `ready`，然后将生成的 HTTPS URL 填入 Grafana Loki 数据源。

### 高写入量时 Pod 重启

- 原因：默认模板资源面向轻量部署。
- 解决：在 StatefulSet 资源卡片中提高 CPU 和内存后，再重试日志写入。

## 其他资源

- [Loki 文档](https://grafana.com/docs/loki/latest/)
- [Loki HTTP API](https://grafana.com/docs/loki/latest/reference/loki-http-api/)
- [LogQL 查询参考](https://grafana.com/docs/loki/latest/query/)
- [Grafana 数据源配置](https://grafana.com/docs/grafana/latest/datasources/loki/)

## 许可证

此 Sealos 模板遵循模板仓库的许可证条款。Loki 使用 GNU Affero General Public License v3.0 许可证。
