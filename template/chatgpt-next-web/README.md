# Deploy and Host NextChat on Sealos

NextChat is a lightweight AI assistant web UI for OpenAI-compatible providers, Azure OpenAI, Claude, DeepSeek, Gemini, and other model gateways. This template deploys the official NextChat container with HTTPS access on Sealos Cloud.

![NextChat Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/chatgpt-next-web/website-screenshot.webp)

## About Hosting NextChat

NextChat runs as a single web application and stores chat state in the browser. The Sealos template creates a Deployment, Service, Ingress, and App entry, then injects model-provider settings through deployment inputs.

Access control is handled by the `CODE` input. When `CODE` is configured, users enter one of the comma-separated access codes on the first screen. When `CODE` is empty, the application opens directly.

## Common Use Cases

- **Private ChatGPT UI**: Run a fast personal chat interface with your own API key.
- **Team Access Code Gateway**: Share one HTTPS endpoint protected by one or more access codes.
- **OpenAI-Compatible Proxy UI**: Point `BASE_URL` to a compatible gateway or self-hosted endpoint.
- **Azure OpenAI Frontend**: Configure Azure deployment URL, key, and API version during deployment.

## Deployment Guide

1. Open the [NextChat template](https://sealos.io/products/app-store/chatgpt-next-web) and click **Deploy Now**.
2. Enter `OPENAI_API_KEY`. Use commas to rotate multiple keys.
3. Optionally configure:
   - `CODE`: access password list, comma-separated
   - `BASE_URL`: OpenAI-compatible API base URL
   - `HIDE_USER_API_KEY`: set to `1` to hide the user API key field
   - `DISABLE_GPT4`: set to `1` to hide GPT-4 model choices
   - `HIDE_BALANCE_QUERY`: set to `1` to hide balance query features
   - `AZURE_URL`, `AZURE_API_KEY`, `AZURE_API_VERSION`: Azure OpenAI settings
4. Wait for the Deployment to become ready, then open the generated HTTPS URL from Sealos Canvas.
5. If an access-code screen appears, enter a value from `CODE`.

## Configuration

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI-compatible API keys, comma-separated when multiple keys should be rotated. | `true` | `<redacted>` |
| `CODE` | Access codes for the web UI, comma-separated when multiple codes are allowed. | `false` | `` |
| `BASE_URL` | OpenAI-compatible API base URL for proxies or self-hosted endpoints. | `false` | `https://api.openai.com` |
| `OPENAI_ORG_ID` | OpenAI organization ID. | `false` | `` |
| `HIDE_USER_API_KEY` | Set to `1` to hide the user-provided API key field in the UI. | `false` | `` |
| `DISABLE_GPT4` | Set to `1` to disable GPT-4 model options. | `false` | `` |
| `HIDE_BALANCE_QUERY` | Set to `1` to hide balance query features. | `false` | `` |
| `AZURE_URL` | Azure OpenAI deployment URL. | `false` | `https://{azure-resource-url}/openai/deployments/{deploy-name}` |
| `AZURE_API_KEY` | Azure OpenAI API key. | `false` | `<redacted>` |
| `AZURE_API_VERSION` | Azure OpenAI API version. | `false` | `` |

Store private API keys and access codes in Sealos-managed inputs.

## Scaling

The template is tuned for a small single-instance web UI. Increase CPU and memory from Sealos Canvas if many users share the same deployment or if the UI serves through a slower model gateway.

## Troubleshooting

### Access code is rejected

Check that the value entered in the browser matches one of the comma-separated values in `CODE`, then restart the Deployment after changing the input.

### Model requests fail

Verify `OPENAI_API_KEY`, `BASE_URL`, Azure settings, and model-provider rate limits. For OpenAI-compatible gateways, confirm that the gateway supports the selected model names.

### Balance query is visible

Set `HIDE_BALANCE_QUERY` to `1` and restart the Deployment.

## Additional Resources

- [NextChat Website](https://nextchat.club/)
- [NextChat Source Code](https://github.com/ChatGPTNextWeb/NextChat)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is provided under the template repository license. NextChat is licensed by its upstream project.
