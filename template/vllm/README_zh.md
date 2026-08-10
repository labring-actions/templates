# 在 Sealos 上部署和托管 vLLM

vLLM 是面向语言模型的推理和服务引擎。此 Sealos 模板运行官方 CPU 镜像，预置轻量指令模型、持久化 Hugging Face 缓存和 OpenAI 兼容 HTTPS API。

![vLLM 官网](website-screenshot.webp)

## 关于托管 vLLM

vLLM 提供 OpenAI 兼容服务器，支持聊天补全、文本补全、模型列表、健康检查和交互式 API 文档。团队可以用熟悉的 API 形式，在自托管基础设施上测试模型服务工作流。

此模板将 `HuggingFaceTB/SmolLM2-135M-Instruct` 以 `smollm2-135m` 名称提供服务。Sealos 会创建 StatefulSet、Service、Ingress、Hugging Face 缓存卷和 App 入口，用户可以从自动生成的 HTTPS URL 打开 `/docs`。

## 常见使用场景

- **OpenAI 兼容模型服务**：用自托管端点测试聊天和补全客户端。
- **Agent 后端原型**：为 Agent 和工作流测试提供小型指令模型。
- **推理链路冒烟验证**：在切换到更大模型前验证部署、健康检查和请求流程。
- **CPU-only 实验**：用低成本基线配置运行轻量模型。
- **持久化模型缓存**：Pod 重启后继续保留 Hugging Face 模型快照。

## vLLM 托管依赖

此模板包含所选 CPU 模型服务配置所需的运行时和 Kubernetes 资源。

### 部署依赖

- [vLLM 文档](https://docs.vllm.ai) - 产品和服务文档
- [vLLM OpenAI 兼容服务器](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html) - API 行为和请求格式
- [vLLM CPU 安装指南](https://docs.vllm.ai/en/latest/getting_started/installation/cpu/) - CPU 运行时说明
- [SmolLM2 模型卡](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct) - 默认模型信息
- [vLLM 源代码仓库](https://github.com/vllm-project/vllm) - 源代码和版本发布

### 实现细节

**配置：**

- 使用 `vllm/vllm-openai-cpu:v0.26.0`。
- 以 `HuggingFaceTB/SmolLM2-135M-Instruct` 启动 vLLM。
- 在 `8000` 端口发布 OpenAI 兼容 API。
- 将生成的 App URL 打开到 `/docs`。
- 将 Hugging Face 模型文件保存到 `/root/.cache/huggingface`。
- 为模型缓存挂载 `1Gi` `openebs-backup` 持久化卷。
- 设置 `--served-model-name smollm2-135m`、`--max-model-len 512`、`--max-num-seqs 1` 和 `--enforce-eager`。
- 使用 `/health` 作为启动、就绪和存活探针。

**许可证信息：**

vLLM 采用 Apache License 2.0。

## 为什么在 Sealos 上部署 vLLM？

- **一键模型服务栈**：通过一个模板创建 StatefulSet、Service、Ingress、缓存卷和 App 入口。
- **熟悉的 API 形式**：使用 OpenAI 兼容聊天、补全和模型列表端点。
- **持久化模型缓存**：Pod 重启后继续保留已下载模型快照。
- **可视化运维**：从 Sealos Canvas 检查日志、健康状态、网络和资源使用量。
- **经过验证的低负载基线**：从实测 CPU 配置起步，并按延迟目标扩展资源。

## 部署指南

1. 打开 [vLLM 模板](https://sealos.io/products/app-store/vllm)，点击 **Deploy Now**。
2. 检查自动生成的应用名称和域名，然后开始部署。
3. 等待应用资源进入 Ready 状态。Sealos 通常会在 2-3 分钟内创建 StatefulSet、Service、Ingress、App 和 PVC；随后 vLLM 会拉取 CPU 镜像和模型，经过验证的低 CPU 启动过程最长可达 10 分钟。
4. 打开生成的 App URL，查看位于 `/docs` 的交互式 API 文档。
5. 将生成的域名作为 OpenAI 兼容客户端的基础 URL。

该模板会下载 `HuggingFaceTB/SmolLM2-135M-Instruct`，并以 `smollm2-135m` 名称提供服务。

## 使用 API

设置生成的 HTTPS 端点：

```bash
export VLLM_URL="https://<your-app>.usw-1.sealos.app"
```

检查服务健康状态和已加载模型：

```bash
curl "$VLLM_URL/health"
curl "$VLLM_URL/v1/models"
```

创建聊天补全：

```bash
curl "$VLLM_URL/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "smollm2-135m",
    "messages": [
      {"role": "user", "content": "What is 2 + 2?"}
    ],
    "max_tokens": 32,
    "temperature": 0
  }'
```

创建文本补全：

```bash
curl "$VLLM_URL/v1/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "smollm2-135m",
    "prompt": "The capital of France is",
    "max_tokens": 16,
    "temperature": 0
  }'
```

## 默认资源

| 资源 | 默认值 |
| --- | --- |
| CPU 限制 | `100m` |
| 内存限制 | `4096Mi` |
| 模型缓存 | `1Gi` |
| CPU KV cache | `1Gi` |
| 最大模型长度 | `512` tokens |
| 最大并发序列数 | `1` |

这是 Sealos CPU 资源阶梯的最低档。线上验证中，`100m` 配置的缓存冷启动约为 8.5 分钟，首次生成 8 个 token 约为 55 秒。将 CPU 限制提高到 `500m` 或 `1` 可显著缩短启动和响应时间，CPU request 应保持为所选限制的 10%。相邻的 `2048Mi` 内存档触发了 OOM 终止，因此 `4096Mi` 是该模型与 1Gi KV cache 的实测最低内存。

## 存储和生命周期

StatefulSet 将 `openebs-backup` 卷挂载到 `/root/.cache/huggingface`。Pod 重启后仍可继续使用模型快照。删除模板实例及其 PVC 会移除缓存模型。

## 安全

公开 HTTPS 端点会直接连接到 vLLM OpenAI 兼容 API。请将自动生成的域名视为敏感推理端点，并为共享部署配置带认证的网关、访问白名单或私有网络边界。

## 故障排查

### 部署期间公共 URL 返回 502

vLLM 仍在拉取镜像、下载模型并加载 CPU 运行时。当 Pod 仍处于启动探针窗口时，请保持部署继续运行。

### `/v1/models` 返回为空或响应延迟

等待就绪探针通过并完成模型加载。默认低 CPU 配置优先控制成本。

### 补全请求较慢

将 CPU 提高到 `500m`、`1` 或更高，以获得更快的 token 生成速度。CPU request 建议保持在所选限制的约 10%。

### Pod 发生 OOM

默认模型与 1Gi CPU KV cache 至少使用经过验证的 `4096Mi` 内存限制。更大的模型需要更高的内存档位和模型缓存卷。

### 获取帮助

- [vLLM 文档](https://docs.vllm.ai)
- [vLLM GitHub Issues](https://github.com/vllm-project/vllm/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [vLLM 官网](https://vllm.ai)
- [CPU 安装指南](https://docs.vllm.ai/en/latest/getting_started/installation/cpu/)
- [默认模型](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct)
- [源代码](https://github.com/vllm-project/vllm)

## 许可证

此模板遵循上游 [Apache License 2.0](https://github.com/vllm-project/vllm/blob/main/LICENSE)。
