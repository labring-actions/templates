# 在 Sealos 上部署 Vane（原 Perplexica）

Vane（原 Perplexica）是一款注重隐私的 AI 问答引擎，可结合大语言模型与带引用的网页搜索、图片、视频、计算组件、文件分析和本地会话历史。

![Vane 展示带引用的回答、图片和视频结果](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/perplexica/website-screenshot.webp)

## 模板包含的组件

- **Vane `v1.12.2`**：使用上游 slim 镜像，以单副本 StatefulSet 运行
- **SearXNG `2026.4.10-7737a0da1`**：作为独立搜索服务运行
- **SQLite、模型服务配置、会话历史和上传文件**：保存在 `1Gi` 持久卷中
- **Transformers 嵌入模型缓存**：保存在同一持久卷中
- **公网 HTTPS**：由 Sealos 管理 Service 和 Ingress
- **启动、就绪和存活探针**：覆盖两个工作负载

Vane 与 SearXNG 分开部署，延续上游 slim 镜像的架构，也便于独立观察和调整资源。SearXNG 使用经过真实查询验证的引擎集合：

| 搜索能力 | 引擎 |
| --- | --- |
| 网页 | Bing |
| 图片 | Bing Images |
| 新闻 | Bing News |
| 视频 | Bing Videos 和 YouTube |
| 计算与知识组件 | WolframAlpha |

Vane `v1.12.2` 使用本地 SQLite 和上传目录。该上游版本仅提供本地持久化后端，因此模板按其支持的方式创建持久卷。

## 适用场景

- 基于实时网页结果生成带引用的 AI 回答
- 搜索图片、视频和新闻
- 使用计算与快捷信息组件
- 上传文档并开展辅助研究
- 为个人或可信团队保存私有搜索历史
- 接入 OpenAI 或 OpenAI 兼容模型服务

## 部署

