# 在 Sealos 上部署和托管 Odysseus

Odysseus 是一个自托管 AI 工作空间，包含聊天、深度研究、记忆、工具、日历、笔记和文档工作流。此模板在 Sealos Cloud 上部署 Odysseus，并内置 Chroma 与 SearXNG 服务。

![Odysseus 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/odysseus/website-screenshot.webp)

## 关于托管 Odysseus

Odysseus 以 Web 应用运行，使用本地 SQLite 数据、持久化文件存储、Chroma 向量记忆和 SearXNG 搜索。模板会分别创建 Odysseus、Chroma、SearXNG StatefulSet，并为应用数据、日志、SSH 状态、Hugging Face 缓存、本地缓存、Chroma 数据和 SearXNG 缓存创建持久卷。

模板会根据部署表单创建初始管理员。OpenAI API Key 是可选项，本地模型端点可在 Odysseus 设置界面中继续配置。

## 常见使用场景

- **自托管 AI 工作空间**：在一个界面中使用聊天、工具、笔记、文档和日历。
- **深度研究**：运行带搜索和综合输出的多步骤研究流程。
- **持久记忆**：通过 Chroma 向量记忆存储和检索知识。
- **私有生产力中心**：把工作区产物保存在自己的 Sealos 部署中。

## Odysseus 托管依赖

Sealos 模板包含 Odysseus 应用镜像、Chroma 向量数据库、SearXNG 搜索服务、持久化存储和公开 HTTPS 入口。

### 部署依赖

- [GitHub 仓库](https://github.com/pewdiepie-archdaemon/odysseus) - 源代码
- [Chroma](https://www.trychroma.com/) - 向量记忆服务
- [SearXNG](https://docs.searxng.org/) - 搜索服务

## 实现细节

**架构组件：**

- **Odysseus**：主 Web UI 和 API 服务。
- **Chroma**：集群内网中的向量记忆服务。
- **SearXNG**：用于 Web research 的内部元搜索服务。
- **持久化存储**：数据、日志、SSH 状态、Hugging Face 缓存、本地缓存、Chroma 数据和 SearXNG 缓存卷。

**配置：**

- `admin_user` 和 `admin_password` 创建初始管理员账号。
- `openai_api_key` 是可选项。
- SQLite 通过上游 `ODYSSEUS_DATA_DIR` 设置保存在 `/app/data` 下。

**许可证信息：**

Odysseus 使用 AGPL-3.0-or-later。

## 为什么在 Sealos 上部署 Odysseus？

Sealos 提供自动 HTTPS、持久化存储、内部服务发现，并支持一键部署 Odysseus 及所需的 Chroma、SearXNG 服务。

## 部署指南

1. 打开 [Odysseus 模板](https://sealos.io/products/app-store/odysseus)，点击 **Deploy Now**。
2. 在弹窗中配置参数。设置初始管理员用户名和密码。
3. 等待部署完成，通常需要 3-5 分钟。部署完成后会进入 Canvas。
4. 打开生成的应用 URL，使用配置的管理员凭据登录。

## 配置

登录后，可在 Odysseus UI 中配置模型供应商、本地模型端点、搜索、记忆和工作区工具。存储和资源限制可在 Sealos Canvas 的资源卡片中调整。

## 更多资源

- [Odysseus GitHub](https://github.com/pewdiepie-archdaemon/odysseus)
- [GitHub Issues](https://github.com/pewdiepie-archdaemon/odysseus/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

此模板遵循上游 Odysseus AGPL-3.0-or-later License。
