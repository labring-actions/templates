# 在 Sealos 上部署和托管 Pi-hole

Pi-hole 是自托管 DNS 黑洞服务，可为整个网络拦截广告与追踪域名，并通过 Web 仪表盘展示查询活动。本 Sealos 模板以单副本 StatefulSet 运行 Pi-hole 2026.11.0，提供持久化配置存储和公网 HTTPS 控制台。

![Pi-hole 仪表盘](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/pi-hole/website-screenshot.webp)

## 关于 Pi-hole 托管

Pi-hole 接收 DNS 查询，按拦截列表匹配域名，将允许的查询转发到上游解析器，并记录结果。Web 控制台覆盖查询日志、拦截列表、允许列表、本地 DNS 记录、上游 DNS、客户端和诊断工具。

本模板运行一个 StatefulSet，使用 `pihole/pihole:2026.11.0` 镜像并监听 `80` 端口。`admin_password` 输入通过 `FTLCONF_webserver_api_password` 设置初始 Web 管理员密码，`FTLCONF_dns_listeningMode=ALL` 允许解析器接受集群网络查询。1Gi 卷挂载到 `/etc/pihole`，保存配置、拦截列表和查询历史。

Service 与 Ingress 通过 HTTPS 在 `/admin` 发布 Web 控制台。DNS 流量使用 UDP 和 TCP 53 端口，本模板将端口 53 留给单独的 DNS Service，使控制台部署与网络级 DNS 暴露相互独立。

## 常见使用场景

- **全网络广告拦截**：通过一个 DNS 解析器保护家庭或办公网络中的全部设备。
- **查询可视化**：在仪表盘查看热门域名、客户端、查询类型和拦截请求。
- **本地 DNS**：为实验服务器、内部工具和开发主机名添加记录。
- **拦截列表测试**：在全网推广前验证新列表和允许列表条目。
- **小团队 DNS**：为团队或社区网络提供私有管理控制台。

## Pi-hole 托管依赖

模板包含 Pi-hole StatefulSet、1Gi 持久卷、Service、HTTPS Ingress 和 Sealos App 入口。Pi-hole 需要至少一个可访问的上游 DNS 解析器。客户端设备需要指向本部署的 UDP/TCP 53 Service。

### 部署依赖

