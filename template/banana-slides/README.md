# 在 Sealos 上部署和托管 Banana Slides

Banana Slides 是一款基于 AI 的智能演示文稿生成应用。本模板在 Sealos 云平台上部署了一个生产就绪的 Banana Slides 实例，支持通过想法、大纲或页面描述自动生成完整的 PPT 演示文稿，并支持多种格式导出。

![Banana Slides](https://raw.githubusercontent.com/labring-actions/templates/main/template/banana-slides/logo.png)

> 推荐使用 [Sealos AI Proxy](os.sealos.io/?openapp=system-aiproxy) 获取API密钥，减小迁移成本

## 关于 Banana Slides 托管

Banana Slides 采用前后端分离的架构运行。前端服务提供用户界面，基于 Nginx 部署并配置了反向代理和静态资源缓存；后端服务处理 AI 生成逻辑和文件管理，运行在 Python Flask 环境中。Sealos 模板自动为后端配置了持久化存储，确保您的演示文稿数据、上传文件和应用实例数据安全存储，并在重启后保持一致。

部署过程中包含自动 SSL 证书配置、域名管理和通过 Sealos 仪表盘的集成监控功能。前端通过优化的 Nginx 配置支持大文件上传（最大 50MB）、API 请求代理和静态资源长期缓存，提供流畅的用户体验。

## 常见使用场景

- **快速制作演示文稿**：通过简单的想法或大纲描述，让 AI 自动生成完整的 PPT 结构和内容
- **内容创作辅助**：为营销、教育、技术分享等场景快速生成专业演示文稿
- **团队协作演示**：支持团队成员快速创建和共享演示文稿
- **多格式导出**：生成的演示文稿可导出为多种格式，便于不同场景使用
- **AI 辅助设计**：利用 AI 能力自动布局和美化幻灯片

## Banana Slides 托管依赖

本 Sealos 模板包含所有必需的依赖项：前端 Nginx 服务器、后端 Flask 应用以及持久化存储。

### 部署依赖

- [Banana Slides 官方文档](https://github.com/Anionex/banana-slides) - 项目官方文档和源代码
- [Sealos 云平台](https://cloud.sealos.run) - 一站式云应用部署平台
- [Sealos 文档中心](https://sealos.run/docs/) - Sealos 使用指南和最佳实践

### 实现细节

**架构组件：**

本模板部署两个主要服务：

- **前端服务**：基于 Nginx 的 Web 服务器，提供用户界面和静态资源服务。配置了 API 反向代理、文件服务代理和静态资源缓存优化，支持大文件上传（最大 50MB）和 SPA 路由

- **后端服务**：Python Flask 应用，处理 AI 生成逻辑、文件上传和演示文稿管理。包含健康检查端点，并通过持久化存储保存应用实例数据和用户上传文件

**配置：**

前端通过 Nginx 反向代理将 `/api` 路径的请求转发到后端服务，`/files` 路径用于动态文件服务。静态资源（JS、CSS、图片等）配置了一年的长期缓存以提高加载速度。后端服务运行在 StatefulSet 中，确保稳定的网络标识和数据持久化。

两个持久化存储卷分别挂载到：
- `/app/backend/instance`：应用实例数据（100Mi）
- `/app/uploads`：用户上传文件（100Mi）

**许可证信息：**

Banana Slides 的许可证信息请参考其[官方仓库](https://github.com/Anionex/banana-slides)。

## 为什么在 Sealos 上部署 Banana Slides？

Sealos 是一个基于 Kubernetes 构建的 AI 赋能云操作系统，统一了从云 IDE 开发到生产部署和管理的整个应用生命周期。非常适合构建和扩展现代 AI 应用、SaaS 平台和复杂的微服务架构。通过在 Sealos 上部署 Banana Slides，您将获得：

- **一键部署**：只需点击一次即可部署复杂应用。无需 YAML 配置，无需容器编排复杂性——只需点击、部署即可

- **内置自动扩展**：您的应用根据需求自动上下扩展。处理流量激增无需人工干预或复杂配置

- **轻松定制**：通过直观的表单配置环境变量、资源限制和存储。无需触碰一行代码即可定制设置

- **无需 Kubernetes 专业知识**：获得 Kubernetes 的所有优势——高可用性、服务发现和容器编排——而无需成为 Kubernetes 专家

- **包含持久化存储**：内置持久化存储解决方案确保您的数据安全，并在部署和扩展事件中可访问

- **即时公网访问**：每次部署都会获得带有 SSL 证书的自动公网 URL。无需复杂网络设置即可即时共享应用

- **自动备份**：自动备份和灾难恢复确保您的数据始终安全

在 Sealos 上部署 Banana Slides，专注于构建产品而不是管理基础设施。

## 部署指南

1. 访问 [Sealos 云平台](https://cloud.sealos.run)
2. 在桌面界面中点击"应用商店"
3. 在应用商店中搜索"Banana Slides"
4. 点击"部署应用"并配置所需参数
5. 等待部署完成（通常需要 1-3 分钟）
6. 通过提供的 URL 访问您的应用

## 配置

### API 密钥配置

Banana Slides 需要配置 AI 服务的 API 密钥才能正常工作：

1. **获取 API 密钥**：
   - 推荐使用 [Sealos AI Proxy](https://os.sealos.io/?openapp=system-aiproxy) 获取 API 密钥
   - Sealos AI Proxy 提供统一的 AI 服务接入，支持多种 AI 模型，可有效减小迁移成本
   - 也可以使用其他兼容的 AI 服务提供商的 API 密钥

2. **在应用中配置**：
   - 通过部署 URL 访问 Banana Slides 应用
   - 点击应用界面右上角的"设置"按钮
   - 在设置页面中填入获取到的 API 密钥
   - 保存配置后即可开始使用 AI 生成功能

### 应用配置

部署完成后，您还可以通过以下方式配置 Banana Slides：

- **应用启动台**：在 Sealos 应用启动台中修改环境变量、资源限制和存储设置
- **API 访问**：应用会自动配置域名和 SSL 证书，可直接通过 HTTPS 访问
- **数据持久化**：所有上传的文件和生成的演示文稿都存储在持久化卷中，确保数据安全

## 扩展

如需扩展应用：

1. 打开应用启动台
2. 选择您的 Banana Slides 部署
3. 调整 CPU/内存资源
4. 点击"更新"应用更改

注意：由于 Banana Slides 使用 StatefulSet 部署后端服务以保持数据持久性，建议在扩展前评估数据迁移需求。

## 故障排除

### 常见问题

**文件上传失败（413 错误）**
- 原因：上传文件超过 Nginx 配置的大小限制
- 解决：本模板已将上传限制配置为 50MB。如需更大限制，可修改 ConfigMap 中的 `client_max_body_size` 参数

**生成的演示文稿无法下载**
- 原因：后端服务存储空间不足或网络问题
- 解决：检查后端服务的持久化存储容量，确保有足够空间

**API 请求超时**
- 原因：AI 生成过程耗时较长
- 解决：本模板已配置 300 秒的代理超时。如需更长超时，可调整 Nginx 配置中的 `proxy_read_timeout` 参数

### 获取帮助

- [Banana Slides GitHub](https://github.com/Anionex/banana-slides) - 报告问题和查看源代码
- [Sealos 文档](https://sealos.run/docs/) - 平台使用指南

## 附加资源

- [Banana Slides 源代码](https://github.com/Anionex/banana-slides) - 查看完整源代码和贡献指南
- [Sealos 模板文档](https://sealos.run/docs/docs/user-guide/templates/) - 了解如何创建和定制模板
- [Kubernetes StatefulSet 文档](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) - 了解有状态应用部署

## 许可证

本 Sealos 模板按 MIT 许可证提供。Banana Slides 本身的许可证请参考其[官方仓库](https://github.com/Anionex/banana-slides)。
