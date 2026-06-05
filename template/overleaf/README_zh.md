# 在 Sealos 上部署和托管 Overleaf

Overleaf 是一个开源的在线实时协作 LaTeX 编辑器。此模板会在 Sealos Cloud 上部署 Overleaf Community Edition 6.1.2，并配置 KubeBlocks MongoDB、KubeBlocks Redis、持久化项目存储和 HTTPS 公网入口。

## 关于托管 Overleaf

Overleaf 为论文、技术报告、书籍和教学材料提供浏览器内 LaTeX 工作区。它把源码编辑、项目管理和 PDF 编译整合在一个 Web 应用中，团队无需安装本地 TeX 环境即可协作。

此 Sealos 模板会创建 Overleaf Web 应用、用于应用元数据的 MongoDB、用于实时协作和会话协调的 Redis，以及挂载到 `/var/lib/overleaf` 的持久化存储。Sealos 负责管理 Kubernetes 资源、公网 Ingress、TLS 证书和应用启动入口。

## 常见使用场景

- **学术写作**：在浏览器中撰写并编译 LaTeX 论文、毕业论文和报告。
- **团队协作**：让可信用户在同一个工作区中编辑共享 LaTeX 项目。
- **教学环境**：为学生提供无需本地安装的 LaTeX 编辑器。
- **技术文档**：用持久化项目存储维护结构化 LaTeX 文档。

## Overleaf 托管依赖

此 Sealos 模板包含运行所需的依赖：Overleaf Community Edition、KubeBlocks MongoDB、KubeBlocks Redis、持久化存储、Service、Ingress 和 Sealos App 元数据。

### 部署依赖

- [Overleaf Community Edition](https://github.com/overleaf/overleaf) - 源码仓库
- [Overleaf Toolkit 快速开始](https://github.com/overleaf/toolkit/blob/master/doc/quick-start-guide.md) - 官方首次管理员和使用流程
- [Sealos](https://sealos.io) - 云应用平台

### 实现细节

**架构组件：**

- **Overleaf Web 服务**：运行 `sharelatex/sharelatex:6.1.2`，通过 80 端口提供 Web UI。
- **MongoDB**：通过 KubeBlocks MongoDB 8.0.4 存储用户、项目和 Overleaf 应用元数据。
- **Redis**：通过 KubeBlocks Redis 7.2.7 提供缓存和实时协作协调能力。
- **持久化项目存储**：将 Overleaf 数据保存在 `/var/lib/overleaf`，容量为 1 GiB。
- **Ingress 和 App 入口**：发布 HTTPS 访问地址，并集成到 Sealos 应用启动器中。

**配置说明：**

模板会根据生成的 Sealos 域名设置 `OVERLEAF_SITE_URL`，启用反向代理模式，并默认关闭邮箱确认，便于 Community Edition 首次初始化。Overleaf Community Edition 适合可信用户环境；隔离编译是 Server Pro 功能，不包含在此模板中。

**许可证信息：**

此 Sealos 模板遵循模板仓库许可证。Overleaf Community Edition 由 Overleaf 项目分发，请查看上游仓库了解应用本身的许可证详情。

## 为什么在 Sealos 上部署 Overleaf？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一了从部署到运维的应用生命周期。在 Sealos 上部署 Overleaf 可以获得：

- **一键部署**：通过一个模板创建 Overleaf 应用、数据库、存储、Ingress 和 App 入口。
- **托管依赖**：使用 KubeBlocks MongoDB 和 Redis，无需手写 Kubernetes 清单。
- **内置持久化存储**：通过挂载数据卷在重启后保留 Overleaf 项目数据。
- **即时公网访问**：获得由 Sealos Ingress 和证书管理的 HTTPS 地址。
- **资源调整简单**：随着使用量增长，可从 Sealos 资源卡片调整 CPU、内存和存储。
- **无需 Kubernetes 专业知识**：通过 Sealos UI 操作 Overleaf，同时保留 Kubernetes 的可靠性。

## 部署指南

1. 打开 [Overleaf 模板](https://sealos.io/products/app-store/overleaf)，点击 **Deploy Now**。
2. 在弹窗中配置参数。首次测试部署可直接使用默认值。
3. 等待部署完成。首次冷启动可能需要数分钟，因为 Overleaf 会初始化 MongoDB 索引并执行迁移。
4. 从 Sealos App 入口打开生成的 Overleaf URL。
5. 打开 `/register` 确认公开自助注册状态。Overleaf Community Edition 通常会显示 **Please contact to create an account**，表示需要管理员创建用户。
6. 通过 Overleaf 容器控制台创建首个管理员或用户，然后从 `/login` 登录，再访问 `/project` 开始使用 Overleaf。

## 配置说明

部署参数：

| 名称 | 说明 | 默认值 |
|------|------|--------|
| `OVERLEAF_SITE_LANGUAGE` | 设置 Overleaf 界面语言。 | `zh-CN` |
| `OVERLEAF_APP_NAME` | 设置显示的 Overleaf 站点名称。 | `Overleaf Community Edition` |
| `ENABLED_LINKED_FILE_TYPES` | 启用的项目关联文件类型，使用逗号分隔。 | `project_file,project_output_file` |
| `ENABLE_CONVERSIONS` | 启用基于 ImageMagick 的缩略图生成。 | `true` |
| `EMAIL_CONFIRMATION_DISABLED` | 关闭邮箱确认，便于首次本地账号初始化。 | `true` |

部署后，请通过 Overleaf 容器控制台创建初始账号，或导入已有数据集，然后从 `/login` 登录。此模板的线上验证确认 `/login` 可访问，且 `/register` 在未启用公开自助注册时会返回 Community Edition 预期提示 **Please contact to create an account**。

## 扩容

此模板面向小型 Community Edition 部署调优。已验证的最低应用资源为 Overleaf 容器 1 vCPU 和 2 GiB 内存，MongoDB 与 Redis 的 KubeBlocks 数据库组件各使用 500 mCPU 和 512 MiB 内存。如果冷启动、迁移或 PDF 编译负载变慢，应优先增加 Overleaf 内存。

如需调整资源，请打开部署 Canvas，点击对应资源卡片，修改 CPU、内存、存储或副本数，然后在对话框中应用变更。

## 故障排除

### 首次启动需要数分钟

Overleaf 会在空 MongoDB 数据库上执行迁移。请等待 Overleaf Pod 进入 Ready 后再打开站点。

### `/register` 显示 “Please contact to create an account”

这是未启用公开自助注册时的 Community Edition 预期行为。请由管理员创建或邀请用户，然后从 `/login` 登录。

### 登录成功但项目打开较慢

在 Sealos 中检查 Overleaf Pod 内存和数据库健康状态。如果实例用于较大文档或较重的编译任务，请提高 Overleaf 内存限制。

### 获取帮助

- [Overleaf Toolkit 文档](https://github.com/overleaf/toolkit/tree/master/doc)
- [Overleaf GitHub Issues](https://github.com/overleaf/overleaf/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [Overleaf 官网](https://www.overleaf.com/)
- [Overleaf 源码仓库](https://github.com/overleaf/overleaf)
- [Overleaf Toolkit](https://github.com/overleaf/toolkit)

## 许可证

此 Sealos 模板遵循 templates 仓库许可证。Overleaf Community Edition 由 Overleaf 项目授权，请查看上游仓库了解当前应用许可证条款。
