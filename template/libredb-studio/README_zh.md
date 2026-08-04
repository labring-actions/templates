# 在 Sealos 上部署和托管 LibreDB Studio

LibreDB Studio 是一款开源数据库 IDE，可直接在浏览器中查询和管理 PostgreSQL、MySQL、SQLite、MongoDB 等数据源。此模板会在 Sealos Cloud 上部署 LibreDB Studio 0.9.66，并配置 HTTPS 入口、持久化服务端存储、健康检查和部署时创建的管理员账号。

![LibreDB Studio 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/libredb-studio/website-screenshot.webp)

## 关于 LibreDB Studio 托管

LibreDB Studio 将 Web 编辑器、Schema 浏览、结果查看、连接管理、监控页面和管理工具整合到一个应用中。默认部署使用 SQLite，将应用状态保存在 1 GiB 持久卷中。部署时也可以选择由 KubeBlocks 托管的独立 PostgreSQL 数据库，用于共享服务端状态。

PostgreSQL 选项保存 LibreDB Studio 的连接配置、收藏查询等应用数据。需要查看和管理的业务数据库仍作为独立数据源，登录后可在 LibreDB Studio 界面中添加。

## 常见使用场景

- **浏览器数据库工作台**：直接运行查询、查看 Schema，省去安装桌面客户端的步骤。
- **共享管理空间**：通过持久化服务端存储保留连接配置和收藏查询。
- **开发与调试**：在同一界面中检查应用数据库并分析查询结果。
- **自托管数据工具**：在自己的 Sealos 工作空间中运行 IDE，并获得自动生成的 HTTPS 地址。

## LibreDB Studio 托管依赖

模板包含可用部署所需的运行组件：

- **LibreDB Studio**：`ghcr.io/libredb/libredb-studio:0.9.66`
- **默认 SQLite 存储**：`/app/data/libredb-storage.db`，使用 1 GiB 应用 PVC
- **可选 PostgreSQL 存储**：KubeBlocks 托管的 `postgresql-16.4.0`，使用 1 GiB 数据 PVC
- **HTTPS 入口**：通过 Sealos Service、Ingress 和 App 资源暴露 `3000` 端口

### 部署依赖链接

