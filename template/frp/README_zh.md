# 在 Sealos 上部署 frp

[frp](https://gofrp.org/zh-cn/) 是一款高性能反向代理工具，可以通过公网服务器发布位于私有网络中的服务。此模板使用官方 frps v0.70.0 镜像，包含 token 认证、受保护的监控面板、HTTP 虚拟主机路由和专用 TCP 代理端口。

![frp 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/frp/website-screenshot.webp)

## 关于 frp

frp 使用客户端与服务端架构。`frps` 在 Sealos 上运行并提供公网连接，`frpc` 在私有服务旁运行。客户端向服务端建立经过认证的出站连接，frps 再通过该连接转发公网流量。

常见场景包括：

- 从笔记本电脑或私有网络发布开发中的 Web 服务。
- 通过受控 TCP 端口访问 SSH、数据库或设备服务。
- 按域名路由多个 HTTP 服务。
- 在 frps 面板中监控客户端、代理和流量。

frps Dashboard 用于监控运行状态。代理规则由每个 frpc 配置文件管理。

## 在 Sealos 上部署 frp 的优势

- 在 Sealos 网络和 HTTPS 入口后运行官方 frps 容器。
- Dashboard、HTTP 虚拟主机和 TCP 数据面使用独立公网入口。
- 所有 frpc 连接都使用必填共享 token 认证。
- 使用已经完成真实端到端 TCP 代理验证的最低 Sealos 计算档位。

## 部署指南

1. 打开 [frp 模板](https://sealos.io/products/app-store/frp)，点击 **Deploy Now**。
2. 填写全部必填参数：
   - `dashboard_username`：Dashboard Basic Authentication 用户名。
   - `dashboard_password`：Dashboard Basic Authentication 密码。
   - `frp_auth_token`：每个 frpc 客户端使用的共享 token。
3. 开始部署，等待 frps 工作负载和初始化任务完成。
4. 打开生成的应用地址，使用 `dashboard_username` 和 `dashboard_password` 登录。

请为 Dashboard 密码和 frp token 使用独立的高强度值，并存入密码管理器。

## 公网入口

部署会提供四类入口：

| 入口 | 用途 |
| --- | --- |
| Dashboard HTTPS 地址 | 查看 frps 状态、客户端、代理和流量 |
| HTTP HTTPS 地址 | 接收使用 `customDomains` 的 HTTP 代理流量 |
| `server` 公网 TCP 端口 | frpc 连接 frps `7000` 端口的控制通道 |
| `tcp-proxy` 公网 TCP 端口 | 为一个 TCP 代理预留的远端端口 |

在 Sealos 中打开 frp 资源详情，即可查看 `server` 和 `tcp-proxy` 对应的公网主机名与 NodePort。

## 连接 frpc 客户端

从 [frp 发布页面](https://github.com/fatedier/frp/releases/tag/v0.70.0) 下载适合客户端系统的 frpc v0.70.0。

### 发布 TCP 服务

创建 `frpc.toml`：

```toml
serverAddr = "<your-public-sealos-host>"
serverPort = <server-public-port>

auth.method = "token"
auth.token = "<your-frp-auth-token>"

[[proxies]]
name = "private-service"
type = "tcp"
localIP = "127.0.0.1"
localPort = 8080
remotePort = <tcp-proxy-public-port>
```

启动客户端：

```bash
./frpc -c ./frpc.toml
```

外部用户可以连接 `<your-public-sealos-host>:<tcp-proxy-public-port>`。连接建立后，Dashboard 会显示在线客户端和代理。

### 发布 HTTP 服务

将生成的 HTTP 入口域名填入 `customDomains`：

```toml
serverAddr = "<your-public-sealos-host>"
serverPort = <server-public-port>

auth.method = "token"
auth.token = "<your-frp-auth-token>"

[[proxies]]
name = "web"
type = "http"
localIP = "127.0.0.1"
localPort = 8080
customDomains = ["<your-http-endpoint-host>"]
```

frpc 显示代理启动成功后，打开 `https://<your-http-endpoint-host>`。

## 资源基线

frps 工作负载的上限为 `100m` CPU 和 `128 MiB` 内存，请求值为 `10m` CPU 和 `12 MiB` 内存。实测使用官方 v0.70.0 frpc 建立连接、转发外部 TCP 请求、校验响应字节完整性，并保持 Pod 零重启。大量并发隧道和高流量场景需要更高资源规格。

## 安全说明

- 凭据泄露后请轮换 `frp_auth_token`，并重启 frpc 客户端。
- Dashboard 凭据和 frp 客户端 token 应分别设置。
- SSH 和数据库等敏感协议还需要在私有服务侧设置访问控制。
- 客户端跨越非受信网络时，请启用 frp 传输加密和 TLS 选项。

## 故障排查

### frpc 无法连接

检查 Sealos 中的公网 `server` 端口、`serverAddr` 主机名和共享 token。客户端与服务端应使用同一 v0.70.0 版本。

### TCP 代理保持离线

将 `remotePort` 设置为 Sealos 显示的公网 `tcp-proxy` 端口，并确认本地服务正在监听 `localIP:localPort`。

### Dashboard 显示认证提示

输入部署时设置的 `dashboard_username` 和 `dashboard_password`。认证成功后会进入监控面板。

## 相关资源

- [frp 文档](https://gofrp.org/zh-cn/docs/)
- [frp GitHub 仓库](https://github.com/fatedier/frp)
- [frp v0.70.0 发布记录](https://github.com/fatedier/frp/releases/tag/v0.70.0)

## 许可证

frp 使用 Apache License 2.0。此 Sealos 模板遵循模板仓库许可证。
