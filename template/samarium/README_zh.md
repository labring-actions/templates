# 在 Sealos 上部署和托管 Samarium

Samarium 是一个面向小型企业运营的开源 Laravel ERP 与 CMS。此模板会在 Sealos Cloud 上部署 Samarium，并配置 Apache/PHP、Laravel 持久化存储和托管 MySQL 数据库。

![Samarium 仪表盘](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/samarium/website-screenshot.webp)

## 关于托管 Samarium

Samarium 将 ERP 工作流和 CMS 页面整合到一个 Laravel 应用中。它提供销售、采购、库存、会计、客户、供应商、任务、日历、公告、图库和公开网站页面等仪表盘模块。

此 Sealos 模板会自动创建 Web 应用、KubeBlocks MySQL 数据库、Laravel 持久化存储、HTTPS Ingress 和启动探针。首次部署时，bootstrap 容器会执行数据库迁移、准备 Laravel 存储与缓存目录、创建初始管理员，并写入最小 CMS 数据，确保首页和仪表盘可直接使用。

## 常见使用场景

- **小型企业 ERP**：集中管理产品、库存、销售、采购、发票和基础会计数据。
- **客户与供应商运营**：统一维护客户、供应商、付款和交易记录。
- **销售点工作流**：为小团队提供轻量收银、结账和收据能力。
- **CMS 网站管理**：发布基础页面、导航、公告、图库和联系信息。
- **运营仪表盘**：无需手动维护 PHP、MySQL 或 Kubernetes，即可通过浏览器跟踪业务活动。

## Samarium 托管依赖

Sealos 模板包含 Samarium 托管所需的运行资源：

- **应用运行时**：Apache 与 PHP 8.2，镜像为 `ghcr.io/yangchuansheng/samarium:0.0.0-9514fcadb867`
- **数据库**：KubeBlocks MySQL 8.0 兼容单节点集群
- **持久化存储**：Laravel `storage` 和 `bootstrap/cache` 数据卷
- **网络访问**：Sealos HTTPS Ingress 和自动生成的公网 URL

### 部署依赖

