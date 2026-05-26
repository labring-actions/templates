# 在 Sealos 上部署和托管 Flarum

Flarum 是一款轻量、可扩展的在线社区论坛平台。此模板会在 Sealos Cloud 上部署 Flarum，并自动配置持久化存储和 ApeCloud MySQL 8.0 数据库。

![Flarum 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/flarum/website-screenshot.webp)

## 关于在 Sealos 上托管 Flarum

Flarum 提供简洁的社区讨论体验，支持主题、回复、标签、内容管理、用户组和管理员后台。它的扩展体系可以按需加入 Markdown、文件上传、单点登录、自定义主题和实时交互等能力，适合从小型社区逐步扩展。

此 Sealos 模板会创建 Flarum 应用、MySQL 数据库、持久化 `/data` 存储、公网 HTTPS 入口和 Sealos 桌面应用入口。模板会在启动阶段等待 MySQL 就绪，并自动创建 `flarum` 数据库，因此首次安装不需要手动初始化数据库。

此部署配置适合小型社区和起步阶段的论坛。Flarum 容器使用经过测试的轻量资源规格：`200m` CPU 和 `256Mi` 内存上限；数据库保留 Sealos Kubeblocks 默认规格，以保证稳定性。

## 常见使用场景

- **社区论坛**：为产品、创作者或开源项目搭建分类清晰、便于管理的讨论区。
- **用户支持论坛**：让用户集中提问、共享解决方案，并沉淀常见问题。
- **知识型社区**：围绕文档、课程或内部知识库构建轻量问答和讨论层。
- **会员空间**：使用用户组和权限管理公开、会员专属和管理员工作流。
- **扩展型论坛**：先用轻量核心上线，再通过 Flarum 扩展加入上传、认证、格式化或自定义集成。

## Flarum 托管依赖

此 Sealos 模板包含运行 Flarum 所需的运行时和平台资源：

- **Flarum 应用**：`crazymax/flarum:1.8.10`，通过 `8000` 端口提供 HTTP 服务
- **数据库**：ApeCloud MySQL `ac-mysql-8.0.30-1`
- **持久化存储**：`1Gi`，挂载到 `/data`，用于保存 Flarum 资源、扩展和运行数据
- **公网访问**：HTTPS Ingress 和 Sealos 应用入口
- **启动初始化**：Init Container 会等待 MySQL 并用 `utf8mb4` 创建 `flarum` 数据库

### 部署依赖

