## frp 是什么？

[frp(Fast Reverse Proxy)](https://github.com/fatedier/frp) 是一个高性能的反向代理工具，使用 Go 语言编写，能够帮助你轻松地将内网服务暴露到公网，实现安全、快速、便捷的内网穿透。它支持 TCP、UDP、HTTP、HTTPS 等多种协议，并提供丰富的功能，例如自定义域名、负载均衡、加密传输等，能够满足各种场景下的内网穿透需求。

目前 frp 在 GitHub 上已经获得了超过 83000 颗星。

![](https://s2.loli.net/2024/08/06/CVWAE9BbHxQh4af.png)

## frp 架构解析

frp 的核心思想是利用反向代理技术，将内网服务通过一个公网服务器进行转发，从而实现外部用户对内网服务的访问。架构图如下：

![](https://s2.loli.net/2024/08/06/PH6hiEWqLfCctQ8.png)

它的工作原理可以简单概括为：

1. 在拥有公网 IP 的服务器上部署 frp 服务端 (frps)。
2. 在内网服务器上部署 frp 客户端 (frpc)，并配置需要暴露的服务端口和转发规则。
3. frpc 连接到 frps，建立反向代理通道。
4. 外部用户通过访问 frps 的公网 IP 和端口，最终访问到内网服务。

## frp 的核心功能

**frp 的主要功能特性包括：**

### 多协议支持

- TCP/UDP 穿透：支持最常见的 TCP 和 UDP 协议。
- HTTP/HTTPS 穿透：轻松暴露内网的 Web 服务。
- STCP：为 TCP 连接提供额外的安全层。
- SUDP：安全的 UDP 协议支持。

### 安全特性

- TLS 加密：支持传输层安全协议，保护数据传输。
- 身份验证：提供多种身份验证方式，如 token、OIDC 等。
- 带宽限制：可以对每个代理进行带宽限制，防止资源滥用。

### 高级功能

- 负载均衡：支持多个代理的负载均衡。
- 健康检查：自动检测后端服务的健康状态。
- 热重载：支持配置热重载，无需重启服务。
- 插件系统：提供插件机制，方便功能扩展。

### 易用性

- 简洁的配置：采用 TOML 格式，配置简单直观。
- Dashboard：提供 Web 界面，方便监控和管理。
- 多平台支持：支持 Windows、Linux、MacOS 等多个平台。

### 性能优化

- 连接池：使用连接池技术，提高连接效率。
- 多路复用：支持 TCP 连接的多路复用，减少连接数。
- 压缩传输：可选择开启压缩，节省带宽。

## frp vs. 其他内网穿透解决方案

为了更直观地展示 frp 的优势，我们可以将其与市面上的其他主流内网穿透解决方案进行对比：

| 特性       | frp             | ngrok            | Cloudflare Tunnel |
| ---------- | --------------- | ---------------- | ----------------- |
| 开源       | 是              | 否               | 否                |
| 免费使用   | 是              | 有限制           | 有限制            |
| 自托管     | 支持            | 不支持           | 不支持            |
| 多协议支持 | TCP/UDP/HTTP(S) | 主要支持 HTTP(S) | HTTP(S)           |
| 配置复杂度 | 低              | 中               | 中                |
| 性能       | 高              | 中               | 高                |
| 安全特性   | 丰富            | 基本             | 丰富              |
| 社区支持   | 活跃            | 有限             | 有限              |

虽然 ngrok 在易用性方面略胜一筹，Cloudflare Tunnel 则在全球化部署上有优势，但 frp 在开源友好度、功能灵活性和成本控制上独树一帜。特别是对于希望完全控制内网穿透基础设施的团队来说，frp 提供了一个完美的平衡点。

## 部署 frp

填一下管理面板的用户名和密码：

![](https://s2.loli.net/2024/08/06/fNka7Rj3FIiU9Hv.png)

填好参数之后，点击右上角的 “部署应用” 开始部署。部署完成后，直接点击应用的 “详情” 进入该应用的详情页面。

![](https://s2.loli.net/2024/08/06/3ZPfnCsLO5YMmp6.png)

等待应用状态变成 running 之后，直接点击端口 7500 对应的外网地址便可打开 frp 的管理界面。

![](https://s2.loli.net/2024/08/06/xwlgtYG4AD2UEOM.png)

除此之外，还有另外一种打开方式，先刷新 Sealos 桌面 (也就是在 **cloud.sealos.run** 界面刷新浏览器)，然后你就会发现 Sealos 桌面多了个图标：

![](https://s2.loli.net/2024/08/06/XB74Fj6CyUv9rmb.jpg)

直接点击这个图标就可以打开 frp 的管理界面。输入之前部署时设置的用户名和密码就可以登录了。

![](https://s2.loli.net/2024/08/06/zrZ5X8APJBu7UMK.jpg)

是不是有点似曾相识？没错，很像 **Windows 的快捷方式！**

单机操作系统可以这么玩，Sealos 云操作系统当然也可以这么玩。

## frp 的使用

下面我们通过一个简单的例子来快速体验一下 frp 的使用。

设我们要将本地 Linux 机器上运行在 80 端口的 Web 服务暴露到公网。首先要在 Web 服务所在的本地机器上下载 frpc 二进制文件：

```bash
# 设置 VERSION 环境变量为 latest 版本号
VERSION=$(curl -s https://api.github.com/repos/fatedier/frp/releases/latest | grep -oE '"tag_name": "[^"]+"' | head -n1 | cut -d'"' -f4 | cut -d 'v' -f2)

# 下载最新版本 frp
wget https://github.com/fatedier/frp/releases/download/v${VERSION}/frp_${VERSION}_linux_amd64.tar.gz

# 解压
tar zxf frp_${VERSION}_linux_amd64.tar.gz
cd frp_${VERSION}_linux_amd64
```

编写客户端配置文件：

```toml
# frpc.toml
serverAddr = "frp-udkhnlcc.bja.sealos.run"
serverPort = 46451

[[proxies]]
name = "web"
type = "http"
localPort = 80
customDomains = ["frp-udkhnlcc.bja.sealos.run"]
```

+ 将 `serverAddr` 的值替换为你的 frp 服务的 80 端口对应的公网地址：

  ![](https://s2.loli.net/2024/08/06/Qakj7cm2EFgCW6p.png)

+ 将 `serverPort` 的值替换为你的 frp 服务的 7000 端口对应的外网端口。在 frp 服务详情页面点击左上角的 “管理所有资源”：

  ![](https://s2.loli.net/2024/08/06/XmBHDZwxnGQCcUr.png)

  然后将鼠标拉到最下面，即可看到 7000 端口对应的外网端口：

  ![](https://s2.loli.net/2024/08/06/zWyvsoOlZijLKHc.png)

+ 和 serverAddr 一样，将 `customDomains` 的值替换为你的 frp 服务的 80 端口对应的公网地址。

启动 frpc：

```bash
./frpc -c ./frpc.toml
```

现在让我们回到 frp 服务详情页面，点击 80 端口对应的外网地址就能打访问地机器的 Web 服务了。

![](https://s2.loli.net/2024/08/06/kmUKi9zwQIJFChS.png)

## frp 的高级用法

frp 不仅可以进行 HTTP/HTTPS 穿透，还有很多高级用法。

### TCP 服务穿透

以 SSH 服务为例，客户端配置如下：

```toml
# frpc.toml
serverAddr = "wvvirfjfkjnt.bja.sealos.run"
serverPort = 46451

[[proxies]]
name = "ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 31577
```

在 frp 服务详情页面点击左上角的 “管理所有资源”：

![](https://s2.loli.net/2024/08/06/XmBHDZwxnGQCcUr.png)

然后将鼠标拉到最下面，除了 7000 端口之外，还暴露了一个 TCP 端口，将这个端口的值作为上述 frpc 配置文件中 remotePort 的值即可。

![](https://s2.loli.net/2024/08/06/IfBWD8VAtPMjov1.png)

启动 frpc：

```bash
./frpc -c ./frpc.toml
```

现在我们到另外一台机器上就可以通过 `ssh -oPort=31577 root@wvvirfjfkjnt.bja.sealos.run` 来访问内网机器的 SSH 服务了：

![](https://images.icloudnative.io/uPic/2024-08-06-11-47-fJxm4d.png)

### 加密与压缩

frp 支持在传输过程中对 TCP 数据进行加密和压缩，以提高安全性和传输效率。还以 SSH 服务为例，直接添加两个参数 transport.useEncryption 和 transport.useCompression 就可以支持加密和压缩了。

```toml
# frpc.toml
serverAddr = "wvvirfjfkjnt.bja.sealos.run"
serverPort = 46451

[[proxies]]
name = "ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 31577
transport.useEncryption = true
transport.useCompression = true
```

### 负载均衡

假设你的本地 Web 有多个服务，分散在不同的机器上 (或者同一个机器的不同端口)，便可以通过配置 `group` 来实现多个代理的负载均衡。

```toml
# frpc.toml
serverAddr = "wvvirfjfkjnt.bja.sealos.run"
serverPort = 46451

[[proxies]]
name = "web1"
type = "http"
localIP = "127.0.0.1"
localPort = 80
customDomains = ["frp-udkhnlcc.bja.sealos.run"]
loadBalancer.group = "web"
loadBalancer.groupKey = "123"

[[proxies]]
name = "web2"
type = "http"
localIP = "x.x.x.x"
localPort = 80
customDomains = ["frp-udkhnlcc.bja.sealos.run"]
loadBalancer.group = "web"
loadBalancer.groupKey = "123"
```

当然，除了 http 之外，frp 也支持 tcp 和 tcpmux 的负载均衡。

## frp 更多高级特性

frp 还有更多强大的特性，如：

- 支持 TCP 多路复用
- 支持 KCP 协议
- 支持通过代理连接 frps
- 支持 P2P 穿透
- 支持 HTTP 请求的 URL 路由
- 支持根据请求的 Hostname 进行路由
- 支持通过密码保护你的 web 服务
- 支持 SSH 隧道网关
- ...

限于篇幅，这里就不一一介绍了。感兴趣的同学可以查看 [frp 的官方文档](https://github.com/fatedier/frp)了解更多细节。

## 总结

frp 作为一款轻量级的内网穿透工具，具有以下优势：

1. 使用简单：只需简单配置，即可快速实现内网穿透；
2. 功能强大：支持多种协议、加密压缩、负载均衡等高级特性；
3. 性能出色：Go 语言开发，资源占用少，性能卓越；
4. 可扩展性强：插件机制使其易于扩展；
5. 活跃度高：社区活跃，持续更新维护。

无论是个人开发测试，还是小型团队内部使用，frp 都是一个非常好的选择。大家可以尝试使用一下，相信会给你的开发工作带来很大的便利。