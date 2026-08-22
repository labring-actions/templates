# 在 Sealos 上部署和托管 Manim

Manim 是一个社区维护的 Python 框架，用于创建精确的数学动画。此模板在 Sealos Cloud 上使用官方 Manim 镜像部署基于浏览器的 JupyterLab 工作区。

![应用截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/manim/website-screenshot.webp)

## 关于托管 Manim

Manim 运行在官方 `manimcommunity/manim` 容器中，其中包含 Python、Manim、图形库和动画渲染所需的 TeX 依赖。Sealos 模板将 JupyterLab 作为浏览器入口启动，便于在 Web 工作区中创建 notebook、脚本和渲染媒体。

部署包含挂载到 `/manim` 的持久化存储，因此 notebook、Python 文件和生成的媒体可在重启后保留。访问通过模板默认值中生成的 Jupyter token 保护。

## 常见使用场景

- **数学动画原型设计**：通过浏览器创建和预览 Manim 场景。
- **教学材料制作**：为代数、几何、微积分和物理构建可视化讲解。
- **Notebook 实验**：将 Python 笔记、代码和渲染输出组合在一起。
- **云端渲染工作区**：将 Manim 项目保存在持久化云存储中。

## Manim 托管依赖

Sealos 模板包含官方 Manim 容器和持久化工作区存储。

### 部署依赖

- [Manim Community 官网](https://www.manim.community/) - 项目主页
- [Manim Docker 文档](https://docs.manim.community/en/stable/installation/docker.html) - 官方容器说明
- [JupyterLab 文档](https://jupyterlab.readthedocs.io/) - 浏览器工作区文档

### 实现细节

**架构组件：**

此模板部署一个服务：

- **Manim JupyterLab**：监听 `8888` 端口的浏览器工作区
- **持久化工作区**：挂载到 `/manim` 的存储卷

**配置：**

- JupyterLab 使用生成的 token 启动。
- Jupyter 登录页要求认证时，使用部署默认值中的 token。
- 项目文件和生成媒体保存在 `/manim` 中。
- CPU 和内存高于基础值，因为渲染、TeX 和 notebook 工作流需要更多资源。

**许可证信息：**

Manim Community Edition 使用 MIT License。

## 为什么在 Sealos 上部署 Manim？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，统一提供部署、存储、网络和后续运维能力。在 Sealos 上部署 Manim 可以获得：

- **一键部署**：从应用商店启动可用的 Manim 工作区。
- **持久化工作区存储**：notebook、脚本和渲染媒体可在重启后保留。
- **即时 HTTPS 访问**：通过生成的公网 URL 打开 JupyterLab。
- **AI 辅助运维**：使用 Canvas AI 对话调整资源或更新配置。
- **按量付费效率**：以适中的渲染工作区起步，并在场景变重时扩容。

## 部署指南

1. 打开 [Manim 模板](https://sealos.io/products/app-store/manim)，点击 **Deploy Now**。
2. 查看生成的 Jupyter token，并保存用于登录。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续修改可在对话框中描述需求，让 AI 应用变更，或点击相关资源卡片修改设置。
4. 通过提供的 URL 访问 JupyterLab，并使用生成的 token 登录。

## 配置

部署后可以通过以下方式配置 Manim：

- **JupyterLab UI**：创建 notebook、Python 文件和终端会话。
- **AI 对话**：让 Sealos 调整 CPU、内存或存储。
- **资源卡片**：在 Canvas 中修改 StatefulSet 和存储资源。

## 扩展

复杂场景、高分辨率渲染或大量 TeX 的项目需要更多内存。打开 Canvas，点击 Manim StatefulSet 资源卡片，调整 CPU 或内存并应用。

## 故障排查

**Jupyter 要求输入 token**

使用模板默认值中生成的 token。

**渲染很慢或因内存压力失败**

通过 StatefulSet 资源卡片提高 CPU 和内存。

## 更多资源

- [Manim 文档](https://docs.manim.community/)
- [Manim Docker 文档](https://docs.manim.community/en/stable/installation/docker.html)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板遵循模板仓库许可证。Manim Community Edition 本身使用 MIT License。
