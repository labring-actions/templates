# 在 Sealos 上部署和托管 CowAgent

CowAgent 是一款开源 AI 助手与智能体运行框架，提供 Web 控制台、持久记忆、可扩展技能和多渠道接入能力。此模板可在 Sealos Cloud 上部署 CowAgent 2.1.3，并配置持久化存储和公网 HTTPS 入口。

![CowAgent 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/chatgpt-on-wechat/website-screenshot.webp)

## 关于 CowAgent 托管

CowAgent 提供浏览器控制台，可用于配置模型供应商、管理技能、与智能体对话，以及连接各类消息渠道。工作区会持续保存技能、运行数据和本地配置，应用重启后依然可用。

Sealos 模板会创建一个 CowAgent StatefulSet、一个挂载到 `/home/agent/cow` 的 1 GiB 持久卷、健康探针和启用 TLS 的公网入口。应用使用专属 `agent` 用户和受限容器安全上下文运行。

## 常见使用场景

- **个人 AI 助手**：运行具有持久记忆和可复用技能的智能体。
- **模型供应商控制台**：在一个 Web 界面中配置多种受支持的模型 API。
- **消息渠道集成**：将智能体接入受支持的聊天和协作平台。
- **技能开发**：查看、启用和管理内置或自定义智能体技能。

## 托管 CowAgent 所需的依赖

模板包含 CowAgent 容器、持久化存储、Service、Ingress、健康探针和 Sealos 应用入口。部署时需要设置 Web 控制台密码，登录后再配置模型供应商。

### 部署依赖

- [CowAgent 官网](https://cowagent.ai/en) - 产品介绍与项目信息
- [CowAgent 源码](https://github.com/zhayujie/CowAgent) - 源代码、版本发布与问题跟踪
- [CowAgent README](https://github.com/zhayujie/CowAgent/blob/master/README.md) - 安装、模型供应商、渠道和功能文档

### 实现细节

**架构组件：**

- **CowAgent**：单个 StatefulSet，通过 9899 端口提供 Web 控制台。
- **持久化工作区**：挂载到 `/home/agent/cow` 的 1 GiB 存储卷，用于保存技能和运行数据。
- **公网入口**：由 Sealos 管理的 HTTPS Ingress，与 CowAgent Web 服务相连。
- **控制台认证**：必填参数 `WEB_PASSWORD` 用于保护 Web 控制台。

模板会启用 Web 渠道，将 CowAgent 数据写入持久化工作区，并保持单副本运行，让本地状态和 ReadWriteOnce 存储卷始终由一个实例持有。CowAgent 采用 MIT License。

## 为什么选择在 Sealos 上部署 CowAgent？

- **一键部署**：通过一个模板同时创建应用、存储、网络和 TLS 入口。
- **智能体数据持久化**：Pod 替换和版本升级期间，技能与工作区数据持续保留。
- **即时 HTTPS 访问**：自动获得带托管证书的公网应用地址。
- **Kubernetes 运维能力**：通过 Sealos Canvas、AI 对话和资源卡片查看并调整资源。
- **资源利用高效**：从经过实测的个人低负载配置起步，再随业务增长逐步扩容。

## 部署指南

1. 打开 [CowAgent 模板](https://sealos.io/products/app-store/chatgpt-on-wechat)，点击 **Deploy Now**。
2. 为 `WEB_PASSWORD` 填写一个高强度密码。该值会成为 CowAgent Web 控制台密码。
3. 等待部署完成，通常需要 2-3 分钟。随后 Sealos 会打开 Canvas，可通过 AI 对话或资源卡片继续调整配置。
4. 打开 Sealos 中显示的 CowAgent 应用地址。

## 登录并配置模型

1. 在 CowAgent 登录页输入部署表单中的 `WEB_PASSWORD`。
2. 进入控制台的 **Models** 页面。
3. 选择受支持的模型供应商，填写 API 密钥和端点配置，然后保存。
4. 进入 **Chat** 使用智能体，或前往 **Skills** 与 **Channels** 配置更多能力。

后续登录会继续使用部署密码，建议将它保存在密码管理器中。

## 配置

模型凭据和渠道设置均在 CowAgent 控制台中管理。Pod 替换期间，工作区文件和技能会保留在持久卷中。

部署层面的变更可通过 Sealos Canvas AI 对话完成，也可以直接打开 StatefulSet、存储和网络资源卡片调整。

## 扩缩容

CowAgent 使用 ReadWriteOnce 存储卷承载本地工作区，模板保持单副本运行。模型集成、并发会话或技能带来更多负载时，可通过 StatefulSet 资源卡片提高 CPU 和内存配置。

## 故障排查

### 控制台提示密码错误

输入部署时设置的完整 `WEB_PASSWORD`。轮换密码时，在 Canvas 中更新 StatefulSet 环境变量，并等待 Pod 恢复 Ready。

### Chat 模型请求报错

打开 **Models**，检查模型供应商、API 密钥、Base URL 和模型名称，并确认 CowAgent Pod 可以访问供应商端点。

### 技能或工作区数据异常

确认 CowAgent 持久卷处于 Bound 状态，并挂载到 `/home/agent/cow`。随后从 StatefulSet 资源卡片查看 Pod 事件和日志。

### 获取帮助

- [CowAgent Issues](https://github.com/zhayujie/CowAgent/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

此 Sealos 模板遵循 templates 仓库的许可条款。CowAgent 采用 [MIT License](https://github.com/zhayujie/CowAgent/blob/master/LICENSE)。
