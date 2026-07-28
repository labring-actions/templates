# 在 Sealos 上部署与托管 Headscale

Headscale 是一个开源、自托管的 Tailscale 控制服务器实现。本模板部署 Headscale 0.29.2 和 Headplane 0.7.0 管理界面，并提供持久化存储、启用 TLS 的公网端点，以及可选的 KubeBlocks PostgreSQL 数据库。

![Headscale 官网截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/headscale/website-screenshot.webp)

## 关于 Headscale

Headscale 为私有 Tailscale 兼容网络提供协调服务，负责管理用户、设备、路由、DNS、ACL 策略和设备注册，兼容客户端则负责建立数据传输路径。

本模板在同一个 StatefulSet 中运行 Headscale 与 Headplane，让 Headplane 可以通过 Kubernetes 集成安全地重新加载 Headscale 配置。SQLite 是默认数据库，也符合上游对新部署的建议。启用 `use_postgresql` 后，模板会为需要独立数据库的运维场景创建 PostgreSQL 16.4.0 集群。

## 常见使用场景

- 为 Tailscale 兼容客户端运行私有控制平面。
- 连接家庭实验室、边缘节点和团队设备。
- 通过 Headplane 管理用户、路由、DNS、ACL 和预授权密钥。
- 将控制平面状态保存在 Sealos 持久化存储中。
- 为特定数据库运维需求使用托管 PostgreSQL。

## 依赖

模板包含完整的服务端运行环境：Headscale、Headplane、持久卷、Service 与 Ingress、限定权限的 Kubernetes RBAC，以及条件启用的 PostgreSQL 资源。

