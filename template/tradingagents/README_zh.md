# 在 Sealos 上部署和托管 TradingAgents

TradingAgents 是多智能体大模型金融交易研究框架。此模板会在 Sealos Cloud 上部署带浏览器 Gradio 启动器、持久化缓存存储和公网 HTTPS 访问的 TradingAgents。

![TradingAgents 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/tradingagents/website-screenshot.webp)

## 关于托管 TradingAgents

TradingAgents 用多个专门的 LLM 智能体模拟金融研究团队，覆盖市场、情绪、技术、基本面、风险和组合分析。上游项目以 CLI 为主，因此此模板为 Sealos 用户提供轻量浏览器启动器。

容器会把上游 `v0.2.5` 源码安装到持久化存储中，启动 Gradio UI，并将缓存和记忆文件保存在 `/home/appuser/.tradingagents` 下。部署时填写的 API Key 会映射为 TradingAgents 官方环境变量。

## 常见使用场景

- **股票研究实验**：对支持的市场代码运行多智能体分析。
- **LLM 提供商对比**：测试 OpenAI、Gemini、Anthropic、DeepSeek、Qwen、GLM、MiniMax 或 OpenRouter。
- **金融工作流演示**：在浏览器中展示多智能体研究流程。
- **持久化研究缓存**：在重启后保留 TradingAgents checkpoint 和 memory 文件。

## TradingAgents 托管依赖

此模板包含 Python 运行时 StatefulSet、ConfigMap 启动器、持久化卷、HTTPS Ingress、Service 和 App 资源。真实分析至少需要一个与 `llm_provider` 匹配的 LLM API Key。

### 部署依赖

- [TradingAgents GitHub 仓库](https://github.com/TauricResearch/TradingAgents) - 源码和文档
- [TradingAgents README](https://github.com/TauricResearch/TradingAgents#readme) - CLI 用法和提供商配置
- [Sealos 文档](https://sealos.io/docs) - Sealos 平台文档

### 实现细节

**架构组件：**

- **Python StatefulSet**：安装并运行 TradingAgents `v0.2.5` 源码。
- **Gradio Launcher**：提供股票代码、日期、研究深度和运行状态页面。
- **持久化卷**：保存源码、依赖缓存、checkpoint 和 memory 日志。
- **ConfigMap**：提供启动脚本和 Gradio 应用。
- **Ingress 和 App 入口**：通过 Sealos 生成的 HTTPS URL 暴露 UI。

**配置：**

- `llm_provider` 选择 TradingAgents 的模型提供商。
- 提供商 API Key 输入会映射为官方环境变量，例如 `OPENAI_API_KEY`、`GOOGLE_API_KEY`、`ANTHROPIC_API_KEY`。
- `alpha_vantage_api_key` 和 `finnhub_api_key` 可改善行情和新闻数据覆盖。

**许可证信息：**

TradingAgents 使用 Apache-2.0 License。此 Sealos 模板提供在 Sealos Cloud 上运行 TradingAgents 的部署配置。

## 为什么在 Sealos 上部署 TradingAgents？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一部署和运维流程。在 Sealos 上部署 TradingAgents，可以把通常从本地 CLI 启动的研究工具变成一键部署、自动 HTTPS、持久化存储、资源可控、可在 Canvas 更新的在线应用。

## 部署指南

1. 打开 [TradingAgents 模板](https://sealos.io/products/app-store/tradingagents)，点击 **Deploy Now**。
2. 选择 `llm_provider`，并提供对应 API Key 以运行真实模型分析。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续修改可以在 AI 对话中描述需求，或点击相关资源卡片调整设置。
4. 打开生成的公网 URL。
5. 点击 **Refresh status**，确认已配置的 API Key。
6. 输入股票代码和日期，然后从页面启动分析。

## 配置

部署后可以通过以下方式配置 TradingAgents：

- **Gradio UI**：启动股票分析并查看运行时 Key 状态。
- **AI 对话**：更新模型提供商 Key 或模型相关设置。
- **资源卡片**：为更长的分析运行增加 CPU 或内存。
- **持久化卷**：在重启后保留 checkpoint 和 memory 数据。

## 扩缩容

TradingAgents 默认一次运行一个分析流程。运行更深研究层级、更大模型或更长股票分析时，可以增加 CPU 和内存。

## 故障排查

### 分析立即失败

- 原因：所选提供商 Key 缺失或无效。
- 解决方法：确认已配置匹配 API Key，然后重启 StatefulSet。

### 启动时间较长

- 原因：首次启动会克隆上游仓库并安装 Python 依赖。
- 解决方法：等待 startup probe 通过；后续重启会复用持久化存储。

### 分析超时

- 原因：较深研究流程可能超过启动器默认 30 分钟超时。
- 解决方法：增加资源或降低研究深度。

## 更多资源

- [TradingAgents GitHub 仓库](https://github.com/TauricResearch/TradingAgents)
- [TradingAgents CLI 用法](https://github.com/TauricResearch/TradingAgents#installation-and-cli)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板作为部署配置提供给 Sealos 用户使用。TradingAgents 本身基于 [Apache-2.0 License](https://github.com/TauricResearch/TradingAgents/blob/main/LICENSE) 授权。
