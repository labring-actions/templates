# 在 Sealos 上部署和托管 frp

frp 是一个高性能反向代理，可将 NAT 或防火墙后的本地服务暴露到公网。本模板在 Sealos Cloud 上部署 frp 服务端 (`frps`)，并提供 Web Dashboard、HTTP 虚拟主机入口和公网 TCP 端口。

![frp 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/frp/website-screenshot.webp)

## 关于 frp 托管

frp 通过公网服务端和本地客户端建立反向代理隧道。Sealos 模板运行公网 `frps` 服务，通过 HTTPS Ingress 暴露内置 Dashboard，并保留 TCP NodePort 供 frpc 连接和 TCP 代理流量使用。

部署会自动为 Dashboard 和 HTTP 虚拟主机域名配置 SSL 证书。模板也会创建 NodePort Service，因为 frp 除了 HTTP Dashboard 之外，还需要公网 TCP 端口承载 frpc 服务端口和用户定义的 TCP remote port。

## 常见使用场景

- **暴露本地 Web 服务**：通过 frp HTTP 虚拟主机域名发布本地 HTTP 服务。
- **访问私有机器 SSH**：通过公网 frp 服务端代理私有网络中的 SSH 流量。
- **自托管隧道服务**：运行自己的内网穿透基础设施。
- **协议测试**：在开发或实验环境中验证 TCP 与 HTTP 代理行为。

## frp 托管依赖

Sealos 模板包含 frp 服务端运行所需的全部组件。该模板不会创建数据库、对象存储桶或持久化卷。

### 部署依赖

- [frp 官方文档](https://gofrp.org/en/docs/) - frp 文档
- [服务端配置](https://gofrp.org/en/docs/reference/server-configures/) - frps 配置参考
- [Web Interface](https://gofrp.org/en/docs/features/common/ui/) - Dashboard 配置
- [GitHub 仓库](https://github.com/fatedier/frp) - 源码和版本发布

## 实现细节

**架构组件：**

本模板部署以下资源：

- **frps Deployment**：运行 `fatedier/frps:v0.69.1`，并挂载 `frps.toml` 配置。
- **ConfigMap**：保存 frp 服务端配置，包括来自 `ADMIN_USER` 和 `ADMIN_PASSWORD` 的 Dashboard 登录凭据。
- **NodePort Service**：暴露 Dashboard、HTTP 虚拟主机、frpc 服务端口和 TCP 代理端口。
- **Ingress**：将 Dashboard 域名转发到 `7500` 端口，将 HTTP 虚拟主机域名转发到 `80` 端口。
- **App Link**：从 Sealos 桌面打开 frp Dashboard。

**配置：**

- `bindPort = 7000` 是 frpc 服务端口。
- `vhostHTTPPort = 80` 处理 HTTP 代理流量。
- `webServer.port = 7500` 提供 Dashboard。
- `ADMIN_USER` 和 `ADMIN_PASSWORD` 是 Dashboard 登录凭据。

**许可证信息：**

frp 使用 Apache License 2.0。本 Sealos 模板遵循 frp 项目文档中的部署假设。

## 为什么在 Sealos 上部署 frp？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一了应用部署、公网访问和资源管理。在 Sealos 上部署 frp 可以获得：

- **一键部署**：打开模板页，配置凭据，然后部署，无需手写 Kubernetes YAML。
- **即时公网访问**：Sealos 为 Dashboard 和 HTTP 虚拟主机入口提供 HTTPS 域名。
- **公网 TCP 访问**：NodePort Service 暴露 frpc 服务端口和 TCP 代理端口。
- **资源高效**：模板使用轻量资源规格运行 frp，并适配按量计费。
- **便捷运维**：部署后可通过 Canvas、AI 对话和资源卡片检查或调整资源。

## 部署指南

1. 打开 [frp 模板](https://sealos.io/products/app-store/frp)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - `ADMIN_USER`：Dashboard 用户名。
   - `ADMIN_PASSWORD`：Dashboard 密码。
3. 等待部署完成，通常需要 2-3 分钟。部署后会进入 Canvas。后续变更可以在对话框中描述需求让 AI 应用，也可以点击相关资源卡片修改配置。
4. 访问 frp 服务：
   - **Dashboard**：打开 Sealos 应用入口，使用 `ADMIN_USER` 和 `ADMIN_PASSWORD` 登录。
   - **HTTP 虚拟主机**：将 HTTP Ingress 域名作为 frpc HTTP 代理配置中的 `customDomains`。
   - **frpc 服务端**：在 Service 详情中，将 `server` 端口对应的 NodePort 作为 `serverPort`。
   - **TCP 代理**：在 Service 详情中，将 `tcp-proxy` 端口对应的 NodePort 作为 `remotePort`。

## frpc 配置示例

本地 `8080` 端口 HTTP 服务示例：

```toml
serverAddr = "<your-frp-node-address-or-domain>"
serverPort = <server-node-port>

[[proxies]]
name = "web"
type = "http"
localPort = 8080
customDomains = ["<your-http-virtual-host-domain>"]
```

SSH 访问示例：

```toml
serverAddr = "<your-frp-node-address-or-domain>"
serverPort = <server-node-port>

[[proxies]]
name = "ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = <tcp-proxy-node-port>
```

## 配置管理

部署后可以通过以下方式管理 frp：

- **Dashboard**：打开 Sealos 应用入口，使用配置的凭据登录。
- **Canvas AI 对话**：描述资源或配置变更，让 AI 应用更新。
- **资源卡片**：打开 Deployment、Service、Ingress 或 ConfigMap 卡片检查生成的资源。

## 故障排查

### Dashboard 登录失败

- 原因：输入的用户名或密码与 `ADMIN_USER` 或 `ADMIN_PASSWORD` 不一致。
- 解决方案：检查模板输入值，或更新 ConfigMap 后重启 Deployment。

### frpc 无法连接

- 原因：frpc 的 `serverPort` 与 Service 中 `server` 端口对应的 NodePort 不一致。
- 解决方案：打开 Service 资源详情，复制 `server` 当前的 NodePort。

### TCP 代理无法打开

- 原因：frpc 的 `remotePort` 与 Service 中 `tcp-proxy` 端口对应的 NodePort 不一致。
- 解决方案：打开 Service 资源详情，复制 `tcp-proxy` 当前的 NodePort。

## 更多资源

- [frp 文档](https://gofrp.org/en/docs/)
- [frp Web Interface](https://gofrp.org/en/docs/features/common/ui/)
- [frp Releases](https://github.com/fatedier/frp/releases)
- [Sealos 应用商店](https://sealos.io/products/app-store)

## License

本 Sealos 模板遵循仓库许可证。frp 本身使用 Apache License 2.0。
