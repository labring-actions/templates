# 在 Sealos 上部署和托管 Sunshine

Sunshine 是面向 Moonlight 的自托管游戏串流主机，提供浏览器配置界面和客户端配对流程。此模板在 Sealos Cloud 上部署带持久化配置存储的 Sunshine。

![应用截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/sunshine/website-screenshot.webp)

## 关于托管 Sunshine

Sunshine 使用官方 LizardByte 容器镜像运行，并按照上游文档在 `47990` 端口暴露 Web UI。Sealos 模板会持久化 Sunshine 配置和缓存目录，确保账号设置、配对状态和应用配置在重启后保留。

此模板适合在云环境中测试 Web UI 配置和 Moonlight 配对流程。真实游戏串流取决于主机 GPU、编码器、网络和客户端连通性约束。

## 常见使用场景

- **Moonlight 主机配置**：通过浏览器管理 Sunshine 设置。
- **客户端配对测试**：验证 Web UI 设置和 PIN 配对流程。
- **远程串流实验环境**：在一次性云工作区中实验 Sunshine 配置。
- **文档和演示环境**：无需在本地桌面主机安装即可展示 Sunshine UI。

## Sunshine 托管依赖

Sealos 模板包含 Sunshine 应用容器和用户配置持久化存储。

### 部署依赖

- [Sunshine 文档](https://docs.lizardbyte.dev/projects/sunshine/latest/) - 官方文档
- [Getting Started Guide](https://docs.lizardbyte.dev/projects/sunshine/latest/md_docs_2getting__started.html) - Web UI 和配置流程
- [Moonlight](https://moonlight-stream.org/) - 客户端应用生态

### 实现细节

**架构组件：**

此模板部署一个服务：

- **Sunshine**：通过 Sealos Ingress 暴露 `47990` 端口的 Web UI
- **持久化配置**：挂载到 `/home/lizard/.config/sunshine` 和 `/home/lizard/.cache/sunshine` 的存储卷

**配置：**

- 首次启动时，打开 Web UI 并创建 Sunshine 用户名和密码。
- 保存首次设置时创建的用户名和密码。
- 使用 Web UI 配对 Moonlight 客户端并管理应用。
- Sunshine 上游 Web UI 内部使用自签名证书 HTTPS；模板通过 Sealos HTTPS Ingress 进行访问。

**许可证信息：**

Sunshine 使用 GNU General Public License v3.0。

## 为什么在 Sealos 上部署 Sunshine？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统，统一提供部署、存储、网络和后续运维能力。在 Sealos 上部署 Sunshine 可以获得：

- **一键部署**：从应用商店启动带持久化配置的 Sunshine。
- **即时公网访问**：通过生成的 HTTPS URL 打开 Web UI。
- **持久化设置**：首次账号设置和配置可在重启后保留。
- **AI 辅助运维**：使用 Canvas AI 对话调优资源和网络。
- **按量付费效率**：用适配当前工作负载的云资源测试 Sunshine 流程。

## 部署指南

1. 打开 [Sunshine 模板](https://sealos.io/products/app-store/sunshine)，点击 **Deploy Now**。
2. 在弹窗中检查部署设置。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续修改可在对话框中描述需求，让 AI 应用变更，或点击相关资源卡片修改设置。
4. 通过提供的 URL 访问 Sunshine。首次访问时创建 Web UI 用户名和密码，并保存用于后续登录。

## 配置

部署后可以通过以下方式配置 Sunshine：

- **Sunshine Web UI**：创建首个用户、配对客户端并管理应用。
- **AI 对话**：让 Sealos 调整 CPU、内存或存储。
- **资源卡片**：在 Canvas 中修改 StatefulSet、Service、Ingress 和存储设置。

## 扩展

Sunshine 串流工作负载可能需要高于默认模板的 CPU 和内存。打开 Canvas，点击 Sunshine StatefulSet 资源卡片，调整 CPU 或内存并应用。

## 故障排查

**出现首次设置页面**

首次访问时创建用户名和密码。请保存这些凭据，因为后续 Web UI 登录会继续使用它们。

**Moonlight 无法连接**

检查客户端连通性、所需串流端口和主机编码器可用性。Web UI 可访问时，完整游戏串流仍可能需要额外网络和硬件支持。

## 更多资源

- [Sunshine 文档](https://docs.lizardbyte.dev/projects/sunshine/latest/)
- [Sunshine GitHub 仓库](https://github.com/LizardByte/Sunshine)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板遵循模板仓库许可证。Sunshine 本身使用 GNU General Public License v3.0。
