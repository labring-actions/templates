# Deploy and Host TradingAgents on Sealos

TradingAgents is a multi-agent LLM financial trading research framework. This template deploys TradingAgents v0.3.1 with a browser-accessible Gradio launcher, persistent cache storage, and public HTTPS access on Sealos Cloud.

![TradingAgents Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/tradingagents/website-screenshot.webp)

## About Hosting TradingAgents

TradingAgents simulates a financial research team with specialized LLM agents for market, sentiment, news, fundamentals, research debate, trading, risk, and portfolio analysis. The upstream project is CLI-first, so this template adds a lightweight Gradio UI for running ticker analysis from a browser.

The container clones the pinned upstream `v0.3.1` source, installs it into a persistent Python environment, and stores cache, checkpoints, and memory files under `/home/appuser/.tradingagents`. The template has no built-in login screen; access is controlled by the generated Sealos URL and your workspace permissions.

## Common Use Cases

- **Ticker research experiments**: Run multi-agent analysis for Yahoo Finance supported symbols such as `AAPL`, `SPY`, `0700.HK`, or `BTC-USD`.
- **Provider evaluation**: Compare OpenAI, Gemini, Anthropic, xAI, DeepSeek, Qwen, GLM, MiniMax, OpenRouter, Mistral, Kimi, Groq, NVIDIA NIM, or OpenAI-compatible endpoints.
- **Financial workflow demos**: Demonstrate multi-agent research workflows in a browser without operating a local CLI.
- **Persistent research cache**: Keep TradingAgents checkpoint, cache, and memory files across restarts.

## Dependencies for TradingAgents Hosting

The Sealos template includes a Python StatefulSet, ConfigMap launcher, persistent volume, Service, HTTPS Ingress, and App entry. Real analysis requires a matching LLM provider API key. Optional Alpha Vantage and FRED keys can improve market data and macro data coverage.

### Deployment Dependencies

- [TradingAgents GitHub Repository](https://github.com/TauricResearch/TradingAgents) - Source code and documentation
- [TradingAgents README](https://github.com/TauricResearch/TradingAgents#readme) - Installation, CLI usage, provider configuration, and package API
- [Sealos Documentation](https://sealos.io/docs) - Sealos platform documentation

### Implementation Details

**Architecture Components:**

- **Python StatefulSet**: Clones and runs TradingAgents `v0.3.1`.
- **Gradio Launcher**: Provides ticker, analysis date, research depth, runtime status, and analysis output controls.
- **Persistent Volume**: Stores the source checkout, virtual environment, package cache, checkpoints, and memory logs.
- **ConfigMap**: Mounts the Sealos launcher script at `/home/appuser/app/sealos_launcher.py`.
- **Ingress and App Entry**: Exposes the UI through the generated Sealos HTTPS URL.

**Configuration:**

- `llm_provider` selects the TradingAgents provider.
- Provider inputs map to upstream environment variables such as `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `ANTHROPIC_API_KEY`, `DASHSCOPE_CN_API_KEY`, `MINIMAX_CN_API_KEY`, `MOONSHOT_API_KEY`, and `NVIDIA_API_KEY`.
- `openai_compatible_base_url` sets `TRADINGAGENTS_LLM_BACKEND_URL` for vLLM, LM Studio, llama.cpp, or a custom OpenAI-compatible relay.
- `alpha_vantage_api_key` and `fred_api_key` are optional data-provider keys.

**License Information:**

TradingAgents is licensed under the Apache-2.0 License. This Sealos template provides deployment configuration for running TradingAgents on Sealos Cloud.

## Why Deploy TradingAgents on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies deployment and operations. By deploying TradingAgents on Sealos, you get one-click deployment, automatic HTTPS, persistent storage, resource controls, pay-as-you-go infrastructure, and Canvas-based updates for a research tool that normally starts from a local CLI.

## Deployment Guide

1. Open the [TradingAgents template](https://sealos.io/products/app-store/tradingagents) and click **Deploy Now**.
2. Choose `llm_provider` and provide the matching API key for real model-backed analysis. Leave optional data keys empty for a basic yfinance-backed run.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog, or click the relevant resource cards to modify settings.
4. Open the generated public URL. The Gradio launcher opens directly, with no app-level login.
5. Click **Refresh status** to confirm which API keys are configured.
6. Edit **Ticker**, **Analysis date**, and **Research depth**, then click **Run analysis**. The launcher validates the selected provider key before starting an LLM-backed run.

## Running a Ticker Analysis

1. Select the same provider you configured in the deployment form.
2. Enter a supported ticker, for example `AAPL`, `SPY`, `0700.HK`, or `BTC-USD`.
3. Keep **Research depth** at `1` for the first run to reduce token usage and runtime.
4. Click **Run analysis** and wait for the output sections: market report, sentiment report, news report, fundamentals report, trader plan, and final decision.

## Configuration

After deployment, configure TradingAgents through:

- **Gradio UI**: Start ticker analysis and inspect runtime key status.
- **AI Dialog**: Update provider keys or model-related settings.
- **Resource Cards**: Increase CPU or memory for deeper research runs.
- **Persistent Volume**: Keep checkpoint and memory data across restarts.

## Scaling

TradingAgents runs one analysis process at a time by default. Increase CPU and memory when running deeper research levels, larger models, or longer ticker analyses.

## Troubleshooting

### Analysis stops before contacting the model

- Cause: The selected provider key is empty, or `openai_compatible` is selected without `openai_compatible_base_url`.
- Solution: Update the deployment inputs, restart the StatefulSet, and click **Refresh status** again.

### Startup takes longer than expected

- Cause: The first boot clones the upstream repository and installs Python dependencies.
- Solution: Wait for the startup probe to pass; later restarts reuse persistent storage.

### Analysis runs for a long time

- Cause: Deep research uses multiple agents and multiple LLM calls.
- Solution: Start with **Research depth** set to `1`, then increase resources before running deeper analyses.

## Additional Resources

- [TradingAgents GitHub Repository](https://github.com/TauricResearch/TradingAgents)
- [TradingAgents CLI Usage](https://github.com/TauricResearch/TradingAgents#installation-and-cli)
- [TradingAgents Package API](https://github.com/TauricResearch/TradingAgents#tradingagents-package)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is provided as deployment configuration for Sealos users. TradingAgents itself is licensed under the [Apache-2.0 License](https://github.com/TauricResearch/TradingAgents/blob/main/LICENSE).
