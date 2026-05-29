# 在 Sealos 上部署和托管 Dolibarr

Dolibarr 是一套开源 ERP 与 CRM 系统，可用于管理客户、供应商、发票、订单、库存、项目和日常业务运营。该模板会在 Sealos Cloud 上部署 Dolibarr、托管 MySQL 数据库和应用持久化存储。

## 关于 Dolibarr 托管

Dolibarr 是基于 Web 的业务管理系统，后端依赖关系型数据库。该 Sealos 模板会自动创建 Dolibarr 应用、由 Kubeblocks 管理的 MySQL 集群、用于上传文件和自定义模块的持久化卷，并通过 Sealos Ingress 提供公开 HTTPS 访问地址。

该部署已配置首次启动自动安装流程。部署时填写管理员用户名、管理员密码、公司名称、国家代码和初始模块后，Dolibarr 会创建数据库结构、初始化公司资料、启用常用业务模块，并通过 Sealos 分配的域名提供 Web 界面。

## 常见使用场景

- **CRM 与联系人管理**：管理客户、供应商、联系人、商机和客户活动。
- **开票与收款**：创建发票、管理付款，并跟进客户账单流程。
- **库存与产品目录**：维护产品、服务、库存记录和相关商业单据。
- **项目运营**：组织项目、任务、业务记录和内部协作。
- **小型企业 ERP**：在一个浏览器应用中运行核心后台业务流程。

## Dolibarr 托管依赖

该 Sealos 模板包含运行 Dolibarr 所需的依赖：Dolibarr PHP 应用运行环境、MySQL 数据库资源、数据库初始化任务、持久化卷、内部服务发现和公开访问入口。

### 部署依赖

