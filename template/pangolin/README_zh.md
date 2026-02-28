# 在 Sealos 上部署并托管 Pangolin

[Pangolin](https://pangolin.net) 是一个基于 WireGuard 的开源身份感知远程访问平台。这个模板会在 Sealos Cloud 上部署 Pangolin 控制平面，提供持久化配置存储与 HTTPS Ingress，同时保留外部 Gerbil 的集成入口。

## 关于在 Sealos 上托管 Pangolin

Pangolin 本质上是一个控制服务器，负责身份、策略与资源访问控制。在这个 Sealos 模板中，Pangolin 以 Kubernetes Deployment 方式运行，通过平台 Ingress 对外暴露，并将 `/app/config` 挂载到持久卷，确保运行配置可长期保留。

相较官方 Docker 拓扑，本模板有意识地移除了内置 Traefik 和内置 Gerbil。公网流量统一由 Sealos Ingress 接入，隧道与出口能力交由外部 Gerbil 提供，再回连 Pangolin 控制面。

## 常见使用场景

- **自托管零信任访问**：为内部 Web 应用和服务提供基于身份的访问控制。
- **团队统一访问网关**：按用户与角色管理研发、运维、支持团队的资源权限。
- **家庭实验室或中小团队远程访问**：在不大面积开放内网的前提下安全暴露指定资源。
- **基于 WireGuard 的私网连接**：将 Pangolin 与外部 Gerbil 组合，实现安全链路与策略落地。

## Pangolin 托管依赖

该 Sealos 模板已包含 Pangolin 控制面运行所需的核心依赖：应用工作负载、持久化存储、服务发现、Ingress 路由，以及 Sealos App 集成。

### 部署依赖参考

- [Pangolin Documentation](https://docs.pangolin.net/) - 官方安装与运维文档。
- [Pangolin GitHub Repository](https://github.com/fosrl/pangolin) - 源码与版本发布信息。
- [Sealos Platform](https://sealos.run) - Sealos 平台入口。
- [Sealos Documentation](https://sealos.run/docs) - Sealos 使用与运维文档。

### 实现细节

**架构组件：**

该模板会部署以下资源：

- **Pangolin Deployment**：`docker.io/fosrl/pangolin:1.15.2`，开放 `3000/3001/3002/3003` 端口。
- **ConfigMap + PVC**：运行配置由 ConfigMap 注入，并持久化到 `/app/config`。
- **Service**：在集群内暴露 Pangolin 端口，供 Ingress 与集群访问。
- **Ingress**：  
路径 `/` -> Pangolin 前端（`3002`）  
路径 `/api/v1` -> Pangolin API（`3000`）
- **App CR**：在 Sealos 中生成应用入口卡片与公网访问地址。

**配置说明：**

- `gerbil_base_endpoint` 表示外部 Gerbil 向 Pangolin 上报的公网地址。
- `server_secret` 默认自动生成并写入 Pangolin 配置。
- 内置 Traefik 已移除，由 Sealos Ingress 统一承接 HTTP(S) 入口。
- 内置 Gerbil 已移除，原因是 Sealos 用户工作负载不支持 `NET_ADMIN` / `SYS_MODULE` 这类特权能力。

**首次管理员初始化（重要）：**

应用启动后，Pangolin 会在容器日志中打印一次性 setup token。必须使用该 token 才能创建首个管理员账号。

1. 进入部署对应的 **Canvas** 页面。
2. 点击 **Pangolin Deployment** 资源卡片，打开 **Logs**。
3. 在日志中找到最新的 `Token:` 行并复制 setup token。
4. 打开 `https://<app_host>.<SEALOS_CLOUD_DOMAIN>/auth/initial-setup`。
5. 填写邮箱、密码以及日志中的 setup token。
6. 在 `https://<app_host>.<SEALOS_CLOUD_DOMAIN>/auth/login` 完成登录。

如果跳过 setup token 这一步，管理员账号将无法创建成功。

## 为什么选择在 Sealos 上部署 Pangolin？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，覆盖应用部署与运维全流程。把 Pangolin 部署在 Sealos 上，你可以获得：

- **一键部署**：无需手工拼装 Docker 与 Ingress 资源，开箱即用。
- **Kubernetes 级可靠性**：天然具备生产级编排与服务网络能力。
- **配置调整更直接**：可通过 Canvas 对话框与资源卡片完成参数更新。
- **内置持久化存储**：借助 PVC（PersistentVolumeClaim）保障配置跨重启保留。
- **公网访问即开即用**：通过 Sealos Ingress 自动获得 HTTPS 暴露能力。
- **运维流程一致化**：可结合 Canvas 与 AI 对话持续迭代部署配置。

## 部署指南

1. 打开 [Pangolin template](https://sealos.run/appstore/pangolin)，点击 **Deploy Now**。
2. 在弹窗中填写部署参数：
   - `gerbil_base_endpoint`（必填）
   - 以及可选默认值，如 `app_name`、`app_host`、`server_secret`
3. 等待部署完成（通常 2-3 分钟），完成后会自动跳转到 Canvas。
4. 打开生成的应用地址，按上文“首次管理员初始化”流程，在 Canvas 日志中获取 setup token 并完成首管创建。
5. 初始化完成后，登录 Pangolin 控制台继续配置。

## 配置项说明

| 参数 | 说明 | 默认值 |
| --- | --- | --- |
| `app_name` | 资源名前缀 | `pangolin-<random>` |
| `app_host` | 公网域名前缀 | `pangolin-<random>` |
| `server_secret` | Pangolin 服务端密钥 | 随机 32 位字符串 |
| `gerbil_base_endpoint` | 外部 Gerbil 对 Pangolin 公告的公网地址 | `pangolin.example.com` |

部署后的变更可以通过以下方式完成：

- **Canvas 中的 AI 对话**：用意图描述方式下发修改。
- **资源卡片**：直接编辑 Deployment、Service、Ingress、ConfigMap 等资源。

## 扩缩容

如需调整 Pangolin 资源规格：

1. 打开对应部署的 Canvas。
2. 选择 Pangolin Deployment 资源卡片。
3. 调整 CPU/内存或副本数。
4. 应用修改并观察 rollout 状态。

## 故障排查

### 常见问题

**问题：无法创建首个管理员账号**
- 原因：未提供 setup token，或 token 已失效。
- 解决：进入 Canvas 的 Pangolin Deployment 资源卡片查看日志，读取最新 `Token:` 后再完成 `/auth/initial-setup`。

**问题：API 写请求返回 403**
- 原因：写操作缺少 CSRF 头。
- 解决：对非 GET API 请求带上 `x-csrf-token: x-csrf-protection`。

**问题：外部 Gerbil 无法注册或同步**
- 原因：`remoteConfig` 地址错误，或 `base_endpoint` 不匹配。
- 解决：Gerbil 侧使用 `--remoteConfig=https://<app_host>.<SEALOS_CLOUD_DOMAIN>/api/v1/`，并把 `gerbil_base_endpoint` 设为 Gerbil 公网地址。

### 获取帮助

- [Pangolin Documentation](https://docs.pangolin.net/)
- [Pangolin GitHub Issues](https://github.com/fosrl/pangolin/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Pangolin Website](https://pangolin.net)
- [Pangolin Self-Host Docs](https://docs.pangolin.net/self-host)
- [Sealos Documentation](https://sealos.run/docs)

## 许可证

本 Sealos 模板遵循 templates 仓库许可证发布。Pangolin 项目本身采用 [AGPL-3.0](https://github.com/fosrl/pangolin/blob/main/LICENSE) 许可证。
