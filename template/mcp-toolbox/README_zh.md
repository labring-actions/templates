# 在 Sealos 上部署和托管 MCP Toolbox for Databases

MCP Toolbox for Databases 是面向数据库工具的开源 Model Context Protocol 服务器。此模板会在 Sealos Cloud 上部署官方 Toolbox 服务和 KubeBlocks PostgreSQL。

![MCP Toolbox 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/mcp-toolbox/website-screenshot.webp)

## 关于托管 MCP Toolbox for Databases

MCP Toolbox 通过 Model Context Protocol 工具把 AI Agent、IDE 和应用连接到数据库。此模板使用 PostgreSQL 预构建配置启动官方 Toolbox 容器，并创建一个可立即探索的 PostgreSQL 数据库。

暴露的端点是面向兼容客户端的 MCP server endpoint。你可以把 Codex、Claude Code、Gemini CLI 或其他 MCP 客户端连接到生成的 Sealos URL。

## 常见使用场景

- **Agent 数据库访问**：让 AI Agent 检查 schema 并执行受控 SQL。
- **IDE 数据库工具**：将 MCP 兼容 IDE 连接到 PostgreSQL 工具。
- **工具原型验证**：在接入生产数据库前验证 MCP 数据库工作流。
- **Schema 探索**：使用表列表、数据库概览等 PostgreSQL 预构建工具。

## MCP Toolbox 托管依赖

Sealos 模板包含 MCP Toolbox 和 KubeBlocks PostgreSQL。

### 部署依赖

- [MCP Toolbox 文档](https://mcp-toolbox.dev/) - 官方文档
- [Docker 部署指南](https://mcp-toolbox.dev/documentation/deploy-to/docker/) - 官方 Docker 部署方式
- [PostgreSQL 预构建配置](https://mcp-toolbox.dev/integrations/postgres/prebuilt-configs/postgresql/) - 可用工具和环境变量
- [GitHub 仓库](https://github.com/googleapis/mcp-toolbox) - 源码和发布版本

### 实现细节

**架构组件：**

- **Toolbox server**：官方 `us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:1.5.0` 镜像
- **PostgreSQL**：包含 `toolbox_db` 数据库的 KubeBlocks PostgreSQL 16.4 集群
- **Ingress**：面向 MCP 客户端和 SDK 的公开 HTTPS 端点

**配置：**

模板通过官方 `POSTGRES_*` 环境变量传入 PostgreSQL 连接信息，并使用 `--prebuilt=postgres`、`--address=0.0.0.0`、`--port=5000` 启动 Toolbox。

**许可证信息：**

MCP Toolbox for Databases 使用 Apache License 2.0。

## 为什么在 Sealos 上部署 MCP Toolbox for Databases？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一应用部署、存储、网络和生命周期管理。部署 MCP Toolbox 到 Sealos 后，你可以获得：

- **一键部署**：从应用商店模板启动 Toolbox 和 PostgreSQL。
- **托管数据库**：KubeBlocks 创建 PostgreSQL，便于立即测试 MCP。
- **即时公网访问**：每次部署都会获得生成的 HTTPS 端点。
- **易于定制**：可在 Sealos 控制台调整资源和环境变量。
- **Agent 就绪运行时**：MCP 兼容工具可直接连接公开端点。

## 部署指南

1. 打开 [MCP Toolbox 模板](https://sealos.io/products/app-store/mcp-toolbox)，点击 **Deploy Now**。
2. 检查生成的 host 和应用名称，然后部署。
3. 等待部署完成。PostgreSQL 数据库会在 Toolbox 启动前创建。
4. 将 MCP 客户端或 SDK 连接到生成的公开 URL，例如 `https://[your-app-url]`。

## 配置

在 MCP 客户端配置中填写生成的 Sealos URL。使用 SDK 时，也用同一个 URL 初始化 Toolbox client。

## 扩缩容

如需扩缩容 Toolbox，打开部署对应 Canvas，点击 Deployment 资源卡，调整 CPU、内存或副本数后应用变更。

## 故障排查

### MCP 客户端无法连接

- 原因：客户端仍使用本地 URL，或部署仍在启动中。
- 解决：使用生成的 Sealos HTTPS URL，并等待 Toolbox Pod 就绪。

### PostgreSQL 工具调用失败

- 原因：数据库为空，或查询需要默认连接之外的权限。
- 解决：创建表，或通过更新 source 配置把 Toolbox 连接到目标数据库。

## 其他资源

- [预构建工具参考](https://mcp-toolbox.dev/documentation/configuration/prebuilt-configs/)
- [PostgreSQL Source 参考](https://mcp-toolbox.dev/integrations/postgres/source/)
- [MCP 协议](https://modelcontextprotocol.io/)

## 许可证

此 Sealos 模板遵循仓库许可证。MCP Toolbox for Databases 本身使用 Apache License 2.0。
