# 在 Sealos 上部署和托管 BentoPDF

BentoPDF 是隐私优先的浏览器端 PDF 工具箱，可在浏览器中编辑、合并、转换和处理 PDF 文件。此模板会在 Sealos Cloud 上部署官方自托管 BentoPDF simple 镜像。

![BentoPDF 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/bentopdf/website-screenshot.webp)

## 关于托管 BentoPDF

BentoPDF 提供基于浏览器的 PDF 工具箱，处理过程发生在用户浏览器本地。模板部署官方自托管 simple build，并通过 Sealos HTTPS 端点暴露服务。

默认自托管版本无需数据库、对象存储或服务端账号系统。用户打开 URL 后即可直接处理 PDF。

## 常见使用场景

- **合并和拆分 PDF**：合并文档或提取页面范围。
- **编辑 PDF**：注释、裁剪、旋转、涂黑和调整 PDF 内容。
- **转换文档**：转换图片、办公文档、文本、Markdown 和 PDF。
- **私密 PDF 处理**：文件保留在浏览器中，适合隐私优先工作流。

## BentoPDF 托管依赖

Sealos 模板包含官方 BentoPDF simple 容器镜像。

### 部署依赖

- [BentoPDF 文档](https://bentopdf.com/docs/) - 官方文档
- [BentoPDF GitHub 仓库](https://github.com/alam00000/bentopdf) - 源码和发布版本
- [自托管指南](https://bentopdf.com/docs/) - 部署和配置说明

### 实现细节

**架构组件：**

- **BentoPDF Web 应用**：官方 `ghcr.io/alam00000/bentopdf-simple:v2.8.6` 镜像
- **NGINX 运行时**：在 8080 端口提供静态客户端应用
- **Ingress**：通过自动 HTTPS 暴露应用

**配置：**

模板设置 `DISABLE_IPV6=true` 以适配仅 IPv4 的 Kubernetes 网络，并保留默认 `PORT=8080` 运行时。

**许可证信息：**

BentoPDF 采用双许可证。自托管 simple build 面向 AGPL 兼容的开源使用；商业用途请查看上游 licensing 页面。

## 为什么在 Sealos 上部署 BentoPDF？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署、存储、网络和生命周期管理。部署 BentoPDF 到 Sealos 后，你可以获得：

- **一键部署**：从应用商店模板启动 PDF 工具箱。
- **即时公网访问**：Sealos 创建生成的 HTTPS 端点。
- **隐私优先设计**：PDF 处理发生在用户浏览器中。
- **简单运维**：运行单个轻量 Web 容器。
- **资源易控**：可在 Sealos 控制台调整 CPU 和内存。

## 部署指南

1. 打开 [BentoPDF 模板](https://sealos.io/products/app-store/bentopdf)，点击 **Deploy Now**。
2. 检查生成的 host 和应用名称，然后部署。
3. 等待部署完成，然后打开生成的应用 URL。
4. 通过提供的 URL 访问应用：
   - **BentoPDF UI**：打开 URL 后直接使用 PDF 工具。默认自托管版本无需登录或注册。

## 配置

部署后，如需自定义品牌或商业构建，可在 Deployment 资源卡中更新环境变量或容器镜像。

## 扩缩容

BentoPDF 是静态客户端 Web 应用，小团队使用单副本即可。预计访问量更高时，可在 Deployment 资源卡中增加副本数。

## 故障排查

### 页面已加载但某个工具无法下载外部 WASM 资源

- 原因：部分可选处理模块默认从上游 CDN 加载。
- 解决：查看上游 WASM 配置文档，为离线或自托管模块托管做配置。

### 浏览器显示连接错误

- 原因：部署仍在启动，或 Ingress 就绪前复制了公开 URL。
- 解决：等待 Deployment 就绪后重新打开 Sealos App URL。

## 其他资源

- [BentoPDF 文档](https://bentopdf.com/docs/)
- [许可证](https://bentopdf.com/licensing.html)
- [Docker Package](https://github.com/alam00000/bentopdf/pkgs/container/bentopdf-simple)

## 许可证

此 Sealos 模板遵循仓库许可证。BentoPDF 本身采用双许可证；商业使用前请查看上游许可证说明。
