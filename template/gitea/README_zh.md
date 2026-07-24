# 在 Sealos 上部署和托管 Gitea

Gitea 是轻量级自托管 Git 服务，可管理源码、工单、合并请求、软件包、发布和自动化任务。此模板会在 Sealos 上部署 Gitea 1.27.0，并配置持久化仓库、HTTPS Ingress，以及可选的托管 MySQL 和 S3 兼容对象存储。

![Gitea 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/gitea/website-screenshot.webp)

## 关于 Gitea 托管

Gitea 以单个有状态应用运行，`/var/lib/gitea` 与 `/etc/gitea` 分别挂载持久卷。默认部署会创建 KubeBlocks MySQL 8 集群，用于保存应用元数据；个人和小型实例也可以选择 SQLite。

Git 仓库数据保存在持久卷。启用 Sealos 对象存储后，Gitea 会把附件、头像、LFS 对象、软件包、发布附件和 Actions 构建产物写入私有 S3 兼容 bucket，并通过应用提供受控下载。

## 常见使用场景

- **私有 Git 托管**：管理个人、团队或企业内部仓库。
- **代码协作**：统一处理工单、合并请求、里程碑和版本发布。
- **软件包分发**：通过同一服务发布软件包和 Release 附件。
- **自动化任务**：配合独立配置的 Gitea Actions Runner 执行工作流。

## Gitea 托管依赖

- **Gitea**：`docker.gitea.com/gitea:1.27.0-rootless`
- **数据库**：默认使用 KubeBlocks MySQL `ac-mysql-8.0.30-1`，也可选择内嵌 SQLite
- **持久化存储**：分别保存 Gitea 数据和配置
- **可选对象存储**：Sealos 私有 S3 兼容 bucket
- **网络入口**：Service、HTTPS Ingress 和 Sealos App 资源

### 部署依赖链接

- [Gitea 文档](https://docs.gitea.com/) - 官方管理与配置指南
- [Gitea Rootless Docker 安装指南](https://docs.gitea.com/installation/install-with-docker-rootless) - 官方容器部署说明
- [Gitea GitHub 仓库](https://github.com/go-gitea/gitea) - 源码和版本发布
- [Sealos 文档](https://sealos.io/docs) - 平台部署与运维指南

### 实现细节

模板使用上游 rootless 镜像，以 UID/GID `1000:1000` 运行，并在启动前为两个持久卷设置对应权限。应用监听 `3000` 端口，健康检查使用 Gitea 官方 `/api/healthz` 接口。

实测应用资源基线为 `100m` CPU 和 `256Mi` 内存。全新 SQLite 初始化在 128Mi 限制下出现 OOM，80Mi 冷启动同样触发 OOM；模板采用 256Mi，覆盖两种数据库分支的首次安装。托管 MySQL 组件使用 `500m` CPU 和 `512Mi` 内存。

Gitea 使用 MIT License。

## 为什么在 Sealos 上部署 Gitea？

- **一键创建完整栈**：通过一个模板创建 Gitea、存储、网络和选定的数据库分支。
- **仓库持久化**：Pod 重启后继续保留仓库和配置。
- **托管数据库选项**：直接使用 KubeBlocks MySQL 和自动生成的连接凭据。
- **私有对象存储选项**：将上传类数据保存到 Sealos bucket，并由应用控制下载。
- **即时 HTTPS 访问**：部署后获得自动生成的公网域名和 TLS 入口。
- **Canvas 运维**：部署完成后继续调整资源和存储容量。

## 部署指南

1. 打开 [Gitea 模板](https://sealos.io/products/app-store/gitea)，点击 **Deploy Now**。
2. 选择部署参数：
   - **使用托管 MySQL**（`use_external_database`）：默认启用，适合团队和长期运行实例。关闭后使用 SQLite。
   - **启用 S3 兼容对象存储**（`enable_s3_storage`）：为 Gitea 上传类数据创建 Sealos 私有对象存储 bucket。
3. 等待 Gitea 工作负载和选定的数据库资源进入就绪状态。
4. 打开生成的 HTTPS 地址。新实例会显示 Gitea 安装页面。
5. 保留模板预填的数据库和服务器配置，展开 **可选设置**，填写管理员用户名、邮箱和强密码，然后点击 **立即安装**。
6. 安装完成后，Gitea 会进入已登录的管理员首页。创建一个仓库即可确认实例可用。

## 首次登录与注册

首位访问者需要完成实例初始化并创建初始管理员：

1. 打开系统生成的 Gitea 地址。
2. 检查预填的数据库类型、数据库路径或 MySQL 连接、域名和基础 URL。
3. 展开 **可选设置**，填写管理员账号字段。
4. 提交安装表单，等待 Gitea 跳转到已登录的控制面板。

后续管理员和用户可通过 `https://<your-gitea-domain>/user/login` 登录。用户注册策略位于 **站点管理** 设置中。

## 配置

- **数据库分支**：默认使用托管 MySQL。SQLite 数据库保存在持久卷路径 `/var/lib/gitea/data/gitea.db`。
- **对象存储分支**：S3 模式用于 Gitea 管理的上传数据；Git 仓库和应用配置继续保存在持久卷。
- **SSH 访问**：容器监听 `2222` 端口。需要 SSH Clone 时，可额外创建 TCP 入口；生成域名可直接用于 HTTPS Clone。
- **邮件**：账号确认和通知邮件需要在 Gitea 设置或环境变量中补充 SMTP 配置。
- **Actions**：Gitea Actions Runner 作为独立工作负载，在服务器部署完成后添加。

## 扩缩容

模板保持一个 Gitea 副本，因为仓库和配置卷使用 `ReadWriteOnce`。仓库数量、软件包用量和并发访问增加时，可在 Canvas 中纵向提高 CPU、内存和 PVC 容量。多副本架构需要共享仓库存储，并按照 Gitea 高可用方案设计。

## 故障排查

**安装页面连接 MySQL 失败**

等待 KubeBlocks MySQL 集群状态变为 `Running`，然后刷新页面，并保留模板预填的数据库配置。

**安装期间 Pod 重启**

保持默认 256Mi 应用内存限制。首次数据库初始化的内存需求高于已配置实例的空闲状态。

**S3 模式上传失败**

确认 ObjectStorageBucket 已就绪，并检查 Gitea StatefulSet 是否收到自动生成的 bucket 凭据。bucket 应保持私有，下载由 Gitea 提供。

**SSH Clone 无法连接**

使用 HTTPS Clone，或创建指向 Gitea Service `2222` 端口的 Sealos TCP 入口。

## 更多资源

- [Gitea 配置速查表](https://docs.gitea.com/administration/config-cheat-sheet)
- [Gitea 管理员指南](https://docs.gitea.com/administration/)
- [Gitea API 文档](https://docs.gitea.com/api/1.27/)

## 许可证

此 Sealos 模板遵循模板仓库许可证。Gitea 使用 MIT License。
