# 在 Sealos 上部署和托管 MoneyPrinterTurbo

MoneyPrinterTurbo 可将主题或文案制作成短视频，支持素材、配音、字幕和背景音乐。本模板在 Sealos 上运行官方 v1.3.6 WebUI，并持久化保存配置和视频文件。

![MoneyPrinterTurbo 项目截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/moneyprinterturbo/website-screenshot.webp)

## 关于 MoneyPrinterTurbo 托管

Streamlit 网页界面提供文案生成、素材选择、配音、字幕和视频导出功能。可选的云服务提供 AI 能力，应用容器内的 FFmpeg 负责视频处理与合成。

Sealos 会创建一个应用实例、一块持久卷和一个 HTTPS 访问地址。已保存的设置、上传素材和生成文件共用持久存储，Pod 重建后仍会保留。应用采用单用户共享配置模式。

## 常见使用场景

- **社交平台短视频**：组合文案、素材、配音和字幕。
- **本地视频编辑**：上传自己的视频，设置画面比例、转场和音频。
- **多语言内容制作**：选择支持目标语言的文本和配音服务。
- **复用视频风格**：通过网页导入、导出生成参数预设。

## MoneyPrinterTurbo 托管依赖

官方镜像包含 Python、Streamlit、FFmpeg、字体和应用依赖。云端文案生成与在线素材服务需要对应的 API Key，可在部署完成后配置。

### 部署参考

- [官方英文文档](https://github.com/harry0703/MoneyPrinterTurbo/blob/v1.3.6/README-en.md)
- [配置参考](https://github.com/harry0703/MoneyPrinterTurbo/blob/v1.3.6/config.example.toml)
- [版本说明](https://github.com/harry0703/MoneyPrinterTurbo/releases/tag/v1.3.6)
- [社区支持](https://github.com/harry0703/MoneyPrinterTurbo/issues)

### 实现细节

| 组件 | 配置 |
| --- | --- |
| 应用 | 单副本 StatefulSet，使用 `ghcr.io/harry0703/moneyprinterturbo:v1.3.6` |
| 网页入口 | Streamlit 监听 8501 端口，通过 HTTPS 提供访问 |
| 应用资源 | 上限：4 CPU、4096Mi 内存；请求：400m CPU、409Mi 内存 |
| 配置初始化 | 上限：100m CPU、128Mi 内存；请求：10m CPU、12Mi 内存 |
| 持久存储 | 一块 1Gi 持久卷，挂载至 `/MoneyPrinterTurbo/storage` |
| 配置保存位置 | `/MoneyPrinterTurbo/storage/config.toml`，通过 `/MoneyPrinterTurbo/config.toml` 加载 |

资源上限遵循上游规定的最低 4 核 CPU、4 GB 内存。线上验证覆盖了冷启动、设置修改、本地素材上传和 1080×1920 视频合成。较长视频、批量任务和本地 Whisper 模型需要更多资源；下载大型模型前请扩容存储。

本模板保留原有的独立 WebUI 架构，采用本地文件系统保存数据。上游可选的 Redis 任务状态服务及独立 API 服务属于此部署之外的扩展组件。

MoneyPrinterTurbo 采用 MIT 许可证。

## 为什么在 Sealos 上部署 MoneyPrinterTurbo？

Sealos 基于 Kubernetes，提供一键部署、托管 HTTPS、持久存储和资源监控。按量计费与可调整的资源上限便于匹配实际工作负载。部署完成后，可通过 Canvas 中的 AI 对话或资源卡片管理应用。

## 部署指南

1. 打开 [MoneyPrinterTurbo 模板页面](https://sealos.io/products/app-store/moneyprinterturbo)，点击 **Deploy Now**。
2. 确认应用资源后部署。服务商 API Key 可在应用启动后通过网页配置。
3. 等待部署完成，通常需要 2-3 分钟；首次拉取镜像可能耗时更久。进入部署的 Canvas，打开应用提供的公网地址。
4. 网页会直接进入操作界面。**此版本的 WebUI 无内置注册或登录功能。** 能访问该地址的人都可以操作应用和共享设置。填写服务商凭据前，请将访问范围限制为可信用户。
5. 使用 **Language / 语言** 切换界面语言。打开 **设置（Settings）** 或 **配置大模型（Configure AI model）**，选择服务商并填写 API Key；通过 **配置素材来源（Configure material sources）** 配置在线素材凭据。
6. 填写主题或文案，选择视频和音频设置，点击 **生成视频（Generate Video）**。完成后预览结果，点击 **下载视频（Download Video）**。

### 体验本地视频流程

验证本地处理流程时，可在 **视频来源 → 本地文件** 中上传宽高均至少为 480 像素的视频，填写文案，选择 **配音模式 → 无配音**、**无背景音乐**，并清除 **启用字幕**。点击 **生成视频** 后下载结果。测试中，3 秒的 640×640 素材成功生成了 1080×1920 竖屏视频。

## 配置与存储

设置会自动保存。初始化容器仅在持久化配置文件尚未创建时复制官方示例。启动器将配置临时文件和保存文件放在同一持久卷内，保证原子更新。

通过 **参数预设（Settings Preset）** 导入或导出视频设置。服务商凭据可通过 **设置 → 密钥备份（Key Backup）** 导出，请妥善保管密钥文件。及时下载需要保留的视频，并通过 Canvas 资源卡片管理 1Gi 存储配额。

现有部署使用旧版持久卷声明名称时，采用本模板前请备份配置和视频数据。规范化后的声明名称会创建新的 PVC；将备份迁移至新部署并验证后，再清理旧存储。

## 故障排查

- **提示填写服务商凭据**：在设置中配置选定的云服务，或使用上述本地视频流程。
- **本地素材被拒绝**：上传有效的视频文件，并确保宽高均至少为 480 像素。
- **大文件上传被拒绝**：Ingress 当前允许最多 32 MB 的请求。上传更大文件时，请提高请求体大小上限，并检查 Streamlit 的上传大小设置。
- **合成较慢或存储已满**：在 Canvas 查看资源卡片与日志。较长视频和本地转录模型需要相应增加 CPU、内存或存储容量。

## 许可证

MoneyPrinterTurbo 采用 [MIT 许可证](https://github.com/harry0703/MoneyPrinterTurbo/blob/v1.3.6/LICENSE)。本模板遵循 Sealos 模板仓库的许可条款。
