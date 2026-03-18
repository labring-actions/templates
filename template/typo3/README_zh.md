# 在 Sealos 上部署并托管 TYPO3

TYPO3 是一个开源企业级内容管理系统，适合搭建编辑型网站、内容门户和多站点平台。该模板会在 Sealos 上部署 TYPO3，并自动配置托管 MySQL、持久化可写目录、CLI 首次初始化和 HTTPS Ingress。

![TYPO3 Logo](./logo.png)

## 关于在 Sealos 上托管 TYPO3

该模板以经典模式运行 TYPO3，使用上游 `martinhelmich/typo3` Apache 镜像。Sealos 会自动创建托管 MySQL 集群、生成 `typo3` 数据库、挂载 `fileadmin`、`typo3conf` 和 `typo3temp` 三个持久化卷，并为应用分配一个可直接访问的 HTTPS 域名。

首次初始化通过 init 容器完成，而不是依赖浏览器安装向导。第一次成功启动时，TYPO3 会写入 `settings.php`、应用你填写的管理员账号信息、创建初始站点配置，并挂载 `additional.php`，让 TYPO3 正确识别 Sealos Ingress 传入的 HTTPS 与 Host 头。模板还会在 setup 开始前校验管理员密码是否满足 TYPO3 默认密码策略；如果出现“`settings.php` 已存在但后台用户不存在”的半初始化状态，init 流程也会自动补建管理员账号。

TYPO3 后台默认通过 `/typo3/` 访问，这是标准后台入口。根路径 `/` 对应前台站点入口，能否正常打开取决于你是否已经完成 TYPO3 的站点与首页配置。如果后台健康但 `/` 返回 `404`，请登录 TYPO3 后台继续完成前台站点配置或发布首页内容。

后续日常运维都在 Canvas 中完成。部署完成后，你可以调整资源、查看日志、重启工作负载，或者直接通过 AI 对话修改存储、网络和运行参数。

## 常见使用场景

- **企业官网**：承载品牌官网、市场站点和结构化内容发布流程。
- **内容门户**：搭建文档中心、杂志站点或知识库等内容密集型网站。
- **多站点运营**：在同一套 TYPO3 中统一管理多个站点。
- **代理商交付**：为客户提供基于 Kubernetes 存储和托管数据库的可维护 CMS 方案。
- **传统主机迁移**：把 TYPO3 从虚机或共享主机迁移到托管 Kubernetes 平台。

## TYPO3 托管依赖

该 Sealos 模板已经包含完整的 TYPO3 运行栈：Apache/PHP、托管 MySQL、持久化存储、集群内服务发现和 HTTPS Ingress。

### 部署依赖