- [LibreDB Studio 官网](https://libredb.org) - 产品信息
- [LibreDB Studio GitHub 仓库](https://github.com/LibreDB/libredb-studio) - 源码、版本发布和问题追踪
- [Sealos Cloud](https://cloud.sealos.io) - 云工作空间与 App Launchpad
- [Sealos 文档](https://sealos.io/docs) - 部署与运维指南

### 实现细节

**架构组件：**

- **LibreDB Studio StatefulSet**：运行一个应用副本，并将持久卷挂载到 `/app/data`。
- **SQLite 模式**：默认选择，将服务端应用状态持久化到应用 PVC。
- **PostgreSQL 模式**：创建 PostgreSQL 集群、数据库访问资源、`libredb_storage` 初始化 Job 和数据库就绪检查容器。
- **Service + Ingress + App**：将生成的 HTTPS 域名路由到应用，并打开 `/login` 页面。
- **健康检查**：使用上游 `/api/db/health` 接口执行启动、就绪和存活探测。

**资源基线：**

Sealos 实测确认应用的稳定最低档位为 `100m` CPU 和 `128Mi` 内存。PostgreSQL 初始化容器和 Job 使用相同档位；可选 PostgreSQL 集群使用 `500m` CPU 和 `512Mi` 内存。两种存储模式均通过冷启动、管理员登录、页面操作、服务端存储写读、查询执行和重启持久化验证。

**安全默认值：**

应用以非 root 用户运行，移除 Linux capabilities，关闭 ServiceAccount Token 挂载，并使用自动生成的 JWT 签名密钥。管理员账号来自必填的部署参数。

## 为什么在 Sealos 上部署 LibreDB Studio？

Sealos 将 Kubernetes 部署、网络、存储和可视化运维集中在同一个云工作空间：

- **一键创建完整拓扑**：通过一个模板启动应用和选定的存储后端。
- **持久化应用状态**：可选择 PVC 支持的 SQLite 或托管 PostgreSQL 集群。
- **即时 HTTPS 访问**：部署完成后自动获得公网域名。
- **App Launchpad 与 Canvas 运维**：通过资源卡片查看工作负载、日志、存储和网络。
- **AI 辅助变更**：在 Canvas 对话中描述资源或配置调整。
- **按量使用资源**：从实测最低档位起步，随实际负载扩容。

## 部署指南

1. 打开 [LibreDB Studio 模板](https://sealos.io/products/app-store/libredb-studio)，点击 **Deploy Now**。
2. 输入管理员邮箱和至少 8 位的密码。
3. 默认关闭 **Use PostgreSQL storage**，应用将使用 SQLite；开启该选项会创建独立 PostgreSQL 后端。
4. 等待部署完成，通常需要 2-3 分钟。PostgreSQL 模式会在数据库集群和初始化 Job 完成后进入就绪状态。
5. 从 Canvas 应用卡片打开访问地址，系统会进入 `/login`。
6. 使用部署时填写的管理员邮箱和密码登录。

## 首次登录

此部署采用仅登录账号模式，模板会根据部署表单创建管理员。

1. 打开系统生成的应用地址。
2. 在 `/login` 页面输入已配置的管理员邮箱和密码。
3. 点击 **Sign In**，进入管理概览页。
4. 选择 **Editor**，添加数据库连接并执行查询。

建议将部署凭据保存到密码管理器。需要更换凭据时，可在 Canvas 中修改 LibreDB Studio StatefulSet 的环境变量，然后重启工作负载。

## 配置

| 参数 | 说明 | 状态 | 默认值 |
| --- | --- | --- | --- |
| `admin_email` | 登录页面使用的管理员邮箱 | 必填 | 部署时填写 |
| `admin_password` | 管理员密码，至少 8 个字符 | 必填 | 部署时填写 |
| `enable_postgres_storage` | 为 LibreDB Studio 服务端状态创建 PostgreSQL | 可选 | `false`（SQLite） |

模板会自动生成应用名称、公网域名和 JWT 签名密钥。SQLite 数据保存在 `/app/data/libredb-storage.db`；PostgreSQL 模式会创建 `libredb_storage` 数据库，并通过 KubeBlocks 凭据 Secret 拼装连接地址。

## 扩缩容

模板保持一个 LibreDB Studio 副本，可在 Canvas 中纵向扩容。并发会话或大型结果集增加时，可提升应用 CPU 和内存。应用状态增长时，可按存储模式扩展应用 PVC 或 PostgreSQL 数据 PVC。

多副本架构需要 PostgreSQL 服务端存储，并需复核会话处理和应用运行方式。当前模板采用已经验证的单副本拓扑。

## 故障排查

### 登录凭据校验失败

确认邮箱和密码与部署时填写的值一致。在 StatefulSet 资源卡片中检查 `ADMIN_EMAIL` 和 `ADMIN_PASSWORD`，应用目标值后重启工作负载。

### 应用页面仍在启动

在 Canvas 中检查 LibreDB Studio StatefulSet。PostgreSQL 模式还需确认 PostgreSQL 集群状态为 `Running`，并且 `-pg-init` Job 已进入 `Complete`。

### 重启后缺少已保存的设置

SQLite 模式应确认应用 PVC 已绑定并挂载到 `/app/data`。PostgreSQL 模式应确认集群健康，并且 `STORAGE_PROVIDER` 的值为 `postgres`。

### 数据库连接失败

填写 Sealos 工作空间可访问的数据库主机名，核对端口和凭据，并选择目标数据库要求的 TLS 设置。

### 获取帮助

- [LibreDB Studio GitHub Issues](https://github.com/LibreDB/libredb-studio/issues)
- [LibreDB Studio Releases](https://github.com/LibreDB/libredb-studio/releases)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [LibreDB Studio 官网](https://libredb.org)
- [LibreDB Studio 源代码](https://github.com/LibreDB/libredb-studio)
- [Sealos Cloud](https://cloud.sealos.io)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

LibreDB Studio 使用 MIT License。此 Sealos 模板遵循模板仓库许可证。
