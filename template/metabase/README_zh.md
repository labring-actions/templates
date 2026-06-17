# 在 Sealos 上部署和托管 Metabase

Metabase 是一个开源商业智能平台，适用于仪表盘、SQL 探索和自助式数据分析。本模板会在 Sealos Cloud 上部署 Metabase 0.61.3，并配套 PostgreSQL、持久化插件存储和公开 HTTPS 访问入口。

![Metabase 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/metabase/website-screenshot.webp)

## 关于托管 Metabase

Metabase 可以帮助团队连接数据库、提出数据问题、创建仪表盘并共享分析结果，不要求每个用户都编写 SQL。它适合内部报表、产品分析、运营指标和轻量级嵌入式 BI 场景。

此 Sealos 模板会将 Metabase 作为 StatefulSet 运行，并创建一个 Kubeblocks PostgreSQL 数据库存储 Metabase 应用数据。模板还会把持久化卷挂载到 `/plugins`，用于保留自定义数据库驱动和插件文件。

Sealos 会自动配置 Kubernetes Service、HTTPS Ingress、生成的公网 URL 和 App 入口。首次访问时，Metabase 会显示初始化流程，用于创建第一个管理员账号并完成工作区配置。

## 常见使用场景

- **自助式 BI**：让业务用户探索数据、保存问题并创建仪表盘。
- **运营仪表盘**：跟踪收入、产品使用、支持队列或基础设施数据。
- **SQL 探索**：为分析师提供浏览器中的 SQL 编辑器和可共享结果集。
- **嵌入式报表**：向团队成员和相关方共享仪表盘或问题。
- **内部分析门户**：在不运行大型 BI 技术栈的情况下集中管理团队指标。

## Metabase 托管依赖

此 Sealos 模板包含运行所需的组件：Metabase 容器镜像、PostgreSQL `postgresql-16.4.0` 数据库、用于创建 `metabaseappdb` 的数据库初始化 Job、持久化插件存储、Kubernetes Service、Ingress 和 Sealos App 入口。

### 部署依赖

