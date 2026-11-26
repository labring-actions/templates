# 在 Sealos 上部署和托管 Minecraft

此模板使用官方 `itzg/minecraft-server:2026.8.0-java25` 镜像，在 Sealos 上运行持久化 Minecraft Java 版服务器。模板支持 Paper、Fabric 和 Forge，通过 TCP NodePort 发布游戏协议，并把全部服务端数据保存在 `/data`。

![Minecraft Server on Docker 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/minecraft/website-screenshot.webp)

## 关于 Minecraft 托管

一个 StatefulSet 副本持有一个世界。持久化卷会在 Pod 替换后保留世界数据、服务端属性、插件、模组和日志。`mc-health` 通过 Minecraft 状态协议驱动启动、就绪和存活检查。

容器镜像固定到 `2026.8.0-java25` 版本。默认 `VERSION=LATEST` 会在每次冷启动时解析最新兼容游戏服务端；插件、模组或可复现升级需要固定版本时，请选择具体 `VERSION`。

## 部署内容

| 组件 | 用途 | 默认配置 |
| --- | --- | --- |
| Minecraft StatefulSet | 一个 Java 版服务端 | 200m CPU / 2 GiB |
| 持久化卷 | `/data` 世界和运行文件 | 1 GiB |
| NodePort Service | 公网 Minecraft Java TCP 协议 | 容器端口 25565 |

JVM 堆内存为 `1024M`。2 GiB 容器限制为原生内存和启动过程提供余量。资源请求量为 20m CPU 和 204 MiB 内存。

## 部署参数

| 参数 | 默认值 | 用途 |
| --- | --- | --- |
| `TYPE` | `PAPER` | 选择 `PAPER`、`FABRIC` 或 `FORGE`。 |
| `VERSION` | `LATEST` | 选择具体 Minecraft 版本，或解析最新兼容版本。 |

部署此模板会设置 `EULA=TRUE`。请先阅读并接受 [Minecraft EULA](https://www.minecraft.net/eula)。

## 访问与管理

玩家使用常规 Minecraft 或 Microsoft 账号从 Minecraft Java 版客户端连接。服务器地址由 Sealos 区域主机和自动生成的 NodePort 组成，例如 `usw-1.sealos.io:46520`。

镜像会启用内部 RCON 管理，并在容器中提供 `rcon-cli`。模板将 RCON 25575 端口保留在 Pod 网络中。请通过 Sealos 终端运行 `rcon-cli list`、`rcon-cli say ...` 和 `rcon-cli save-all` 等命令。

## 部署指南

1. 打开 [Minecraft 模板](https://sealos.io/products/app-store/minecraft)，选择 **Deploy Now**。
2. 选择 `PAPER`、`FABRIC` 或 `FORGE`。
3. 使用 `VERSION=LATEST` 跟随滚动版本目标，或输入具体游戏版本构建可复现服务器。
4. 启动部署，为下载、patch 和首次世界生成预留数分钟。
5. 在 Sealos 中打开 Service 卡片，复制容器端口 25565 对应的 NodePort。
6. 在 Minecraft Java 版中添加 `<region-host>:<mapped-port>` 服务器地址。

## 配置

- **服务端文件**：编辑 `/data` 下的持久化文件，包括 `server.properties`、插件、模组和白名单文件。
- **RCON**：使用容器内置的 `rcon-cli` 运行管理命令。
- **Sealos Canvas**：查看日志、资源指标、StatefulSet 健康状态、Service 映射和卷容量。
- **白名单与管理员**：按照社区策略配置 Minecraft 白名单和 operator 列表。

## 扩容

Minecraft 世界由单个进程持有实时状态，因此采用纵向扩容。模拟距离、实体、插件或玩家数量增长时请提高 CPU；主动扩大 JVM 堆时，请同步提高容器内存限制和 `MEMORY`。

经过验证的启动下限为 200m CPU 和 2 GiB 内存限制。100m CPU 与 1 GiB 候选配置反复出现退出码 137，并持续处于未就绪状态；选定配置完成了 Paper 启动、世界生成、协议检查和 RCON 命令。

## 运行验证

全新 Paper 部署解析到 Paper `26.2`，生成三个维度，达到就绪状态且重启数为零，并从 localhost 和公网 NodePort 成功响应 Minecraft 状态协议。

运行管理通过 RCON 完成了 `list`、广播消息和 `save-all`。绑定的持久化卷在操作后包含 `server.properties`、`world/level.dat` 和已保存世界数据。

## 故障排查

### 服务端仍在启动

查看 Pod 日志中的下载、patch 和世界生成进度。首次启动可能持续数分钟，startup probe 在初始延迟后提供最长五分钟的探测窗口。

### 客户端连接失败

确认 Pod 已经 Ready，从 Service 卡片复制 TCP NodePort，并使用 Sealos 区域主机和该映射端口。

### Paper、Fabric 或 Forge 启动失败

检查 `TYPE`、`VERSION`、Java 25、插件和模组之间的兼容性。固定模组包或插件集请使用具体 `VERSION`。

### 世界需要更多容量

请在世界数据或备份接近 1 GiB 前扩展持久化卷。影响 Pod 或卷的维护操作前请运行 `save-all`。

## 资源

- [Minecraft Server on Docker 文档](https://docker-minecraft-server.readthedocs.io/en/latest/)
- [2026.8.0 发布页](https://github.com/itzg/docker-minecraft-server/releases/tag/2026.8.0)
- [官方 Docker Compose](https://github.com/itzg/docker-minecraft-server/blob/2026.8.0/docker-compose.yml)
- [Paper 文档](https://docs.papermc.io/)
- [Minecraft EULA](https://www.minecraft.net/eula)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此模板遵循 Sealos templates 仓库许可证。Minecraft、Paper、Fabric、Forge 和 `itzg/docker-minecraft-server` 分别遵循各自上游许可证和条款。
