# 在 Sealos 上部署托管 OpenClaw

OpenClaw 是面向浏览器智能体控制台和聊天渠道自动化的 AI 智能体网关。本模板会在 Sealos 云平台上以单个 StatefulSet 部署 OpenClaw，并配置持久化状态存储。

![OpenClaw 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/openclaw/website-screenshot.webp)

## 关于托管 OpenClaw

OpenClaw 在 `18789` 端口运行 Gateway 和 Control UI。Gateway 负责智能体配置、模型提供商访问、设备配对，以及浏览器智能体工作流所需的工作空间文件。

本 Sealos 模板遵循官方 Docker 与 Kubernetes 运行模型：一个 OpenClaw 容器、Gateway token 认证、`/healthz` 与 `/readyz` 探针，以及 PVC 支撑的本地状态。部署会持久化 OpenClaw 配置、工作空间数据、浏览器配对资料和包缓存。

## 常见应用场景

- **个人 AI 操作员**：运行一个可连接您所配置模型提供商的浏览器助手。
- **团队智能体控制台**：托管用于智能体设置、测试和运维检查的共享 Control UI。
- **聊天渠道自动化**：创建平台 token 后，将智能体接入消息渠道。
- **工作流原型验证**：在任务迭代过程中保留智能体工作空间文件和指令。

## 托管 OpenClaw 的依赖项

模板包含 OpenClaw Gateway 镜像和持久卷。部署时需要提供兼容的模型端点、API key 和默认模型 id。

### 部署依赖

- [官方网站](https://openclaw.ai/) - 产品网站
- [Docker 安装文档](https://docs.openclaw.ai/install/docker) - 官方容器运行指南
- [Kubernetes 安装文档](https://docs.openclaw.ai/install/kubernetes) - 官方 Kubernetes 拓扑
- [Control UI 指南](https://docs.openclaw.ai/web/control-ui) - 浏览器访问、token 与设备配对
- [安全指南](https://docs.openclaw.ai/gateway/security) - token 与远程 origin 配置

### 实现细节

**架构组件：**

本模板部署一个 OpenClaw Gateway 服务：

- **OpenClaw Gateway**：在 `18789` 端口提供 Control UI、WebSocket Gateway 和健康端点。
- **状态 PVC**：挂载 `/home/node/.openclaw`，保存 `openclaw.json`、工作空间文件和智能体状态。
- **Profile PVC**：挂载 `/home/node/.config/openclaw`，保存浏览器设备配对资料。
- **NPM 缓存 PVC**：挂载 `/home/node/.npm`，保存 OpenClaw 扩展使用的包缓存。

**配置方式：**

首次启动时，模板会写入 `openclaw.json`，内容包括：

- 启用 Gateway token 认证
- Gateway bind 模式适配 Sealos Ingress 访问
- Control UI origin 限定为生成的 Sealos HTTPS URL
- 基于 `provider_kind`、`base_url`、`api_key` 和 `model` 生成默认模型提供商
- 默认智能体工作空间 `~/.openclaw/workspace`

持久化方式采用 PVC 支撑的本地状态，和官方 Docker、Kubernetes 部署指南一致。

**许可证信息：**

OpenClaw 使用 MIT License。本 Sealos 模板遵循 templates 仓库的许可条款。

## 为什么选择在 Sealos 上部署 OpenClaw？

Sealos 是基于 Kubernetes 构建的 AI 云操作系统。在 Sealos 上部署 OpenClaw 可以获得：

- **一键部署**：打开模板页面，填写模型提供商参数，然后部署。
- **托管 HTTPS 访问**：Sealos 会为 Gateway 创建公网 URL 和 TLS 证书。
- **持久化智能体状态**：PVC 会保存工作空间、配置、profile 和缓存数据。
- **资源控制**：模板按 OpenClaw 推荐的 2 GB 内存档位映射到 Sealos resource ladder。
- **Canvas 运维**：部署后可在 Sealos Canvas 中调整环境变量、资源和副本设置。

## 部署指南

1. 打开 [OpenClaw 模板页面](https://sealos.io/products/app-store/openclaw)，点击 **Deploy Now**。
2. 在弹窗中配置参数：
   - **provider_kind**：选择 `openai_compat` 或 `anthropic_compat`。
   - **base_url**：填写提供商基础 URL，例如兼容 OpenAI 的 `/v1` 端点。
   - **api_key**：填写提供商 API key。
   - **model**：填写模型 id，例如 `claude-opus-4-6` 或 `gpt-5.2`。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后，Sealos 会跳转到 Canvas。后续修改可在 AI 对话框描述需求，或打开对应资源卡调整配置。
4. 打开 **OpenClaw** App 卡片 URL。该 URL 已在 fragment 中包含生成的 Gateway token。
5. 当 Control UI 要求首次设备配对时，执行审批：

```bash
openclaw devices list
openclaw devices approve <requestId>
```

在 Canvas 中打开 OpenClaw 容器终端运行上述命令。审批后刷新 Control UI 继续设置。

## 初始设置和登录

App URL 包含 `#token=<gateway-token>`，Control UI 会使用它向 Gateway 认证。浏览器设备配对用于保护远程访问：首次浏览器审批完成后，profile PVC 会在重启后保留配对数据。

打开 Control UI 后：

1. 确认默认 provider 和 model 已出现在模型设置中。
2. 打开默认 assistant 工作空间并发送一条简短提示词。
3. 在 Control UI 中添加消息渠道凭据，或在 StatefulSet 资源卡上编辑环境变量。

## 配置说明

部署后可通过以下方式更新 OpenClaw：

- **Control UI**：管理智能体、模型提供商、工作空间文件和渠道设置。
- **Canvas AI 对话框**：描述配置变更，让 Sealos 应用修改。
- **StatefulSet 资源卡**：编辑 provider 参数、API key 和资源限制。

调整 provider 时，让 provider 协议与 base URL 保持一致：

- `openai_compat` 用于兼容 OpenAI Chat Completions 的端点
- `anthropic_compat` 用于兼容 Anthropic Messages 的端点

## 扩展指南

OpenClaw 使用 PVC 保存本地状态，因此模板运行一个副本。调整资源的步骤：

1. 打开 OpenClaw 部署对应的 Canvas。
2. 打开 StatefulSet 资源卡。
3. 使用 Sealos 资源控件调整 CPU 或内存。
4. 应用更新并等待 Pod 进入 Ready 状态。

模板默认使用 `1` CPU 和 `2G` 内存，因为官方部署指南推荐 2 GB 内存档位以获得稳定运行表现。

## 故障排除

### Control UI 显示设备配对页面

从 Canvas 打开 OpenClaw 容器终端，运行 `openclaw devices list`，然后使用 `openclaw devices approve <requestId>` 审批页面展示的 request id。

### 模型调用失败

确认 `provider_kind`、`base_url`、`api_key` 和 `model` 与您的模型提供商匹配。对于 OpenAI 兼容提供商，base URL 通常以 `/v1` 结尾。

### Gateway 健康检查失败

打开 StatefulSet 日志，确认 Gateway 正在监听 `18789` 端口。探针调用 `/healthz` 和 `/readyz`，与官方容器健康检查保持一致。

## 额外资源

- [OpenClaw 文档](https://docs.openclaw.ai/)
- [OpenClaw GitHub 仓库](https://github.com/openclaw/openclaw)
- [Sealos 文档](https://sealos.run/docs)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

本 Sealos 模板遵循 templates 仓库的许可条款。OpenClaw 使用 MIT License。