- [Metabase 官网](https://www.metabase.com/) - 产品概览和商业版本说明
- [Metabase 文档](https://www.metabase.com/docs/latest/) - 管理、初始化和用户文档
- [Metabase GitHub 仓库](https://github.com/metabase/metabase) - 源码与版本发布
- [Metabase Docker 镜像](https://hub.docker.com/r/metabase/metabase) - 官方容器镜像标签

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **Metabase Web 服务**：运行 `metabase/metabase:v0.61.3`，监听 `3000` 端口，提供 Web UI、API 和后台应用任务。
- **PostgreSQL**：由 Kubeblocks 管理的 PostgreSQL `postgresql-16.4.0`，用于存储 Metabase 用户、权限、仪表盘元数据、问题和已保存设置。
- **PostgreSQL 初始化 Job**：在 PostgreSQL 就绪后，以幂等方式创建 `metabaseappdb` 数据库。
- **持久化插件存储**：挂载到 `/plugins` 的 `1Gi` 卷，用于在重启后保留自定义驱动和插件文件。
- **Ingress 与 App 入口**：Sealos 通过 HTTPS 域名暴露 Metabase，并在仪表盘中创建应用入口。

**配置：**

模板会从 Kubeblocks 连接 Secret 中读取 PostgreSQL 环境变量并配置 Metabase：

- `MB_DB_TYPE=postgres`
- `MB_DB_DBNAME=metabaseappdb`
- `MB_DB_HOST`、`MB_DB_PORT`、`MB_DB_USER` 和 `MB_DB_PASS` 来自 `${{ defaults.app_name }}-pg-conn-credential`
- `JAVA_OPTS=-XX:MaxRAMPercentage=75 -XX:InitialRAMPercentage=25`，用于在容器限制内稳定设置 JVM 大小

部署时不需要填写必填参数。第一个管理员创建完成后，可以在 Metabase 管理界面中配置数据库连接、用户、SSO、邮件和嵌入式分析设置。

**许可证信息：**

Metabase 开源版使用 AGPLv3 License。此 Sealos 模板只是 Metabase 的部署配置，不改变上游应用许可证。

## 为什么在 Sealos 上部署 Metabase？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，覆盖从云端开发到生产部署和运维管理的完整应用生命周期。在 Sealos 上部署 Metabase 可以获得：

- **一键部署**：通过一个模板同时部署 Metabase、PostgreSQL、存储、网络和 App 入口。
- **无需 Kubernetes 经验**：不用手写清单，也能获得 Kubernetes 的可靠性。
- **内置持久化存储**：Metabase 元数据保存在 PostgreSQL 中，插件文件保存在持久化存储中。
- **即时公网访问**：每次部署都会获得 HTTPS URL，可用于初始化、登录和仪表盘共享。
- **易于自定义**：可通过 Sealos Canvas 和 AI 对话调整资源、环境变量和存储。
- **按量使用资源**：从经过验证的资源规格起步，并在使用量增长时扩容。

在 Sealos 上部署 Metabase，可以把精力放在数据分析本身，而不是基础设施维护上。

## 部署指南

1. 打开 [Metabase 模板](https://sealos.io/products/app-store/metabase)，点击 **Deploy Now**。
2. 除非需要自定义生成名称或访问域名，否则保留默认参数即可。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续如需修改，可在 AI 对话框中描述需求，或点击对应资源卡片调整配置。
4. 从 App 入口打开生成的 Metabase URL。
5. 完成首次初始化向导：
   - 输入首个管理员的姓名、邮箱地址和密码。
   - 设置组织或站点名称。
   - 选择是否立即连接第一个分析数据库，也可以跳过后续再添加。
   - 检查使用数据偏好并完成初始化。
6. 初始化完成后，后续可在登录页使用同一个管理员邮箱和密码登录。

本模板不会创建公开自助注册流程。初始化过程中创建的第一个用户会成为管理员。

## 配置

部署后，你可以通过以下方式配置 Metabase：

- **初始化向导**：创建首个管理员账号和基础站点设置。
- **Metabase 管理设置**：添加数据源、用户、用户组、权限、邮件、SSO、嵌入式分析和本地化设置。
- **Sealos AI 对话**：描述环境变量、资源或存储调整需求，让 AI 协助修改。
- **资源卡片**：在 Canvas 中点击 StatefulSet、PostgreSQL、Ingress 或存储卡片，查看并调整配置。

如果需要添加自定义数据库驱动，请将驱动 JAR 上传到 `/plugins` 并重启 Metabase 工作负载。数据库凭据应保存在 Metabase 或 Sealos 管理的配置中，不要提交到模板仓库。

## 扩展

在 Sealos 上扩展 Metabase：

1. 打开 Metabase 部署对应的 Canvas。
2. 点击 Metabase StatefulSet 资源卡片。
3. 当启动、迁移、仪表盘渲染或并发查询需要更多容量时，提高 CPU 或内存资源。
4. 如果元数据或插件使用量增长，可提高 PostgreSQL 或存储资源。
5. 应用变更并等待 Pod 重新就绪。

默认应用规格为 `1` CPU 和 `2G` 内存。实际验证显示，Metabase 0.61.3 使用 `1024Mi` 时可能在冷启动或重启过程中失败；`2G` 已通过冷启动、首次初始化、重启和登录检查。

## 故障排查

### 应用打开后进入初始化向导

这是新部署的正常行为。请完成向导并创建首个管理员账号。初始化完成后，未登录访问会显示登录页。

### 应用启动慢或启动期间重启

Metabase 冷启动时会执行 JVM 启动和数据库迁移。首次部署时请等待几分钟。如果工作负载重启或仪表盘运行缓慢，请先在 StatefulSet 资源卡片中提高内存，再按需提高 CPU。

### 无法连接分析数据库

请在 Metabase 管理设置中检查目标数据库的主机、端口、用户名、密码、网络访问和 TLS 要求。若数据库需要自定义 JDBC 驱动，请将驱动文件放入 `/plugins` 并重启工作负载。

### 获取帮助

- [Metabase 文档](https://www.metabase.com/docs/latest/)
- [Metabase 故障排查指南](https://www.metabase.com/docs/latest/troubleshooting-guide/)
- [Metabase GitHub Issues](https://github.com/metabase/metabase/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Metabase 初始化指南](https://www.metabase.com/docs/latest/configuring-metabase/setting-up-metabase)
- [Metabase 管理指南](https://www.metabase.com/docs/latest/configuring-metabase/)
- [使用 Docker 运行 Metabase](https://www.metabase.com/docs/latest/installation-and-operation/running-metabase-on-docker)

## 许可证

此 Sealos 模板遵循仓库中的模板许可证。Metabase 开源版本身使用 AGPLv3。
