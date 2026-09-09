# 在 Sealos 上部署和托管 Project Zomboid

Project Zomboid 是一款支持多人联机的僵尸生存游戏。此模板在 Sealos Cloud 上部署持久化专用服务器，支持 Steam 联机、私人世界和远程控制台（RCON）管理。

![Project Zomboid 官方网站](website-screenshot.webp)

## 关于托管 Project Zomboid

部署使用 Danixu 的 `42.20.4-release` 镜像，内含 Project Zomboid 42.20.4 和 Java 运行时。每个服务器管理一个世界，存档、玩家账号、服务器设置和创意工坊内容分别保存在持久卷中。

Sealos 自动创建服务器、存储和公网 UDP/TCP 端点。初始化容器会配置平台分配的公网 UDP 端口，让游戏公布的端口与实际可访问的端口一致。玩家通过 Project Zomboid 客户端加入游戏，管理员通过游戏内账号或 RCON 管理世界。

## 常见使用场景

- **私人生存世界**：为朋友保留持续运行的世界，让大家在不同时间继续游玩。
- **合作生存战役**：使用服务器加入密码和各自的玩家账号，共同维护一个世界。
- **世界管理**：通过 RCON 查看在线玩家、保存进度和执行管理操作。
- **创意工坊测试**：增加资源和存储后，在独立世界中测试服务器与客户端配套的模组。

## Project Zomboid 托管依赖

镜像已包含专用服务器和 Java 运行时。模板提供持久化存储，并使用临时 Python 初始化容器完成配置。Project Zomboid 的账号数据库和世界数据保存在世界数据卷中。

### 部署依赖

