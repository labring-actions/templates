# 在 Sealos 上部署和托管 FreeLLMAPI

FreeLLMAPI 是面向个人的 AI 网关，可统一管理供应商密钥，并通过兼容 OpenAI 的应用程序接口（API）转发请求。本模板在 Sealos Cloud 上部署官方 FreeLLMAPI v0.9.8 镜像，包含网页控制台和持久化 SQLite 存储。

![FreeLLMAPI 官网](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/freellmapi/website-screenshot.webp)

## 关于托管 FreeLLMAPI

FreeLLMAPI 集成了供应商密钥管理、模型路由、自动回退、聊天测试和请求分析。创建控制台账号后，添加自己的供应商凭据，再使用网关提供的统一 API 密钥和 `/v1` 基础地址连接兼容客户端。模型可用性、配额和费用均遵循各供应商的规则。

官方容器通过 3001 端口同时提供 React 控制台和 Express API。Sealos 自动创建一个应用副本、1 GiB 持久卷和公网 HTTPS 地址。SQLite 数据库、已保存对话、供应商设置和加密密钥均存放在持久卷中，Pod 重启后继续保留。

本部署遵循 FreeLLMAPI 面向个人的单用户模式。首个账号创建后即成为控制台账号；密码用于登录控制台，独立的统一 API 密钥用于验证模型调用客户端。

## 常见使用场景

- **个人编程助手：** 将兼容 OpenAI 的工具接入统一网关地址。
- **供应商回退：** 根据可用性，在已配置的供应商和模型之间转发请求。
- **模型测试：** 在 Playground 中测试提示词，通过 Analytics 查看使用情况。
- **密钥管理：** 在自己的部署中保存供应商密钥，为客户端提供统一 API 密钥。

## FreeLLMAPI 托管依赖

模板已包含 Node.js、编译后的控制台、API 服务、SQLite 和持久化存储。供应商凭据在应用部署完成后填写。

### 部署依赖