- [Dolibarr 官方网站](https://www.dolibarr.org/) - 产品概览和社区信息
- [Dolibarr 文档](https://wiki.dolibarr.org/) - 官方用户和管理员文档
- [Dolibarr Docker 仓库](https://github.com/Dolibarr/dolibarr-docker) - Docker 镜像与环境变量配置
- [Sealos 文档](https://sealos.io/docs) - 平台指南和运维文档

### 实现细节

**架构组件：**

该模板会部署以下服务：

- **Dolibarr StatefulSet**：主应用服务，运行按 digest 固定的 `dolibarr/dolibarr:23.0.3-php8.2` 镜像。
- **MySQL 集群**：由 Kubeblocks 管理的 ApeCloud MySQL `ac-mysql-8.0.30-1`，用于持久化关系型数据。
- **MySQL 初始化任务**：在应用执行自动安装流程前创建 `dolibarr` 数据库。
- **Service + Ingress**：内部服务监听 `80` 端口，公开 HTTPS Ingress 负责 Sealos 域名路由。
- **持久化存储**：PVC 挂载到 `/var/www/documents` 和 `/var/www/html/custom`。

**配置说明：**

- 数据库连接信息由 Kubeblocks 生成的 MySQL Secret 注入。
- `DOLI_INSTALL_AUTO=1` 启用首次启动自动安装和数据库结构创建。
- `DOLI_ADMIN_LOGIN` 与 `DOLI_ADMIN_PASSWORD` 定义首个管理员账号。
- `DOLI_COMPANY_COUNTRYCODE` 与 `DOLI_ENABLE_MODULES` 用于完成初始公司设置并启用常用模块。
- Dolibarr 应用容器已通过线上冷启动部署验证，最小资源为 `100m` CPU 和 `128Mi` 内存。托管 MySQL 集群使用 `500m` CPU 和 `512Mi` 内存。

**许可证信息：**

Dolibarr 使用 GNU General Public License v3.0 或更高版本授权。

## 为什么在 Sealos 上部署 Dolibarr？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一了从部署到生产运维的应用生命周期。在 Sealos 上部署 Dolibarr 可以获得：

- **一键部署**：无需手动配置 Kubernetes，即可启动 Dolibarr 及数据库栈。
- **托管数据库体验**：使用 Kubeblocks MySQL，并通过标准 Secret 和服务发现完成连接。
- **内置持久化存储**：上传文件和自定义模块在 Pod 重启后仍可保留。
- **即时公开访问**：平台 Ingress 自动提供带 TLS 的公开域名。
- **易于定制**：可在 Canvas 对话中调整资源和环境变量。
- **无需 Kubernetes 专业知识**：不用手写基础设施 YAML，也能获得 Kubernetes 的可靠性。
- **AI 辅助运维**：可使用 Canvas AI 对话完成部署后的常规调整。

在 Sealos 上部署 Dolibarr，可以把精力放在业务流程上，而不是基础设施维护上。

## 部署指南

1. 打开 [Dolibarr 模板](https://sealos.io/products/app-store/dolibarr)，点击 **Deploy Now**。
2. 在弹窗中配置部署参数：
   - `DOLI_ADMIN_LOGIN`：首次启动时创建的管理员用户名，默认值为 `admin`。
   - `DOLI_ADMIN_PASSWORD`：首次启动时创建的管理员密码，部署前请设置强密码。
   - `DOLI_COMPANY_NAME`：初始 Dolibarr 设置使用的公司名称。
   - `DOLI_COMPANY_COUNTRYCODE`：两个字母的国家代码，例如 `US`、`CN` 或 `DE`。
   - `DOLI_ENABLE_MODULES`：首次启动时启用的模块列表，用英文逗号分隔。默认会启用公司、发票、库存和项目功能。
3. 等待部署完成。Dolibarr 首次冷启动会执行数据库初始化，因此首次启动可能需要几分钟。
4. 部署完成后，从应用卡片打开生成的 Dolibarr 访问地址。
5. 使用部署时配置的 `DOLI_ADMIN_LOGIN` 和 `DOLI_ADMIN_PASSWORD` 登录。首个管理员账号会在首次启动时自动创建，不需要单独注册。
6. 首次登录后，请根据安全策略创建其他用户，并轮换管理员密码。

## 配置

部署后可通过以下方式配置 Dolibarr：

- **Canvas AI 对话**：描述需要的调整，让 AI 协助更新部署配置。
- **资源卡片**：打开 StatefulSet、Service、Ingress 或数据库卡片，调整资源和环境变量。
- **Dolibarr 设置与管理菜单**：在 Web 界面中配置公司资料、用户、模块、权限、邮件设置和业务流程。

## 扩缩容

调整 Dolibarr 资源：

1. 在 Canvas 中打开该部署。
2. 点击 Dolibarr StatefulSet 资源卡片。
3. 调整 CPU 和内存的限制与请求值。
4. 应用更新并观察滚动发布状态。

大多数 Dolibarr 场景建议保持单个应用副本，并优先纵向扩容，因为上传文件和自定义模块存储在 StatefulSet 挂载的持久化卷中。

## 故障排查

### 常见问题

**问题：首次启动时间较长**
- 原因：Dolibarr 会在首次启动时创建数据库表并初始化模块。
- 解决方法：等待 StatefulSet Pod 进入就绪状态；如果超过探针窗口仍未就绪，请查看应用日志。

**问题：提交账号密码后仍返回登录页**
- 原因：用户名或密码与部署输入不一致。
- 解决方法：使用部署时配置的 `DOLI_ADMIN_LOGIN` 和 `DOLI_ADMIN_PASSWORD` 登录。

**问题：Dolibarr 提示设置未完成**
- 原因：必要的公司或模块设置缺失，或被错误修改。
- 解决方法：检查 `DOLI_COMPANY_NAME`、`DOLI_COMPANY_COUNTRYCODE` 和 `DOLI_ENABLE_MODULES`，然后在 Dolibarr 管理界面完成剩余设置。

**问题：数据库连接错误**
- 原因：MySQL 集群仍在初始化，或生成的 Secret 尚未就绪。
- 解决方法：在 Canvas 中检查 MySQL 集群和初始化任务状态，数据库健康后重启 Dolibarr Pod。

### 获取帮助

- [Dolibarr 文档](https://wiki.dolibarr.org/)
- [Dolibarr GitHub Issues](https://github.com/Dolibarr/dolibarr/issues)
- [Dolibarr Docker Issues](https://github.com/Dolibarr/dolibarr-docker/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [Dolibarr 用户文档](https://wiki.dolibarr.org/index.php/User_documentation)
- [Dolibarr 管理员文档](https://wiki.dolibarr.org/index.php/Admin_documentation)
- [Dolibarr Docker 环境变量](https://github.com/Dolibarr/dolibarr-docker)

## 许可证

Dolibarr 使用 GNU General Public License v3.0 或更高版本授权。
该 Sealos 模板遵循 templates 仓库的许可条款发布。
