# 在 Sealos 上部署和托管 NextChat

NextChat 是一个轻量 AI 助手 Web UI，支持 OpenAI 兼容模型、Azure OpenAI、Claude、DeepSeek、Gemini 以及其他模型网关。此模板会在 Sealos Cloud 上部署官方 NextChat 容器，并提供 HTTPS 访问入口。

![NextChat 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/chatgpt-next-web/website-screenshot.webp)

## 关于托管 NextChat

NextChat 以单个 Web 应用运行，聊天状态保存在浏览器中。Sealos 模板会创建 Deployment、Service、Ingress 和 App 入口，并通过部署输入注入模型服务配置。

访问控制由必填的 `CODE` 输入管理。模板会生成唯一默认访问码，用户在首屏输入逗号分隔列表中的任意访问码。

## 常见使用场景

- **私有 ChatGPT 界面**：使用自己的 API Key 运行快速聊天界面。
- **团队访问码入口**：通过一个 HTTPS 地址和一组访问码共享 AI 助手。
- **OpenAI 兼容代理界面**：将 `BASE_URL` 指向兼容网关或自托管端点。
- **Azure OpenAI 前端**：在部署时配置 Azure 部署地址、密钥和 API 版本。

## 部署指南

1. 打开 [NextChat 模板](https://sealos.io/products/app-store/chatgpt-next-web)，点击 **Deploy Now**。
2. 填写 `OPENAI_API_KEY`。多个 Key 使用英文逗号分隔，以便轮询使用。
3. 保留自动生成的 `CODE`，或替换为私有访问码列表，多个值使用英文逗号分隔。
4. 按需配置：
   - `BASE_URL`：OpenAI 兼容 API 基础地址
   - `HIDE_USER_API_KEY`：设置为 `1` 后隐藏用户 API Key 输入框
   - `DISABLE_GPT4`：设置为 `1` 后隐藏 GPT-4 模型选项
   - `ENABLE_BALANCE_QUERY`：设置为 `1` 后启用余额查询功能
   - `AZURE_URL`、`AZURE_API_KEY`、`AZURE_API_VERSION`：Azure OpenAI 配置
5. 等待 Deployment 就绪，然后从 Sealos Canvas 打开生成的 HTTPS 地址。
6. 在访问码页面输入 `CODE` 中的任意一个值。

## 配置说明

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `OPENAI_API_KEY` | OpenAI 兼容 API Key，多个 Key 使用英文逗号分隔。 | `是` | `<已隐藏>` |
| `CODE` | Web UI 访问码，多个访问码使用英文逗号分隔。 | `是` | 自动生成 16 位值 |
| `BASE_URL` | OpenAI 兼容 API 基础地址，用于代理或自托管端点。 | `否` | `https://api.openai.com` |
| `OPENAI_ORG_ID` | OpenAI 组织 ID。 | `否` | `` |
| `HIDE_USER_API_KEY` | 设置为 `1` 后隐藏用户自行填写 API Key 的输入框。 | `否` | `` |
| `DISABLE_GPT4` | 设置为 `1` 后关闭 GPT-4 模型选项。 | `否` | `` |
| `ENABLE_BALANCE_QUERY` | 设置为 `1` 后启用余额查询功能。 | `否` | `` |
| `AZURE_URL` | Azure OpenAI 部署地址。 | `否` | `https://{azure-resource-url}/openai/deployments/{deploy-name}` |
| `AZURE_API_KEY` | Azure OpenAI API Key。 | `否` | `<已隐藏>` |
| `AZURE_API_VERSION` | Azure OpenAI API 版本。 | `否` | `` |

请将私有 API Key 和访问码保存在 Sealos 管理的输入项中。公开 HTTPS 入口会使用部署端的模型 API Key，因此请妥善保管 `CODE`。

## 扩展

模板按小型单实例 Web UI 调优。多人共用同一部署或模型网关响应较慢时，可在 Sealos Canvas 中提高 CPU 和内存。

## 故障排查

### 访问码校验失败

检查浏览器中输入的值是否与 `CODE` 的英文逗号分隔列表一致，修改输入后重启 Deployment。

### 模型请求失败

检查 `OPENAI_API_KEY`、`BASE_URL`、Azure 配置和模型服务商限流状态。使用 OpenAI 兼容网关时，确认网关支持当前选择的模型名。

### 页面没有余额查询功能

将 `ENABLE_BALANCE_QUERY` 设置为 `1`，然后重启 Deployment。

## 更多资源

- [NextChat 官网](https://nextchat.club/)
- [NextChat 源代码](https://github.com/ChatGPTNextWeb/NextChat)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板遵循模板仓库许可证提供。NextChat 遵循上游项目许可证。
