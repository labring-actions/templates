# 在 Sealos 上部署和托管 MAZANOKE

MAZANOKE 是一款在浏览器中运行的自托管本地图片优化工具。本模板会在 Sealos Cloud 上将 MAZANOKE 部署为单个 Web 服务。

![MAZANOKE 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/mazanoke/website-screenshot.webp)

## 关于托管 MAZANOKE

MAZANOKE 提供浏览器端图片优化界面，用户可以压缩、调整尺寸并转换图片格式，无需把图片上传到远程处理服务。应用静态资源由 Nginx 提供，图片处理在用户浏览器中完成。

Sealos 模板会自动创建 Web 容器、Service、HTTPS Ingress 和 App 入口。MAZANOKE 默认无需账号，用户打开应用即可开始处理图片。

## 常见使用场景

- **私密图片压缩**：减小图片体积，同时让图片数据保留在用户设备上。
- **格式转换**：在 JPG、PNG、WebP 和 ICO 之间转换图片，并支持 HEIC、AVIF、TIFF、GIF、SVG 等输入格式。
- **离线友好的工具**：将 MAZANOKE 安装为 Web App，初次加载后可继续离线使用。
- **团队工具入口**：通过 Sealos 域名为团队提供简单的内部图片优化工具。

## MAZANOKE 托管依赖

Sealos 模板包含 MAZANOKE 所需的全部运行依赖：官方容器镜像、内部 Kubernetes Service、公共 HTTPS Ingress，以及 Sealos App 启动入口。

### 部署依赖

- [官方网站](https://mazanoke.com/) - MAZANOKE 公共实例
- [GitHub 仓库](https://github.com/civilblur/mazanoke) - 源代码和版本发布
- [Docker 配置](https://github.com/civilblur/mazanoke/blob/main/docs/configuration.md) - 可选基础认证环境变量
- [Web App 安装指南](https://github.com/civilblur/mazanoke/blob/main/docs/install-web-app.md) - PWA 安装说明

### 实现细节

**架构组件：**

本模板部署一个服务：

- **MAZANOKE Web**：基于 Nginx 的 Web 容器，在 80 端口提供 MAZANOKE 静态应用。

**配置：**

MAZANOKE 运行时无需注册、登录、数据库或对象存储。图片文件在浏览器中处理，因此部署服务端不会保存上传图片。

上游容器支持通过 `USERNAME` 和 `PASSWORD` 环境变量启用可选基础认证。模板保留默认免账号流程，便于一键使用；需要访问提示时，可在部署后为 Deployment 添加这两个变量。

**许可证信息：**

MAZANOKE 使用 GNU General Public License v3.0 许可证。

## 为什么在 Sealos 上部署 MAZANOKE？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，统一应用部署、运维和管理。在 Sealos 上部署 MAZANOKE，你可以获得：

- **一键部署**：从 App Store 部署 MAZANOKE，无需编写 Kubernetes YAML。
- **自动 HTTPS**：每个部署都会获得由平台管理证书的公共 URL。
- **简单运维**：通过 Canvas、AI 对话和资源卡片调整资源或环境变量。
- **平台化管理**：Sealos 负责 Kubernetes 原生健康检查、服务发现和工作负载管理。
- **按量计费效率**：用较小资源规格运行轻量图片工具，并在需要时调整容量。

在 Sealos 上部署 MAZANOKE，为用户提供私密的浏览器端图片优化工具，同时把基础设施管理交给平台。

## 部署指南

1. 打开 [MAZANOKE 模板](https://sealos.io/products/app-store/mazanoke)，点击 **Deploy Now**。
2. 保留默认参数，或按需调整应用名称和公共域名前缀。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续需要修改时，可以在对话框中描述需求让 AI 应用更新，也可以点击相关资源卡片修改设置。
4. 通过平台提供的公共 URL 访问 MAZANOKE 并开始优化图片。无需注册或登录。

## 配置

部署后，你可以通过以下方式配置 MAZANOKE：

- **AI 对话**：描述添加环境变量或调整资源限制等变更。
- **资源卡片**：点击 Deployment 卡片编辑 CPU、内存、副本数或环境变量。
- **基础认证**：添加 `USERNAME` 和 `PASSWORD` 环境变量，启用上游容器内置的 HTTP 基础认证。

## 扩缩容

扩缩容 MAZANOKE：

1. 打开当前部署的 Canvas。
2. 点击 Deployment 资源卡片。
3. 调整 CPU、内存或副本数。
4. 在对话框中应用变更。

MAZANOKE 在浏览器中处理图片，因此服务端资源需求通常较小。

## 故障排查

### 页面可加载，但图片处理较慢

- 原因：压缩和转换运行在用户浏览器设备上。
- 解决方案：使用较小源图片测试，使用现代浏览器，或减少一次处理的图片数量。

### 基础认证未出现

- 原因：上游容器只有在同时设置 `USERNAME` 和 `PASSWORD` 时才启用基础认证。
- 解决方案：将两个环境变量都添加到 Deployment，并重启工作负载。

### 获取帮助

- [GitHub Issues](https://github.com/civilblur/mazanoke/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [官方网站](https://mazanoke.com/)
- [GitHub 仓库](https://github.com/civilblur/mazanoke)
- [Attributions](https://github.com/civilblur/mazanoke/blob/main/docs/ATTRIBUTIONS.md)

## License

本 Sealos 模板基于 Apache License 2.0 提供。MAZANOKE 本身基于 GNU General Public License v3.0 授权。