- [Project Zomboid](https://projectzomboid.com/) — 游戏介绍与客户端购买入口。
- [Docker 镜像文档](https://github.com/Danixu/project-zomboid-server-docker) — 镜像版本和服务器配置说明。
- [Project Zomboid 社区](https://theindiestone.com/forums/) — 游戏支持和多人联机讨论。

### 实现细节

**架构组件：**

| 组件 | 用途 |
| --- | --- |
| 专用服务器 | 一个 StatefulSet 副本，以用户 1000 运行 Project Zomboid 42.20.4。 |
| 初始化容器 | 仅查询和更新本实例的 Service，随后写入分配的游戏端口及持久化服务器设置。 |
| 世界数据卷 | 1 GiB，挂载到 `/home/steam/Zomboid`，保存账号、配置、存档和备份。 |
| 创意工坊数据卷 | 1 GiB，挂载到 `/home/steam/pz-dedicated/steamapps/workshop`，保存下载的创意工坊内容。 |
| 公网连接 | 独立的 `${{ defaults.app_name }}-nodeport` Service 选中原服务器工作负载，提供 `game` UDP、`direct` UDP，以及需要认证的 `rcon` TCP 端点。 |

**配置：** 世界名称固定为 `sealos`，初始玩家上限为 4，默认关闭公开服务器列表展示。初始化步骤负责设置端口、服务器加入密码、RCON、公开列表、玩家上限和 UPnP，其余已保存的 INI 选项会继续保留。关闭时，Kubernetes 向服务器控制台发送 `quit` 命令，并留出最多 120 秒供游戏保存数据。

**已验证的低负载资源：**

| 容器 | CPU 限额 / 请求 | 内存限额 / 请求 | Java 堆 |
| --- | --- | --- | --- |
| 专用服务器 | 100m / 10m | 4096 MiB / 409 MiB | 初始 64m，最大 2048m |
| 初始化容器 | 100m / 10m | 128 MiB / 12 MiB | — |

以上是空世界、无模组场景通过实测的最低 Sealos 资源档位。验证覆盖冷启动、管理员创建与账号复用、公网 Steam/RakNet 查询、RCON 认证、`players`、持久化 `save`，以及超过 60 秒的稳定运行。实际游玩和多人容量需要单独评估资源。100m CPU 下冷启动约需 21 分钟，200m CPU 下约需 10 分钟。

每个世界保持一个副本。随着活跃玩家、世界规模或模组增加，适当提高 CPU、内存、Java `MAX_MEMORY` 和存储容量。Java 堆上限与容器内存上限之间应保留余量，供原生游戏库及其他运行时数据使用。

## 为什么在 Sealos 上部署 Project Zomboid？

[Sealos](https://sealos.io) 基于 Kubernetes，提供一键部署和按量付费的资源管理。持久卷让世界数据跨服务器重启保留，资源卡片集中展示日志、资源用量和公网连接地址。

部署完成后，可在 Canvas 的 AI 对话框中描述修改需求，也可打开服务器资源卡片调整设置。此模板由单个服务器管理世界，支持按需增加资源。

## 部署指南

1. 打开 [Project Zomboid 模板](https://sealos.io/products/app-store/project-zomboid)，点击 **Deploy Now**。
2. 设置 `admin_username` 和 `admin_password`。管理员用户名仅使用 ASCII 字母和数字，密码应为强度足够的单行文本。还可设置 `server_password`，加入服务器的所有玩家都需要提供此密码。
3. 资源创建通常需要 2-3 分钟。部署完成后进入 Canvas，等待服务器达到 **Running/Ready**。镜像下载和首次游戏、世界初始化耗时更长；启动探针最多等待 30 分钟。
4. 打开服务器资源卡片的 **Networks** 区域，复制 `game` UDP 条目中的公网主机名和分配的外部端口，同时保持 `direct` UDP 端点启用。连接时填写这里显示的外部端口。
5. 启动版本匹配的 Project Zomboid 42.20.4 客户端。进入 **Join**，添加收藏服务器，填写公网主机名和 `game` 的外部端口。在账号栏填写玩家用户名与密码；设置过 `server_password` 时，还需在独立的服务器密码栏填写该值。
6. 管理世界时，使用部署时设置的 `admin_username` 和 `admin_password` 连接。管理员账号在首次启动时创建，随后保存在世界数据卷中。后续修改管理员密码应使用游戏的账号管理命令；修改部署参数中的初始化密码时，已有账号会继续使用原密码。

资源定义中的 `game` 和 `direct` Service 端口分别显示为 16261 和 16262。Sealos 分配外部端口后，初始化容器会同步游戏的实际监听端口。`rcon` 条目将平台分配的外部 TCP 端口映射到服务器的 TCP 27015 端口。

## 配置

### RCON 管理

在服务器资源卡片的环境变量设置中查看 `RCONPASSWORD`。此密码独立生成，与游戏管理员密码、服务器加入密码分别使用。在 RCON 客户端中填写公网主机名和 `rcon` 网络条目的外部 TCP 端口，以 `RCONPASSWORD` 认证后，可执行 `players`、`save` 等命令。

请妥善保管 RCON 密码，向玩家单独提供玩家所需的凭据。RCON 可执行服务器管理命令，建议通过可信网络进行管理。

### 存档、设置与模组

服务器配置位于 `/home/steam/Zomboid/Server/sealos.ini`，游戏数据保存在 `/home/steam/Zomboid` 下。修改版本或模组前，先备份世界数据卷。添加创意工坊内容时，配置对应的 `WorkshopItems` 和 `Mods`，让所有客户端使用相同内容，并按下载体积扩容创意工坊数据卷。

游戏程序保留在固定版本的镜像中。升级前先备份世界，再选择兼容的镜像标签；恢复游玩前，确认客户端版本和存档兼容。

## 故障排查

- **启动持续数分钟**：查看日志中的世界初始化进度。较低 CPU 限额下，新世界启动会明显长于资源创建时间，达到就绪状态后再加入。
- **Java 堆错误或 OOMKilled**：提高容器内存限额，并调整 `MAX_MEMORY`，同时为原生库预留内存。负载下出现启动或游戏命令超时时，提高 CPU 限额。
- **加入失败**：核对客户端版本、`game` 的外部 UDP 端口、两个 UDP 条目的启用状态，以及各自独立的账号密码和服务器密码。连接地址以当前部署的 Networks 区域为准。
- **修改参数后管理员登录失败**：账号沿用首次启动时保存的凭据。使用已有密码，或按游戏文档执行账号管理操作。
- **地图元数据提示**：镜像中的游戏可能输出 mannequin-zone 和 room-metaID 消息，[上游报告](https://theindiestone.com/forums/topic/98551-maniqui-and-basements-error/) 中有相同记录。本次验证已完成世界重载、RCON 操作和保存。请保留备份，并关注游戏上游修复。
- **世界或模组存储已满**：扩容对应持久卷，并在添加更多内容前检查旧备份的占用。

镜像问题可在[上游问题追踪器](https://github.com/Danixu/project-zomboid-server-docker/issues)反馈。游戏问题可前往[官方社区论坛](https://theindiestone.com/forums/)寻求支持。

## 许可证

此模板遵循 [Sealos 模板仓库许可证](https://github.com/labring-actions/templates#-license)。上游 Docker 打包项目采用 [GPL-3.0](https://github.com/Danixu/project-zomboid-server-docker/blob/main/LICENSE)。Project Zomboid 是 The Indie Stone 开发的商业游戏，玩家需要拥有自己的游戏许可。
