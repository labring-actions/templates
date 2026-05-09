# 在 Sealos 上部署和托管 Presenton

Presenton 是一款开源 AI 演示文稿生成器，同时提供 API，可根据提示词、上传文件或可复用模板生成幻灯片、报告和文档。此模板会在 Sealos 云平台上部署一个自托管 Presenton 实例，并自动配置持久化存储和 HTTPS 访问入口。

## 关于 Presenton 托管

Presenton 同时提供 Web 界面和 REST API，可用于生成、编辑和导出演示文稿。用户可以用自然语言提示创建幻灯片，也可以上传现有材料作为内容来源，复用模板，控制语气与内容密度，并将结果导出为可编辑的 PPTX 或便于分享的 PDF。

此 Sealos 模板会将 Presenton 作为单个 StatefulSet 运行，并把持久化存储挂载到 `/app_data`。应用数据、生成文件、本地配置、上传资源和默认本地数据库都会写入持久化卷，重启后仍可保留。

模板还会创建 Kubernetes Service、HTTPS Ingress 和 Sealos App 入口，用于公网访问。默认情况下不会启动 Ollama（`START_OLLAMA=false`），因此你可以在应用设置中连接自己使用的大语言模型（LLM）和图像服务，或在部署后通过环境变量进行配置。

## 常见使用场景

- **AI 生成幻灯片**：把主题、提纲、简报或上传文档转换成结构清晰的演示文稿。
- **报告与方案初稿**：快速生成业务报告、融资路演、培训材料和技术分享幻灯片。
- **演示文稿自动化 API**：把生成能力接入内部工具、CRM 流程、内容流水线或自动化 Agent。
- **品牌模板复用**：基于已有 PPTX 或 PDF 模板生成内容，让输出保持统一品牌风格。
- **自托管 AI 工作流**：在自己的基础设施上运行生成流程，并使用自有模型或 API Key。

## Presenton 托管依赖

此 Sealos 模板包含 Presenton 应用容器、持久化存储、内部网络、HTTPS Ingress 和 Sealos App 快捷入口。默认不会额外创建外部数据库、对象存储桶或本地 Ollama 模型服务。

### 部署依赖

