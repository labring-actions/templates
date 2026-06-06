# 在 Sealos 上部署和托管 Tududi

Tududi 是一款自托管效率工具，用于管理任务、项目、笔记、领域和个人工作流。这个模板会在 Sealos Cloud 上部署一个带持久化存储的 Tududi Web 应用。

![Tududi 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/tududi/website-screenshot.webp)

## 关于 Tududi 托管

Tududi 将任务、项目、笔记、智能视图、领域、标签和个人计划整合到一个安静的工作空间中。它面向自托管场景设计，并会根据部署环境变量创建初始管理员账户。

这个 Sealos 模板运行官方 Tududi 容器，并为 SQLite 数据库和上传文件配置持久化存储。Sealos 为应用提供公开 HTTPS 地址、入口、服务发现、资源控制和持久化卷。

## 常见使用场景

- **个人任务管理**：收集收件箱事项，规划今日任务，查看未来安排，组织周期性任务。
- **项目计划**：将任务归入项目，跟踪状态，并集中管理相关工作。
- **笔记与知识收集**：将笔记与任务、项目、领域和标签一起保存。
- **自托管效率系统**：用轻量 SQLite 后端在自己的部署中保存工作流数据。

## Tududi 托管依赖

Sealos 模板将所有运行时依赖封装在官方 Tududi 镜像中。模板会创建两个持久化卷：一个用于 SQLite 数据库，一个用于上传文件。

### 部署依赖

- [官方网站](https://tududi.com/) - 产品网站
- [官方文档](https://docs.tududi.com/) - Tududi 文档
- [GitHub 仓库](https://github.com/chrisvel/tududi) - 源代码和问题追踪

## 实现细节

### 架构组件

该模板会部署以下资源：

- **Tududi StatefulSet**：运行 `chrisvel/tududi:1.1.0`，监听端口 `3002`。
- **SQLite 数据库卷**：持久化 `/app/backend/db`，保存生产 SQLite 数据库和自动数据库备份。
- **上传文件卷**：持久化 `/app/backend/uploads`，保存用户上传文件。
- **Service 和 Ingress**：通过 Sealos 托管的 HTTPS 地址暴露 Tududi。
- **Sealos App 入口**：将 Tududi 添加到 Sealos 应用启动器中。

### 配置

模板会配置 Tududi 的初始管理员邮箱、管理员密码、会话密钥、公开 URL、安全 Cookie、可信代理和上传目录。Tududi 官方生产配置使用 SQLite，因此该模板将数据库保存在应用持久化卷中。

部署默认使用一个副本，因为 Tududi 的 SQLite 数据库和上传文件都保存在本地持久化卷中。为了保持数据一致性，请保持单副本运行。上游提供集群数据库和共享对象存储支持后，可以评估多副本部署。

### 许可证信息

Tududi 使用 MIT License。

## 为什么在 Sealos 上部署 Tududi？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一覆盖从云端 IDE 开发到生产部署和运维管理的完整应用生命周期。在 Sealos 上部署 Tududi 可以获得：

- **一键部署**：通过应用商店表单直接部署 Tududi。
- **自动 HTTPS 访问**：Sealos 自动提供公开 URL 和 TLS 证书。
- **内置持久化存储**：数据库和上传文件会在重启和升级后保留。
- **资源控制**：可以在 Sealos 控制台中按工作空间规模调整 CPU 和内存。
- **运维可视化**：在同一平台查看 Pod、日志、事件和存储。

## 部署指南

1. 打开 [Tududi 模板](https://sealos.io/products/app-store/tududi)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - **Initial administrator email address**：首次登录使用的管理员邮箱。
   - **Initial administrator password**：首次登录使用的管理员密码。保存该值，并在首次登录后修改密码。
3. 等待部署完成。部署完成后，页面会跳转到 Canvas。
4. 从 App 入口或 Ingress 卡片打开 Tududi 公开地址。
5. 使用部署时配置的管理员邮箱和密码登录。

## 配置

部署后，你可以通过以下方式管理 Tududi：

- **Tududi 用户菜单**：登录后更新账号设置。
- **Sealos AI 对话框**：描述环境变量或资源变更需求，由 Sealos 应用更新。
- **资源卡片**：点击 StatefulSet、Ingress、Service 或存储卷卡片，查看并修改运行配置。

请将管理员邮箱和密码保存在安全的密码管理器中。生产部署完成首次登录后，建议立即修改初始密码。

## 扩展

Tududi 以单副本 StatefulSet 运行，因为官方生产配置使用 SQLite。提升容量时：

1. 打开 Tududi 部署对应的 Canvas。
2. 点击 StatefulSet 资源卡片。
3. 增加 CPU 或内存资源。
4. 应用变更并等待 Pod 进入就绪状态。

## 故障排查

### 登录失败

- 原因：邮箱或密码与部署时填写的值不同。
- 解决方案：在 Sealos 中检查部署输入，或通过 Tududi 数据库重置管理员凭据，也可以使用目标凭据重新部署。

### 重启后上传文件丢失

- 原因：上传文件卷被修改或移除。
- 解决方案：确认 `/app/backend/uploads` 已挂载到持久化上传卷。

### 升级后应用启动较慢

- 原因：Tududi 启动时可能运行数据库迁移并创建 SQLite 自动备份。
- 解决方案：通过 StatefulSet 资源卡片查看应用日志，等待迁移完成。

### 获取帮助

- [官方文档](https://docs.tududi.com/)
- [GitHub Issues](https://github.com/chrisvel/tududi/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Tududi 网站](https://tududi.com/)
- [Tududi GitHub](https://github.com/chrisvel/tududi)
- [Tududi Docker 镜像](https://hub.docker.com/r/chrisvel/tududi)

## 许可证

该 Sealos 模板遵循本仓库许可证。Tududi 本身使用 MIT License。
