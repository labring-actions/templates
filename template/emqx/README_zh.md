# 在 Sealos 上部署和托管 EMQX

EMQX 是一个面向物联网、工业遥测和互联设备消息的开源 MQTT 消息服务器。此模板会把 EMQX 社区版 `5.8.9` 部署为三节点 StatefulSet，并配置 DNS 集群发现以及每节点独立的数据和日志持久化卷。

![EMQX 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/emqx/website-screenshot.webp)

## 关于 EMQX 托管

EMQX 提供 MQTT、MQTT over TLS、MQTT over WebSocket、管理 REST API 和浏览器 Dashboard。此模板使用官方开源镜像 `emqx/emqx:5.8.9`，并采用三个副本作为实用的奇数成员集群基线。

Dashboard 会获得自动生成的 HTTPS 地址。公网 MQTT WebSocket 和 NodePort 监听器由部署参数明确控制。

## 部署内容

| 组件 | 用途 | 默认配置 |
| --- | --- | --- |
| EMQX StatefulSet | 三个集群 broker 节点 | 每节点 500m CPU / 512 MiB |
| Headless Service | 为 Erlang 分布式通信提供稳定 DNS SRV 发现 | 集群内部 |
| ClusterIP Service | Dashboard 和 MQTT WebSocket 后端 | 集群内部 |
| Dashboard Ingress | 公网 HTTPS Dashboard | 已启用 |
| MQTT WebSocket Ingress | 公网 `wss://.../mqtt` 地址 | 由 `WS_ENABLE` 控制 |
| MQTT NodePort Service | MQTT、TLS、WS 和 WSS 端口 | 由 `TCP_ENABLE` 控制 |
| 持久化卷 | `/opt/emqx/data` 和 `/opt/emqx/log` | 每节点两个 1 GiB 卷 |

每个 broker 节点的资源请求量为 50m CPU 和 51 MiB 内存。

## 部署参数

| 参数 | 默认值 | 用途 |
| --- | --- | --- |
| `ADMIN_PASSWORD` | 必填 | Dashboard `admin` 账号的初始密码，长度使用 8-64 个字符。 |
| `WS_ENABLE` | `false` | 在 `wss://<app-host>/mqtt` 发布 MQTT over WebSocket。 |
| `TCP_ENABLE` | `false` | 为 1883、8883、8083 和 8084 端口创建 NodePort Service。 |

## 账号与安全

Dashboard 用户名为 `admin`，初始密码来自必填的 `ADMIN_PASSWORD` 参数。首次登录后请修改此密码。

全新的 EMQX 社区版安装会按照默认监听策略接受未认证 MQTT 客户端。生产流量启用 `WS_ENABLE` 或 `TCP_ENABLE` 前，请先在 Dashboard 中配置 MQTT 认证和授权。

## 部署指南

1. 打开 [EMQX 模板](https://sealos.io/products/app-store/emqx)，选择 **Deploy Now**。
2. 设置高强度 `ADMIN_PASSWORD`。
3. 配置 broker 认证期间保留 `WS_ENABLE=false` 和 `TCP_ENABLE=false`。
4. 等待三个 StatefulSet Pod 全部就绪并组成同一个集群。
5. 打开生成的 HTTPS 地址，以 `admin` 身份登录。
6. 配置 MQTT 认证和授权，然后通过受控重新部署启用需要的公网监听器。

## 客户端地址

- **Dashboard**：`https://<app-host>.<region-domain>/`
- **MQTT WebSocket**：`WS_ENABLE=true` 时使用 `wss://<app-host>.<region-domain>/mqtt`
- **MQTT TCP/TLS**：`TCP_ENABLE=true` 时使用 Sealos 显示的 NodePort 映射

## 配置

- **EMQX Dashboard**：管理监听器、认证、授权、客户端、规则、连接器和集群设置。
- **REST API**：在 Dashboard 域名下使用 `/api/v5`，并携带 Dashboard access token。
- **Sealos Canvas**：查看日志、集群 Pod、Service、Ingress 路由、指标和持久化卷。
- **集群发现**：Headless Service 的 DNS SRV 记录会连接三个稳定 Pod 主机名。

## 扩容

此模板将初始拓扑固定为三个副本。后续拓扑变更需要同时规划 MQTT 会话行为、持久化卷归属、滚动更新顺序和客户端重连测试。

经过验证的每节点内存下限为 512 MiB。256 MiB 冷启动候选配置反复出现 OOMKilled，退出码为 137；512 MiB 配置组成三节点集群且重启数为零。

## 运行验证

三个节点均加入同一个集群，并同时出现在 `emqx ctl cluster status` 和已认证的 `/api/v5/nodes` 接口中。Dashboard 认证结果显示 EMQX `5.8.9` 社区版。

使用 `WS_ENABLE=true` 时，两个公网 TLS WebSocket 客户端通过 MQTT v5 完成 QoS 1 订阅和发布操作，接收 topic 与 payload 哈希均匹配发布值。已认证的未知 REST 路径返回 HTTP 404。

## 故障排查

### Broker Pod 长时间未就绪

检查 `emqx ctl status`、Pod 重启原因和内存指标。确认所有 Pod 都能解析 Headless Service，并共享相同的 node cookie。

### Dashboard 登录失败

使用用户名 `admin` 和通过 `ADMIN_PASSWORD` 提交的密码。管理员可在需要时通过 EMQX CLI 重置 Dashboard 用户。

### MQTT 客户端连接失败

检查选择的公网监听参数、地址类型、端口映射、TLS 模式、WebSocket 路径和 MQTT 认证策略。

## 资源

- [EMQX 文档](https://docs.emqx.com/zh/emqx/latest/)
- [EMQX 5.8.9 发布页](https://github.com/emqx/emqx/releases/tag/v5.8.9)
- [官方 Helm Values](https://github.com/emqx/emqx/blob/v5.8.9/deploy/charts/emqx/values.yaml)
- [EMQX Dashboard 指南](https://docs.emqx.com/zh/emqx/latest/dashboard/introduction.html)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

EMQX `5.8.9` 社区版采用 Apache License 2.0。此模板遵循 Sealos templates 仓库许可证。