- [Presenton 官网](https://presenton.ai/) - 产品概览与在线体验。
- [Presenton 文档](https://docs.presenton.ai/) - 官方安装、托管、使用与 API 指南。
- [Presenton API 介绍](https://docs.presenton.ai/api-introduction) - API 能力与生成流程说明。
- [Presenton GitHub 仓库](https://github.com/presenton/presenton) - 源代码、版本发布和问题反馈。
- [Sealos 文档](https://sealos.run/docs/) - Sealos 平台指南与应用部署说明。

## 实现细节

### 架构组件

本模板会部署以下资源：

- **Presenton 应用**：运行 `ghcr.io/presenton/presenton:v0.8.2-beta` 容器，通过 `80` 端口提供 Web UI 和 API。
- **应用数据持久化**：创建 1Gi 持久化卷并挂载到 `/app_data`，保存生成的演示文稿、上传文件、配置、本地数据和应用状态。
- **ClusterIP Service**：在集群内部把流量转发到 Presenton 容器。
- **HTTPS Ingress**：提供公网 HTTPS 入口，自动配置 TLS 证书，并包含静态资源缓存、32Mi 请求体限制和 300 秒代理超时。
- **Sealos App 入口**：在 Sealos 界面中生成可点击的应用链接，直接打开你的 Presenton 实例。

### 配置说明

部署时会使用以下关键默认值：

- `APP_DATA_DIRECTORY=/app_data`：将应用数据写入持久化卷。
- `MIGRATE_DATABASE_ON_STARTUP=true`：应用启动时自动执行数据库迁移。
- `START_OLLAMA=false`：保持模板轻量，不默认启动内嵌本地模型服务。
- `MEM0_ENABLED=false`：默认关闭记忆能力，同时保留相关配置项，便于后续扩展。
- CPU 请求为 `50m`，上限为 `500m`；内存请求为 `204Mi`，上限为 `2Gi`。

Presenton 支持多种 LLM 和图像服务配置。部署完成后，可在 Presenton 界面中配置服务凭据；如需固定生产配置，也可以通过 Canvas 资源卡片更新环境变量。请将 API Key 保存在 Sealos 管理的配置中，不要把私有凭据提交到模板仓库。

### 扩展注意事项

默认部署使用一个 StatefulSet 副本，因为模板会把应用数据写入单个持久化卷。对个人、团队和内部自动化场景来说，优先通过 CPU 与内存做纵向扩展，通常最稳妥。

如果需要多副本或更高吞吐的 API 工作负载，应先规划外部共享服务，例如托管数据库和共享对象存储。这些组件默认不包含在本模板中。

### 许可证信息

Presenton 使用 Apache-2.0 许可证。此 Sealos 模板作为 Sealos templates 仓库的一部分提供；模板的分发和修改请以该仓库适用条款为准。

## 为什么在 Sealos 上部署 Presenton？

Sealos 是一个基于 Kubernetes 构建的 AI 辅助云操作系统，覆盖从云端 IDE 开发到生产部署和运维管理的完整应用生命周期。它适合现代 AI 应用、内部工具、SaaS 产品和微服务工作负载。在 Sealos 上部署 Presenton，你可以获得：

- **一键部署**：直接从模板页部署 Presenton，无需编写 Kubernetes YAML，也不用手动配置网络和存储。
- **Kubernetes 底座**：获得服务发现、工作负载隔离、健康检查和标准化资源管理能力。
- **内置持久化存储**：生成的演示文稿、上传资源和本地应用数据可跨重启保留。
- **即时公网访问**：部署后自动获得带 TLS 证书的 HTTPS 访问地址。
- **易于定制**：可通过 Canvas 资源卡片调整环境变量、存储和资源限制，也可以在 AI 对话框中描述变更需求。
- **按量使用更高效**：先用较小资源启动，再根据使用量逐步调整 CPU、内存和存储。
- **无需 Kubernetes 专业经验**：通过可视化界面管理应用，同时享受 Kubernetes 的底层能力。

在 Sealos 上部署 Presenton，把精力放在演示文稿工作流上，而不是维护部署基础设施。

## 部署指南

1. 打开 [Presenton 模板](https://sealos.io/products/app-store/presenton)，点击 **Deploy Now**。
2. 在弹出的对话框中配置参数。默认生成的 `app_name` 和 `app_host` 通常足以完成首次部署。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后，你会被重定向到 Canvas。后续如需调整，可在对话框中描述需求，让 AI 协助修改；也可以点击对应资源卡片手动更新配置。
4. 通过生成的访问地址打开应用：
   - **Presenton Web UI**：打开生成的 HTTPS 地址，创建和管理演示文稿。
   - **Presenton API**：在启用并完成认证后，可使用同一基础地址访问 REST API，例如 `/api/v1/ppt/presentation/generate`。

## 配置

部署完成后，可以通过以下方式配置 Presenton：

- **Presenton 设置**：如果应用界面提供相关入口，可直接配置 LLM、图像服务和生成参数。
- **AI 对话框**：在 Canvas 对话框中描述需要调整的内容，让 AI 应用支持的变更。
- **资源卡片**：点击 StatefulSet、Ingress 或存储资源卡片，修改环境变量、资源限制、请求体大小、超时时间或存储容量。
- **持久化数据卷**：生成内容和本地应用状态保存在 `/app_data`；如果团队会生成大量文稿或上传大文件，请及时扩容。

常见的服务商相关环境变量包括模型服务选择、API Key、图像服务配置和可选认证控制。生产环境固定配置前，请先查看 Presenton 官方文档中的最新变量列表。

## 扩展

如需扩展部署：

1. 打开 Presenton 部署对应的 Canvas。
2. 点击 StatefulSet 资源卡片。
3. 根据生成延迟和并发使用情况调整 CPU 与内存。
4. 在对话框中应用变更。
5. 如果生成的文稿、上传文件或导出文件增长较快，请扩容 `/app_data` 存储卷。

除非你已经重新设计共享存储和数据库依赖，否则建议副本数保持为 `1`。

## 故障排除

### 常见问题

**问题 1：缺少服务商凭据导致生成失败**
- 原因：Presenton 需要 LLM 服务；根据图像配置不同，也可能需要图像服务 Key。
- 解决：在 Presenton 设置中配置凭据，或通过 Canvas 更新受支持的环境变量。密钥只应保存在 Sealos 管理的配置中。

**问题 2：大文件上传失败或 API 返回请求体过大错误**
- 原因：Ingress 默认请求体限制为 32Mi。
- 解决：压缩源文件、拆分输入内容，或在资源卡片中调整 Ingress 的 body-size 注解。

**问题 3：生成速度慢或请求超时**
- 原因：幻灯片生成会受到 CPU、内存、模型服务和网络延迟影响。
- 解决：提高 CPU 与内存上限，减少幻灯片数量，选择更快的模型，或检查服务商响应延迟。本模板已为长时间生成请求配置 300 秒代理超时。

**问题 4：重启后数据看起来丢失**
- 原因：应用可能没有使用挂载的数据目录，或持久化卷空间不足。
- 解决：确认 `APP_DATA_DIRECTORY=/app_data`，检查 StatefulSet 的卷挂载，并在需要时扩容默认 1Gi 存储卷。

### 获取帮助

- [Presenton 文档](https://docs.presenton.ai/)
- [Presenton GitHub Issues](https://github.com/presenton/presenton/issues)
- [Sealos 文档](https://sealos.run/docs/)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 附加资源

- [Presenton API 介绍](https://docs.presenton.ai/api-introduction) - 通过程序创建、编辑和导出演示文稿。
- [生成配置指南](https://docs.presenton.ai/guide/configuration-and-controls-for-generation) - 了解语气、内容密度、语言、页数、图片类型和导出格式等选项。
- [Presenton GitHub 仓库](https://github.com/presenton/presenton) - 查看源代码和版本说明。
- [Sealos 应用商店](https://sealos.run/products/app-store) - 浏览更多一键部署模板。

## 许可证

此 Sealos 模板作为 Sealos templates 仓库的一部分提供。Presenton 本身使用 [Apache-2.0 许可证](https://github.com/presenton/presenton/blob/main/LICENSE)。