- [Flarum 文档](https://docs.flarum.org/) - Flarum 官方文档
- [Flarum 扩展](https://docs.flarum.org/extensions/) - 扩展管理指南
- [Flarum 社区](https://discuss.flarum.org/) - 社区支持和扩展讨论
- [Docker 镜像仓库](https://github.com/crazy-max/docker-flarum) - 此模板使用的容器镜像

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **Flarum StatefulSet**：运行论坛应用，包含 Nginx、PHP-FPM，并将 Flarum 数据挂载到 `/data`。
- **MySQL Cluster**：保存讨论、用户、权限、扩展状态和论坛配置。
- **Init Container**：等待 MySQL 端点就绪，并在 Flarum 启动前创建初始数据库。
- **Service 和 Ingress**：通过生成的 Sealos HTTPS 域名暴露 `8000` 端口。
- **Sealos 应用入口**：在桌面中添加可点击的论坛快捷入口。

**配置说明：**

- `FLARUM_FORUM_TITLE` 用于设置首次安装时的论坛标题。
- `FLARUM_BASE_URL` 会根据 Sealos 域名生成：`https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。
- 数据库地址、端口、用户名和密码来自 Sealos 管理的 MySQL 连接密钥。
- Flarum 默认关闭调试模式，PHP 内存为 `256M`，上传大小上限为 `16M`。
- 容器镜像会创建初始管理员用户 `flarum`，密码为 `flarum`；首次登录后请立即修改密码。

**许可证信息：**

Flarum 使用 MIT 许可证发布。此 Sealos 模板随 Sealos templates 仓库提供。

## 为什么在 Sealos 上部署 Flarum？

Sealos 是基于 Kubernetes 的 AI 云操作系统。它可以让你部署和运维应用，而不必为每个服务手写 Kubernetes 配置。

- **一键部署**：打开应用商店模板，配置论坛标题，即可完成部署，无需手写 YAML。
- **托管运行资源**：Sealos 会从一个模板中创建应用、数据库、存储、入口和桌面快捷方式。
- **内置持久化存储**：论坛资源、扩展文件和生成数据会在重启后保留。
- **即时公网访问**：每个部署都会获得当前 Sealos Cloud 域名下的 HTTPS 地址。
- **资源更省**：模板使用经过测试的小规格 Flarum 配置，适合起步阶段的社区。
- **Canvas 与 AI 运维**：部署后可以通过 Canvas、AI 对话和资源卡片检查或调整资源。
- **Kubernetes 底座**：无需直接管理 Kubernetes，也能使用调度、服务发现和存储能力。

## 部署指南

1. 打开 [Flarum 模板](https://sealos.run/products/app-store/flarum)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - `FLARUM_FORUM_TITLE`：初始论坛标题，默认值为 `Flarum`。
3. 等待部署完成，通常需要 2-3 分钟。部署开始后，Sealos 会跳转到 Canvas。后续如需调整配置，可以在 AI 对话中描述需求，或点击对应资源卡片修改设置。
4. 通过以下地址访问应用：
   - **论坛地址**：`https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`
   - **管理员后台**：`https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}/admin`
5. 使用初始管理员账号登录，并立即修改密码：
   - 用户名：`flarum`
   - 密码：`flarum`

## 配置

部署完成后，可以通过以下方式配置 Flarum：

- **Flarum 管理后台**：在 `/admin` 管理扩展、标签、权限、邮件设置和外观。
- **AI 对话**：描述基础设施变更需求，让 Sealos 辅助应用调整。
- **资源卡片**：在 Canvas 中调整 StatefulSet、MySQL 集群、Ingress 和存储资源。
- **Flarum 扩展**：通过管理后台或容器级维护流程安装扩展。

用于生产社区前，建议先配置出站邮件、检查注册策略、设置论坛权限，并修改默认管理员密码。

## 扩缩容

在 Sealos 上调整 Flarum 资源：

1. 打开当前部署的 Canvas。
2. 点击 Flarum StatefulSet 资源卡片。
3. 根据访问量、扩展数量和上传使用情况调整 CPU 与内存。
4. 如果论坛需要更多数据库容量，点击 MySQL 资源卡片调整数据库资源。
5. 在对话中应用变更，并在滚动更新后观察应用状态。

对于大多数小型论坛，建议先使用模板默认值。如果安装了较多扩展或出现 PHP 内存压力，优先增加内存。

## 故障排查

### 首次登录使用默认账号

- 原因：容器镜像会在首次启动时创建初始管理员账号。
- 解决方法：使用 `flarum` / `flarum` 登录，然后立即在管理后台修改密码。

### 论坛长时间未完成启动

- 原因：MySQL 可能仍在初始化，或数据库连接密钥尚未就绪。
- 解决方法：等待几分钟后检查 Flarum StatefulSet 日志。Init Container 会在应用启动前等待 MySQL 可用。

### 上传或扩展需要更多空间

- 原因：Flarum 会将资源、扩展和生成文件保存到 `/data`。
- 解决方法：在大量上传文件或安装较多扩展前，通过 Canvas 资源卡片扩容持久化存储。

### 获取帮助

- [Flarum 文档](https://docs.flarum.org/)
- [Flarum 社区](https://discuss.flarum.org/)
- [Flarum 扩展指南](https://docs.flarum.org/extensions/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Flarum 官网](https://flarum.org/)
- [Flarum 源码仓库](https://github.com/flarum/framework)
- [Flarum Docker 镜像](https://github.com/crazy-max/docker-flarum)
- [Sealos 应用商店](https://sealos.run/products/app-store/flarum)

## 许可证

此 Sealos 模板随 Sealos templates 仓库提供。Flarum 和 `crazymax/flarum` 容器镜像均使用 MIT 许可证发布。
