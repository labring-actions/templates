# 在 Sealos 上部署和托管 Stirling-PDF

Stirling-PDF 是一个自托管 PDF 工具箱，支持合并、拆分、转换、OCR、压缩、涂黑等文档处理流程。此模板会在 Sealos Cloud 上部署 Stirling-PDF `2.14.2-fat`，提供登录保护、持久化存储，以及需要许可证的可选 PostgreSQL 拓扑。

![Stirling-PDF 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/s-pdf/website-screenshot.webp)

## 关于托管 Stirling-PDF

Stirling-PDF 通过 `8080` 端口提供 Web 界面和 API。模板会创建单副本 StatefulSet、四个持久卷、Service、HTTPS Ingress 和 Sealos App 入口。四个持久卷分别保存 `/usr/share/tessdata` 下的 OCR 语言数据、`/configs` 下的应用配置与默认 H2 数据库、`/logs` 下的日志，以及 `/storage` 下受登录保护的用户文件。

每次部署都会开启登录保护。必填参数 `SECURITY_INITIALLOGIN_USERNAME` 和 `SECURITY_INITIALLOGIN_PASSWORD` 用于初始化全新 `/configs` 数据卷上的管理员账户。

## 常见使用场景

- **PDF 操作入口**：在浏览器中完成合并、拆分、旋转、压缩、加水印、涂黑和整理。
- **文档格式转换**：借助 fat 镜像内置工具转换 PDF、Office、图片、HTML 和电子书格式。
- **OCR 工作流**：使用持久化 OCR 语言数据处理扫描文档。
- **团队私有工具**：通过管理员登录保护文档工具和存储文件。

## Stirling-PDF 托管依赖

社区拓扑使用 Stirling-PDF 内置 H2 数据库和本地持久化文件存储。当 `use_postgresql=true` 且 `PREMIUM_KEY` 已填写时，持证拓扑会增加 KubeBlocks PostgreSQL 16 集群。

### 实现细节

**架构组件：**

- **Stirling-PDF**：使用 `stirlingtools/stirling-pdf:2.14.2-fat`，对应官方版本的多架构摘要 `sha256:aa91c68b85992986302fbdb6735f2c0824e329304e43c814a9b77c9dd0dbe410`。
- **持久化存储**：四个 `1Gi` 存储卷，分别用于 OCR 数据、配置/H2、日志和受保护的用户文件。
- **PostgreSQL**：启用 PostgreSQL 并填写许可证密钥后，模板会创建独立 KubeBlocks `postgresql-16.4.0` 集群，并通过幂等初始化 Job 创建 `stirling_pdf` 数据库。

**许可证边界：**

默认 H2 和本地存储拓扑使用社区许可证。Stirling-PDF 将自定义 PostgreSQL 列为 Pro 或 Enterprise 功能。模板仅在 `use_postgresql=true` 且 `PREMIUM_KEY` 有值时创建 PostgreSQL 资源；空密钥会选择社区拓扑。

## 为什么选择 Sealos 部署 Stirling-PDF？

- **一键创建拓扑**：应用、HTTPS 路由、持久卷和所选托管服务会一起部署。
- **托管凭据**：PostgreSQL 连接信息来自 Sealos 管理的 Secret。
- **资源可控**：可在 Canvas 中调整 CPU 和内存，同时保持应用单副本运行。

## 部署指南

1. 打开 [Stirling-PDF 模板](https://sealos.io/products/app-store/s-pdf)，点击 **Deploy Now**。
2. 填写初始管理员用户名和密码。
3. 社区 H2/本地存储拓扑保持 `use_postgresql=false`。
4. 持证拓扑需启用 PostgreSQL，并填写有效的 `PREMIUM_KEY`。
5. 选择界面语言以及电子书/高级 HTML 转换设置。
6. 等待 2-3 分钟，StatefulSet 和所选托管服务就绪后，从 Canvas 打开生成的 HTTPS 地址。

## 配置说明

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `SECURITY_INITIALLOGIN_USERNAME` | 全新配置卷的初始管理员用户名。 | `是` | 用户填写 |
| `SECURITY_INITIALLOGIN_PASSWORD` | 全新配置卷的初始管理员密码。 | `是` | 用户填写 |
| `use_postgresql` | 创建并使用独立 PostgreSQL，需要 Pro 或 Enterprise。 | `否` | `false` |
| `PREMIUM_KEY` | PostgreSQL 拓扑使用的 Stirling-PDF 许可证密钥。 | 条件必填 | 空 |
| `SYSTEM_DEFAULTLOCALE` | 默认界面语言。 | `否` | `en-US` |
| `INSTALL_BOOK_AND_ADVANCED_HTML_OPS` | 启用基于 Calibre 的电子书和高级 HTML 转换。 | `否` | `false` |

## 拓扑选项

| `use_postgresql` | `PREMIUM_KEY` | 运行拓扑 | 许可证 |
|------------------|---------------|----------|--------|
| `false` | 空或已填写 | 内置 H2 + 持久化 `/storage` | 社区版 |
| `true` | 空 | 内置 H2 + 持久化 `/storage` | 社区回退 |
| `true` | 有效密钥 | KubeBlocks PostgreSQL + 持久化 `/storage` | Pro 或 Enterprise |

## 故障排查

### 初始凭据无法登录

初始凭据只会写入全新的 `/configs` 数据卷。后续重启请继续使用该数据卷中已有的管理员账户。

### 持证 PostgreSQL 拓扑仍使用 H2

同时设置 `use_postgresql=true` 并填写 `PREMIUM_KEY`。Stirling-PDF 会在启动时校验 Pro 或 Enterprise 权益。

### 大型转换任务需要更多资源

执行大批量 OCR、电子书转换或团队并发任务前，可通过 Sealos Canvas 提高 StatefulSet 的 CPU 和内存。

## 更多资源

- [Stirling-PDF 文档](https://docs.stirlingpdf.com/)
- [Stirling-PDF 源代码](https://github.com/Stirling-Tools/Stirling-PDF)
- [Stirling-PDF 版本记录](https://github.com/Stirling-Tools/Stirling-PDF/releases)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

Stirling-PDF 社区代码采用 MIT 许可证，专有目录遵循上游各自的许可证。自定义 PostgreSQL 需要付费的 Stirling-PDF Pro 或 Enterprise 权益。此 Sealos 模板遵循模板仓库许可证。
