# 在 Sealos 上部署和托管 LLMIO

LLMIO 是一个基于 Go 的 LLM 网关，在你的上游模型服务前面提供权重负载均衡、协议互转、用量分析与费用追踪。本模板在 Sealos Cloud 上部署官方 LLMIO v0.9.4 镜像，包含网页控制台和持久化 SQLite 存储。

![LLMIO 控制台](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/llmio/website-screenshot.webp)

## 关于托管 LLMIO

LLMIO 是一个 Go 二进制，用同一个进程在 7070 端口同时提供网关和内嵌的 React 控制台，因此一个公网地址就覆盖了控制台和全部 API 入口。客户端可以使用 OpenAI Chat Completions、OpenAI Responses、Anthropic Messages 或 Gemini 原生格式；当客户端协议与上游协议不一致时，LLMIO 会在 OpenAI 与 Anthropic 之间双向互转，流式事件同样覆盖。上游的可用性、配额与计费仍遵循各服务商自己的规则。

提供商、模型以及「模型 × 上游」关联都在控制台里配置，每条关联各自带权重。请求会按权重抽签或按权重轮转分发到已绑定的上游。每次请求都会记录 TraceID、延迟分解、TPS、Token 用量和可选费用，分析页可按时间范围、提供商、模型与密钥下钻查看。

控制台由部署时设置的口令保护。同一个口令可用于调用 API 并拥有全部模型权限；面向客户端的更细粒度密钥在「密钥管理」中签发，每把密钥可以单独启用停用、设置过期时间、限制可用模型，并选择是否记录请求内容。

Sealos 会自动创建一个应用副本、一块 1 GiB 持久卷和一个公网 HTTPS 地址。保存配置、密钥与请求日志的 SQLite 数据库就落在这块卷上，Pod 重启后继续保留。

## 常见使用场景

- **一个地址接入多个客户端：** 把 Claude Code、Codex、Gemini CLI、Cherry Studio、Open WebUI 等工具都指向同一个网关。
- **权重调度与故障转移：** 在多个上游账号或服务商之间分摊流量，调整权重时客户端无需改动。
- **成本与用量可见：** 按提供商和密钥查看 Token 用量、缓存命中率、首包耗时与单次请求费用。
- **协议互转：** 让 Anthropic 协议的客户端接在 OpenAI 协议的上游上，反向亦然，客户端不必改配置。
- **按客户端发密钥：** 为每个客户端单独签发密钥并设置过期时间与模型白名单，不必共用同一个凭据。

## LLMIO 托管依赖

模板已包含网关二进制、内嵌控制台、SQLite 和持久化存储。上游服务商的凭据在应用部署完成后于 LLMIO 内配置。

### 部署依赖

