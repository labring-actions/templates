# 在 Sealos 上部署和托管 WordPress

WordPress 是用于发布网站、博客、新闻和其他 Web 内容的开源内容管理系统。此模板会在 Sealos Cloud 上部署 WordPress `7.0.0`，并配套 KubeBlocks MySQL、持久化站点存储、HTTPS Ingress 和 Sealos App 入口。

![WordPress 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/wordpress/website-screenshot.webp)

## 关于托管 WordPress

模板会让官方 WordPress 镜像通过托管 Kubernetes Service 提供服务。挂载到 `/var/www/html` 的 1 GiB 持久化卷保存 WordPress 文件、主题、插件和上传内容，Pod 重启后站点内容仍会保留。

KubeBlocks MySQL `ac-mysql-8.0.30-1` 保存 WordPress 数据库。MySQL 就绪后，幂等初始化 Job 会创建 `mydb` 数据库。Sealos 会配置生成的 HTTPS 主机名，并在 Sealos App 入口中提供访问地址。

## 常见使用场景

- **内容站点**：发布博客、新闻、文档和企业官网。
- **营销页面**：组合主题与插件，搭建活动页面和线索收集流程。
- **编辑团队**：为作者和编辑提供共享发布工作流。
- **小型社区**：运行带持久化媒体和用户数据的自托管站点。

## 架构与依赖

- **WordPress Web 服务**：WordPress `7.0.0` 监听 `80` 端口。
- **MySQL**：单实例 KubeBlocks MySQL 提供 `mydb` 数据库和 1 GiB 数据卷。
- **数据库初始化 Job**：使用托管 MySQL 连接 Secret 创建 `mydb`，成功后结束。
- **持久化站点存储**：`/var/www/html` 卷保存核心文件、主题、插件和媒体上传内容。
- **Service、Ingress 和 App 入口**：Sealos 发布 HTTPS 地址，并提供直接启动入口。

## 为什么在 Sealos 上部署 WordPress？

Sealos 是基于 Kubernetes 的 AI 云操作系统。此模板把 WordPress、MySQL、存储、HTTPS 路由和 App 入口组合在一起，一次部署即可启动内容站点。

- **一键配置**：同时创建应用和数据库。
- **内容持久化**：在托管存储中保留主题、插件和上传文件。
- **运维简单**：部署后通过 Canvas 资源卡片和 AI 对话进行调整。
- **按需计费**：根据流量和媒体存储增长扩展站点。

## 配置说明

此模板没有额外部署输入项。Sealos 会生成应用名称和主机名，KubeBlocks 会生成数据库连接凭据。

## 部署指南

1. 打开 [WordPress 模板](https://sealos.io/products/app-store/wordpress)，点击 **Deploy Now**。
2. 保留默认参数；需要自定义应用名称或主机名时再调整。
3. 等待 MySQL、初始化 Job 和 WordPress 进入 Ready。Sealos 部署通常需要 2-3 分钟；首次创建数据库时冷启动可能更久。部署完成后，Canvas 会提供 AI 对话和资源卡片，便于继续调整。
4. 从 Sealos App 入口打开生成的 URL。
5. 完成 WordPress 首次运行表单，选择站点语言，创建管理员账号并登录。

### 首次设置、登录与用户注册

- 新部署会打开 `/wp-admin/install.php`。选择站点语言，填写站点标题，创建首个管理员用户名和密码，然后提交表单。
- 后续使用 `/wp-login.php` 登录，管理员后台地址为 `/wp-admin/`。
- 首个管理员账号在安装流程中创建。登录后进入 **Settings > General > Membership**，启用 **Anyone can register** 后，访客可以自行注册账号，并可设置默认角色。
- 启用注册后用隐私窗口验证注册流程。管理员密码请保存到密码管理器。

## 存储与运维

随着媒体和插件增长，可在 Canvas 资源卡片中提高 WordPress CPU、内存并扩展 `/var/www/html` 卷。Sealos 基于 Kubernetes，并按实际资源用量计费。迁移或升级大型插件前，请同时备份 WordPress 卷和 MySQL 数据；配置调整可通过 Canvas AI 对话提交。

WordPress 会从托管连接 Secret 获取 MySQL 主机、端口、用户名、密码和数据库名。Ingress 允许 32 MiB 请求体，并将上传代理超时设置为 300 秒。

## 故障排查

### 初始化页面提示数据库错误

检查 MySQL Cluster 是否 Ready，以及 `wordpress-mysql-init` Job 是否已完成。确认连接 Secret 指向当前 MySQL Service 后再重新运行 Job。

### 媒体上传失败

检查 `/var/www/html` 卷容量和 Ingress 请求限制。媒体库较大时扩展存储，并让单次上传保持在配置的 32 MiB 限制内。

### 站点仍显示旧主机名

在 Canvas 中检查 Ingress 和 App 资源的 `app_host`。更换自定义域名后，在 WordPress 设置中同步更新 WordPress 地址和站点地址。

### 获取帮助

- [WordPress 文档](https://wordpress.org/documentation/)
- [WordPress 支持论坛](https://wordpress.org/support/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 官方链接

- [WordPress 官网](https://wordpress.org/)
- [WordPress 源码仓库](https://github.com/WordPress/WordPress)

## 其他资源

- [WordPress 开发者资源](https://developer.wordpress.org/)
- [WordPress 插件目录](https://wordpress.org/plugins/)

## 许可证

此 Sealos 模板遵循 templates 仓库许可证。WordPress 采用 GNU GPL v2 或更高版本发布。
