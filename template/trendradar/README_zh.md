# 在 Sealos 上部署和托管 TrendRadar

TrendRadar 用于追踪热点话题、定时生成报告，并通过内置 Web 服务展示最新 HTML 报告。此模板默认使用本地持久化存储，并提供可选 S3 兼容远程存储。

![TrendRadar 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/trendradar/website-screenshot.webp)

## 关于托管 TrendRadar

TrendRadar 会按 cron 周期采集主题信号，保存生成的 SQLite 和 HTML 报告文件，并通过 HTTP 展示报告。模板使用官方 Docker 镜像，挂载应用 ConfigMap 和持久化 `/app/output` 卷。

默认后端是本地存储。使用 S3 兼容存储时，将 **Storage Backend** 设置为 `remote`，并填写 S3 endpoint、bucket、access key、secret key 和 region 字段。

## 常见使用场景

- **趋势监控**：追踪 AI、云计算、创业、产品发布等主题。
- **定时报告**：按 cron 周期生成最新 HTML 报告。
- **Newsletter 研究**：收集高信号素材供编辑筛选。
- **轻量情报看板**：通过稳定 HTTPS URL 展示生成报告。

## TrendRadar 托管依赖

Sealos 模板包含 TrendRadar 容器、配置文件、本地持久化存储、公开 HTTPS 入口和可选 S3 兼容存储输入。

### 部署依赖

- [GitHub 仓库](https://github.com/sansan0/TrendRadar) - 源代码
- [公开演示](https://sansan0.github.io/TrendRadar) - 生成报告示例
- [Docker 镜像](https://hub.docker.com/r/wantcat/trendradar) - 上游容器镜像

## 实现细节

**架构组件：**

- **TrendRadar**：调度器、采集器、报告生成器和 Web 服务。
- **ConfigMap**：挂载精简 `config.yaml` 和 `frequency_words.txt` 到 `/app/config`。
- **持久化存储**：`/app/output` 保存本地生成报告。
- **可选 S3 存储**：通过 `STORAGE_BACKEND=remote` 和 `S3_*` 环境变量连接 S3 兼容存储。

**配置：**

- `cron_schedule` 控制报告采集周期。
- `storage_backend` 可选 `local` 或 `remote`。
- S3 字段是普通可选输入；选择 `remote` 时填写这些字段。

**许可证信息：**

TrendRadar 使用 GPL-3.0。

## 为什么在 Sealos 上部署 TrendRadar？

Sealos 提供自动 HTTPS、持久化存储，以及用于 cron 和存储配置的简单部署表单。此模板让 TrendRadar 以很低运维成本获得稳定公网报告 URL。

## 部署指南

1. 打开 [TrendRadar 模板](https://sealos.io/products/app-store/trendradar)，点击 **Deploy Now**。
2. 在弹窗中配置参数。内置持久卷使用 `local`；使用远程 S3 时选择 `remote` 并填写 S3 字段。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会进入 Canvas。
4. 打开生成的应用 URL 查看最新 HTML 报告。

## 配置

可在 Sealos Canvas 中编辑 ConfigMap 来调整主题组、过滤词和报告行为。CPU、内存、存储和环境变量可通过资源卡片调整。

## 更多资源

- [TrendRadar README](https://github.com/sansan0/TrendRadar)
- [GitHub Issues](https://github.com/sansan0/TrendRadar/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## License

此模板遵循上游 TrendRadar GPL-3.0 License。