- [Samarium GitHub 仓库](https://github.com/shyamsitaula/samarium) - 应用源码
- [Docker 镜像构建仓库](https://github.com/yangchuansheng/samarium-docker) - 此模板使用的可复现容器构建
- [Laravel 文档](https://laravel.com/docs) - 框架文档
- [Sealos 文档](https://sealos.io/docs) - Sealos 平台文档

## 实现细节

**架构组件：**

此模板会部署以下服务：

- **Samarium Web 应用**：单副本 StatefulSet，运行 Apache/PHP，监听 80 端口。
- **Bootstrap Init Container**：在主容器启动前执行 Laravel 迁移、创建初始管理员、准备存储，并清理不适合运行时保留的路由缓存。
- **MySQL 数据库**：KubeBlocks `apecloud-mysql` 集群，用于存储 Samarium 业务数据。
- **持久化卷**：分别挂载 `/var/www/html/storage` 和 `/var/www/html/bootstrap/cache`。
- **Ingress 与应用入口**：由 Sealos 管理的 HTTPS 访问入口和应用卡片。

**配置：**

- 数据库名为 `samarium`，连接凭据来自 KubeBlocks 连接密钥。
- 应用以 `APP_ENV=production`、`APP_DEBUG=false`、文件缓存、文件 Session 和同步队列运行。
- 初始管理员来自部署参数 `ADMIN_NAME`、`ADMIN_EMAIL` 和 `ADMIN_PASSWORD`。
- 经过线上部署调试，Web 容器最小资源为 `100m` CPU 和 `128Mi` 内存。bootstrap init 容器保留 `200m` CPU 和 `256Mi` 内存，用于迁移和首次初始化。MySQL 使用 `500m` CPU 和 `512Mi` 内存。

**登录与注册行为：**

请使用部署时配置的管理员邮箱和密码访问 `/login` 登录。`/register` 页面可用于创建额外标准用户，但自助注册账号可能进入 Samarium 的邮箱验证或资料补全流程，并且不是初始仪表盘管理员。仪表盘初始化和管理请使用配置的管理员账号。

## 为什么在 Sealos 上部署 Samarium？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，覆盖从部署到运维的应用生命周期。在 Sealos 上部署 Samarium 可以获得：

- **一键部署**：从模板页面启动，无需手动配置 PHP、Apache、MySQL 和 Kubernetes。
- **托管公网访问**：每个部署都会获得带自动证书处理的 HTTPS URL。
- **持久化数据**：数据库与 Laravel 存储卷可在重启和升级后保留数据。
- **易于定制**：可通过 Canvas 资源卡片或 AI 对话调整环境变量、资源限制、存储和网络。
- **资源高效**：按量使用 Kubernetes 资源，并采用经过线上部署验证的模板资源配置。
- **运维可见性**：可在 Sealos 工作区查看 Pod、日志、服务、Ingress 和数据库资源。

在 Sealos 上部署 Samarium，把精力放在业务流程，而不是基础设施维护上。

## 部署指南

1. 打开 [Samarium 模板](https://sealos.io/products/app-store/samarium)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - `ADMIN_NAME`：初始管理员显示名称。
   - `ADMIN_EMAIL`：用于登录的管理员邮箱。
   - `ADMIN_PASSWORD`：初始管理员密码。请使用至少 8 个字符，并在部署前妥善保存。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续如需调整配置，可以在 AI 对话中描述需求，或点击对应资源卡片修改设置。
4. 打开 Sealos 生成的公网应用 URL。
5. 在 `/login` 使用配置的管理员邮箱和密码登录。
6. 可选：打开 `/register` 创建额外标准用户。仪表盘管理请使用管理员账号。

## 配置

部署后，可以通过以下方式配置 Samarium：

- **Samarium 仪表盘**：以管理员身份登录后，管理 ERP、CMS、公司、产品、销售、采购和会计数据。
- **AI 对话**：在 Canvas 中描述部署后的变更需求，让 Sealos 协助应用修改。
- **资源卡片**：点击应用、StatefulSet、Ingress、存储或 MySQL 资源卡片调整设置。
- **管理员参数**：如果需要不同的初始管理员邮箱或密码，可以重新部署并设置新的 `ADMIN_EMAIL` 或 `ADMIN_PASSWORD`。

## 扩缩容

Samarium 将 Laravel Session、上传文件和缓存数据保存在持久化卷中。除非额外配置共享 Session 和共享文件存储，否则建议保持单副本运行。

调整资源步骤：

1. 打开当前部署的 Canvas。
2. 点击 Samarium StatefulSet 资源卡片。
3. 根据业务负载调整 CPU、内存或存储。
4. 通过对话或资源编辑器应用变更。

## 故障排查

### 注册后无法访问仪表盘

- 原因：自助注册用户不是初始管理员，且可能需要邮箱验证或额外资料配置。
- 解决：在 `/login` 使用部署时配置的 `ADMIN_EMAIL` 和 `ADMIN_PASSWORD` 登录。

### 首次启动时间较长

- 原因：bootstrap 容器会执行 Laravel 迁移、创建初始数据、准备存储权限，并预热部分 Laravel 缓存。
- 解决：在 Canvas 中等待应用 Pod 变为 Ready 后，再重新打开应用 URL。

### 公开页面可访问但仪表盘登录失败

- 原因：部署时输入的管理员邮箱或密码可能不正确。
- 解决：使用确定的 `ADMIN_EMAIL` 和 `ADMIN_PASSWORD` 重新部署，或在你自行管理数据库的情况下更新用户记录。

### 获取帮助

- [Samarium GitHub Issues](https://github.com/shyamsitaula/samarium/issues)
- [Sealos 文档](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Samarium 源码](https://github.com/shyamsitaula/samarium)
- [Samarium Docker 构建仓库](https://github.com/yangchuansheng/samarium-docker)
- [Laravel 文档](https://laravel.com/docs)
- [MySQL 文档](https://dev.mysql.com/doc/)

## 许可证

此 Sealos 模板遵循 templates 项目的仓库许可证。Samarium 本身使用 [MIT License](https://github.com/shyamsitaula/samarium/blob/main/LICENSE)。
