# 在 Sealos 上部署和托管 CowAgent

CowAgent 是开源超级 AI 助手，提供浏览器控制台、工具、技能、记忆、知识管理、定时任务和多渠道集成。此模板在 Sealos Cloud 上部署 CowAgent，配置持久化用户数据、密码保护的 Web 控制台和公开 HTTPS 访问。

![CowAgent 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/cowagent/website-screenshot.webp)

## 关于托管 CowAgent

CowAgent 作为单个有状态 Web 控制台服务运行在 9899 端口。Sealos 模板会配置 Web 渠道，将控制台绑定到 `0.0.0.0`，把运行数据保存到 `/home/agent/cow`，并使用部署密码保护公开控制台。

Web 控制台是聊天、配置模型 Provider、管理技能、浏览记忆和知识、连接渠道以及查看日志的主要入口。

## 常见使用场景

- **个人 AI 助手**：运行一个可通过浏览器访问的持久化 AI 助手。
- **技能自动化**：安装并使用面向文件、工具、媒体和工作流的可复用技能。
- **知识和记忆中心**：维护长期记忆和个人知识库。
- **多渠道运维**：连接 Web、Telegram、Slack、Discord、微信、飞书、钉钉等支持渠道。

## CowAgent 托管依赖

此 Sealos 模板包含 CowAgent 容器镜像、持久化数据存储、ClusterIP Service、HTTPS Ingress 和 Sealos App 入口。

### 部署依赖

- [官方网站](https://cowagent.ai/) - 产品网站
- [文档](https://docs.cowagent.ai/intro/index) - 官方文档
- [GitHub 仓库](https://github.com/zhayujie/CowAgent) - 源码和版本发布
- [Skill Hub](https://skills.cowagent.ai/) - CowAgent 技能市场

### 实现细节

**架构组件：**

此模板部署以下服务：

- **CowAgent Web 控制台**：运行在 9899 端口的浏览器 UI 和 API。
- **持久化数据卷**：在 `/home/agent/cow` 下保存配置、日志、会话数据、记忆、知识、浏览器资料和已安装资产。
- **Sealos Ingress**：通过生成的 Sealos 域名提供 HTTPS 访问。

**配置：**

模板设置 `CHANNEL_TYPE=web`、`WEB_HOST=0.0.0.0`，并从部署输入设置 `WEB_PASSWORD`。模型 Provider 可在登录后通过 Web 控制台配置。

**许可证信息：**

CowAgent 使用 MIT License。此 Sealos 模板遵循 Sealos templates 仓库许可证。

## 为什么在 Sealos 上部署 CowAgent？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一部署、存储、网络和持续运维。部署 CowAgent 到 Sealos 后，你可以获得：

- **一键部署**：从应用商店启动 CowAgent，并获得生成的公开控制台 URL。
- **持久化 Agent 数据**：配置、记忆、知识、日志和用户数据可在重启后保留。
- **密码保护访问**：使用部署密码保护公开 Web 控制台。
- **Canvas 运维**：通过 Canvas、AI 对话和资源卡调优资源、查看日志和修改运行设置。
- **Provider 灵活性**：在控制台中配置 OpenAI 兼容、Claude、Gemini、DeepSeek、Qwen 等 Provider。
- **按量托管**：从单实例持久化部署起步，并在需要时扩容资源。

## 部署指南

1. 打开 [CowAgent 模板](https://sealos.io/products/app-store/cowagent)，点击 **Deploy Now**。
2. 在弹窗中配置 Web 控制台密码。
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续变更可以在对话框中描述需求让 AI 应用更新，也可以点击资源卡修改设置。
4. 通过提供的 URL 访问 CowAgent。
5. 输入部署表单中的 Web 控制台密码。
6. 在控制台中打开 **Model Management**，配置至少一个模型 Provider 后再运行聊天或 Agent 任务。

## 登录和注册

CowAgent Web 控制台使用密码登录。此模板不需要单独注册账号。

使用部署表单中的 `web_password` 值登录。登录后会在浏览器 Cookie 中保存会话，后续也可以在控制台配置页更新密码。

## 配置

部署后可以通过以下方式配置 CowAgent：

- **Web 控制台**：配置模型、渠道、工具、技能、记忆、知识、定时任务和日志。
- **Canvas 资源卡**：调整 CPU、内存、存储或环境值。
- **AI 对话**：描述运维变更，并让 Sealos 更新资源。

## 扩容

扩容 CowAgent 资源：

1. 打开部署对应的 Canvas。
2. 点击 CowAgent StatefulSet 资源卡。
3. 为更重的浏览器自动化、工具执行或多渠道使用增加 CPU 或内存。
4. 应用变更并观察日志。

## 故障排查

### 登录页拒绝密码

- 原因：输入值与 `web_password` 部署输入不同。
- 解决：检查部署参数，或从 Canvas 资源卡更新 `WEB_PASSWORD`。

### 聊天返回 Provider 错误

- 原因：尚未配置模型 Provider，或 Provider Key/Base URL 无效。
- 解决：登录控制台，打开 **Model Management** 并配置有效 Provider。

### 浏览器自动化不稳定

- 原因：浏览器工具执行较重任务时可能需要更多内存。
- 解决：在 Canvas 中提高 CowAgent StatefulSet 内存。

## 其他资源

- [CowAgent 文档](https://docs.cowagent.ai/intro/index)
- [Web 控制台指南](https://docs.cowagent.ai/channels/web)
- [Skill Hub](https://skills.cowagent.ai/)
- [GitHub Releases](https://github.com/zhayujie/CowAgent/releases)

## License

此 Sealos 模板遵循 Sealos templates 仓库许可证。CowAgent 本身使用 MIT License。