- [官方网站](https://freellmapi.co)
- [Docker 部署指南](https://github.com/tashfeenahmed/freellmapi/blob/v0.9.8/docker/README.md)
- [安装文档](https://github.com/tashfeenahmed/freellmapi/blob/v0.9.8/docs/en/install/01-install.md)
- [支持与问题反馈](https://github.com/tashfeenahmed/freellmapi/issues)

### 实现细节

**架构组件：**

- **应用：** 一个 StatefulSet，运行 `ghcr.io/tashfeenahmed/freellmapi:v0.9.8`，提供控制台和 API。
- **初始化：** 一个轻量初始化容器，在服务启动前创建并校验持久化加密密钥。
- **存储：** 一个 1 GiB 持久卷，挂载到 `/app/server/data`，运行数据存放在其中的 `runtime` 子目录。
- **网络：** 3001 端口的 Service，以及自动提供 HTTPS 的 Sealos Ingress。

**配置：**

| 项目 | 模板设置 |
| --- | --- |
| 应用副本数 | 1 |
| 主容器限制 / 预留资源 | 100m CPU、128Mi 内存 / 10m CPU、12Mi 内存 |
| 初始化容器限制 / 预留资源 | 100m CPU、128Mi 内存 / 10m CPU、12Mi 内存 |
| 数据库 | `/app/server/data/runtime/freeapi.db` |
| 加密密钥 | `/app/server/data/runtime/.encryption-key`，仅所有者可读写，权限为 `0600` |
| 健康检查接口 | `/api/ping` |
| 运行身份 | 非 root 用户，UID/GID 为 1000 |

加密密钥在首次启动时通过操作系统随机源生成，校验为 64 位十六进制字符串，并在生产模式下加载为 `ENCRYPTION_KEY`。请将数据库和原始加密密钥一并备份到受保护的位置。SQLite 部署保持一个副本，使用量增加时可提高 CPU 或内存。

模板设置了 `FREEAPI_BLOCK_PRIVATE_PROVIDER_URLS=true`，会拦截指向私有网络的供应商地址。自定义供应商请使用公网可访问的 HTTPS 接口。

**许可证信息：** FreeLLMAPI 采用 MIT 许可证。

## 为什么在 Sealos 上部署 FreeLLMAPI？

[Sealos](https://sealos.io) 基于 Kubernetes，支持通过 Canvas、资源卡片和 AI 对话框管理应用。

- **一键部署：** 一个模板即可创建应用、持久化存储和 HTTPS 地址。
- **资源效率：** 从经过个人低负载测试的配置起步，资源按量付费。
- **持久化状态：** 重启后保留账号、供应商配置、对话和密钥。
- **运行状态可见：** 在应用的 Canvas 资源卡片中查看日志和资源使用情况。

## 部署指南

1. 打开 [FreeLLMAPI 模板](https://sealos.io/products/app-store/freellmapi)，点击 **Deploy Now（立即部署）**。
2. 检查部署配置并确认。账号和供应商凭据在应用启动后填写。
3. 等待部署完成，通常需要 **2-3 分钟**。Sealos 随后打开 Canvas，应用资源卡片提供日志、配置和公网 HTTPS 地址。
4. 打开应用地址，在 **Create your account（创建账号）** 页面填写有效邮箱和至少 **8 个字符**的密码，点击 **Create account（创建账号）**。
5. 远程注册会出现 **Setup code（设置码）** 输入框。回到 Canvas，打开 FreeLLMAPI 资源卡片，查看主容器日志中的最新 `First-run setup code:`，将对应代码填入表单并再次提交。应用在账号创建前每次重启都会生成新代码，注册成功后代码即失效。
6. 打开 **Keys → Add key（密钥 → 添加密钥）**，配置供应商。添加兼容 OpenAI 的自定义供应商时，填写其 HTTPS 基础地址、API 密钥和支持的模型 ID。
7. 打开 **Playground**，选择已配置的模型并发送一条简短消息。兼容客户端所需的凭据和基础地址可在 **Keys → Unified API key（密钥 → 统一 API 密钥）** 标签页查看。

### 登录和密码恢复

注册完成后，在 **Sign in（登录）** 页面使用相同邮箱和密码登录。账号创建入口仅在首个账号创建前开放。

需要恢复密码时，选择 **Forgot password? → Send reset code（忘记密码？→ 发送重置码）**。通过 Canvas 查看应用主容器日志，找到刚生成的密码重置码，填入重置码和至少 8 个字符的新密码，再重新登录。远程首次注册和密码恢复均需要查看应用日志。

## 配置与扩容

供应商、模型、路由和客户端凭据在 FreeLLMAPI 内管理。调整基础设施时，打开 Canvas，在 AI 对话框中描述修改要求，或编辑应用资源卡片。处理更大请求或更多并发时可增加 CPU 和内存，并保持一个应用副本。

## 故障排查

**设置码被拒绝：** 查看当前运行的主容器日志，使用最新 `First-run setup code:` 对应的代码。账号创建前重启应用会生成新代码。

**客户端提示身份验证错误：** 连接此网关时，使用 **Keys → Unified API key（密钥 → 统一 API 密钥）** 中的密钥。上游供应商自己的密钥单独配置在 **Keys** 页面中。

**模型请求失败：** 检查供应商密钥、模型 ID、可用配额和 HTTPS 基础地址。自定义供应商填写的模型 ID 需要与对应接口实际提供的模型一致。

**删除密钥后，已有数据库启动失败：** 将原始 `.encryption-key` 恢复到数据库所在目录。初始化检查要求保留原始密钥，以确保已加密的供应商凭据可以继续使用。

## 许可证

本 Sealos 模板遵循模板仓库的许可证。FreeLLMAPI 本身采用 [MIT 许可证](https://github.com/tashfeenahmed/freellmapi/blob/v0.9.8/LICENSE)。
