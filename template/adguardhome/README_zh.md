# 在 Sealos 上部署和托管 AdGuard Home

AdGuard Home 是网络级 DNS 服务，提供 Web 管理控制台，可拦截广告、追踪器和恶意域名。本 Sealos 模板以单副本 StatefulSet 运行 AdGuard Home 1.0.0，分别持久化配置与工作数据，并提供公网 HTTPS 控制台。

![AdGuard Home 仪表盘](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/adguardhome/website-screenshot.webp)

## 关于 AdGuard Home 托管

AdGuard Home 按拦截列表过滤 DNS 查询，将允许的请求转发到上游解析器，并通过仪表盘展示查询活动。控制台可管理过滤器、客户端、DNS 重写、上游服务器、加密设置和查询日志。

本模板运行一个 StatefulSet，使用 `adguard/adguardhome:v1.0.0` 镜像并监听 `80` 端口。容器使用显式的 `--config`、`--work-dir` 和 `--web-addr 0.0.0.0:80` 参数启动，确保设置向导和仪表盘可通过 Service 访问。两个 1Gi 卷分别持久化 `/opt/adguardhome/conf` 与 `/opt/adguardhome/work`。

Service 与 Ingress 通过 HTTPS 发布管理控制台。DNS 流量使用 UDP 和 TCP 53 端口，本模板将端口 53 留给单独的 DNS Service，使控制台管理与网络级解析器暴露相互独立。

## 常见使用场景

- **全网过滤**：为家庭或办公网络拦截广告与追踪域名。
- **过滤器开发**：在全网推广前测试拦截列表、允许列表和自定义规则。
- **DNS 可视化**：在一个仪表盘查看查询量、热门客户端和拦截域名。
- **内部 DNS 重写**：将内部服务和实验主机映射到私有地址。
- **加密上游**：将允许的查询转发到 DNS-over-HTTPS 或 DNS-over-TLS 服务。

## AdGuard Home 托管依赖

模板包含 AdGuard Home StatefulSet、两个 1Gi 卷、Service、HTTPS Ingress 和 Sealos App 入口。AdGuard Home 需要至少一个可访问的上游 DNS 解析器。

客户端设备需要指向本部署的 UDP/TCP 53 Service。管理员账号由设置向导创建，模板不预置密码。

### 部署依赖

