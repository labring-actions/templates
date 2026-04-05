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


## frp 的使用

下面给出一个“部署完马上可用”的最短路径。假设你要把本地机器上的 `127.0.0.1:80` 暴露到公网。

### 1. 先拿到 3 个关键参数

- `管理面板地址`：应用卡片里的访问地址（对应模板里的管理 Ingress，端口 7500）。
- `serverAddr`：frp 的 HTTP 入口域名（对应模板里的 `app_host_http`）。
- `serverPort`：frp 服务端监听端口（7000）对应的外网端口，来自 `xxx-nodeport` Service 的 `server` 端口。

如果你习惯用 kubectl，可以这样查：

```bash
# 1) HTTP 入口域名（serverAddr）
kubectl -n <namespace> get ingress <app_name1> -o jsonpath='{.spec.rules[0].host}'; echo

# 2) frps 的 serverPort（7000 对应的 nodePort）
kubectl -n <namespace> get svc <app_name>-nodeport -o jsonpath='{.spec.ports[?(@.name=="server")].nodePort}'; echo
```

### 2. 在本地机器下载 frpc

```bash
# 设置 VERSION 环境变量为 latest 版本号
VERSION=$(curl -s https://api.github.com/repos/fatedier/frp/releases/latest | grep -oE '"tag_name": "[^"]+"' | head -n1 | cut -d'"' -f4 | cut -d 'v' -f2)

# 下载最新版本 frp
wget https://github.com/fatedier/frp/releases/download/v${VERSION}/frp_${VERSION}_linux_amd64.tar.gz

# 解压
tar zxf frp_${VERSION}_linux_amd64.tar.gz
cd frp_${VERSION}_linux_amd64
```

### 3. 编写客户端配置 `frpc.toml`

```toml
# frpc.toml
serverAddr = "你的-http-入口域名.sealos.run"
serverPort = 46451 # 替换为你的 7000 对应外网端口

[[proxies]]
name = "local-web"
type = "http"
localIP = "127.0.0.1"
localPort = 80
customDomains = ["你的-http-入口域名.sealos.run"]
```

### 4. 启动 frpc

```bash
./frpc -c ./frpc.toml
```

### 5. 访问与验证

- 打开管理面板：`https://<管理面板地址>`，使用部署时填写的 `ADMIN_USER` / `ADMIN_PASSWORD` 登录。
- 打开业务地址：`https://<serverAddr>`，如果本地 `127.0.0.1:80` 正常，就能看到你的本地服务。

### 本地 K8s（无 Sealos 域名）怎么用？

如果你是在本地 Kubernetes（没有自动公网域名）部署 frps，也可以使用：

- `serverAddr` 填任意可达 Node IP
- `serverPort` 填 7000 对应的 NodePort

这种场景推荐优先用 `tcp` 代理（不依赖 `customDomains`），示例：

```toml
serverAddr = "你的NodeIP"
serverPort = 30070

[[proxies]]
name = "local-ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 6000
```

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
