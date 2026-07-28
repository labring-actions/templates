# 在 Sealos 上部署和托管 changedetection.io

changedetection.io 是一款开源监控服务，可持续检查网页、JSON 接口与 PDF 文档。此模板会在 Sealos Cloud 上部署 changedetection.io 0.55.8，并配置持久化存储、公网 HTTPS 入口和健康检查。

![changedetection.io 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/changedetection/website-screenshot.webp)

## changedetection.io 托管说明

changedetection.io 会按计划检查目标、保存快照、突出显示内容差异，并通过支持的集成发送通知。可视化选择器可以聚焦页面中的关键元素，筛选器则可以减少时间戳、计数器等频繁变化内容带来的干扰。

Sealos 模板会创建单副本 changedetection.io StatefulSet、挂载到 `/datastore` 的 1 GiB 持久化数据卷、5000 端口 Service、公网 HTTPS Ingress，以及启动、就绪和存活探针。应用设置、监控项、快照与历史记录都会保存在持久化数据卷中。

## 常见使用场景

- **网站变更提醒**：监控商品页、政策页、版本说明和技术文档。
- **价格与库存跟踪**：关注页面中的商品信息，并在内容变化时接收通知。
- **API 与数据监控**：检查 JSON 接口和结构化数据中的关键差异。
- **内容审核流程**：保留快照历史，并通过管理面板查看变更。

## 托管 changedetection.io 所需依赖

模板包含应用容器、持久化存储、Kubernetes 网络、健康检查和 Sealos 应用入口。

### 部署依赖

- [changedetection.io 文档](https://github.com/dgtlmoon/changedetection.io/wiki) - 配置与使用指南
- [changedetection.io 源码](https://github.com/dgtlmoon/changedetection.io) - 源代码、版本发布和问题追踪
- [通知 URL](https://github.com/dgtlmoon/changedetection.io/wiki/Notification-configuration-notes) - 通知服务配置说明

### 实现细节

**架构组件：**

- **changedetection.io**：单副本 StatefulSet，通过 5000 端口提供管理面板并执行定时检查。
- **持久化存储**：挂载到 `/datastore` 的 1 GiB 数据卷。
- **公网入口**：由 Sealos 管理的 HTTPS Ingress，已经配置较长的请求与响应超时时间。
- **健康检查**：Kubernetes 探针通过 `/worker-health` 同时检查 Web 进程和抓取工作线程。

`BASE_URL` 使用 Sealos 生成的 HTTPS 地址，`FETCH_WORKERS` 使用部署输入值，`HIDE_REFERER` 可以在 changedetection.io 抓取监控目标时保护管理面板地址。

changedetection.io 使用 Apache License 2.0 许可证。

## 为什么在 Sealos 上部署 changedetection.io？

- **一键部署**：通过一个模板创建应用、存储、网络和健康检查。
- **监控历史持久保存**：应用重启后，监控项、设置、快照和历史记录仍然保留。
- **自动配置 HTTPS**：通过 Sealos 获得公网域名和 TLS 证书。
- **Kubernetes 运维能力**：在 Sealos Canvas 中查看日志、存储、网络设置和资源用量。
- **经过验证的起步资源**：从实测可用的低负载配置开始，并随监控数量和检查频率增长逐步扩容。

## 部署指南

1. 打开 [changedetection.io 模板](https://sealos.io/products/app-store/changedetection)，点击 **Deploy Now**。
2. 小型个人部署可以将 **Fetch workers** 保持为 `10`。极小负载可以选择更低数值，更多并发检查可以选择更高数值。
3. 点击 **Deploy**，等待 StatefulSet 进入 Ready 状态。
4. 打开 Sealos 中显示的 changedetection.io 应用入口。

## 访问与密码保护

全新部署会直接打开管理面板。changedetection.io 提供可选的共享管理密码：

1. 打开 **Settings**。
2. 在常规应用设置中填写密码并保存。
3. 后续访问会打开 `/login`，输入同一密码即可进入管理面板。

请妥善保存此密码。所有管理面板用户都使用这一个共享密码登录。

## 添加第一个监控项

1. 在 URL 输入框中填写公网网页或 JSON 接口。
2. 选择网页处理器或库存处理器。
3. 点击 **Watch**。
4. 使用 **Recheck** 立即执行一次检查。
5. 打开 **Edit** 配置筛选规则、检查频率和通知方式。

## 配置

| 名称 | 默认值 | 必填 | 说明 |
|------|--------|------|------|
| `fetch_workers` | `10` | 否 | changedetection.io 可以并发处理的检查数量。 |

经过测试的起步配置使用 `100m` CPU 上限和 `128Mi` 内存上限。管理面板接近内存上限时先增加内存；需要更高检查并发时，再增加 CPU 和 `fetch_workers`。

## 持久化与扩缩容

`/datastore` 数据卷包含应用配置和监控历史。迁移或重大升级前，请备份持久化数据卷。

StatefulSet 保持单副本运行，以匹配共享一个持久化数据卷的任务调度器和文件数据存储。提高吞吐量时，可以增加 CPU、内存和 `fetch_workers`，也可以参考上游文档规划更复杂的分布式部署。

## 故障排查

### 管理面板无法访问

等待 StatefulSet 进入 Ready 状态，然后确认 Service 已生成可用端点。在 Sealos Canvas 中查看 Pod 日志和 `/worker-health` 探针状态。

### 监控项持续显示错误

确认应用 Pod 可以访问目标地址，并检查目标认证、TLS、速率限制、反爬策略和抓取方式。

### 检查速度变慢

在 Sealos 中查看 CPU 和内存用量。内存接近 `128Mi` 时增加内存，再配合增加 CPU 与 `fetch_workers` 来提升并发能力。

### 获取帮助

- [changedetection.io Issues](https://github.com/dgtlmoon/changedetection.io/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

此 Sealos 模板遵循模板仓库的许可证条款。changedetection.io 使用 [Apache License 2.0](https://github.com/dgtlmoon/changedetection.io/blob/0.55.8/LICENSE)。