- [AdGuard Home 官网](https://adguard.com/adguard-home/overview.html) - 产品介绍与下载
- [AdGuard Home 文档](https://adguard-dns.io/kb/adguard-home/overview/) - 设置、过滤器与 DNS 指南
- [AdGuard Home 仓库](https://github.com/AdguardTeam/AdGuardHome) - 源代码与 Issue
- [AdGuard Home Docker 镜像](https://hub.docker.com/r/adguard/adguardhome) - 本模板使用的官方镜像
- [AdGuard Home 配置](https://adguard-dns.io/kb/adguard-home/configuration/) - YAML 配置参考

## 实现细节

**架构组件：**

- **AdGuard Home StatefulSet**：单副本运行 `adguard/adguardhome:v1.0.0`，监听 `80` 端口。
- **配置卷**：1Gi 卷挂载到 `/opt/adguardhome/conf`，保存 `AdGuardHome.yaml`。
- **工作卷**：1Gi 卷挂载到 `/opt/adguardhome/work`，保存查询数据和运行文件。
- **Service**：ClusterIP 的 `80` 端口提供管理控制台。
- **Ingress**：Sealos 管理的 HTTPS 域名。
- **DNS 暴露**：客户端使用该解析器时，新增单独的 UDP/TCP 53 Service。

**配置：**

- **镜像**：`adguard/adguardhome:v1.0.0`
- **Web 监听**：`0.0.0.0:80`
- **配置路径**：`/opt/adguardhome/conf/AdGuardHome.yaml`
- **工作目录**：`/opt/adguardhome/work`
- **持久化**：2 × 1Gi ReadWriteOnce 卷
- **副本数**：`1`
- **健康检查**：对 `/` 执行 HTTP 启动、就绪和存活探针

**资源分配：**

| 组件 | CPU 请求 | CPU 限制 | 内存请求 | 内存限制 | 存储 |
| --- | ---: | ---: | ---: | ---: | ---: |
| AdGuard Home | 10m | 100m | 12Mi | 128Mi | 2Gi |

该规格通过了冷启动、首次设置、`/control/status` 检查、Pod 重启后的配置持久化和稳定性验证，Pod 重启次数为 0。

## 为什么在 Sealos 上部署 AdGuard Home？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，将部署、网络、存储和运维统一在一个界面中。在 Sealos 上部署 AdGuard Home 可以带来：

- **一键部署**：通过一个模板创建控制台、配置存储和 HTTPS 入口。
- **DNS 配置持久化**：在重启后保留过滤器、重写、客户端和查询数据。
- **Canvas 与 AI 对话**：在一个视图中查看 StatefulSet、Service、Ingress、PVC、日志和资源卡，并通过 Sealos AI 对话调整部署。
- **按量计费**：以经验证的 100m CPU 和 128Mi 内存限制运行紧凑解析器。
- **自动 HTTPS**：通过托管域名和 TLS 证书访问管理控制台。
- **Kubernetes 可靠性**：使用健康探针、自动恢复和声明式资源管理。

## 部署指南

1. 打开 [AdGuard Home 模板](https://sealos.io/products/app-store/adguardhome)，点击 **Deploy Now**。
2. 检查自动生成的应用名称，确认存储规格后开始部署。
3. 等待部署完成，通常需要 2-3 分钟。资源创建完成后 Sealos 会打开 Canvas。
4. 从 Canvas 或应用商店入口打开公网地址，首次访问会进入设置向导。
5. 创建管理员用户名和密码，Web 地址保持 `0.0.0.0:80`，DNS 监听使用容器内 53 端口。
6. 设置可访问的上游解析器并完成向导，确认 `/login.html` 能加载仪表盘。

## 登录与账号设置

AdGuard Home 通过首次设置向导创建管理员账号，模板不提供默认用户名或密码。全新卷上打开公网地址后，填写管理员用户名和密码，检查 Web 与 DNS 监听地址，并选择上游 DNS 服务。

设置完成后控制台跳转到 `/login.html`，使用向导中创建的账号登录。账号与全部设置保存在配置卷的 `/opt/adguardhome/conf/AdGuardHome.yaml`。

## 配置

- **过滤器**：在 **Filters → DNS blocklists** 添加拦截列表。
- **上游 DNS**：在 **Settings → DNS settings** 设置解析器。
- **DNS 重写**：在 **Filters → DNS rewrites** 添加内部主机名。
- **客户端**：在 **Settings → Client settings** 创建客户端专属设置。
- **查询日志**：保存在工作卷，可在 **Settings → General settings** 调整保留时间。
- **DNS 端口**：将设备指向该解析器前，新增 UDP/TCP 53 Service。
- **Web 监听**：保持 `0.0.0.0:80`，确保 Ingress 能访问控制台。

## 扩缩容

模板保持单副本，因为解析器在 ReadWriteOnce 卷上维护本地配置和查询数据。查询量、大体积过滤列表或更长保留窗口需要更多资源时，提高 CPU 和内存限制。过滤数据或查询历史增长时，从 StatefulSet 资源卡扩展配置卷或工作卷。

## 故障排查

### 没有出现设置向导

确认 Pod 已 Ready 且 Ingress 能访问控制台。配置卷中已存在 `AdGuardHome.yaml` 时，AdGuard Home 会跳过向导并显示登录页。

### 控制台出现重定向循环

确认 Web 监听地址为 `0.0.0.0:80`，且 Ingress 使用 HTTP 转发到 Service。模板已将这些值作为显式容器参数传入。

### 设备无法通过 AdGuard Home 解析 DNS

模板只发布 Web 控制台，端口 53 由单独 Service 提供。为 StatefulSet 创建 UDP/TCP 53 Service，再将客户端配置为该地址。

### 重启后配置丢失

确认 `/opt/adguardhome/conf` 和 `/opt/adguardhome/work` 都挂载了持久卷。设置向导会将账号和设置写入配置卷。

### 获取帮助

- [AdGuard Home 文档](https://adguard-dns.io/kb/adguard-home/overview/)
- [AdGuard Home Issues](https://github.com/AdguardTeam/AdGuardHome/issues)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

AdGuard Home 使用 [GNU General Public License v3.0](https://github.com/AdguardTeam/AdGuardHome/blob/master/LICENSE.txt) 许可证。本 Sealos 模板遵循 templates 仓库许可证。
