# 在 Sealos 上部署和托管 Whoogle Search

Whoogle Search 是一个自托管的 Google 搜索结果元搜索前端，提供隐私控制、可选 Basic Auth，并减少跟踪型客户端脚本。此模板会在 Sealos 上以单个 Web 服务部署 Whoogle Search。

![Whoogle Search 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/whoogle-search/website-screenshot.webp)

## 关于托管 Whoogle Search

Whoogle Search 使用官方容器镜像运行，并在 `5000` 端口提供搜索界面。Sealos 会创建工作负载、内部 Service、HTTPS Ingress、公开 App 入口，以及与官方 Docker Compose 内存设置一致的资源限制。

模板通过部署输入支持可选 HTTP Basic Auth。两个字段都留空时，搜索页面会直接打开；同时填写用户名和密码时，访问界面需要登录。

## 常见使用场景

- **私有搜索前端**：通过自托管界面搜索，减少跟踪和广告型页面元素。
- **团队搜索工具**：为小团队提供受保护的搜索入口。
- **浏览器搜索引擎**：把部署后的 URL 添加为浏览器自定义搜索引擎。
- **Google CSE 备用方案**：当常规抓取不稳定时，在 Whoogle 中配置 Custom Search Engine 凭据。

## Whoogle Search 托管依赖

此 Sealos 模板包含 Whoogle Search 容器、Kubernetes Service、HTTPS Ingress 和 Sealos App 入口。

### 部署依赖

- [官方仓库](https://github.com/benbusby/whoogle-search) - 源代码与部署说明
- [环境变量](https://github.com/benbusby/whoogle-search#environment-variables) - 运行配置参考
- [Sealos](https://sealos.io) - 基于 Kubernetes 的应用托管平台

### 实现细节

**架构组件：**

- **Whoogle Search Web 服务**：运行 `benbusby/whoogle-search:1.2.4`，在 `5000` 端口提供界面。
- **Service 与 Ingress**：提供集群内路由和公开 HTTPS 访问。
- **Sealos App 入口**：从 Sealos 控制台打开生成的公开 URL。

**配置：**

模板会把 `WHOOGLE_CONFIG_URL` 设置为生成的 HTTPS URL，并提供可选 `WHOOGLE_USER` 与 `WHOOGLE_PASS` 输入。Whoogle 会在容器管理的配置路径中保存轻量运行配置。

**许可证信息：**

此 Sealos 模板遵循仓库许可证。Whoogle Search 使用 MIT License。

## 为什么在 Sealos 上部署 Whoogle Search？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署、公开访问和运维。通过 Sealos 部署 Whoogle Search，你可以获得：

- **一键部署**：从 App Store 模板页面启动搜索前端。
- **即时公开访问**：Sealos 自动创建 HTTPS URL。
- **资源控制**：模板中已经定义 CPU 和内存限制。
- **运维 Canvas**：部署后可从 Sealos Canvas 更新输入和资源。

## 部署指南

1. 打开 [Whoogle Search 模板](https://sealos.io/products/app-store/whoogle-search)，点击 **Deploy Now**。
2. 配置可选 Basic Auth 输入。填写用户名和密码可启用登录保护，两个字段留空则直接访问。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续需要修改时，可以在对话框描述需求让 AI 应用更新，或点击相关资源卡片修改设置。
4. 通过提供的 App URL 访问 Whoogle Search。启用 Basic Auth 时，使用第 2 步设置的用户名和密码登录。

## 配置

部署后，可以在 Whoogle UI 配置菜单中调整可选搜索行为。基础设施调整可以通过 Sealos Canvas、AI 对话框或工作负载资源卡完成。

## 更多资源

- [Whoogle Search README](https://github.com/benbusby/whoogle-search)
- [Custom Search Engine 设置](https://github.com/benbusby/whoogle-search#google-custom-search-byok)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板遵循仓库许可证。Whoogle Search 使用 MIT License。
