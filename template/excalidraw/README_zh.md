# 在 Sealos 上部署和托管 Excalidraw

Excalidraw 是一个开源虚拟白板，用于绘制手绘风格的图表、流程和视觉笔记。此模板会在 Sealos Cloud 上将 Excalidraw 部署为轻量级单服务 Web 应用。

![Excalidraw 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/excalidraw/website-screenshot.webp)

## 关于托管 Excalidraw

Excalidraw 以无状态 Web 服务运行，通过 HTTP 提供基于浏览器的绘图界面。应用主要将绘图内容保存在浏览器中，或由用户自行导出文件，因此此模板不会创建数据库或持久化存储卷。

Sealos 模板会为 Excalidraw 创建 Deployment、Service、Ingress 和 App 入口。Sealos 会自动提供公网 HTTPS 访问入口、TLS 证书集成、Kubernetes 调度能力，以及 Canvas 中的资源管理能力。

此部署适合需要快速搭建共享图表白板的团队，无需手动管理服务器、反向代理或 Kubernetes 清单。

## 常见使用场景

- **架构草图**：在规划阶段绘制系统图、部署流程和服务关系。
- **产品与 UX 构思**：用手绘风格记录线框图、用户流程和界面想法。
- **会议白板**：为工作坊、站会和远程协作提供浏览器白板。
- **文档图表**：导出图表用于 README、设计文档和工程方案。
- **教学与讲解**：为技术或非技术受众制作简单直观的视觉说明。

## Excalidraw 托管依赖

Sealos 模板包含 Excalidraw Web 容器，以及公开访问所需的 Kubernetes 资源。它不依赖 PostgreSQL、MySQL、Redis、对象存储或持久化存储卷。

### 部署依赖

- [官方网站](https://excalidraw.com/) - Excalidraw 在线编辑器和产品信息
- [源码仓库](https://github.com/excalidraw/excalidraw) - 应用源码和版本动态
- [Excalidraw 文档](https://docs.excalidraw.com/) - 产品和开发者文档
- [GitHub Issues](https://github.com/excalidraw/excalidraw/issues) - 社区支持和问题反馈

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **Excalidraw Web 应用**：单容器服务，在 80 端口提供 Excalidraw 浏览器应用。
- **Service**：将集群内部流量转发到 Excalidraw 容器。
- **Ingress**：通过 Sealos 管理的域名提供公网 HTTPS 访问入口。
- **App 入口**：在 Sealos 控制台中添加可点击的 Excalidraw 链接。

**配置：**

模板使用生成的默认值设置 `app_name` 和 `app_host`，因此每次部署都会获得唯一的应用名称和公网主机名。部署时不需要额外填写用户输入项。

工作负载在 `/` 上配置健康检查，禁用自动挂载 Service Account Token，并使用适合轻量级静态 Web 应用的最小资源配置。

**许可证信息：**

Excalidraw 使用 MIT License。此 Sealos 模板作为 Sealos templates 仓库的一部分提供。

## 为什么在 Sealos 上部署 Excalidraw？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用从部署到持续运维的生命周期。在 Sealos 上部署 Excalidraw，你可以获得：

- **一键部署**：打开模板页面，点击 **Deploy Now**，Sealos 会创建所需的 Kubernetes 资源。
- **即时公网访问**：每次部署都会获得自动配置证书的 HTTPS 访问地址。
- **无需 Kubernetes 经验**：无需自己编写或维护清单，也能在 Kubernetes 上运行 Excalidraw。
- **资源高效**：使用按量计费的云资源，并采用轻量级 CPU 和内存配置。
- **便捷自定义**：部署后可通过 Canvas、AI 对话框或资源卡片调整资源和运行时设置。
- **内置运维视图**：可在 Sealos 控制台中查看 Deployment、Service、Ingress 和 App 入口。

在 Sealos 上部署 Excalidraw，把精力放在表达想法上，而不是管理基础设施。

## 部署指南

1. 打开 [Excalidraw 模板](https://sealos.run/products/app-store/excalidraw)，点击 **Deploy Now**。
2. 在弹出的对话框中配置参数。标准部署保留默认值即可。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后，你会被重定向到 Canvas。后续如需修改，可在对话框中描述需求让 AI 应用变更，或点击相关资源卡片修改设置。
4. 通过提供的访问地址打开应用：
   - **Excalidraw Web UI**：打开生成的 HTTPS 访问入口，即可在浏览器中开始绘图。

## 配置

部署完成后，你可以通过以下方式配置 Excalidraw：

- **AI 对话框**：描述资源调整等变更需求，让 AI 应用更新。
- **资源卡片**：点击 Deployment、Service 或 Ingress 资源卡片，查看和修改设置。
- **应用访问地址**：使用 Sealos 生成的 HTTPS 地址访问白板。

默认 Web 编辑器体验不需要管理员账号或数据库配置。

## 扩缩容

如需扩缩容或调整资源：

1. 打开 Excalidraw 部署对应的 Canvas。
2. 点击 Deployment 资源卡片。
3. 根据预期流量调整 CPU、内存或副本数。
4. 在对话框中应用变更。

对于大多数小团队和个人工作区，默认单副本部署已经足够。

## 故障排查

### 部署后 Excalidraw 页面无法打开

- 原因：容器或 Ingress 可能仍在启动。
- 解决方案：等待 Canvas 中的 Deployment 就绪后，再重新打开应用访问地址。

### 浏览器数据没有在用户之间共享

- 原因：默认 Excalidraw Web 应用主要基于浏览器运行，此模板不会创建后端数据库。
- 解决方案：按需将图表导出为文件，或使用 Excalidraw 支持的共享能力。

### 获取帮助

- [Excalidraw 文档](https://docs.excalidraw.com/)
- [Excalidraw GitHub Issues](https://github.com/excalidraw/excalidraw/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [Excalidraw 官方网站](https://excalidraw.com/)
- [Excalidraw 源码仓库](https://github.com/excalidraw/excalidraw)
- [Excalidraw 博客](https://plus.excalidraw.com/blog)
- [Sealos 文档](https://sealos.run/docs)

## 许可证

此 Sealos 模板作为 Sealos templates 仓库的一部分提供。Excalidraw 本身使用 [MIT License](https://github.com/excalidraw/excalidraw/blob/master/LICENSE)。
