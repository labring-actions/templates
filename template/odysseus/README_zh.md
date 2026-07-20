# 在 Sealos 上部署和托管 Odysseus

Odysseus 是一个自托管 AI 工作空间，支持聊天、自主 Agent、工具、模型服务、邮件、研究、笔记和记忆。此模板会在 Sealos Cloud 上部署官方 Odysseus 1.0.2 运行包，包括 Chroma 向量记忆、SearXNG 搜索、ntfy 通知、持久化存储和公开 HTTPS 访问入口。

![Odysseus 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/odysseus/website-screenshot.webp)

## 关于托管 Odysseus

Odysseus 作为带认证的 Web 应用运行，使用本地 SQLite 数据、文件存储、Chroma、SearXNG 和 ntfy。主 Odysseus 服务在 7000 端口提供 Web UI 和 API，Chroma、SearXNG 与 ntfy 留在 Sealos 集群内网中。

此模板会创建四个 StatefulSet：Odysseus 应用、用于向量记忆的 Chroma、用于元搜索的 SearXNG、用于通知的 ntfy。持久卷会保存 Odysseus 数据、日志、SSH 状态、Hugging Face 缓存、本地模型服务文件、Chroma 数据、SearXNG 缓存和 ntfy 缓存。

Odysseus 使用 SQLite，并在进程内运行轮询器和定时任务。Odysseus StatefulSet 应保持一个副本，让所有写入操作共享同一个数据库和任务调度器。

首次管理员账号来自部署表单。全新部署中，`admin_user` 对应 `ODYSSEUS_ADMIN_USER`，`admin_password` 对应 `ODYSSEUS_ADMIN_PASSWORD`。

## 常见使用场景

- **私有 AI 工作空间**：在一个带认证的界面中运行聊天、Agent、笔记、文档和研究工具。
- **本地优先模型工作流**：连接本地或远程模型端点，并把工作区数据保存在自己的 Sealos 部署中。
- **研究助手**：使用 SearXNG 支持的 Web 研究和 Chroma 支持的记忆，构建可重复的研究会话。
- **团队生产力中心**：管理邮件、日历、工具、记忆和工作区产物，并通过管理员权限控制访问。

## Odysseus 托管依赖

Sealos 模板包含 Odysseus 应用容器、Chroma 向量数据库、SearXNG 搜索服务、ntfy 通知服务、持久化存储和 HTTPS Ingress。

### 部署依赖

- [Odysseus 官网](https://pewdiepie-archdaemon.github.io/odysseus/) - 官方项目页面
- [Odysseus GitHub 仓库](https://github.com/pewdiepie-archdaemon/odysseus) - 源代码和安装文档
- [Chroma](https://www.trychroma.com/) - 向量记忆服务
- [SearXNG](https://docs.searxng.org/) - 自托管元搜索服务
- [ntfy](https://docs.ntfy.sh/) - 通知服务

### 实现细节

**架构组件：**

- **Odysseus**：主认证 Web UI 和 API 服务。
- **Chroma**：Odysseus 使用的内部向量记忆服务。
- **SearXNG**：Odysseus 研究功能使用的内部搜索服务。
- **ntfy**：提醒集成使用的内部通知服务。
- **持久化存储**：保存应用数据、日志、SSH 状态、模型与缓存目录、Chroma 数据、SearXNG 缓存和 ntfy 缓存。
- **Ingress 与 App 入口**：由 Sealos 管理的 HTTPS 入口和仪表盘链接。

**配置：**

- `admin_user`：空数据卷首次启动时创建的初始管理员用户名。
- `admin_password`：空数据卷首次启动时创建的初始管理员密码。
- `openai_api_key`：可选 OpenAI API Key，用于云模型访问。
- `ALLOWED_ORIGINS`：自动设置为 Sealos 公开 URL。
- `SECURE_COOKIES`：为 Sealos HTTPS 入口启用安全 Cookie。

**许可证信息：**

Odysseus 使用 AGPL-3.0-or-later 许可证。此 Sealos 模板遵循上游应用的许可证条款。

## 为什么在 Sealos 上部署 Odysseus？

Sealos 是构建在 Kubernetes 上的 AI 辅助云操作系统，统一应用部署、持久化存储、网络和运维。在 Sealos 上部署 Odysseus 可以获得：

- **一键部署**：通过一个 App Store 模板部署 Odysseus、Chroma、SearXNG、ntfy、存储、Ingress 和仪表盘入口。
- **内置持久化存储**：在重启后保留工作区数据、认证文件、缓存、Chroma 记忆和搜索缓存。
- **即时公开访问**：获得托管 HTTPS URL，用于访问带认证的 Odysseus Web UI。
- **资源控制**：通过 Sealos Canvas 资源卡片调整 CPU、内存和存储。
- **AI 辅助运维**：部署后使用 Sealos AI 对话请求配置和资源变更。

## 部署指南

1. 打开 [Odysseus 模板](https://sealos.io/products/app-store/odysseus)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - `admin_user`：初始管理员用户名，例如 `admin`。
   - `admin_password`：初始管理员密码。
   - `openai_api_key`：可选 OpenAI API Key。
3. 等待部署完成，通常需要 3-5 分钟。部署完成后会进入 Canvas。
4. 打开生成的应用 URL，使用配置的 `admin_user` 和 `admin_password` 登录。

## 配置

登录后，可以在 Odysseus UI 中配置模型供应商、本地端点、SearXNG 支持的研究、记忆设置、工具、邮件、日历和用户权限。基础设施变更可以通过 Sealos Canvas AI 对话完成，也可以点击对应的 StatefulSet、Service、Ingress 或存储资源卡片调整。

初始管理员凭据会在空数据卷首次启动并创建 `/app/data/auth.json` 时生效。已有部署会继续使用持久化数据卷里保存的账号。

## 扩展

扩展或调优 Odysseus：

1. 打开当前部署的 Canvas。
2. 点击 Odysseus、Chroma、SearXNG 或 ntfy StatefulSet 资源卡片。
3. 根据工作负载调整 CPU、内存或存储。所有 StatefulSet 都应保持一个副本，以维持运行包的单实例数据模型。
4. 在对话中应用变更。

## 故障排查

### 修改部署参数后登录失败

- 原因：Odysseus 会把用户保存在持久化数据卷的 `/app/data/auth.json` 中。
- 处理：使用已有账号登录，或重置数据卷后进行全新首次启动。

### 研究工具返回结果较少

- 原因：SearXNG 启动状态或上游搜索引擎速率限制会影响元搜索结果。
- 处理：查看 SearXNG StatefulSet 日志，并在 Odysseus UI 中调整搜索设置。

### 模型下载耗时较长

- 原因：Hugging Face 与本地模型服务文件会下载到持久化缓存目录中。
- 处理：保留缓存卷，并在大模型操作前分配更多 CPU 或内存。

### 获取帮助

- [Odysseus GitHub Issues](https://github.com/pewdiepie-archdaemon/odysseus/issues)
- [Odysseus 安装指南](https://github.com/pewdiepie-archdaemon/odysseus/blob/dev/docs/setup.md)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [Odysseus 官网](https://pewdiepie-archdaemon.github.io/odysseus/)
- [Odysseus 源代码](https://github.com/pewdiepie-archdaemon/odysseus)
- [Chroma 文档](https://docs.trychroma.com/)
- [SearXNG 文档](https://docs.searxng.org/)
- [ntfy 文档](https://docs.ntfy.sh/)

## License

此 Sealos 模板遵循上游仓库许可证。Odysseus 本身使用 AGPL-3.0-or-later 许可证。
