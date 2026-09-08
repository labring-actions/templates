# 在 Sealos 上部署和托管 BentoPDF

BentoPDF 是一款在浏览器中运行的 PDF 工具箱，支持合并、转换、编辑和整理文档。本模板在 Sealos Cloud 上部署官方自托管版本，并提供公网 HTTPS 地址。

![BentoPDF 官网](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/bentopdf/website-screenshot.webp)

## 关于托管 BentoPDF

BentoPDF 在浏览器中本地处理文档。服务器提供应用页面和静态资源，PDF 操作与结果保存均由用户设备完成。打开部署后的地址即可直接使用工具，采用匿名访问方式。

本模板运行一个 `ghcr.io/alam00000/bentopdf-simple:2.8.8` Nginx 容器，通过 Kubernetes Service 和 Sealos HTTPS Ingress 提供访问。自托管版本直接显示工具列表，上方截图展示的是产品官网。

## 常见使用场景

- **合并文档**：将报告、收据或申请材料合并为一个 PDF。
- **整理页面**：旋转页面、拆分文档，以及重新排序或提取指定页面。
- **转换与编辑文件**：转换支持的文件格式、添加 PDF 批注，并整理待分享文档。

## BentoPDF 托管依赖

官方镜像包含 Web 服务器和应用资源。PDF 处理使用浏览器所在设备的内存和 CPU。部分工具从上游配置的内容分发网络（CDN）加载 WebAssembly 模块，使用这些工具时，浏览器需要能够访问相应的外部资源。

### 部署依赖

- [BentoPDF 文档](https://bentopdf.com/docs/)
- [Docker 部署指南](https://bentopdf.com/docs/self-hosting/docker)
- [Kubernetes 部署指南](https://bentopdf.com/docs/self-hosting/kubernetes)
- [GitHub 问题反馈](https://github.com/alam00000/bentopdf/issues)

### 实现细节

- **资源配置**：验证通过的最低服务器上限为 `100m` CPU 和 `128Mi` 内存，对应资源请求为 `10m` CPU 和 `12Mi` 内存。
- **运行架构**：一个无状态 Nginx Deployment、一个使用 `8080` 端口的 Service、一个 HTTPS Ingress，以及一个 Sealos App 入口。
- **安全配置**：Nginx 使用用户和用户组 `101` 运行，限制 Linux 权限，并关闭服务账号令牌挂载。
- **浏览器兼容性**：Ingress 保留镜像提供的跨源隔离响应头，使兼容的浏览器能够使用 `SharedArrayBuffer` 完成 Office 文件转换。
- **存储方式**：文档保留在用户设备上。上游的 S3 + CloudFront 指南介绍了独立的静态网站托管架构；本模板通过 Nginx 提供官方镜像内置的资源。应用运行时无需配置数据库或对象存储。

## 为什么在 Sealos 上部署 BentoPDF？

Sealos 提供基于 Kubernetes 的一键部署、公网 HTTPS 地址和资源监控。按量计费的资源适合轻量静态服务器，文档处理则使用各用户浏览器所在设备的资源。

部署完成后，可在 Canvas 的 AI 对话框中描述配置需求，也可以打开 Deployment、Service 和 Ingress 资源卡片调整设置。

## 部署指南

1. 打开 [BentoPDF 模板页面](https://sealos.io/products/app-store/bentopdf)，点击 **Deploy Now（立即部署）**。
2. 确认自动生成的应用名称和资源配置，然后开始部署。
3. 等待部署完成，通常需要 **2-3 分钟**。随后 Sealos 会打开该部署的 Canvas。
4. 打开 BentoPDF App 地址，即可匿名访问工具列表，选择工具开始使用。
5. 首次使用可选择 **Rotate PDF（旋转 PDF）**，选取本地 PDF，点击 **Right（向右旋转）**，再点击 **Apply Rotations（应用旋转）**。处理结果会下载到你的设备。
6. 打开 **Merge PDF（合并 PDF）**，选择两个 PDF，等待每个文件显示页数且加载提示关闭，然后点击 **Merge PDFs（合并 PDF）**，下载合并后的文档。

## 故障排查

- **Office 转换停滞**：使用新版浏览器打开公网 HTTPS 地址。添加自定义代理时保留镜像的跨源响应头，以启用 `SharedArrayBuffer`。
- **工具持续等待处理引擎**：检查浏览器能否访问配置的 WebAssembly CDN。在隔离网络中运行时，请参考上游的离线部署指南。
- **大文档耗尽内存**：分批处理文件，或使用可用内存更大的设备。PDF 处理在浏览器中完成。

## 许可证

BentoPDF 采用 [AGPL-3.0 许可证](https://github.com/alam00000/bentopdf/blob/v2.8.8/LICENSE)。上游项目也提供商业许可证，详见其[许可页面](https://bentopdf.com/licensing)。
