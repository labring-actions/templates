# 在 Sealos 上部署和托管 TradingAgents

TradingAgents 是多智能体大模型金融交易研究框架。此模板会在 Sealos Cloud 上部署 TradingAgents v0.3.1，提供浏览器 Gradio 启动器、持久化缓存存储和公网 HTTPS 访问。

![TradingAgents 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/tradingagents/website-screenshot.webp)

## 关于托管 TradingAgents

TradingAgents 使用多个专门的 LLM 智能体模拟金融研究团队，覆盖市场、情绪、新闻、基本面、研究辩论、交易、风险和组合分析。上游项目以 CLI 为主，此模板为 Sealos 用户增加了轻量 Gradio UI，方便在浏览器里运行股票代码分析。

容器会克隆固定版本的上游 `v0.3.1` 源码，将其安装到持久化 Python 环境中，并把 cache、checkpoint 和 memory 文件保存在 `/home/appuser/.tradingagents` 下。模板本身没有内置登录页；访问控制由生成的 Sealos URL 和你的工作区权限承担。

## 常见使用场景

- **股票研究实验**：对 Yahoo Finance 支持的代码运行多智能体分析，例如 `AAPL`、`SPY`、`0700.HK` 或 `BTC-USD`。
- **模型提供商评估**：对比 OpenAI、Gemini、Anthropic、xAI、DeepSeek、Qwen、GLM、MiniMax、OpenRouter、Mistral、Kimi、Groq、NVIDIA NIM 或 OpenAI-compatible endpoint。
- **金融工作流演示**：在浏览器中展示多智能体研究流程，无需维护本地 CLI。
- **持久化研究缓存**：重启后保留 TradingAgents checkpoint、cache 和 memory 文件。

## TradingAgents 托管依赖

此模板包含 Python StatefulSet、ConfigMap 启动器、持久化卷、Service、HTTPS Ingress 和 App 入口。真实分析需要提供与 `llm_provider` 匹配的 LLM API Key。可选的 Alpha Vantage 和 FRED Key 可以改善市场数据与宏观数据覆盖。

### 部署依赖

- [TradingAgents GitHub 仓库](https://github.com/TauricResearch/TradingAgents) - 源码和文档
- [TradingAgents README](https://github.com/TauricResearch/TradingAgents#readme) - 安装、CLI 用法、模型提供商配置和 Package API
- [Sealos 文档](https://sealos.io/docs) - Sealos 平台文档

### 实现细节

**架构组件：**

- **Python StatefulSet**：克隆并运行 TradingAgents `v0.3.1`。
- **Gradio Launcher**：提供股票代码、分析日期、研究深度、运行状态和分析输出控件。
- **持久化卷**：保存源码、虚拟环境、依赖缓存、checkpoint 和 memory 日志。
- **ConfigMap**：将 Sealos 启动器脚本挂载到 `/home/appuser/app/sealos_launcher.py`。
- **Ingress 和 App 入口**：通过 Sealos 生成的 HTTPS URL 暴露 UI。

**配置：**

- `llm_provider` 选择 TradingAgents 的模型提供商。
- Provider 输入会映射为上游环境变量，例如 `OPENAI_API_KEY`、`GOOGLE_API_KEY`、`ANTHROPIC_API_KEY`、`DASHSCOPE_CN_API_KEY`、`MINIMAX_CN_API_KEY`、`MOONSHOT_API_KEY` 和 `NVIDIA_API_KEY`。
- `openai_compatible_base_url` 会设置 `TRADINGAGENTS_LLM_BACKEND_URL`，用于 vLLM、LM Studio、llama.cpp 或自定义 OpenAI-compatible relay。
- `alpha_vantage_api_key` 和 `fred_api_key` 是可选数据源 Key。

**许可证信息：**

TradingAgents 使用 Apache-2.0 License。此 Sealos 模板提供在 Sealos Cloud 上运行 TradingAgents 的部署配置。

## 为什么在 Sealos 上部署 TradingAgents？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一部署和运维流程。在 Sealos 上部署 TradingAgents，可以把通常从本地 CLI 启动的研究工具变成一键部署、自动 HTTPS、持久化存储、资源可控、按量付费、可在 Canvas 更新的在线应用。

## 部署指南

1. 打开 [TradingAgents 模板](https://sealos.io/products/app-store/tradingagents)，点击 **Deploy Now**。
2. 选择 `llm_provider`，并提供对应 API Key 以运行真实模型分析。可选数据源 Key 可以先留空，基础运行会使用 yfinance 数据。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会跳转到 Canvas。后续修改可以在 AI 对话中描述需求，或点击相关资源卡片调整设置。
4. 打开生成的公网 URL。Gradio 启动器会直接打开，无需应用内登录。
5. 点击 **Refresh status**，确认已配置的 API Key。
6. 修改 **Ticker**、**Analysis date** 和 **Research depth**，然后点击 **Run analysis**。启动器会在开始 LLM 分析前校验所选 provider 的 Key。

## 运行股票代码分析

1. 选择与你在部署表单中配置一致的 provider。
2. 输入支持的股票代码，例如 `AAPL`、`SPY`、`0700.HK` 或 `BTC-USD`。
3. 首次运行建议将 **Research depth** 保持为 `1`，以减少 token 消耗和运行时间。
4. 点击 **Run analysis**，等待输出 market report、sentiment report、news report、fundamentals report、trader plan 和 final decision。

## 配置

部署后可以通过以下方式配置 TradingAgents：

- **Gradio UI**：启动股票分析并查看运行时 Key 状态。
- **AI 对话**：更新模型提供商 Key 或模型相关设置。
- **资源卡片**：为更深研究流程增加 CPU 或内存。
- **持久化卷**：在重启后保留 checkpoint 和 memory 数据。

## 扩缩容

TradingAgents 默认一次运行一个分析流程。运行更深研究层级、更大模型或更长股票分析时，可以增加 CPU 和内存。

## 故障排查

### 分析在调用模型前停止

- 原因：所选 provider 的 Key 为空，或选择 `openai_compatible` 时未填写 `openai_compatible_base_url`。
- 解决方法：更新部署输入，重启 StatefulSet，然后再次点击 **Refresh status**。

### 启动时间较长

- 原因：首次启动会克隆上游仓库并安装 Python 依赖。
- 解决方法：等待 startup probe 通过；后续重启会复用持久化存储。

### 分析运行时间较长

- 原因：深度研究会使用多个智能体和多次 LLM 调用。
- 解决方法：先将 **Research depth** 设为 `1`，运行更深分析前再提高资源配置。

## 更多资源

- [TradingAgents GitHub 仓库](https://github.com/TauricResearch/TradingAgents)
- [TradingAgents CLI 用法](https://github.com/TauricResearch/TradingAgents#installation-and-cli)
- [TradingAgents Package API](https://github.com/TauricResearch/TradingAgents#tradingagents-package)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板作为部署配置提供给 Sealos 用户使用。TradingAgents 本身基于 [Apache-2.0 License](https://github.com/TauricResearch/TradingAgents/blob/main/LICENSE) 授权。
