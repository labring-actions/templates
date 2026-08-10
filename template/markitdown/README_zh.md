# 在 Sealos 上部署和托管 MarkItDown MCP

MarkItDown MCP 是 Microsoft 官方 MCP 服务，用于将文档和远程资源转换为 Markdown。此模板在 Sealos Cloud 上运行上游 Streamable HTTP 与 SSE 服务，并通过 HTTPS 公开协议端点。

![MarkItDown MCP](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/markitdown/website-screenshot.webp)

## 关于托管 MarkItDown MCP

`markitdown-mcp` 软件包提供一个 MCP 工具 `convert_to_markdown(uri)`，支持 `http:`、`https:`、`file:` 和 `data:` URI。官方容器在端口 `3001` 启动服务，并提供 Streamable HTTP 和 SSE 传输协议。

Sealos 模板完整保留上游协议接口。它为 MCP 服务需要读取的文件配置 1 GiB `/workdir` 持久卷，为 `/mcp/`、`/sse` 和 `/messages/` 配置 HTTPS Ingress，并创建指向 `/mcp/` 的 Canvas App 入口。服务器以无内置认证模式运行，请通过可信 MCP 客户端和网络访问控制限制访问范围。

## 常见使用场景

- **智能体文档摄取**：让 MCP 客户端转换 PDF、Office 文件、HTML、CSV 和其他受支持格式。
- **远程资源转换**：直接转换 HTTPS 或 data URI，无需增加独立应用封装层。
- **本地工作区转换**：将可信文件放入 `/workdir`，再通过 `file:` URI 引用。
- **MCP Inspector 测试**：检查官方工具 schema，并通过 `/mcp/` Streamable HTTP 端点执行转换请求。

## MarkItDown MCP 托管依赖

此模板包含从 Microsoft 上游 `packages/markitdown-mcp/Dockerfile` 构建的 Docker MCP Catalog 镜像、StatefulSet、持久化 `/workdir` 卷、Service、HTTPS Ingress 和 Canvas App 入口。

### 部署依赖

- [MarkItDown 仓库](https://github.com/microsoft/markitdown) - 源代码与版本
- [MarkItDown MCP README](https://github.com/microsoft/markitdown/blob/main/packages/markitdown-mcp/README.md) - 官方传输协议与客户端配置
- [MarkItDown MCP 软件包](https://pypi.org/project/markitdown-mcp/) - Python 软件包元数据
- [模型上下文协议（Model Context Protocol）](https://modelcontextprotocol.io/) - 客户端与协议文档
- [Sealos 文档](https://sealos.io/docs) - 平台文档

## 实现细节

### 架构组件

- **MCP 服务**：运行上游 `markitdown-mcp --http --host 0.0.0.0 --port 3001` 命令。
- **持久工作目录**：挂载 `/workdir` 以存放可信本地文件。
- **Service 与 Ingress**：通过 `/mcp/` 提供 Streamable HTTP，通过 `/sse` 提供 SSE，并通过 `/messages/` 接收 SSE 消息请求。

### 配置

上游镜像启用官方 MarkItDown 插件，并包含 `ffmpeg` 与 `exiftool`。运行时仅依赖持久工作目录，无需数据库、S3 或登录参数。服务器以无内置认证模式运行；处理敏感文档前，请使用私有 Sealos 工作区、额外的认证代理或网络白名单。

### 资源配置

| 组件 | 副本数 | CPU 上限 | 内存上限 | 存储 |
| --- | ---: | ---: | ---: | ---: |
| MarkItDown MCP | 1 | `100m` | `256Mi` | - |
| 工作目录 | 1 | - | - | `1Gi` |

这是协议请求和小型文档面向个人低负载场景的初始档位。处理大型 PDF 或包含大量嵌入图片的转换任务时，请增加内存。

### 许可证信息

MarkItDown 和官方 MCP 软件包均采用 MIT License。

## 为什么在 Sealos 上部署 MarkItDown MCP？

Sealos 是基于 Kubernetes 构建的 AI 辅助云操作系统。在 Sealos 上托管官方 MCP 服务可获得一键配置、自动 HTTPS、持久工作区存储、按量付费资源，以及适用于可信智能体环境的 Canvas 运维能力。

- **一键部署**：从应用商店模板启动，并保留官方 MCP 命令。
- **协议原生端点**：将 MCP 客户端直接连接到 `/mcp/` 或 `/sse`。
- **持久工作区**：在重启后继续保留 `/workdir` 下的可信本地输入文件。
- **运维可见性**：通过 Canvas、AI 对话和资源卡片检查日志与资源用量。

## 部署指南

1. 打开 [MarkItDown MCP 模板](https://sealos.io/products/app-store/markitdown)，点击 **Deploy Now**。
2. 等待部署完成，通常需要 2-3 分钟。随后 Sealos 会打开 Canvas。
3. 复制生成的 HTTPS 主机地址并选择传输协议：Streamable HTTP 使用 `https://<host>/mcp/`，SSE 使用 `https://<host>/sse`。
4. 在可信 MCP 客户端中配置所选端点，并运行 `tools/list` 验证 `convert_to_markdown` 工具。

## MCP 客户端配置

Streamable HTTP 客户端使用：

```text
https://<your-markitdown-host>/mcp/
```

SSE 客户端使用：

```text
https://<your-markitdown-host>/sse
```

服务器以无登录页和无内置认证模式运行。请将此端点视为高权限文档获取服务：`convert_to_markdown` 可以读取容器可访问的文件，并获取运行时网络范围内的远程资源。

## 配置与扩缩容

将可信本地文件放入 `/workdir`，并通过 `file:///workdir/<name>` 引用。通过 Canvas 资源卡片调整 CPU、内存和存储。使用 ReadWriteOnce 工作目录时保持单副本；配置外部共享文件方案和访问控制层后再扩展副本。

## 故障排查

### MCP 客户端无法连接

确认 Streamable HTTP 客户端使用 `/mcp/`，SSE 客户端使用 `/sse`，且 Sealos URL 使用 HTTPS。通过 Canvas 检查 MCP 容器日志和 Service 端点。

### 本地文件无法转换

将文件上传到 `/workdir` 并使用 `file:///workdir/...` URI。容器仅能读取已上传到其工作区的文件。

### 大型文档超时

处理大型 PDF、嵌入图片或音频转换时，请在 Canvas 中增加容器内存档位和 Ingress 读写超时时间。

### 安全审查

上游服务以无认证模式运行。处理机密文档前，请使用网络策略或认证反向代理限制公网域名，并将 MCP 端点开放范围限定为可信客户端。

### 获取帮助

- [MarkItDown MCP 文档](https://github.com/microsoft/markitdown/blob/main/packages/markitdown-mcp/README.md)
- [MarkItDown Issues](https://github.com/microsoft/markitdown/issues)
- [Sealos 文档](https://sealos.io/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [MarkItDown v0.1.7 版本](https://github.com/microsoft/markitdown/releases/tag/v0.1.7)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- [Sealos 应用商店](https://sealos.io/products/app-store)

## 许可证

此 Sealos 模板依据 templates 仓库许可证提供给 Sealos 用户。MarkItDown 本身采用 [MIT License](https://github.com/microsoft/markitdown/blob/main/LICENSE)。