- [Pi-hole 官网](https://pi-hole.net/) - 产品介绍与发布信息
- [Pi-hole 文档](https://docs.pi-hole.net/) - 安装、DNS、DHCP 和 API 指南
- [Pi-hole 仓库](https://github.com/pi-hole/pi-hole) - 源代码与 Issue
- [Pi-hole Docker 镜像](https://hub.docker.com/r/pihole/pihole) - 本模板使用的官方镜像
- [Pi-hole v6 配置](https://docs.pi-hole.net/docker/configuration/) - `FTLCONF_` 环境变量与持久化路径

## 实现细节

**架构组件：**

- **Pi-hole StatefulSet**：单副本运行 `pihole/pihole:2026.11.0`，监听 `80` 端口。
- **持久卷**：1Gi 卷挂载到 `/etc/pihole`，保存配置、拦截列表和查询历史。
- **Service**：ClusterIP 的 `80` 端口提供 Web 控制台。
- **Ingress**：Sealos 管理的 HTTPS 域名，App 入口打开 `/admin`。
- **DNS 暴露**：客户端使用该实例时，新增单独的 UDP/TCP 53 Service。

**配置：**

- **镜像**：`pihole/pihole:2026.11.0`
- **Web 端口**：`80`
- **时区**：`Asia/Shanghai`
- **管理员密码**：必填输入 `admin_password`
- **DNS 监听模式**：`ALL`
- **持久化**：1Gi ReadWriteOnce 卷，挂载到 `/etc/pihole`
- **副本数**：`1`

**资源分配：**

| 组件 | CPU 请求 | CPU 限制 | 内存请求 | 内存限制 | 存储 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Pi-hole | 10m | 100m | 12Mi | 128Mi | 1Gi |

该规格通过了冷启动、管理员登录、Query Log 导航和稳定性验证，Pod 重启次数为 0。

## 为什么在 Sealos 上部署 Pi-hole？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，将部署、网络、存储和运维统一在一个界面中。在 Sealos 上部署 Pi-hole 可以带来：

- **一键部署**：通过一个模板创建控制台、存储和 HTTPS 入口。
- **DNS 状态持久化**：在 Pod 重启后保留配置、拦截列表和查询历史。
- **Canvas 与 AI 对话**：在一个视图中查看 StatefulSet、Service、Ingress、PVC、日志和资源卡，并通过 Sealos AI 对话调整部署。
- **按量计费**：以经验证的 100m CPU 和 128Mi 内存限制运行紧凑 DNS 服务。
- **自动 HTTPS**：通过托管域名和 TLS 证书访问控制台。
- **Kubernetes 可靠性**：使用健康探针、自动恢复和声明式资源管理。

## 部署指南

1. 打开 [Pi-hole 模板](https://sealos.io/products/app-store/pi-hole)，点击 **Deploy Now**。
2. 输入管理员密码，检查自动生成的应用名称，确认 1Gi 存储规格。
3. 等待部署完成，通常需要 2-3 分钟。资源创建完成后 Sealos 会打开 Canvas。
4. 从 Canvas 或应用商店入口打开公网地址，路径指向 `/admin`。
5. 使用第 2 步的密码登录，打开 **Query Log** 确认仪表盘可读取实时数据。
6. 客户端需要解析 DNS 时，新增暴露 UDP 和 TCP 53 端口的 Service。

## 登录与账号设置

Pi-hole 使用一个 Web 管理员账号。`admin_password` 输入在部署时设置密码，登录页面位于 `/admin`，没有单独的注册流程。

使用部署表单中填写的原始密码登录。登录后可在 **Settings → DNS** 选择上游解析器，在 **Settings → All settings** 调整高级解析行为。模板未配置邮件找回，请由部署负责人妥善保存密码。

## 配置

- **上游 DNS**：在 **Settings → DNS** 配置一个或多个解析器。
- **拦截列表**：在 **Lists** 添加或替换列表，Pi-hole 会按更新计划下载。
- **本地 DNS 记录**：在 **Local DNS → DNS Records** 添加主机名。
- **客户端**：在 **Clients** 分组设备并按需应用单独规则。
- **查询历史**：保存在 `/etc/pihole` 卷，按 Pi-hole 数据库设置保留。
- **DNS 端口**：将设备指向该解析器前，先创建专用 UDP/TCP 53 Service。

## 扩缩容

模板保持单副本，因为 Pi-hole 在 ReadWriteOnce 卷上维护本地 SQLite 数据和解析器状态。查询量、大体积拦截列表或更长保留窗口需要更多资源时，提高 CPU 和内存限制。查询历史或列表需要更多空间时，从 StatefulSet 资源卡扩展 1Gi 卷。

## 故障排查

### 登录页面拒绝密码

使用部署表单中填写的原始 `admin_password`。输入在首次启动后发生变化时，可在 Pi-hole 控制台更新密码，或使用新卷重新部署。

### 设备无法通过 Pi-hole 解析 DNS

模板只发布 Web 控制台，端口 53 由单独 Service 提供。为 StatefulSet 创建 UDP/TCP 53 Service，再将客户端配置为该地址。

### 查询未被拦截

打开 **Lists** 确认拦截列表已启用并完成下载。在 **Query Log** 查看域名状态，同时确认客户端使用本 Pi-hole 实例作为解析器。

### 查询历史较大时仪表盘变慢

在 Pi-hole 设置中缩短查询保留时间，或扩展持久卷。较小历史记录可让紧凑资源规格下的仪表盘保持响应。

### 获取帮助

- [Pi-hole 文档](https://docs.pi-hole.net/)
- [Pi-hole 论坛](https://discourse.pi-hole.net/)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

Pi-hole 使用上游自定义许可证，完整条款见 [Pi-hole license](https://github.com/pi-hole/pi-hole/blob/master/LICENSE)。本 Sealos 模板遵循 templates 仓库许可证。
