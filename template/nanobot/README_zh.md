# 在 Sealos 上部署和托管 nanobot

nanobot 是一款自托管 AI 智能体，提供浏览器工作台、工具调用、记忆和定时任务。本模板在 Sealos Cloud 上部署 nanobot 网关及其内置 WebUI，并配置持久化存储。

![nanobot 官网](./website-screenshot.webp)

## 关于托管 nanobot

网关通过 8765 端口同时提供 WebUI 和需要身份验证的 WebSocket 连接。单个实例使用 1Gi 持久卷保存配置、对话、记忆、生成的文件和自动化任务状态。

模板在首次启动时初始化配置并准备分词器缓存，后续重启会保留通过 WebUI 修改的设置。浏览器访问使用你在部署表单中设置的密码。文件工具默认限制在工作区内运行。

## 常见使用场景

- **个人 AI 工作台**：按研究、写作和项目任务分别保存对话。
- **文件助手**：让智能体在持久化工作区中创建、查看和编辑文件。
- **重复任务处理**：通过内置工具、技能和定时自动化处理日常工作。
- **聊天平台集成**：使用自己的平台凭证接入受支持的聊天渠道。

## nanobot 托管依赖

模板包含 Python 运行环境、内置 WebUI、工具和持久化存储。部署时需要填写同一家模型服务商的 API 密钥、兼容 OpenAI 的 API 基础地址和准确的模型 ID。

### 部署依赖

- [官方网站](https://nanobot.wiki)
- [WebUI 指南](https://github.com/HKUDS/nanobot/blob/v0.3.0/docs/webui.md)
- [部署指南](https://github.com/HKUDS/nanobot/blob/v0.3.0/docs/deployment.md)
- [GitHub 问题反馈](https://github.com/HKUDS/nanobot/issues)

### 实现细节

| 组件 | 配置 |
| --- | --- |
| 版本 | nanobot v0.3.0 |
| 运行服务 | 单个网关及内置 WebUI，以 UID 1000 运行 |
| 存储 | `/home/nanobot/.nanobot` 路径下的 1Gi 持久卷 |
| 配置文件 | `/home/nanobot/.nanobot/config.json`，首次启动时初始化 |
| 模型服务 | 由部署参数指定的 OpenAI 兼容端点 |
| 公共入口 | 支持 WebSocket 的 HTTPS WebUI，服务端口为 8765 |
| 健康检查 | 容器内部的 18790 端口 |
| 轻量使用验证配置 | 网关：200m CPU / 256Mi 内存；初始化容器：100m CPU / 128Mi 内存 |

镜像 `ghcr.io/yangchuansheng/sealos-template-init:nanobot-v0.3.0` 使用上游 v0.3.0 的原始 Dockerfile 和源码构建。选定的上游部署方式通过本地文件保存数据，本模板为其配置对应的持久卷。该运行方式使用共享的本地状态，请保持单副本。

## 为什么在 Sealos 上部署 nanobot？

Sealos 为网关提供 Kubernetes 调度、持久化存储、HTTPS 路由和按量付费资源。部署完成后，可以通过 Canvas 的 AI 对话框或资源卡片调整资源并查看日志。

## 部署指南

1. 打开 [nanobot 模板](https://sealos.io/products/app-store/nanobot)，点击 **Deploy Now**（立即部署）。
2. 填写模型服务商的 API 密钥、API 基础地址和模型 ID。地址应包含服务商要求的版本路径，例如 `https://api.openai.com/v1`。
3. 在必填项 **web_token（WebUI 登录密码）** 中设置自己的强密码，并在部署前妥善保存。
4. 等待部署完成，通常需要 2-3 分钟。部署完成后，Canvas 会显示网关及其持久化存储。
5. 打开应用公共地址，在 **Password** 中输入部署时设置的 `web_token`，然后点击 **Connect**。通过共享密码验证后即可进入 WebUI。
6. 点击 **New topic** 新建对话，发送一条简短消息验证模型连接，再让智能体创建并读取一个小文件，验证工作区工具。

## 配置

通过 **Settings → Models** 管理模型设置，通过 **Settings → Channels** 配置聊天平台。配置修改会保存到持久卷；WebUI 提示需要重启时，按提示操作。部署时填写的模型参数也会通过 `OPENAI_API_KEY`、`OPENAI_API_BASE` 和 `NANOBOT_MODEL` 提供给应用。

浏览器会在本地记住访问密码。更换浏览器或清除浏览器存储后，再次输入部署时设置的密码即可连接。当前密码也可以在网关资源卡片的 `NANOBOT_WEB_TOKEN` 环境变量中查看。网关采用共享访问密码，获得密码的可信用户可以操作同一个智能体工作区。

远程安装可选 Python 包的功能默认关闭。默认镜像包含 WhatsApp 支持；启用其他聊天渠道前，可能需要通过上游的 `NANOBOT_CHANNELS` 构建参数重新构建包含所需依赖的镜像。

## 故障排查

- **密码验证失败**：从网关资源卡片复制当前的 `NANOBOT_WEB_TOKEN`，输入时去掉首尾多余空格。
- **模型请求失败**：确认 API 密钥、基础地址和准确的模型 ID 属于同一服务商，并检查服务商的可用额度。
- **网关仍在启动**：查看初始化容器和网关日志。首次运行会先准备分词器缓存，再开始处理请求。
- **工作负载增加**：随着对话、附件和工具任务增长，通过 Canvas 资源卡片提高 CPU、内存或持久卷容量。

## 许可证

本 Sealos 模板遵循 [模板仓库许可证](../../LICENSE)。nanobot 使用 [MIT License](https://github.com/HKUDS/nanobot/blob/v0.3.0/LICENSE)。
