# vLLM

vLLM 是面向语言模型的推理和服务引擎。该 Sealos 模板运行官方 CPU 镜像，预置轻量指令模型、持久化 Hugging Face 缓存和 OpenAI 兼容 HTTPS API。

![vLLM 官网](website-screenshot.webp)

## 功能特性

- 官方 `vllm/vllm-openai-cpu:v0.26.0` 镜像
- OpenAI 兼容的聊天和文本补全 API
- 位于 `/docs` 的交互式 API 文档
- 持久化 Hugging Face 模型缓存
- 默认使用纯 CPU 部署

## 在 Sealos 上部署

1. 打开 [vLLM 模板](https://sealos.io/products/app-store/vllm)。
2. 点击 **Deploy Now**。
3. 等待 StatefulSet 进入 Ready 状态。首次拉取镜像需要几分钟，低 CPU 配置下的服务启动时间最长约为 10 分钟。
4. 打开生成的 App URL，查看交互式 API 文档。

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

## 持久化

StatefulSet 将 `openebs-backup` 卷挂载到 `/root/.cache/huggingface`。Pod 重启后仍可继续使用模型快照。删除模板实例及其 PVC 会移除缓存模型。

## 访问控制

默认端点接受无需 API key 的请求。Sealos Ingress 会将生成的 HTTPS 端点发布到互联网。请在向非受信客户端共享前配置带认证的 API 网关或网络访问策略。

## 相关链接

- [vLLM 官网](https://vllm.ai)
- [vLLM 文档](https://docs.vllm.ai)
- [CPU 安装指南](https://docs.vllm.ai/en/latest/getting_started/installation/cpu/)
- [默认模型](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct)
- [源代码](https://github.com/vllm-project/vllm)
- [Apache 2.0 许可证](https://github.com/vllm-project/vllm/blob/main/LICENSE)