- [源码仓库](https://github.com/atopos31/llmio)
- [Docker Compose 部署说明](https://github.com/atopos31/llmio/blob/v0.9.4/docker-compose.yml)
- [环境变量说明](https://github.com/atopos31/llmio/blob/v0.9.4/README_cn.md#环境变量)
- [支持与问题反馈](https://github.com/atopos31/llmio/issues)

### 实现细节

**架构组件：**

- **应用：** 一个 StatefulSet，运行 `atopos31/llmio:0.9.4`，在 7070 端口提供控制台和全部网关接口。
- **存储：** 一块 1 GiB 持久卷挂载到 `/app/db`，存放 `llmio.db` 与配额配置文件。
- **网络：** 7070 端口的 Service，以及自动提供 HTTPS 的 Sealos Ingress；控制台与各 API 前缀共用这一个地址。

**配置：**

| 项目 | 模板设置 |
| --- | --- |
| 应用副本数 | 1 |
| 容器限制 / 预留资源 | 1000m CPU、1024Mi 内存 / 100m CPU、128Mi 内存 |
| 监听端口 | 7070，通过 `LLMIO_SERVER_PORT` 显式固定 |
| 数据库路径 | `/app/db/llmio.db`，通过 `LLMIO_DB_PATH` 显式固定 |
| 凭据 | `TOKEN`，取自部署时填写的口令 |
| 配额配置 | `/app/db/quota.config.json` |
| 健康检查路径 | `/`，即控制台页面 |
| Ingress 代理超时 | 读写均为 300 秒 |
| 运行身份 | 镜像默认（root），与上游 Docker Compose 部署一致 |

请保持单副本。SQLite 是单写入端数据库，后台的日志压缩与空间回收任务也假设只有一个进程；需要更高吞吐时请提升 CPU 与内存，而不是增加副本。

请求与响应正文会写入日志库，新写入的行默认压缩存储。长期运行的网关会让持久卷持续增长：部署时可以调大存储容量，或在「系统配置」中设置日志保留天数，并使用同一页面的压缩与空间回收功能。如需把历史数据留存在别处，请从持久卷中备份 `llmio.db`。

口令必须保持非空。`TOKEN` 未设置时 LLMIO 会完全跳过鉴权，公网网关将对外界完全开放；模板默认会生成一个随机口令。

**许可证信息：** LLMIO 采用 MIT 许可证。

## 为什么在 Sealos 上部署 LLMIO？

[Sealos](https://sealos.io) 基于 Kubernetes，支持通过 Canvas、资源卡片和 AI 对话框管理应用。

- **一键部署：** 一个模板即可创建应用、持久化存储和 HTTPS 地址。
- **资源效率：** 从适合个人与小队网关流量的小规格单副本起步，资源按量付费。
- **持久化状态：** 重启后保留提供商、模型、密钥与请求日志。
- **运行状态可见：** 在应用的 Canvas 资源卡片中查看日志和资源使用情况。

## 部署指南

1. 打开 [LLMIO 模板](https://sealos.io/products/app-store/llmio)，点击 **立即部署**。
2. 保留自动生成的口令或替换为自己的口令，选择存储容量后确认。上游服务商凭据在应用启动后再配置。
3. 等待部署完成，通常需要 **1-2 分钟**。Sealos 随后打开 Canvas，应用资源卡片提供日志、配置和公网 HTTPS 地址。
4. 打开应用地址，使用访问令牌登录。全新部署的控制台初始为空库。
5. 打开「提供商管理」逐个添加上游（提供商类型、基础地址、API 密钥），再打开「模型管理」创建模型并绑定到上游，为每条绑定设置权重。
6. 打开「密钥管理」为每个客户端创建密钥。仅面向单个工具的密钥可以限制可用模型或设置过期时间。
7. 打开「快速开发」，选择 API 格式、模型与密钥后复制现成的请求示例，也可以直接使用下面的基础地址。

### 网关基础地址

| 客户端协议 | 基础地址 |
| --- | --- |
| OpenAI Chat Completions / Responses | `https://<你的应用地址>/openai/v1` |
| OpenAI 兼容（别名） | `https://<你的应用地址>/v1` |
| Anthropic Messages | `https://<你的应用地址>/anthropic/v1` |
| Google Generative | `https://<你的应用地址>/gemini/v1beta` |

OpenAI 风格的两个前缀使用 `Authorization: Bearer <密钥>` 传递密钥，`/anthropic` 使用 `x-api-key: <密钥>`（也接受 Bearer），`/gemini` 使用 `x-goog-api-key: <密钥>`。

## 配置与扩容

提供商、模型、权重、密钥与日志保留策略都在 LLMIO 内管理。调整基础设施时，打开 Canvas，在 AI 对话框中描述修改要求，或编辑应用资源卡片。并发压力更大时提升 CPU 与内存，同时保持单副本。

网关会代理长时间流式响应，因此 Ingress 的读写超时都设置为 300 秒。单次生成如果流式输出超过这个时长会被中断，需要时可以在 Ingress 上调整超时。

## 故障排查

**控制台提示口令错误：** 使用应用资源卡片中显示的 `TOKEN`。如果在 Pod 启动后修改了该值，需要重启 Pod 才会生效。

**客户端返回 401 Invalid token：** 先确认密钥传递位置是否正确——`/openai` 与 `/v1` 用 `Authorization: Bearer`，`/anthropic` 用 `x-api-key`，`/gemini` 用 `x-goog-api-key`。被限制模型白名单的密钥也会拒绝名单之外的模型，调试时先使用全量权限的密钥。

**提供商连通性检测失败：** 在控制台的提供商页面执行检测。基础地址写错、上游密钥失效、或上游从集群内不可达，都会在这里最先暴露。

**请求报协议相关错误：** 查看请求日志详情。其中会显示客户端协议、本次实际选中的上游协议，以及协议互转记录的字段级说明。

**持久卷被写满：** 日志库里占比最大的是请求正文。可以调小日志保留天数、在「系统配置」中执行压缩与空间回收，或直接扩容持久卷。

## 许可证

本 Sealos 模板遵循模板仓库的许可证。LLMIO 本身采用 [MIT 许可证](https://github.com/atopos31/llmio/blob/v0.9.4/LICENSE)。
