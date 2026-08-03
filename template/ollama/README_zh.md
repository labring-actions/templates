# Ollama

Ollama 通过 REST API 和 OpenAI 兼容 API 运行开放模型。该 Sealos 模板部署官方 CPU 镜像，提供持久化模型存储和公网 HTTPS 端点。

![Ollama 官网](website-screenshot.webp)

## 功能特性

- 官方 `ollama/ollama:0.32.5` 镜像
- 原生 Ollama API 和 OpenAI 兼容端点
- `/root/.ollama` 持久化模型存储
- 通过 `/api/version` 执行健康检查
- 默认使用纯 CPU 部署

## 在 Sealos 上部署

1. 打开 [Ollama 模板](https://sealos.io/products/app-store/ollama)。
2. 点击 **Deploy Now**。
3. 等待 StatefulSet 进入 Ready 状态。首次拉取镜像可能需要几分钟。
4. 打开生成的 App URL，或从 Sealos 应用详情中复制该地址。

App URL 指向 Ollama API。在浏览器中访问 `/` 会返回 `Ollama is running`。

## 使用 API

设置生成的 HTTPS 端点：

```bash
export OLLAMA_URL="https://<your-app>.usw-1.sealos.app"
```

检查部署版本和可用模型：

```bash
curl "$OLLAMA_URL/api/version"
curl "$OLLAMA_URL/api/tags"
```

拉取模板验证使用的轻量模型：

```bash
curl "$OLLAMA_URL/api/pull" \
  -H "Content-Type: application/json" \
  -d '{"model":"smollm2:135m","stream":false}'
```

生成回复：

```bash
curl "$OLLAMA_URL/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "smollm2:135m",
    "prompt": "What is 2 + 2?",
    "stream": false
  }'
```

OpenAI 兼容客户端可将 `$OLLAMA_URL/v1` 设置为基础 URL。完整端点说明请参阅 [Ollama API 文档](https://docs.ollama.com/api/introduction)。

## 默认资源

| 资源 | 默认值 |
| --- | --- |
| CPU 限制 | `500m` |
| 内存限制 | `512Mi` |
| 模型存储 | `1Gi` |
| 副本数 | `1` |

该默认配置已在 Sealos 上使用 `smollm2:135m` 完成验证，其模型文件约为 271 MB。更大的模型需要足够的内存容纳权重和运行缓冲区；当模型文件超过可用空间时，还需要扩大持久卷。

## 持久化

StatefulSet 使用挂载到 `/root/.ollama` 的 `openebs-backup` 卷保存下载的模型和元数据。Pod 重建后会继续使用这些数据。删除模板实例及其 PVC 会移除已存储的模型。

## 访问控制

Ollama 本地 API 采用无内置认证的访问方式。Sealos Ingress 会将生成的 HTTPS 端点发布到互联网。请将该 URL 视为敏感信息，并在向非受信客户端共享前配置带认证的网关或网络访问策略。

## 相关链接

- [Ollama 官网](https://ollama.com)
- [Ollama 文档](https://docs.ollama.com)
- [源代码](https://github.com/ollama/ollama)
- [MIT 许可证](https://github.com/ollama/ollama/blob/main/LICENSE)
