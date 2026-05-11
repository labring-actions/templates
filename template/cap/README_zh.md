# 在 Sealos 上部署和托管 Cap

Cap 是一款开源屏幕录制与视频分享平台，适合希望掌控录制流程和数据的团队。这个模板会在 Sealos Cloud 上部署 Cap Web、媒体服务器、MySQL 数据库和兼容 S3 的对象存储。

![Cap 应用预览](https://raw.githubusercontent.com/CapSoftware/Cap/refs/heads/main/apps/web/public/landing-cover.png)

## 关于在 Sealos 上托管 Cap

Cap 提供 Web 控制台，用来查看、分享和管理通过 Cap 桌面端录制的视频。它支持分享链接、团队协作、评论、字幕、分析、自定义存储以及自托管部署，适合对数据控制有更高要求的团队。

这个 Sealos 模板会自动创建自托管 Cap 所需的服务。Cap Web 负责用户界面、API 路由、认证流程和控制台，媒体服务器负责 Web 应用所需的媒体处理任务。Sealos 还会创建 MySQL 数据库和兼容 S3 的对象存储桶，保证元数据和录制文件在重启后仍然保留。

部署完成后，你会获得公开 HTTPS 访问地址、组件间服务发现、自动生成的应用密钥、数据库初始化任务，以及 Web 和媒体服务的健康检查。

## 常见使用场景

- **产品演示**：录制清晰的功能 walkthrough，并分享给潜在客户、客户或内部团队。
- **问题反馈**：用屏幕、摄像头和麦克风一起记录可复现的问题上下文。
- **异步站会**：用短视频替代状态会议，让团队成员按自己的节奏查看更新。
- **客户上手引导**：制作可复用的教程、功能介绍和帮助视频。
- **设计与工程评审**：分享 UI 反馈、代码讲解或实现说明，并把评论附着在录制内容上。

## Cap 托管依赖

这个 Sealos 模板包含基础自托管 Cap 所需的运行依赖：Cap Web、Cap Media Server、MySQL、兼容 S3 的对象存储桶，以及用于准备 `cap` 数据库的初始化任务。

### 部署依赖

- [Cap 官网](https://cap.so) - 产品网站与客户端下载
- [Cap 文档](https://cap.so/docs) - 官方产品文档
- [自托管指南](https://cap.so/docs/self-hosting) - 自托管说明与生产配置
- [Cap GitHub 仓库](https://github.com/CapSoftware/Cap) - 源码、Issue 与发布记录
- [Cap Discord](https://cap.link/discord) - 社区支持

### 实现细节

**架构组件：**

此模板会部署以下资源：

- **Cap Web**：核心 Next.js Web 应用，提供控制台、分享页面、API 路由、认证和数据库迁移能力。
- **Cap Media Server**：Cap Web 的配套服务，用于媒体处理流程。
- **MySQL**：由 KubeBlocks 管理的 MySQL 数据库，用于保存 Cap 元数据、用户、录制记录和应用状态。
- **MySQL 初始化任务**：启动安全的初始化任务，会等待 MySQL 就绪，创建 `cap` 数据库，并配置 MySQL 认证兼容性。
- **对象存储桶**：Sealos 提供的兼容 S3 的存储桶，用于保存录制文件和媒体资源。
- **Ingress 与应用入口**：公开 HTTPS 入口和 Sealos App 资源，方便从控制台直接打开 Cap。

**配置：**

Cap Web 会使用模板生成的 `DATABASE_ENCRYPTION_KEY`、`NEXTAUTH_SECRET` 和 `MEDIA_SERVER_WEBHOOK_SECRET`。它通过 KubeBlocks 管理的连接密钥访问 MySQL，并使用 Sealos 对象存储凭据完成兼容 S3 的上传。

模板提供可选的 `RESEND_API_KEY` 和 `RESEND_FROM_DOMAIN` 输入项，用于邮件发送。如果留空，Cap 仍可启动，但不会通过 Resend 发送邮箱验证码；测试时可以在服务日志中查看开发模式验证码。

**许可证信息：**

Cap 主要采用 AGPLv3 许可证，部分录制相关 crate 使用 MIT 许可证。生产使用前，请阅读 [Cap 许可证文件](https://github.com/CapSoftware/Cap/blob/main/LICENSE)。

## 为什么在 Sealos 上部署 Cap？

Sealos 是基于 Kubernetes 构建的 AI 云操作系统，覆盖从开发到生产部署和运维的完整应用生命周期。在 Sealos 上部署 Cap，你可以获得：

- **一键部署**：无需手写 Kubernetes 配置，即可部署完整 Cap 技术栈。
- **内置 Kubernetes 运维能力**：获得托管网络、服务发现和工作负载编排能力。
- **持久化数据服务**：用 MySQL 保存元数据，用兼容 S3 的对象存储保存录制资源。
- **即时公网访问**：部署完成后自动获得带 HTTPS 证书的公网地址。
- **易于调整配置**：可通过 Canvas、AI 对话或资源卡片修改环境变量、资源和存储设置。
- **按量付费更高效**：从较小规格开始，随着使用量增长再逐步调整资源。
- **平台自动化管理**：让 Sealos 处理常见基础设施工作，你专注使用 Cap 本身。

如果你想自托管屏幕录制平台，又不想自己维护 Kubernetes 底层细节，Sealos 是一个合适的部署选择。

## 部署指南

1. 打开 [Cap 模板](https://sealos.io/products/app-store/cap)，点击 **Deploy Now**。
2. 在弹窗中配置参数。生产环境建议填写 `RESEND_API_KEY` 和 `RESEND_FROM_DOMAIN`；测试环境可以留空。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续如需修改配置，可以在对话框中描述需求让 AI 执行，也可以点击对应资源卡片调整设置。
4. 通过系统提供的公网地址访问 Cap：
   - **Cap Web**：使用邮箱验证码或邮件链接登录。
   - **桌面端连接**：如果使用自托管服务，可在 Cap Desktop 的 `Settings > Cap Server URL` 中填写你的部署地址。

## 配置说明

部署完成后，你可以通过以下方式配置 Cap：

- **AI 对话**：描述需要调整的环境变量、资源或域名，让 AI 帮你应用修改。
- **资源卡片**：打开 Cap Web、Media Server、MySQL 或 Object Storage 资源卡片，查看并修改设置。
- **邮件发送**：配置 `RESEND_API_KEY` 和 `RESEND_FROM_DOMAIN` 后，可通过 Resend 发送登录邮件。
- **桌面客户端**：将 Cap Desktop 的 Cap Server URL 指向你的部署地址。
- **密钥与 URL**：开始录制后应保持生成密钥稳定，因为修改加密或认证密钥可能导致会话失效或加密数据不可用。

## 扩容

在 Sealos 上扩容 Cap：

1. 打开该部署对应的 Canvas。
2. 点击 Cap Web 或 Cap Media Server 资源卡片。
3. 根据访问量和处理压力调整 CPU、内存或副本数。
4. 在对话框中应用修改，并从 Canvas 观察滚动发布状态。

团队规模变大时，建议先提升 Cap Web 资源；如果媒体处理成为瓶颈，再扩容媒体服务器。MySQL 和对象存储容量应根据录制量和保留周期调整。

## 故障排查

### 常见问题

**收不到登录邮件**
- 原因：`RESEND_API_KEY` 和 `RESEND_FROM_DOMAIN` 为空或配置错误。
- 解决方法：配置 Resend 凭据。测试部署如果不配置邮件，可以从 Canvas 的 Cap Web 资源卡片查看日志，并复制开发模式验证码。

**Cap Web 启动时反复重启**
- 原因：Next.js 启动和数据库迁移阶段可能需要更多内存。
- 解决方法：在资源卡片中提高 Cap Web 的内存限制，然后等待滚动发布完成。

**录制文件能上传但无法观看**
- 原因：对象存储端点或存储桶访问设置可能不正确。
- 解决方法：检查 Object Storage 存储桶、Cap Web 资源卡片中的 S3 环境变量和公网端点配置。

### 获取帮助

- [Cap 文档](https://cap.so/docs)
- [Cap GitHub Issues](https://github.com/CapSoftware/Cap/issues)
- [Cap Discord](https://cap.link/discord)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Cap 自托管指南](https://cap.so/docs/self-hosting)
- [Cap 下载](https://cap.so/download)
- [Cap GitHub 仓库](https://github.com/CapSoftware/Cap)
- [Sealos 文档](https://sealos.run/docs)

## 许可证

此 Sealos 模板由 Sealos templates 仓库维护。Cap 本身主要采用 AGPLv3 许可证，部分录制相关 crate 使用 MIT 许可证；详情请查看 [Cap 许可证文件](https://github.com/CapSoftware/Cap/blob/main/LICENSE)。
