# 在 Sealos 上部署和托管 CyberChef

CyberChef 是 GCHQ 开源的浏览器端数据处理工作台，可在同一份配方中完成编码、解码、加密、压缩与数据分析。

![CyberChef 界面](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/cyberchef/website-screenshot.webp)

## 关于 CyberChef 托管

本模板在 Sealos 上运行 CyberChef 官方镜像，提供公网 HTTPS 地址和单副本部署。所有操作都在浏览器内执行，服务端仅负责分发静态资源，资源占用很低。

部署完成后可从 App 卡片直接打开工作台。将操作拖入 Recipe 区域，在上方输入数据，即可在下方查看结果。配方可以通过 URL 保存或加入书签，便于重复执行。

## 常见使用场景

- 在应急响应中解码 Base64、十六进制、URL、JWT 或二进制载荷。
- 为数据管道编写可重复使用的编码、哈希和压缩配方。
- 在隔离的浏览器标签页中分析恶意样本和混淆脚本。
- 通过实时输入输出面板讲解密码学与数据编码。
- 转换时间戳、字符集以及 JSON、CSV 等结构化格式。

## CyberChef 托管依赖

- 具备可用 CPU 和内存配额的 Sealos 工作空间。
- 支持 JavaScript 的现代浏览器。
- 无需数据库、对象存储或外部服务。
- 模板 Ingress 提供公网 HTTPS 访问。

## 为什么在 Sealos 上部署 CyberChef？

- 从 Sealos 应用商店一键部署，无需配置服务器。
- 由平台负责 Kubernetes 调度、健康探针和自动重启。
- 按量计费的资源卡让空闲开销保持很低。
- 自动生成域名并签发公网 HTTPS 证书。
- 通过 Canvas 查看工作负载、Service 和 Ingress。
- 在 Sealos 桌面中使用 AI 对话了解部署运行情况。

## 部署指南

1. 打开 [CyberChef 模板](https://sealos.io/products/app-store/cyberchef)，点击 **Deploy Now**。
2. 保留自动生成的应用名称或自定义名称，确认资源规格后提交部署。
3. 等待 2-3 分钟让 Pod 就绪，然后从 App 卡片打开公网地址。
4. 粘贴 `SGVsbG8sIFNlYWxvcyE=` 并执行 **From Base64** 操作，确认工作台可用。
5. 从 App 卡片打开 Canvas，查看本次发布创建的 Deployment 或 StatefulSet、Service 和 Ingress。

## 许可证

CyberChef 使用 [Apache License 2.0](https://github.com/gchq/CyberChef/blob/master/LICENSE) 许可证。
