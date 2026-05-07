# 在 Sealos 上部署并托管 Project Quay

Project Quay 是一款企业级容器镜像仓库，用于存储、保护和分发 OCI 镜像。该模板会在 Sealos Cloud 上一次性部署 Quay、PostgreSQL、Redis、持久化存储，以及首个管理员自动初始化流程。

## 关于在 Sealos 上托管 Project Quay

Project Quay 提供私有仓库管理、机器人账号（robot account）、漏洞与元数据能力，并支持基于应用程序接口（API）的 CI/CD 自动化集成。在本模板中，Quay 以 StatefulSet 方式运行，镜像数据持久化挂载到 `/datastorage`，确保重启后数据不丢失。

部署过程中还会自动创建 PostgreSQL 16.4.0（Kubeblocks）和 Redis 7.2.7（含 Sentinel 的主从拓扑）作为后端依赖。模板内置 PostgreSQL 初始化任务用于启用扩展，同时通过管理员初始化任务在首次部署时创建第一个 Quay 管理员账号。

Sealos 会自动分配公网 HTTPS 域名并配置 Ingress 路由，你无需手动申请证书或编写网关规则，就能直接开始推送和拉取镜像。

## 常见使用场景

- **私有镜像仓库**：托管开发、测试、生产环境的内部镜像。
- **CI/CD 镜像分发**：统一存放构建产物，打通自动化流水线。
- **多团队仓库治理**：按组织与权限模型管理团队访问。
- **安全镜像交付**：通过 HTTPS 对外提供统一镜像入口。
- **自建仓库迁移**：从零散脚本部署迁移到 Kubernetes 原生托管方案。

## 托管 Project Quay 的依赖组件

该 Sealos 模板已包含生产可用的单实例 Quay 所需核心依赖：

- Project Quay（`quay.io/projectquay/quay:v3.9.8`）
- PostgreSQL 16.4.0（Kubeblocks 集群）
- Redis 7.2.7 + Sentinel（Kubeblocks 集群）
- 镜像数据持久化存储卷
- Kubernetes Ingress（TLS 终止）

### 部署依赖参考

- [Project Quay 官方文档](https://docs.projectquay.io/) - Quay 使用与运维文档
- [Project Quay GitHub 仓库](https://github.com/quay/quay) - 源码与问题跟踪
- [OCI Distribution 规范](https://github.com/opencontainers/distribution-spec) - 镜像分发协议参考
- [Sealos 文档](https://sealos.run/docs) - 平台能力与运维指南

## 实现细节

### 架构组件

该模板会部署以下组件：

- **Quay StatefulSet**：主服务，提供 Web UI、API 与镜像仓库端点。
- **PostgreSQL 集群**：存储 Quay 元数据与业务数据。
- **PostgreSQL 初始化任务**：启用 Quay 依赖的 `pg_trgm` 扩展。
- **Redis 集群（主从 + Sentinel）**：承担缓存、事件与队列相关能力。
- **管理员初始化任务**：等待 Quay 健康检查通过后，通过 API 初始化首个管理员。
- **持久化存储**：通过 PVC 将仓库数据持久化到 `/datastorage/registry`。

### 配置说明

- Quay 启动时会基于环境变量和密钥引用动态生成 `config.yaml`。
- 健康检查使用 `8080` 端口 HTTP 接口（`/health/instance`、`/health/endtoend`）。
- TLS 在 Sealos Ingress 层终止（`EXTERNAL_TLS_TERMINATION: true`），后端服务走 HTTP。
- 部署时需要填写初始化管理员输入参数：
  - `initial_admin_username`
  - `initial_admin_password`
  - `initial_admin_email`
- 管理员初始化任务具备幂等性：若数据库已初始化，会安全退出，不覆盖既有账号。

### 许可证信息

Project Quay 采用 Apache License 2.0 许可证。

## 为什么在 Sealos 上部署 Project Quay？

Sealos 是构建在 Kubernetes 之上的 AI 驱动云操作系统，覆盖从部署到运维的完整生命周期。在 Sealos 上部署 Project Quay，你可以获得：

- **一键部署**：Quay 与数据库、缓存依赖一次完成交付。
- **托管数据库能力**：PostgreSQL 与 Redis 自动创建、自动接线。
- **持久化保障**：仓库数据可跨重启、跨升级保留。
- **自动 HTTPS 访问**：系统自动生成公网域名与 TLS 入口。
- **简化运维**：通过 Canvas + AI 对话即可做日常调整。
- **按量使用**：按实际资源消耗计费，成本更可控。

## 部署指南

1. 打开 [Project Quay 模板页面](https://sealos.io/products/app-store/quay)，点击 **Deploy Now**。
2. 在弹窗中配置参数，重点填写：
   - `initial_admin_username`
   - `initial_admin_password`
   - `initial_admin_email`
3. 等待部署完成（通常 2-3 分钟）。部署完成后会跳转到 Canvas，后续可通过 AI 对话或资源卡片继续调整。
4. 通过系统生成的地址访问应用：
   - **Quay Web UI**：`https://<your-app-host>`
   - **Registry/API 端点**：同一域名，可供 Docker/OCI 客户端与自动化系统调用
5. 使用第 2 步中设置的管理员账号密码登录。

## 配置

部署完成后，你可以通过以下方式调整 Quay：

- **AI 对话**：用自然语言描述需要变更的配置或资源。
- **资源卡片**：直接修改 StatefulSet、存储、任务和网络配置。
- **Quay 管理后台**：创建组织、仓库、机器人账号与访问策略。

## 扩缩容

该模板默认面向“单实例 + 本地持久化存储”的 Quay 部署形态。

1. 打开对应部署的 Canvas。
2. 点击 Quay StatefulSet 资源卡片。
3. 根据流量和仓库规模调整 CPU/内存。
4. 应用变更。

如果需要多副本 Registry，请切换为外部共享对象存储方案，并同步调整 Quay 的存储配置。

## 故障排查

### 常见问题

**问题：部署后无法登录**
- 原因：部署时未正确设置管理员初始化参数。
- 处理：使用明确的 `initial_admin_*` 参数重新部署，或按 Quay 管理/数据库流程重置账号。

**问题：管理员初始化任务提示 non-empty database 后退出**
- 原因：Quay 数据库中已有用户或历史数据。
- 处理：这是预期行为；初始化任务会跳过创建，避免覆盖已有账号。

**问题：仓库存储写入失败**
- 原因：自定义调整后导致挂载路径或权限不匹配。
- 处理：确认仓库路径保持为 `/datastorage/registry`，并确保 PVC 可写、security context 配置正确。

### 获取帮助

- [Project Quay 文档](https://docs.projectquay.io/)
- [Project Quay Issues](https://github.com/quay/quay/issues)
- [Sealos Discord 社区](https://discord.gg/wdUn538zVP)

## 更多资源

- [Quay API 与集成文档](https://docs.projectquay.io/api/)
- [Quay 安全与架构文档](https://docs.projectquay.io/solution/georep.html)
- [Sealos 应用部署与管理](https://sealos.run/docs)

## License

该 Sealos 模板采用 MIT License。Project Quay 本身采用 Apache License 2.0。
