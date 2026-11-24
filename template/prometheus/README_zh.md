# 在 Sealos 上部署和托管 Prometheus

Prometheus 是开源监控系统与时序数据库，用于指标采集、PromQL 查询、告警和云原生可观测性。本 Sealos 模板以单副本 StatefulSet 运行 Prometheus 3.16.0，提供持久化存储和公网 HTTPS 入口。

![Prometheus 界面](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/prometheus/website-screenshot.webp)

## 关于 Prometheus 托管

Prometheus 按计划抓取 HTTP 指标端点，将样本写入本地时序数据库，并执行 PromQL 查询与告警规则。Web UI 提供查询控制台、图表、抓取目标状态、告警规则和运行时配置。

本模板运行一个 StatefulSet，使用 `prom/prometheus:v3.16.0` 镜像并监听 `9090` 端口。1Gi 持久卷挂载到 `/prometheus`，保存 TSDB、WAL 和压缩数据。容器以 UID/GID `65534` 运行，使用非 root 安全上下文，并保留可写根文件系统以写入运行文件。

Prometheus 启动时使用镜像内置配置，并通过命令行限制保留窗口：24 小时或 800MB，以先达到的限制为准。Service 将 `80` 端口映射到 `9090`，Sealos Ingress 通过 HTTPS 发布 UI。模板未提供认证层；生产环境可保持 URL 私密，或在前面增加认证代理。

## 常见使用场景

- **Kubernetes 监控**：抓取 kube-state-metrics、node-exporter 和应用 `/metrics` 端点。
- **应用可观测性**：采集请求速率、延迟、错误数、队列深度和自定义业务指标。
- **告警规则验证**：在接入生产 Alertmanager 前编写和测试 PromQL 告警规则。
- **仪表盘开发**：为 Grafana 提供专用 Prometheus 数据源并验证查询。
- **短期指标保留**：为开发、预发或边缘环境保留紧凑的本地 TSDB。

## Prometheus 托管依赖

模板包含 Prometheus StatefulSet、1Gi 持久卷、Service、HTTPS Ingress 和 Sealos App 入口。Prometheus 自身不需要外部数据库或缓存。

抓取目标需要能从 Pod 网络访问。常见目标包括 node-exporter、kube-state-metrics、应用 `/metrics` 端点和 Prometheus 自抓取任务。需要发送告警时，再单独部署 Alertmanager。

### 部署依赖

