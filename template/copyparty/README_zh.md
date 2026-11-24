# 在 Sealos 上部署和托管 copyparty

copyparty 是便携式文件服务器，支持断点续传、媒体索引、WebDAV 访问和浏览器端文件管理。

![copyparty 文件浏览](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/copyparty/website-screenshot.webp)

## 关于 copyparty 托管

本模板以单副本 StatefulSet 运行 copyparty 官方镜像，并将 1 GiB 持久卷挂载到 `/w`。管理员账号为 `admin`，密码在部署时由模板输入提供。

公网地址会打开文件浏览器。使用 **Upload** 添加文件，可在目录间拖动文件，并通过缩略图和预览浏览已索引媒体。WebDAV 客户端可连接同一共享，在桌面文件管理器中访问。

## 常见使用场景

- 通过私有浏览器文件服务器共享大文件。
- 使用断点续传收集协作者上传的文件。
- 浏览带缩略图的照片、音频和视频库。
- 通过 WebDAV 将共享挂载到桌面文件管理器。
- 为实验室机器和内部团队提供轻量文件中转。

## copyparty 托管依赖

- 具备 CPU、内存和存储配额的 Sealos 工作空间。
- 用于上传文件和历史记录的 1 GiB 持久卷。
- 通过模板 input 提供的管理员密码。
- 用于桌面挂载的 WebDAV 客户端。

## 为什么在 Sealos 上部署 copyparty？

- 一键部署即可通过公网 HTTPS 使用文件浏览器。
- 由 Kubernetes 提供健康探针、调度和 Pod 自动恢复。
- 持久化存储保留文件、媒体索引和上传历史。
- 按量计费的资源卡适合个人文件服务器。
- 通过 Canvas 查看 StatefulSet、Service、Ingress 和 PVC。
- 在 Sealos 桌面中通过 AI 对话了解部署情况。

## 部署指南

1. 打开 [copyparty 模板](https://sealos.io/products/app-store/copyparty)，点击 **Deploy Now**。
2. 输入管理员密码，保留自动生成的应用名称，并确认 1 GiB 存储规格。
3. 等待 2-3 分钟让 StatefulSet 就绪，然后从 App 卡片打开公网地址。
4. 使用 `admin` 和第 2 步的密码登录，并上传一个小文件测试。
5. 使用 WebDAV 客户端连接同一 HTTPS 地址，再通过 Canvas 查看 StatefulSet、Service、Ingress 和 PVC。

## 许可证

copyparty 使用 [MIT License](https://github.com/9001/copyparty/blob/hovudstraum/LICENSE) 许可证。
