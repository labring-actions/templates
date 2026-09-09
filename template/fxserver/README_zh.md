# 在 Sealos 上部署和托管 FXServer

FXServer 用于运行 FiveM 多人游戏服务器，并内置 txAdmin 管理界面。此模板在 Sealos 上部署一个服务器实例，配备持久化存储、HTTPS 管理地址和公网 TCP/UDP 游戏端口。

![Grand Theft Auto V 游戏内驾驶画面](./website-screenshot.webp)

游戏素材：Rockstar Games 在 [Steam](https://store.steampowered.com/app/271590/Grand_Theft_Auto_V_Legacy/) 发布的 Grand Theft Auto V 游戏 logo 与游戏内截图，用于展示 FiveM 所基于的游戏；服务器具体内容取决于安装的配置方案。

## 关于 FXServer 托管

容器启动后会进入 txAdmin，由它引导你创建管理员账号、安装服务器配方并填写 Cfx.re 服务器许可密钥。管理面板提供服务器设置、实时控制台、玩家管理和定时重启等功能。

Sealos 会创建一个 StatefulSet，并将 1Gi 持久卷挂载到 `/txdata`。账号设置、玩家数据、日志以及安装在此目录中的服务器配方会在 Pod 重建后保留。游戏程序由固定版本的容器镜像提供。每个独立游戏服务器使用一个副本。

### 架构组件

- **FXServer 和 txAdmin：** 共用一个容器，采用上游 `35245` 构建版本及已核验的镜像摘要。
- **持久化存储：** 为 `/txdata` 提供 1Gi 存储；请将配方和资源安装在此目录中。
- **管理入口：** HTTPS Ingress 通过应用的 ClusterIP Service 将请求转发到 txAdmin 的 `40120` 端口。
- **游戏入口：** 独立的 `<app-name>-nodeport` Service 将 TCP 和 UDP `30120` 映射到同一个公网游戏端口。

所选原版服务器方案使用本地存储。需要数据库的框架配方应按其文档另外配置依赖。

## 常见使用场景

- **私人联机：** 为小团体运行 FiveM 服务器，并设置自己的游戏规则。
- **资源开发：** 在持久化开发服务器中安装和测试 FiveM 资源。
- **社区管理：** 通过 txAdmin 管理玩家、定时重启和服务器设置。
- **配方评估：** 先体验 CFX Default FiveM 配方，再规划更大的服务器。

## FXServer 托管依赖

模板包含 FXServer 运行环境、txAdmin、持久化存储和网络资源。首次创建管理员需要 Cfx.re 账号，启动游戏服务器需要有效的服务器许可密钥。玩家还需具备 FiveM 要求的软件和游戏授权。

- [容器文档](https://github.com/routmoute/fxserver)
- [txAdmin 官方安装指南](https://docs.fivem.net/docs/server-manual/setting-up-a-server-txadmin/)
- [Cfx.re Portal](https://portal.cfx.re/)
- [txAdmin 文档](https://github.com/citizenfx/txAdmin)

## 为什么在 Sealos 上部署 FXServer？

Sealos 基于 Kubernetes 提供一键部署，CPU、内存和存储按量计费。持久化存储能够在重启后保留服务器状态，管理界面会获得公网 HTTPS 地址。

部署完成后，可在 Canvas 中查看服务器状态，通过 AI 对话框描述配置修改，或打开资源卡片调整 CPU、内存、存储和网络。根据配方和玩家数量调整资源，并保持单个服务器副本。

## 部署指南

1. 打开 [FXServer 模板页面](https://sealos.io/products/app-store/fxserver)，点击 **Deploy Now**。
2. 检查部署设置并开始部署。资源创建通常需要 **2-3 分钟**，随后可以在 Canvas 中管理本次部署。
3. 打开自动生成的 HTTPS 应用地址。首次访问时，txAdmin 会显示 **No Cfx.re account linked** 并要求输入 PIN。在 Canvas 中打开服务器资源卡片，查看容器日志，找到 txAdmin 初始化 PIN。
4. 输入 PIN 并点击 **Link Account**。登录 Cfx.re，批准账号关联，然后按 txAdmin 提示创建备用密码。请保存该密码，方便以后使用本地密码登录。
5. 按服务器设置向导继续。原版方案选择 **CFX Default FiveM** 配方，将安装目录保留在 `/txdata` 下，并填写从 [Cfx.re Portal](https://portal.cfx.re/) 获取的服务器许可密钥。运行配方并启动服务器。
6. 打开 `<app-name>-nodeport` Service 资源卡片，找到 `game-tcp` 和 `game-udp` 共用的公网端口。在 FiveM 客户端中使用该游戏地址连接。HTTPS 应用地址用于打开 txAdmin。

### 连接 FiveM 客户端

使用所在 Sealos 区域显示的公网 TCP/UDP 主机地址，以及分配到的游戏 NodePort。美国西部区域的主机地址是 `tcp.usw-1.sealos.app`。打开 FiveM 的 F8 控制台，将下面命令中的 `GAME_NODEPORT` 替换为实际端口：

```text
connect tcp.usw-1.sealos.app:GAME_NODEPORT
```

游戏连接使用 `game-tcp`/`game-udp` 对应的端口。另行分配给 `http` 的端口属于管理界面。

### 后续登录

再次打开同一个 HTTPS 地址，使用已关联的 Cfx.re 账号，或初始化时设置的管理员用户名和备用密码登录。管理员状态保存在持久卷中。首次初始化所需的 PIN 可从服务器日志中获取，每次新部署都会生成自己的 PIN。

## 配置和存储

通过 txAdmin 修改服务器设置和管理资源。模板将内部管理端口固定为 `40120`，内部游戏端口固定为 `30120`，Service 和 Ingress 使用相同配置。

请将配方、服务器资源和数据保存在 `/txdata` 下。随着资源和日志增长，可在 Canvas 中扩容持久卷。增加玩家或启用资源消耗较大的框架前，应根据所选配方调整 CPU 和内存。

模板当前的初始资源候选值为 `200m` CPU 和 `256Mi` 内存。管理界面启动已检查；使用有效许可启动游戏、登录后的操作和游戏服务器最低资源验证仍待完成。此模板在这些验收完成前保持草稿状态。

## 故障排查

- **一直停留在账号关联页面：** 输入本次部署日志中的 PIN，完成 Cfx.re 授权，并创建备用密码。
- **txAdmin 可以打开，游戏服务器仍离线：** 完成配方向导，填写有效的 Cfx.re 服务器许可密钥，并在实时控制台中查看具体启动错误。
- **客户端连接失败：** 在 Service 卡片中核对共用游戏 NodePort 和所在区域的 TCP/UDP 主机地址，然后确认 txAdmin 中的游戏服务器已经启动。
- **配方运行时内存或存储不足：** 在 Canvas 中增加对应资源并重启服务器。依赖数据库的配方还需要按文档配置数据库。

## 许可证

FXServer 和 FiveM 的使用受 [Cfx.re 条款](https://fivem.net/terms)约束。txAdmin 采用 [MIT 许可证](https://github.com/citizenfx/txAdmin/blob/master/LICENSE)。容器源码及贡献说明见[容器仓库](https://github.com/routmoute/fxserver)和 [Sealos 模板仓库](https://github.com/labring-actions/templates)。
