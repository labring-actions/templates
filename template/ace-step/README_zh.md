# ACE-Step 1.5

## 应用概览

开源音乐生成AI。商业级质量，A100上每首歌不到2秒。支持文本生成音乐、翻唱、重绘、LoRA训练，支持50+语言。

此 Sealos 模板会将 **ACE-Step 1.5** 部署为 `ace-step` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `cpu_limit` | `cpu_limit` 部署参数。 | `否` | `4000` |
| `dit_model` | `dit_model` 部署参数。 | `否` | `acestep-v15-turbo` |
| `gpu_count` | `gpu_count` 部署参数。 | `是` | `1` |
| `init_service` | `init_service` 部署参数。 | `否` | `true` |
| `llm_backend` | `llm_backend` 部署参数。 | `否` | `pt` |
| `lm_model` | `lm_model` 部署参数。 | `否` | `acestep-5Hz-lm-1.7B` |
| `memory_limit` | `memory_limit` 部署参数。 | `否` | `16384` |
| `output_volume_size` | `output_volume_size` 部署参数。 | `否` | `10` |
| `startup_mode` | `startup_mode` 部署参数。 | `是` | `gradio` |
| `volume_size` | `volume_size` 部署参数。 | `是` | `30` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://ace-step.github.io/ace-step-v1.5.github.io/
- 源码仓库: https://github.com/ace-step/ACE-Step
