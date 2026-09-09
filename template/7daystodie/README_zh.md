# 在 Sealos 上部署和托管 7 Days to Die

7 Days to Die 是一款支持多人联机的生存建造游戏。本模板通过 `vinanrra/7dtd-server:v0.9.3` 和 LinuxGSM，在 Sealos 上部署带持久化存档的私人专用服务器。

![LinuxGSM 的 7 Days to Die 服务器产品页面](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/7daystodie/website-screenshot.webp)

## 关于 7 Days to Die 托管

模板运行一个服务器实例，默认使用游戏自带的 Navezgane 地图，允许四名玩家同时在线。SteamCMD 会在启动时下载当前稳定版专用服务器，LinuxGSM 负责游戏进程管理和正常关服。

Sealos 会创建 1 GiB 持久化存档卷，并提供原生 TCP/UDP 访问。初始化步骤会预留连续的公网端口，并将同一组端口写入游戏配置。服务器完成安装、加载世界并成功响应游戏查询后，才会进入就绪状态。

## 常见使用场景

- **好友合作生存：** 与小规模好友队伍一起探索、建造和抵御尸潮。
- **长期存档：** Pod 重建后继续使用原有世界和玩家进度。
- **独立服务器：** 将服务端与玩家的游戏客户端分开运行。

## 托管依赖

容器包含 LinuxGSM、SteamCMD 和安装专用服务器所需的工具。玩家需要拥有版本兼容的正版游戏客户端。

- [Docker 镜像文档](https://github.com/vinanrra/Docker-7DaysToDie/tree/v0.9.3/docs)
- [LinuxGSM 服务器指南](https://linuxgsm.com/servers/sdtdserver/)
- [官方专用服务器配置要求](https://7-days-to-die.zendesk.com/hc/en-us/articles/48451066199188-System-Requirements-for-Dedicated-Server)
- [官方网络端口指南](https://7-days-to-die.zendesk.com/hc/en-us/articles/48451426400916-Opening-Ports-in-Firewall)

### 部署实现

| 组件 | 配置 |
| --- | --- |
| 游戏服务器 | 一个 StatefulSet，运行 `vinanrra/7dtd-server:v0.9.3` |
| CPU 与内存上限 | 4 核 CPU、8192 MiB 内存，对应官方专用服务器最低要求 |
| 存档空间 | 1 GiB，挂载到 `/home/sdtdserver/.local/share/7DaysToDie/Saves` |
| 可重建安装文件 | 20 GiB 容器存储，用于 SteamCMD 和游戏文件 |
| 原生网络 | 一个 NodePort Service：基础端口同时开放 TCP 和 UDP，随后三个端口开放 UDP |
| 端口分配 | 初始化容器仅有读取、修改本应用 Service 的权限 |
| 管理入口 | 容器终端内的本地 Telnet：`127.0.0.1:8081` |

服务器使用自动生成的密码，并在公共服务器列表中隐藏。Web 管理和主机跨平台联机功能默认关闭。上游运行方式使用本地存档，模板为存档目录配置持久化存储。

游戏安装文件保存在容器可写层中。每次 Pod 重建都会重新下载这些文件，世界和玩家存档则由持久卷保留。随着玩家探索范围扩大，请关注存档空间，在用满前扩容。模板保持一个服务器副本；长期游玩或增加玩家时，可相应增加 CPU、内存和存储。

## 为什么在 Sealos 上部署 7 Days to Die？

Sealos 基于 Kubernetes，提供一键部署、持久化存储、原生公网端口和资源监控。资源按量计费，玩家数量和世界规模增长后，可以在 Canvas 中通过 AI 对话或资源卡片调整配置。

## 部署指南

1. 打开 [7 Days to Die 模板页面](https://sealos.io/products/app-store/7daystodie)，点击 **Deploy Now**。
2. 填写服务器名称和最大在线人数。模板支持 1-8 名玩家，默认四人。
3. 等待 Sealos 创建资源，通常需要 2-3 分钟。首次 SteamCMD 下载和游戏启动还需要额外时间，可在 Canvas 中查看服务器日志，直到工作负载进入 Ready 状态。
4. 打开服务器的网络资源卡片，复制公网主机地址及 `game-tcp` 或 `game-udp` 端口。两者使用相同的基础端口，连接时请填写分配到的公网端口。
5. 在服务器资源卡片的环境变量设置中找到 `ServerPassword`，将主机地址、基础端口和密码分享给玩家。
6. 在版本兼容的 PC 游戏客户端中选择 **Join a Game**，点击 **Connect to IP**，输入公网主机地址和基础端口，再按提示输入生成的密码。

连接和身份验证均在游戏客户端中完成。日常管理可以通过 Canvas 和容器终端进行。

## 配置

在 Canvas 中使用 AI 对话或资源卡片修改资源和环境变量。`ServerName` 控制显示名称，`ServerMaxPlayerCount` 控制人数上限，`ServerPassword` 控制入服密码。修改后重启 Pod，并等待游戏文件下载完成。

需要使用管理控制台时，在容器终端运行：

```sh
telnet 127.0.0.1 8081
```

常用命令包括 `listplayers` 和 `saveworld`。Telnet 监听回环地址，可从容器内部访问。

## 故障排查

**启动长时间等待：** 查看日志中的 SteamCMD 下载进度和 Steam 连接错误。启动过程包含游戏安装，耗时会受网络条件影响。

**客户端无法加入：** 确认客户端与已安装的稳定版服务端版本一致，使用资源卡片中的公网基础端口，并允许客户端侧防火墙放行对应的四个连续 UDP 端口。入服密码位于服务器环境变量 `ServerPassword` 中。

**存档空间将满：** 在 Canvas 中扩容存档卷，并将 Saves 目录额外备份到外部存储。更多玩家、更大的探索范围和额外世界都会增加空间需求。

## 许可证

Docker 打包项目采用 [GPL-3.0](https://github.com/vinanrra/Docker-7DaysToDie/blob/v0.9.3/LICENSE) 许可证。7 Days to Die 是 The Fun Pimps 拥有的商业软件，使用时仍需遵守游戏许可条款。截图展示的是官方 LinuxGSM 服务器产品页面。
