# 在 Sealos 上部署和托管 TeslaMate

TeslaMate 是面向 Tesla 车辆的自托管数据记录器。此模板会在 Sealos Cloud 上部署 TeslaMate，并配套 PostgreSQL、Mosquitto 和 Grafana。

![TeslaMate 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/teslamate/website-screenshot.webp)

## 关于托管 TeslaMate

TeslaMate 会记录车辆数据，将数据存储到 PostgreSQL，并提供 Web 界面用于 Tesla 账号登录和车辆状态查看。它也会通过 Mosquitto 发布遥测事件，方便接入 Home Assistant 等系统。

该模板会自动创建 KubeBlocks PostgreSQL 数据库、私有 Mosquitto Broker、TeslaMate Web 应用和 Grafana 仪表盘服务。Sealos 提供 HTTPS 入口、持久化存储、生命周期管理和 Canvas 资源控制能力。

## 常见使用场景

- **车辆历史记录**：持续追踪行程、充电、位置和能耗效率。
- **能源监控**：查看充电会话和长期能耗趋势。
- **家庭自动化**：把车辆状态接入基于 MQTT 的自动化系统。
- **仪表盘分析**：使用 TeslaMate Grafana 仪表盘分析车辆、行程和充电数据。

## TeslaMate 托管依赖

Sealos 模板包含 TeslaMate、Grafana、Mosquitto 和 KubeBlocks PostgreSQL。

### 部署依赖

- [TeslaMate 文档](https://docs.teslamate.org/) - 官方文档
- [Docker 安装指南](https://docs.teslamate.org/docs/installation/docker) - 官方 Docker 运行结构
- [GitHub 仓库](https://github.com/teslamate-org/teslamate) - 源码和版本发布

### 实现细节

**架构组件：**

此模板会部署四个服务：

- **TeslaMate**：运行在 4000 端口的主 Web 应用。
- **Grafana**：运行在 3000 端口并带持久化存储的仪表盘服务。
- **Mosquitto**：用于 TeslaMate 事件发布的私有 MQTT Broker。
- **PostgreSQL**：由 KubeBlocks 管理的车辆和遥测数据数据库。

**配置：**

TeslaMate 通过 KubeBlocks 凭据连接 PostgreSQL，并通过 Kubernetes Service DNS 连接 Mosquitto。Grafana 使用同一个 PostgreSQL 数据库，并通过独立 HTTPS 入口暴露。加密密钥会在部署时生成，用于加密 Tesla API Token。

**许可证信息：**

TeslaMate 使用 MIT License。此 Sealos 模板遵循仓库许可证。

## 为什么在 Sealos 上部署 TeslaMate？

Sealos 是基于 Kubernetes 的 AI 云操作系统，统一应用部署、运维和扩缩容。将 TeslaMate 部署到 Sealos 后，你可以获得：

- **一键部署**：从 App Store 模板直接部署 TeslaMate 和配套服务。
- **托管 PostgreSQL**：使用带持久化存储的 KubeBlocks PostgreSQL。
- **即时 HTTPS 访问**：自动获得 TeslaMate 和 Grafana 的 HTTPS URL。
- **Canvas 运维**：通过 Canvas、AI 对话和资源卡片调整服务。
- **按量资源**：用适合该监控栈的资源限制运行服务。

## 部署指南

1. 打开 [TeslaMate 模板](https://sealos.io/products/app-store/teslamate)，点击 **Deploy Now**。
2. 在弹窗中配置参数。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后会进入 Canvas。后续变更可以在对话框中描述需求让 AI 应用更新，或点击对应资源卡片修改设置。
4. 通过系统提供的 URL 访问应用：
   - **TeslaMate UI**：使用 Tesla 账号登录并完成 TeslaMate 设置流程。
   - **Grafana Dashboard**：打开 Grafana URL，使用应用显示的初始凭据登录，然后设置安全密码。

## 配置

部署后可以通过以下方式配置 TeslaMate：

- **TeslaMate UI**：连接 Tesla 账号并管理车辆追踪。
- **Grafana UI**：查看仪表盘并更新 Grafana 用户设置。
- **AI 对话**：描述运行时变更，让 AI 应用更新。
- **资源卡片**：调整 CPU、内存、存储或入口设置。

## 扩缩容

调整 TeslaMate 资源：

1. 打开该部署的 Canvas。
2. 点击 TeslaMate、Grafana、Mosquitto 或 PostgreSQL 资源卡片。
3. 调整 CPU、内存、存储或副本设置。
4. 在对话框中应用变更。

## 故障排查

### Tesla 账号登录无法完成

- 原因：Tesla API 认证或外部网络访问异常。
- 解决：重新打开 TeslaMate UI，重试 Tesla 账号流程，并确认部署可以访问外部 Tesla 服务。

### Grafana 要求初始密码

- 原因：Grafana 在部署后需要首次登录流程。
- 解决：使用 Grafana 初始凭据登录，然后按提示设置安全密码。

### MQTT 集成无法连接

- 原因：Mosquitto 默认是部署内部私有服务。
- 解决：从同一命名空间内的服务连接，或通过受控网络路径有意暴露 MQTT。

## 其他资源

- [TeslaMate FAQ](https://docs.teslamate.org/docs/faq)
- [TeslaMate MQTT 集成](https://docs.teslamate.org/docs/integrations/mqtt)
- [Sealos](https://sealos.io)

## 许可证

此 Sealos 模板遵循仓库许可证。TeslaMate 本身使用 MIT License。
