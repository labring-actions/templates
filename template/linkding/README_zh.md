# 在 Sealos 上部署和托管 linkding

linkding 是一个简洁、快速、自托管的书签管理器，用于收藏、打标签、搜索和分享链接。此模板会在 Sealos 上部署带 PostgreSQL 和持久化数据存储的 linkding。

![linkding 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/linkding/website-screenshot.webp)

## 关于托管 linkding

linkding 是基于 Django 的 Web 应用，运行在 `9090` 端口。模板使用官方容器镜像，为应用数据库创建 KubeBlocks PostgreSQL，并把持久化存储挂载到 `/etc/linkding/data`。

首个管理员会通过部署输入传入 linkding 官方文档中的 `LD_SUPERUSER_NAME` 和 `LD_SUPERUSER_PASSWORD` 环境变量创建。部署完成后，使用这些凭据从 App URL 登录。

## 常见使用场景

- **个人书签库**：用标签、描述、备注和归档元数据保存链接。
- **团队链接集合**：在小团队内共享精选链接。
- **稍后阅读流程**：保存网页，后续整理和搜索。
- **浏览器扩展后端**：把 linkding 作为浏览器集成的同步目标。

## linkding 托管依赖

此 Sealos 模板包含运行所需依赖：linkding、KubeBlocks PostgreSQL `postgresql-16.4.0`、用于创建 `linkding` 数据库的初始化 Job、持久化存储、Service、Ingress 和 App 入口。

### 部署依赖

- [官方仓库](https://github.com/sissbruecker/linkding) - 源代码和设置说明
- [Docker Compose](https://github.com/sissbruecker/linkding/blob/master/docker-compose.yml) - 官方容器部署基线
- [环境变量示例](https://github.com/sissbruecker/linkding/blob/master/.env.sample) - 环境变量参考
- [Sealos](https://sealos.io) - 基于 Kubernetes 的应用托管平台

### 实现细节

**架构组件：**

- **linkding Web 服务**：运行 `sissbruecker/linkding:1.45.0`，在 `9090` 端口提供界面。
- **PostgreSQL**：KubeBlocks 托管的 `postgresql-16.4.0`，用于保存应用数据。
- **持久化数据卷**：挂载到 `/etc/linkding/data`，保存应用数据文件。
- **Service 与 Ingress**：通过 HTTPS 暴露 Web 界面。

**配置：**

模板设置 `LD_DB_ENGINE=postgres`，并从 KubeBlocks 连接 Secret 注入数据库字段。模板还会把 `LD_CSRF_TRUSTED_ORIGINS` 设置为生成的 Sealos HTTPS URL。

**许可证信息：**

此 Sealos 模板遵循仓库许可证。linkding 使用 MIT License。

## 为什么在 Sealos 上部署 linkding？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署、公开访问和运维。通过 Sealos 部署 linkding，你可以获得：

- **一键部署**：从 App Store 启动完整书签管理器。
- **托管 PostgreSQL**：使用 KubeBlocks 数据库存储书签。
- **持久化存储**：重启后保留 linkding 数据。
- **即时公开访问**：Sealos 自动创建 HTTPS URL。

## 部署指南

1. 打开 [linkding 模板](https://sealos.io/products/app-store/linkding)，点击 **Deploy Now**。
2. 配置初始管理员用户名和密码。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续需要修改时，可以在对话框描述需求让 AI 应用更新，或点击相关资源卡片修改设置。
4. 通过提供的 App URL 访问 linkding，并使用第 2 步设置的管理员凭据登录。

## 配置

部署后，可以在 linkding Web UI 中管理书签、标签、用户和集成。资源或环境变量调整可以通过 Sealos Canvas、AI 对话框或工作负载资源卡完成。

## 更多资源

- [linkding README](https://github.com/sissbruecker/linkding)
- [环境变量示例](https://github.com/sissbruecker/linkding/blob/master/.env.sample)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板遵循仓库许可证。linkding 使用 MIT License。