- [Headscale 0.29.2](https://github.com/juanfont/headscale/releases/tag/v0.29.2) 提供控制服务器和 API。
- [Headplane 0.7.0](https://github.com/tale/headplane/releases/tag/v0.7.0) 提供管理界面。
- 启用 `use_postgresql` 后，KubeBlocks 会提供 PostgreSQL 16.4.0。
- 每台接入网络的设备需要安装兼容的 [Tailscale 客户端](https://tailscale.com/download)。

## 架构

| 组件 | 版本 | 用途 | 实测最低限制 |
| --- | --- | --- | --- |
| Headscale | `0.29.2-debug` | 控制服务器、REST API、gRPC API 和指标 | `100m` CPU / `128Mi` 内存 |
| Headplane | `0.7.0` | Web 管理界面 | `100m` CPU / `256Mi` 内存 |
| SQLite | 内置 | 位于持久化存储中的默认 Headscale 数据库 | 包含在 Headscale 容器中 |
| PostgreSQL | `16.4.0` | 可选的 KubeBlocks 托管数据库 | `500m` CPU / `512Mi` 内存 |
| PostgreSQL 初始化 | `postgres:16-alpine` | 创建并验证 `headscale` 数据库 | `100m` CPU / `128Mi` 内存 |

应用使用三个 `512Mi` 持久卷：

| 路径 | 内容 |
| --- | --- |
| `/var/lib/headscale` | SQLite 数据库、密钥和 Headscale 运行状态 |
| `/etc/headscale` | 经过校验且不含敏感值的 Headscale 配置 |
| `/var/lib/headplane` | Headplane 状态 |

主公网域名提供 Headscale HTTP API，并在 `/admin/` 路径提供 Headplane。独立公网域名提供 Headscale gRPC 端点。指标端口 `9090` 仅在集群内部开放。

## 为什么在 Sealos 上部署 Headscale？

- 从应用商店模板一次部署完整的 Headscale 与 Headplane 服务。
- 自动获得带托管 TLS 证书的 HTTPS 应用域名和 gRPC 域名。
- 使用持久卷保存配置、密钥和数据库状态。
- 部署时可以选择内置 SQLite 或 KubeBlocks 托管 PostgreSQL。
- 在 Sealos Canvas 中查看资源、日志、事件并使用容器终端。
- 从实测最低资源起步，并随 tailnet 规模增长调整容量。

## 在 Sealos 上部署

1. 打开 [Headscale 模板](https://sealos.io/products/app-store/headscale)，点击 **Deploy Now**。
2. 保持 `use_postgresql` 关闭即可使用默认 SQLite；启用该选项会创建独立 PostgreSQL 集群。
3. 等待全部资源进入就绪状态。SQLite 通常在几分钟内启动，新建 PostgreSQL 集群的首次初始化可能需要数分钟。
4. 打开应用地址，根路径会跳转到 `/admin/` 下的 Headplane 登录页。

## 登录 Headplane

Headplane 使用 Headscale API key 完成身份验证。在 Sealos 终端中进入 Headscale 容器并执行：

```bash
headscale apikeys create
```

命令只显示一次密钥。请妥善保存，并将完整密钥粘贴到 Headplane 登录页的 **API Key** 输入框。Headscale 默认给新密钥设置 90 天有效期，也可以指定有效期：

```bash
headscale apikeys create --expiration 365d
```

登录后完成以下操作：

1. 打开 **Users**，点击 **Add user**，创建第一个 Headscale 用户。
2. 打开 **Settings > Auth Keys**，点击 **Create pre-auth key**，选择用户并设置有效期与密钥选项。

## 连接设备

安装兼容的 Tailscale 客户端，然后使用 Sealos 主应用地址和 Headplane 中创建的预授权密钥：

```bash
tailscale up \
  --login-server=https://your-headscale-domain.example.com \
  --authkey=<pre-auth-key>
```

注册完成后，设备会出现在 Headplane 的 **Machines** 页面。

## 远程使用 Headscale CLI

模板通过独立 TLS 域名提供 gRPC。使用与服务端 `0.29.2` 版本一致的 `headscale` CLI，并配置端点和 API key：

```bash
export HEADSCALE_CLI_ADDRESS=your-headscale-grpc-domain.example.com:443
export HEADSCALE_CLI_API_KEY=<api-key>
headscale users list
```

Headplane 已覆盖常用管理流程，远程 gRPC 适合 CLI 自动化场景。

## 数据库选项

### SQLite

SQLite 默认启用，数据库位于 `/var/lib/headscale/db.sqlite`。模板开启 write-ahead logging，持久卷会在 Pod 重建后保留数据。

### PostgreSQL

部署时启用 `use_postgresql` 即可创建 KubeBlocks PostgreSQL 集群。模板会创建 `headscale` 数据库并等待数据库接受认证查询。Headscale 通过官方 `HEADSCALE_DATABASE_POSTGRES_*` 环境变量，直接从 KubeBlocks Secret 获取主机、端口、用户名和密码。

Kubernetes Secret 是凭据来源，`/etc/headscale/config.yaml` 只保存静态且不敏感的数据库设置。PostgreSQL 会增加一个数据库 Pod 和一个 `1Gi` 数据卷。初始化 Job 为数据库冷启动预留最多 6 分钟。

## 配置

- 使用 Headplane 管理用户、设备、路由、DNS、ACL 策略和预授权密钥。
- Headscale 从持久化存储中的 `/etc/headscale/config.yaml` 读取配置。init 容器会校验数据库模式、占位符和完整 Headscale 配置，再通过同目录原子移动修复不完整文件。
- Headplane 从模板 ConfigMap 中的 `/etc/headplane/config.yaml` 读取配置。
- Headplane 通过 `HEADPLANE_SERVER__COOKIE_SECRET` 接收生成的 cookie secret，使该值与 ConfigMap 分离。
- PostgreSQL 凭据直接从 KubeBlocks 连接 Secret 注入 Headscale 容器，并与持久卷分离。
- `shareProcessNamespace` 和限定为 Pod 读取权限的 RBAC 支持 Headplane 在配置变更后通知 Headscale。
- Pod 使用 UID/GID `1000` 运行，启用 `RuntimeDefault` seccomp，并移除全部 Linux capabilities。

## 故障排查

### Headplane 拒绝 API key

在 Headscale 容器中创建新的 API key，并将完整值粘贴到登录表单。API key 只显示一次，并会按照设置的有效期过期。

### 客户端注册失败

确认 `--login-server` 使用主 HTTPS 应用地址，预授权密钥也归属于现有用户。可以在 Headplane 的 **Machines** 和 **Auth Keys** 页面检查状态。

### PostgreSQL 部署仍在初始化

打开 Sealos Canvas，检查 PostgreSQL Cluster、`*-pg-init` Job 和 Headscale StatefulSet。数据库可以接受认证查询且 `headscale` 数据库创建完成后，应用会自动启动。

### 健康检查

使用以下端点检查两个应用容器：

```text
https://your-headscale-domain.example.com/health
https://your-headscale-domain.example.com/admin/healthz
```

## 相关资源

- [Headscale 官方文档](https://headscale.net/stable/)
- [Headscale API 文档](https://headscale.net/stable/ref/api/)
- [Headscale GitHub 仓库](https://github.com/juanfont/headscale)
- [Headplane 官方文档](https://headplane.net/)
- [Headplane GitHub 仓库](https://github.com/tale/headplane)
- [Tailscale 文档](https://tailscale.com/kb/)
- [Sealos 文档](https://sealos.io/docs/)

## 许可证

Headscale 使用 BSD-3-Clause 许可证，Headplane 使用 MIT 许可证。本模板遵循 Sealos templates 仓库许可证。