- [Prometheus 文档](https://prometheus.io/docs/) - 概念、配置与 PromQL 参考
- [Prometheus 仓库](https://github.com/prometheus/prometheus) - 源代码、发布版本与 Issue
- [Prometheus 容器镜像](https://hub.docker.com/r/prom/prometheus) - 本模板使用的官方镜像
- [配置参考](https://prometheus.io/docs/prometheus/latest/configuration/configuration/) - 抓取任务、规则文件与服务发现
- [PromQL 基础](https://prometheus.io/docs/prometheus/latest/querying/basics/) - 查询语法与函数

## 实现细节

**架构组件：**

- **Prometheus StatefulSet**：单副本运行 `prom/prometheus:v3.16.0`，监听 `9090` 端口。
- **持久卷**：1Gi 卷挂载到 `/prometheus`，保存 TSDB、WAL 和压缩数据。
- **Service**：ClusterIP 的 `80` 端口转发到 Prometheus UI。
- **Ingress**：Sealos 管理的 HTTPS 域名，提供 Web UI 和 API。
- **命令行保留策略**：`--storage.tsdb.retention.time=1d` 和 `--storage.tsdb.retention.size=800MB`。

**配置：**

- **镜像**：`prom/prometheus:v3.16.0`
- **配置文件**：`/etc/prometheus/prometheus.yml`
- **存储路径**：`/prometheus`
- **保留策略**：1 天或 800MB
- **副本数**：`1`
- **安全上下文**：UID/GID `65534`，非 root，移除全部 capabilities
- **持久化**：1Gi ReadWriteOnce 卷

**资源分配：**

| 组件 | CPU 请求 | CPU 限制 | 内存请求 | 内存限制 | 存储 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Prometheus | 10m | 100m | 12Mi | 128Mi | 1Gi |

该规格通过了冷启动、`/-/ready` 检查、PromQL 查询和稳定性验证，Pod 重启次数为 0。

## 为什么在 Sealos 上部署 Prometheus？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，将部署、网络、存储和运维统一在一个界面中。在 Sealos 上部署 Prometheus 可以带来：

- **一键部署**：通过一个模板创建 Prometheus、持久存储和公网 HTTPS 入口。
- **指标持久化**：通过专用卷在 Pod 重启和重新调度后保留 TSDB。
- **Canvas 与 AI 对话**：在一个视图中查看 StatefulSet、Service、Ingress、PVC、日志和资源卡，并通过 Sealos AI 对话调整部署。
- **按量计费**：从紧凑规格起步，抓取量和时间序列增长后再提高限制。
- **Kubernetes 基础**：使用托管调度、健康探针、服务发现和声明式资源。
- **便捷查询**：通过托管域名在任意浏览器中打开 PromQL 控制台。

## 部署指南

1. 打开 [Prometheus 模板](https://sealos.io/products/app-store/prometheus)，点击 **Deploy Now**。
2. 检查自动生成的应用名称和域名，确认 1Gi 存储规格后开始部署。
3. 等待部署完成，通常需要 2-3 分钟。资源创建完成后 Sealos 会打开 Canvas。
4. 打开公网地址，在查询控制台执行 `up`，切换到 **Graph** 标签页确认查询链路。
5. 打开 **Status → Targets** 查看当前抓取任务，再通过 Prometheus ConfigMap 添加自有任务。
6. 打开 Canvas 查看 StatefulSet、Service、Ingress、PVC 和实时日志。

## 配置

通过创建包含 `prometheus.yml` 的 ConfigMap、挂载到 `/etc/prometheus/prometheus.yml` 并重启 Pod 来添加抓取目标。最小任务示例如下：

```yaml
scrape_configs:
  - job_name: my-app
    metrics_path: /metrics
    static_configs:
      - targets: ["my-app.namespace.svc.cluster.local:8080"]
```

需要 Kubernetes 服务发现时，添加 `kubernetes_sd_configs` 配置及相应 RBAC 权限。模板保持 `automountServiceAccountToken: false`；服务发现需要专用 ServiceAccount 并授予 list 与 watch 权限。

保留策略由 StatefulSet 启动参数控制。需要更长历史时，可提高时间或容量限制，并在显著增加保留量前扩展 PVC。

## 扩缩容

Prometheus 以单副本 StatefulSet 运行，因为本地 TSDB 绑定单个写入者。时间序列数量、抓取目标或 PromQL 负载增加时，提高 CPU 和内存限制。保留策略和序列数量需要更多磁盘时，扩展 1Gi 卷。需要横向扩展时，可运行多个 Prometheus 分片并拆分抓取目标，或通过 remote write 写入长期存储。

## 故障排查

### Targets 页面为空

Prometheus 需要 `prometheus.yml` 中的抓取任务。通过 ConfigMap 添加任务、挂载到 Pod 并重启 StatefulSet，同时确认目标主机名可从 Prometheus 所在命名空间解析。

### 目标状态为 DOWN

在 **Status → Targets** 查看目标错误信息。常见原因包括网络策略、端口错误、`/metrics` 路径缺失，或 Prometheus 不信任目标 TLS 证书。

### Pod 因磁盘压力重启

TSDB 卷容量为 1Gi，保留上限为 800MB。检查 PVC 使用量，降低保留策略，或从 StatefulSet 资源卡扩展卷。

### 查询超时

高基数查询和大时间范围需要更多 CPU 与内存。缩小时间范围、减少序列数量，或提高容器限制。

### 获取帮助

- [Prometheus 文档](https://prometheus.io/docs/)
- [Prometheus Issues](https://github.com/prometheus/prometheus/issues)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

Prometheus 使用 [Apache License 2.0](https://github.com/prometheus/prometheus/blob/main/LICENSE) 许可证。本 Sealos 模板遵循 templates 仓库许可证。
