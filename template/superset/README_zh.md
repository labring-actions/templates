# 在 Sealos 上部署和托管 Apache Superset

Apache Superset 是现代化数据探索与可视化平台。此模板在 Sealos Cloud 上部署 Superset，并包含托管 PostgreSQL、托管 Redis、持久化应用存储和公网 HTTPS 地址。

![Apache Superset 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/superset/website-screenshot.webp)

## 关于托管 Apache Superset

Superset 以 Web 应用运行，使用 PostgreSQL 保存元数据，使用 Redis 保存缓存、限流状态和异步运行时状态。模板包含数据库创建 Job 和 Superset 初始化 Job，用于执行迁移、创建管理员账号并初始化权限。

Sealos 通过托管 KubeBlocks 集群创建 PostgreSQL 16.4 和 Redis 7.2.7。Web 应用通过 HTTPS Ingress 发布，并通过 Sealos App 快捷入口访问。

## 常见使用场景

- **业务仪表盘**：构建和共享图表、仪表盘和 KPI 视图。
- **SQL 探索**：通过 SQL Lab 查询已连接数据库。
- **嵌入式分析**：作为团队内部分析层使用 Superset。
- **运营报表**：监控产品、销售、基础设施或财务数据。

## Apache Superset 托管依赖

Sealos 模板包含 Superset、PostgreSQL、Redis、配置 ConfigMap、初始化 Jobs、持久化存储和 HTTPS Ingress。

### 部署依赖

- [Apache Superset 文档](https://superset.apache.org/docs/intro) - 官方文档
- [Superset Docker 指南](https://superset.apache.org/docs/installation/docker-compose) - Docker 部署参考
- [Superset GitHub 仓库](https://github.com/apache/superset) - 源码与发布版本

### 实现细节

**架构组件：**

- **PostgreSQL 16.4**：在 `superset` 数据库中保存 Superset 元数据。
- **Redis 7.2.7**：保存缓存和限流状态。
- **PostgreSQL init Job**：幂等创建 `superset` 数据库。
- **Superset init Job**：运行 `superset db upgrade`，创建配置的管理员用户，并执行 `superset init`。
- **Superset StatefulSet**：在 `8088` 端口运行 Web 应用。
- **持久卷**：保存 `/app/superset_home`。

**配置：**

- 管理员用户名通过 `admin_username` 部署输入项配置。
- 管理员密码通过 `admin_password` 部署输入项配置。
- 管理员邮箱为 `admin@superset.local`。
- `SUPERSET_SECRET_KEY` 自动生成。

**许可证信息：**

Apache Superset 使用 Apache-2.0 许可证。此 Sealos 模板遵循仓库许可证。

## 为什么在 Sealos 上部署 Apache Superset？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一从云端 IDE 到生产部署和管理的完整应用生命周期。在 Sealos 上部署 Superset 可以获得：

- **一键部署**：同时部署 Superset、PostgreSQL 和 Redis。
- **托管依赖**：自动创建数据库和缓存服务。
- **已初始化管理员账号**：初始化 Job 完成后即可登录。
- **内置持久化存储**：重启后保留 Superset 状态。
- **即时公网访问**：无需手动配置 Ingress 即可使用公网 HTTPS 地址。

## 部署指南

1. 打开 [Apache Superset 模板](https://sealos.io/products/app-store/superset)，点击 **Deploy Now**。
2. 填写 `admin_username` 和 `admin_password`，然后部署。
3. 等待部署完成。部署完成后会跳转到 Canvas。
4. 打开 Superset 地址并使用以下信息登录：
   - **用户名**：部署表单中的 `admin_username` 值。
   - **密码**：部署表单中的 `admin_password` 值。
5. 从 **Settings > Database Connections** 添加第一个数据库连接。

## 配置

部署后可通过以下方式配置 Superset：

- **Superset UI**：添加数据库连接、数据集、图表、仪表盘和角色。
- **AI Dialog**：描述部署变更，让 Sealos 自动应用。
- **资源卡片**：调整 Superset、PostgreSQL、Redis、Service 和 Ingress 设置。

## 扩缩容

模板部署单个 Superset Web 副本，适合紧凑自托管场景。更高吞吐量场景建议先提高 CPU 和内存，再根据异步报表或长任务需求拆分 worker 和 beat 工作负载。

## 故障排查

### 无法登录

- 原因：初始化 Job 还在运行，或部署表单中的用户名、密码复制错误。
- 解决方法：等待 `superset-init` Job 完成，然后使用部署表单中的 `admin_username` 和 `admin_password` 登录。

### 数据库连接测试失败

- 原因：Superset 无法访问目标数据库，或基础镜像缺少对应驱动。
- 解决方法：检查目标数据库网络地址；需要额外驱动时使用自定义镜像。

## 其他资源

- [Superset 文档](https://superset.apache.org/docs/intro)
- [创建第一个仪表盘](https://superset.apache.org/docs/creating-charts-dashboards/creating-your-first-dashboard)
- [连接数据库](https://superset.apache.org/docs/configuration/databases)

## 许可证

此 Sealos 模板遵循仓库许可证。Apache Superset 本身使用 Apache-2.0 许可证。
