# 在 Sealos 上部署和托管 NocoDB

NocoDB 可以将数据库转换为协作式智能表格和无代码应用。此模板会在 Sealos Cloud 上部署 NocoDB，并自动创建 Kubeblocks 托管的 PostgreSQL 元数据库和持久化应用存储。

![NocoDB 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/nocodb/website-screenshot.webp)

## 关于托管 NocoDB

NocoDB 提供类似电子表格的界面，可用于创建表格、视图、表单、自动化和轻量级内部工具。它常被用作开源 Airtable 替代方案，适合希望基于数据库进行协作、但不想自行开发后台系统的团队。

此 Sealos 模板使用固定版本镜像 `nocodb/nocodb:2026.05.2` 运行 NocoDB Web 服务。Sealos 会创建 PostgreSQL `postgresql-16.4.0` 集群用于保存 NocoDB 元数据，并创建 `/usr/app/data` 持久卷、内部服务和带 HTTPS 的公网访问入口。

## 常见使用场景

- **内部数据工具**：为运营、客服和管理流程构建表格化操作界面。
- **无代码应用**：基于结构化数据创建表单、视图和协作界面。
- **数据库前端**：通过可视化界面管理 PostgreSQL、MySQL、MariaDB、SQLite、SQL Server 等数据库。
- **团队协作**：通过权限控制共享数据库工作区。

## NocoDB 托管依赖

此 Sealos 模板包含独立运行 NocoDB 所需的运行时依赖。

### 部署依赖

- [NocoDB 文档](https://docs.nocodb.com/) - 官方产品文档
- [NocoDB GitHub 仓库](https://github.com/nocodb/nocodb) - 源码和发布说明
- [NocoDB Docker 镜像](https://hub.docker.com/r/nocodb/nocodb) - 官方容器镜像

### 实现细节

**架构组件：**

- **NocoDB**：运行在 `8080` 端口的 Web 应用和 API 服务
- **PostgreSQL**：Kubeblocks 托管的 `postgresql-16.4.0` 集群，用于保存 NocoDB 元数据
- **持久化存储**：挂载到 `/usr/app/data` 的 `1Gi` 数据卷
- **Ingress**：Sealos 托管的 HTTPS 公网入口

**配置：**

- `NC_DB` 由 Kubeblocks PostgreSQL 连接密钥自动组装。
- `NC_PUBLIC_URL` 设置为生成的 Sealos HTTPS 地址。
- `NC_ADMIN_EMAIL` 和 `NC_ADMIN_PASSWORD` 用于初始化第一个管理员账号。

**许可证信息：**

NocoDB 使用 GNU Affero General Public License v3.0。请以官方仓库中的最新许可说明为准。

## 为什么在 Sealos 上部署 NocoDB？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用从开发、部署到运维的完整生命周期。它适合运行现代 Web 应用和数据库驱动工具。将 NocoDB 部署到 Sealos 后，你可以获得：

- **一键部署**：通过一个模板部署 NocoDB、PostgreSQL、持久化存储、服务和公网入口。
- **托管数据库**：使用 Kubeblocks PostgreSQL 集群，无需手动维护数据库 YAML。
- **内置持久化存储**：重启或重新调度后仍保留 NocoDB 本地数据。
- **即时公网访问**：部署完成后通过自动生成的 HTTPS 地址访问应用。
- **便捷自定义**：通过 Sealos 资源卡片或 AI 对话调整资源和环境变量。
- **降低 Kubernetes 使用复杂度**：底层运行在 Kubernetes 上，但可通过 Sealos 控制台管理。

## 部署指南

1. 打开 [NocoDB 模板](https://sealos.io/products/app-store/nocodb)，点击 **Deploy Now**。
2. 配置部署参数：
   - `NC_ADMIN_EMAIL`：初始管理员邮箱。
   - `NC_ADMIN_PASSWORD`：初始管理员密码。模板默认会生成随机值；打开 NocoDB 前请保存最终密码。
3. 等待部署完成，通常需要 2-4 分钟。完成后会跳转到 Canvas。
4. 从 App 卡片打开生成的 NocoDB 访问地址。
5. 使用部署时填写的 `NC_ADMIN_EMAIL` 和 `NC_ADMIN_PASSWORD` 登录。

## 配置说明

部署完成后，可以通过以下方式配置 NocoDB：

- **NocoDB 界面**：创建工作区、base、表格、视图、表单和集成。
- **AI 对话**：描述希望 Sealos 调整的资源配置。
- **资源卡片**：点击 StatefulSet、PostgreSQL 集群、Service 或 Ingress 卡片修改配置。

## 扩容说明

如需调整资源：

1. 打开此部署的 Canvas。
2. 点击 NocoDB StatefulSet 资源卡片。
3. 按需调整 CPU 或内存资源。
4. 在对话中应用变更。

此模板采用保守的单副本部署并使用持久化存储。修改副本数前，请先查阅 NocoDB 官方运行建议。

## 故障排查

### 无法登录

请确认使用的是部署时填写的 `NC_ADMIN_EMAIL` 和 `NC_ADMIN_PASSWORD`。如果保留了随机生成的密码，请从部署参数中复制该值。模板会在首次启动时初始化该账号。

### 应用仍在启动

首次冷启动时，NocoDB 需要等待 PostgreSQL 就绪并初始化元数据表，可能需要几分钟。请在 Sealos Canvas 中等待 NocoDB StatefulSet 显示为 `Ready`。

### 获取帮助

- [NocoDB 文档](https://docs.nocodb.com/)
- [NocoDB GitHub Issues](https://github.com/nocodb/nocodb/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [NocoDB 官网](https://nocodb.com/)
- [NocoDB API 文档](https://docs.nocodb.com/api-reference/introduction/)
- [NocoDB Docker Hub](https://hub.docker.com/r/nocodb/nocodb)

## 许可证

NocoDB 使用 AGPL-3.0 许可证。详情请参考上游项目。