- [TYPO3 官网](https://typo3.org) - 产品概览与生态入口
- [TYPO3 安装指南](https://docs.typo3.org/installation) - 官方安装与运维文档
- [TYPO3 Docker 文档](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Administration/Docker/Index.html) - 官方 Docker 部署参考
- [TYPO3 反向代理指南](https://docs.typo3.org/permalink/t3coreapi:reverse-proxy-setup) - 反向代理与 HTTPS 检测配置说明
- [TYPO3 GitHub 仓库](https://github.com/TYPO3/typo3) - 上游源码仓库
- [Sealos 文档](https://sealos.run/docs) - 平台使用与运维说明

## 实现细节

### 架构组件

该模板会部署以下资源：

- **TYPO3 StatefulSet**：运行主应用，提供 Apache 服务和持久化可写目录。
- **托管 MySQL 集群（`ac-mysql-8.0.30-1`）**：由 KubeBlocks 提供 TYPO3 所需的关系型数据库。
- **MySQL 初始化 Job**：在 TYPO3 setup 之前创建 `typo3` 数据库。
- **TYPO3 Setup Init Container**：校验管理员密码、等待 MySQL 就绪、执行 `typo3 setup`，并确保后台管理员用户存在。
- **ConfigMap（`additional.php`）**：注入 Sealos Ingress 所需的 trusted host 和反向代理设置。
- **持久化卷**：
  - `/var/www/html/fileadmin`（1Gi），用于上传文件和用户管理的媒体资源
  - `/var/www/html/typo3conf`（0.1Gi），用于生成配置和站点设置
  - `/var/www/html/typo3temp`（0.1Gi），用于缓存和运行时临时文件
- **Service + Ingress**：在集群内暴露 TYPO3，并对外提供 HTTPS 访问入口。

### 配置项

模板对外暴露以下部署参数：

- `TYPO3_SETUP_ADMIN_EMAIL`：初始 TYPO3 管理员邮箱
- `TYPO3_SETUP_ADMIN_USERNAME`：初始 TYPO3 管理员用户名
- `TYPO3_SETUP_ADMIN_PASSWORD`：初始 TYPO3 管理员密码。必须至少 8 位，并同时包含大写字母、小写字母、数字和特殊字符。
- `TYPO3_PROJECT_NAME`：初始站点名称

运行时行为：

- 模板会自动生成 `TYPO3_SETUP_CREATE_SITE=https://<app-host>.<domain>/`，作为首次站点初始化的 URL。
- TYPO3 以 `TYPO3_CONTEXT=Production` 运行。
- 反向代理和 trusted host 配置通过 `typo3conf/system/additional.php` 注入。
- MySQL 连接的 host、port、username 和 password 从 `${app_name}-mysql-conn-credential` Secret 中注入。
- 健康检查会以 `/typo3/` 为探针路径，并携带公网 Host 头，避免被 trusted host 校验误判。
- 管理员输入参数只用于首次引导。第一次成功初始化之后，如需修改账号或密码，应在 TYPO3 内部完成，而不是重新修改模板变量。
- 如果 `settings.php` 已存在但后台管理员不存在，init 流程会自动修复安装并显式创建管理员。
- 根路径 `/` 是否可访问，取决于 TYPO3 前台站点和页面配置；后台入口始终是 `https://<app-host>.<domain>/typo3/`。

### 许可证信息

TYPO3 采用 GPL-2.0 许可证。完整许可证信息请以上游仓库和 TYPO3 官方文档为准。

## 为什么选择在 Sealos 上部署 TYPO3？

Sealos 是一个构建在 Kubernetes 之上的 AI 辅助云操作系统，能够简化生产部署和日常运维。将 TYPO3 部署到 Sealos 后，你可以获得：

- **一键部署**：无需手写 Kubernetes 编排，就能启动 TYPO3、MySQL、Ingress 和持久化存储。
- **托管数据库集成**：直接使用 KubeBlocks 托管的 MySQL，并通过 Secret 安全注入连接信息。
- **内置持久化存储**：上传文件、配置和运行时数据都能在重启和升级后继续保留。
- **默认 HTTPS 公网访问**：自动获得外部域名和 TLS 终止能力，无需手工处理网络入口。
- **AI + Canvas 运维体验**：部署完成后可通过 AI 对话或资源卡片完成重启、扩容和调优。
- **按量使用更省心**：按实际资源需求调整计算和存储，避免过度配置。
- **保留 Kubernetes 的可靠性**：享受 Kubernetes 的稳定底座，同时省去大量平台维护工作。

把 TYPO3 部署到 Sealos，把精力集中在内容交付，而不是基础设施组装。

## 部署指南

1. 打开 [TYPO3 模板页](https://sealos.io/products/app-store/typo3) 并点击 **Deploy Now**。
2. 在弹窗中配置部署参数：
   - `TYPO3_SETUP_ADMIN_EMAIL`
   - `TYPO3_SETUP_ADMIN_USERNAME`
   - `TYPO3_SETUP_ADMIN_PASSWORD`
   - `TYPO3_PROJECT_NAME`
   管理员密码必须至少 8 位，并至少包含一个大写字母、一个小写字母、一个数字和一个特殊字符。
3. 等待 2-3 分钟完成部署。Sealos 会自动创建 MySQL、初始化 `typo3` 数据库、执行 TYPO3 CLI 引导，然后跳转到 Canvas。后续如需修改配置，可通过 AI 对话描述需求，或直接点击相应资源卡片进行调整。
4. 使用系统生成的域名访问应用：
   - **TYPO3 后台**：`https://<app-host>.<domain>/typo3/`
   - **TYPO3 前台**：`https://<app-host>.<domain>/`，前提是你已经完成 TYPO3 的站点和首页配置

## 配置与运维

部署完成后，你可以通过以下方式管理 TYPO3：

- **AI 对话**：让 Sealos AI 帮你重启工作负载、调整资源或扩容存储。
- **资源卡片**：在 Canvas 中直接修改 StatefulSet、Service、Ingress、ConfigMap 或 MySQL 配置。
- **TYPO3 后台**：通过 `https://<app-host>.<domain>/typo3/` 安装扩展、配置站点、管理用户并发布内容。

建议的上线后动作：

1. 使用部署时填写的管理员信息登录 TYPO3 后台。
2. 检查站点配置；如果根路径 `/` 还不可用，先补齐前台站点和首页内容。
3. 按需轮换初始管理员密码。
4. 检查语言环境、邮件设置和扩展依赖。
5. 为 MySQL 和 `fileadmin` 中的媒体资源建立备份策略。

## 扩缩容建议

如需扩缩容，可以按以下步骤操作：

1. 在 Canvas 中打开当前部署。
2. 当后台流量、扩展数量或缓存生成压力增大时，提高 TYPO3 StatefulSet 的 CPU 和内存。
3. 当编辑操作或前台查询变慢时，调优 MySQL 组件资源。
4. 当存储需求增长时，扩容 `fileadmin`、`typo3conf` 或 `typo3temp` 对应卷。

该模板默认以单实例 TYPO3 为基线。生产环境通常先做垂直扩容，再结合数据库调优逐步提升吞吐能力。

## 故障排查

### 常见问题

**问题：setup init 容器反复重启**
- 原因：MySQL 仍在初始化，或者 TYPO3 引导步骤执行失败。
- 解决：先检查 MySQL Pod 是否健康，再查看 TYPO3 StatefulSet Pod 中 init 容器的日志。

**问题：部署因为管理员密码失败**
- 原因：`TYPO3_SETUP_ADMIN_PASSWORD` 不满足 TYPO3 默认密码策略。
- 解决：使用至少 8 位、且同时包含大写字母、小写字母、数字和特殊字符的密码重新部署。

**问题：用部署时填写的管理员账号无法登录后台**
- 原因：管理员输入参数只会在第一次成功引导时生效，后续再改模板变量不会回写现有 TYPO3 用户。
- 解决：使用首次初始化时的管理员凭据登录，在 TYPO3 后台内修改密码；如果需要全新初始化，请使用全新的持久化存储重新部署。

**问题：后台正常，但根路径 `/` 返回 `404`**
- 原因：TYPO3 后台已经初始化完成，但前台站点或首页还没有配置好。
- 解决：登录 `/typo3/` 后台，检查 Site Management、根页面和首页内容配置，并发布前台页面。

**问题：TYPO3 跳转到 HTTP，或后台登录表现异常**
- 原因：反向代理头未被信任，或者生成的域名与 trusted host 配置不匹配。
- 解决：确认 Pod 已挂载 `additional.php`，并检查 Ingress 主机名是否与 Sealos 生成的域名一致。

**问题：上传失败或存储很快写满**
- 原因：默认卷大小不足以承载当前媒体资源规模。
- 解决：在 Canvas 中扩容对应卷，优先关注 `fileadmin`。

### 获取帮助

- [TYPO3 文档](https://docs.typo3.org/)
- [TYPO3 Docker 文档](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Administration/Docker/Index.html)
- [TYPO3 GitHub Issues](https://github.com/TYPO3/typo3/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [TYPO3 入门文档](https://docs.typo3.org/m/typo3/tutorial-getting-started/main/en-us/)
- [TYPO3 扩展仓库](https://extensions.typo3.org/)
- [TYPO3 安全指南](https://docs.typo3.org/permalink/t3coreapi:security-administrators)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

该 Sealos 模板遵循本仓库的许可证约定。TYPO3 本体由上游项目按 GPL-2.0 发布。