1. 打开 [Sealos 应用商店中的 Vane 模板](https://sealos.io/products/app-store/perplexica)。
2. 填写 OpenAI 或 OpenAI 兼容服务的 API Key 和 Base URL；也可以留空 API Key，进入 Vane 后配置其他模型服务。
3. 点击 **Deploy**，等待 Vane 和 SearXNG 工作负载进入 Ready 状态。
4. 打开 Sealos 展示的 HTTPS 地址。
5. 完成模型设置向导。

### 部署参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `OPENAI_API_KEY` | 空 | OpenAI 或 OpenAI 兼容服务的可选 API Key |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | 环境变量方式创建的 OpenAI 服务所使用的 API 地址 |

API Key 会以服务端环境变量传入 Vane。请将 Sealos 应用配置和持久卷权限限定给可信管理员。

## 首次模型设置

首次访问时，Vane 会展示设置向导：

1. 部署参数中已经填写 OpenAI 兼容连接时，打开 **OpenAI** 服务卡片。
2. 使用自定义兼容地址时，进入 **Chat Models**，点击 **Add**，填写显示名称和该服务接受的准确模型标识。
3. 进入模型选择页面，选择刚配置的聊天模型。
4. 嵌入模型选择 **Transformers** 下的 `Xenova/all-MiniLM-L6-v2`。该本地嵌入模型适合未提供 embeddings API 的兼容服务。
5. 点击 **Finish**，提交一条测试问题。

你也可以在 Vane 设置中添加 Ollama、Anthropic、Gemini、Groq、LM Studio、Lemonade 等服务。目标服务需要允许 Sealos 工作负载访问。

## 访问与安全

Vane `v1.12.2` 未提供内置账号、登录流程和访问控制。部署地址会直接打开应用。获得该地址的访问者可以使用已配置的模型凭据、修改设置并查看已保存的会话。

向可信范围之外分享前，请通过认证网关、私有网络或等效的 Sealos 访问策略保护公网入口。部署地址、应用配置和持久化数据都应按敏感信息管理。

## 验证部署

完成设置后：

1. 提问一条时效性问题，确认回答中出现可点击的引用来源。
2. 提问 `What is 2+2?`，确认 WolframAlpha 计算卡片返回 `4`。
3. 打开图片或视频搜索，确认媒体结果正常展示。
4. 打开 **Library**，确认刚才的会话已经保存。
5. 业务需要文件分析时，上传一个小型受支持文档并针对内容提问。

## 持久化

| 路径 | 用途 |
| --- | --- |
| `/home/vane/data/db.sqlite` | 会话、来源和应用记录 |
| `/home/vane/data/config.json` | 模型服务与应用配置 |
| `/home/vane/data/uploads` | 上传文件 |
| `/home/vane/node_modules/@huggingface/transformers/.cache` | Transformers 模型缓存，通过数据卷持久化 |

模板使用 `1Gi` 的 `openebs-backup` 持久卷。大量保存会话、文档或模型缓存时，请持续观察容量。

## 默认资源

以下资源档位已通过冷启动、首次模型配置、带引用网页搜索、WolframAlpha 计算和图片/视频搜索测试：

| 组件 | CPU 上限 | 内存上限 | CPU 请求 | 内存请求 |
| --- | ---: | ---: | ---: | ---: |
| Vane | `1` | `1024Mi` | `100m` | `102Mi` |
| SearXNG | `100m` | `256Mi` | `10m` | `25Mi` |

并发搜索增多时可提高 Vane CPU；大文件和嵌入任务会增加内存需求。启用更多搜索引擎或增加并发查询时，请同步提高 SearXNG 资源。

## 扩容

模板保持一个 Vane 副本，因为 SQLite 和上传文件位于 ReadWriteOnce 持久卷。`v1.12.2` 的受支持存储模型适合维持该拓扑。SearXNG 默认也使用一个副本，并可按搜索流量独立调整资源。

## 备份与升级

升级前请备份 Vane 持久卷，其中包含数据库、模型服务配置、上传文件和嵌入模型缓存。

升级步骤：

1. 阅读目标 Vane 与 SearXNG 版本的发布说明。
2. 备份 `/home/vane/data`。
3. 更新 Vane slim 镜像和 SearXNG 镜像版本。
4. 确认配置的 SearXNG 引擎在目标版本中仍然可用。
5. 重新验证模型设置、带引用搜索、计算、媒体、上传和 Library。

## 故障排查

### 设置向导中缺少可用聊天模型

自定义 OpenAI 兼容地址需要在 **OpenAI → Chat Models** 中添加准确的模型标识，并确认 Sealos 工作负载可以使用当前 API Key 和 Base URL 访问目标服务。

### 搜索结果中没有来源

检查 SearXNG 工作负载，并确认其 Service 的 `8080` 端口可访问。模板已经启用 Vane 所需的 JSON 输出，以及 Bing 和 WolframAlpha 引擎集合。

### 首次使用本地嵌入模型耗时较长

Transformers 模型会在首次嵌入请求时下载。模型缓存保存在 Vane 数据卷中，后续启动可以直接复用。

### 重新部署后会话或上传文件消失

确认 Vane StatefulSet 仍引用原来的 `vn-homevn-vanevn-data` 存储声明。新的存储声明会从空的 SQLite 数据库和上传目录开始。

## 文档

- [Vane GitHub 仓库](https://github.com/ItzCrazyKns/Vane)
- [Vane 架构文档](https://github.com/ItzCrazyKns/Vane/tree/v1.12.2/docs/architecture)
- [Vane Search API](https://github.com/ItzCrazyKns/Vane/blob/v1.12.2/docs/API/SEARCH.md)
- [SearXNG 文档](https://docs.searxng.org)
- [Sealos 应用商店](https://sealos.io/products/app-store)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

Vane 使用 [MIT License](https://github.com/ItzCrazyKns/Vane/blob/v1.12.2/LICENSE)。本仓库仅提供 Sealos 部署模板，并保持上游许可证不变。
