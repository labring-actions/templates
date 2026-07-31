# 在 Sealos 上部署和托管 MLflow

MLflow 是一个开源 AI 工程平台，可用于实验跟踪、模型管理、应用评估和产物存储。此模板会在 Sealos Cloud 上部署一套启用身份认证的 MLflow 3.14.0 服务，并可独立选择数据库和产物存储方案。

![MLflow 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/mlflow/website-screenshot.webp)

## 关于托管 MLflow

MLflow 提供浏览器界面和 REST API，可记录运行、比较指标、注册模型并查看产物。模板会启用 MLflow 内置的 Basic Auth 应用，生成高强度初始管理员密码，并将用户和权限持久化到 SQL 存储中。

数据库可选择轻量的持久化 SQLite，也可选择由 Sealos 托管的 PostgreSQL 16.4 独立数据库服务。产物可保存到持久化本地卷，也可存入 Sealos 私有 S3 兼容存储桶。四种组合均保持一个 MLflow 服务副本。

## 常见使用场景

- **实验跟踪**：记录训练或评估任务产生的参数、指标、标签、追踪数据和产物。
- **模型管理**：注册模型、审查版本并协同完成发布流程。
- **AI 应用评估**：在同一工作区中比较应用质量、追踪数据和评估结果。
- **团队机器学习运维**：为 Notebook、脚本和 CI 任务提供共享且经过身份认证的跟踪入口。

## MLflow 托管依赖

模板包含官方 `ghcr.io/mlflow/mlflow:v3.14.0-full` 镜像、持久化应用存储、HTTPS Ingress 和 App 链接。启用相应选项后，模板还会创建 PostgreSQL 和 Sealos Object Storage。

### 部署依赖

- [MLflow 文档](https://mlflow.org/docs/latest/) - 官方文档
- [MLflow Tracking Server](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/) - 服务端与产物代理架构
- [MLflow Basic Auth](https://mlflow.org/docs/latest/self-hosting/security/basic-http-auth/) - 登录、用户与权限
- [MLflow GitHub 仓库](https://github.com/mlflow/mlflow) - 源代码与版本发布

### 实现细节

**架构组件：**

- **MLflow Server**：一个 `Deployment` 在 5000 端口提供 Web 界面、REST API、实验跟踪、模型注册和产物代理服务。
- **持久卷**：一个 1 GiB 的 `ReadWriteOnce` 卷，用于保存认证配置，以及对应分支使用的 SQLite 文件和本地产物。
- **PostgreSQL**：可选的 KubeBlocks PostgreSQL 16.4 集群，在 `mlflow` 数据库中同时保存跟踪数据和认证数据。MLflow 使用独立的 Alembic 版本表管理跟踪与认证迁移。
- **对象存储**：可选的私有 `ObjectStorageBucket`，通过 MLflow 身份认证代理保存产物。
- **Ingress 与 App 链接**：Sealos 提供公网 HTTPS 入口和证书。

**存储组合：**

| PostgreSQL | Sealos S3 | 元数据与认证 | 产物 |
| --- | --- | --- | --- |
| 关闭 | 关闭 | 持久化 SQLite 文件 | 持久化本地卷 |
| 关闭 | 开启 | 持久化 SQLite 文件 | Sealos 私有 S3 存储桶 |
| 开启 | 关闭 | 托管 PostgreSQL | 持久化本地卷 |
| 开启 | 开启 | 托管 PostgreSQL | Sealos 私有 S3 存储桶 |

MLflow 通过 `--serve-artifacts` 和 `--artifacts-destination` 启动。客户端经由经过身份认证的 MLflow 入口上传和下载产物，对象存储凭据始终保留在服务端。

**身份认证：**

部署运行 `mlflow server --app-name basic-auth`。自动生成的 Flask secret 用于保护浏览器会话和 CSRF 操作。部署表单会显示初始管理员用户名和自动生成的密码，请在开始部署前妥善记录。

**初始资源候选值：**

- MLflow 服务：CPU 上限 `2`，内存上限 `2Gi`
- 认证准备容器和 PostgreSQL 就绪检查容器：CPU 上限 `100m`，内存上限 `128Mi`
- 可选 PostgreSQL 组件：CPU 上限 `500m`，内存上限 `512Mi`

这些资源值面向个人低负载场景，部署后可在 Canvas 中继续调整。

**许可证信息：**

MLflow 使用 Apache License 2.0。此 Sealos 模板遵循 Sealos templates 仓库的许可证。

## 为什么在 Sealos 上部署 MLflow？

Sealos 是构建在 Kubernetes 之上的 AI 辅助云操作系统。此模板通过一次部署即可创建应用、数据库、对象存储、持久卷、网络和 TLS 资源。

- **一键部署**：通过一个应用商店表单创建完整的 MLflow 技术栈。
- **独立存储选择**：可组合轻量本地方案，也可启用托管 PostgreSQL 和 S3 服务。
- **数据持久化**：Pod 替换后，元数据、用户、权限和产物依然保留。
- **即时 HTTPS 访问**：自动获取带 TLS 的公网入口。
- **AI 辅助运维**：后续可通过 Canvas 中的 AI 对话框和资源卡片进行调整。
- **按量付费**：从个人工作负载配置起步，并随使用量增长提高资源。

## 部署指南

1. 打开 [MLflow 模板](https://sealos.io/products/app-store/mlflow)，点击 **Deploy Now**。
2. 查看自动生成的管理员用户名和密码，将其保存到密码管理器，然后选择 PostgreSQL 和 Sealos S3 选项。
3. 等待部署完成。SQLite 方案通常需要 2-3 分钟，新建 PostgreSQL 集群可能增加数分钟。部署完成后，Sealos 会打开 Canvas；后续可通过 AI 对话框或资源卡片调整配置。
4. 打开自动生成的 MLflow HTTPS 地址，在浏览器认证提示框中输入管理员用户名和密码。
5. 打开 **Experiments**，创建一个实验，再进入新实验页面，确认功能可用。

## 登录与用户管理

### 登录 Web 界面

1. 从 App 资源打开自动生成的 HTTPS 地址。
2. 输入部署表单中记录的 `admin_username` 和 `admin_password`。
3. 保持浏览器开启即可继续使用当前 Basic Auth 会话。关闭浏览器会结束浏览器会话。

### 创建其他用户

1. 使用管理员账号登录。
2. 打开 `https://<your-mlflow-host>/signup`。
3. 输入新用户名和密码并提交表单。
4. 打开 MLflow Admin UI，为用户分配所需工作区和资源对应的角色或直接权限。

新用户采用模板的安全工作区策略，通过管理员分配的 RBAC 角色或直接权限获得访问能力。

### 修改密码

每位用户都可以通过经过身份认证的 MLflow REST API 修改自己的密码：

```bash
export MLFLOW_TRACKING_URI='https://<your-mlflow-host>'
export MLFLOW_TRACKING_USERNAME='admin'
export MLFLOW_TRACKING_PASSWORD='<current-password>'
export MLFLOW_NEW_PASSWORD='<new-strong-password>'

python - <<'PY'
import os
import requests

uri = os.environ["MLFLOW_TRACKING_URI"].rstrip("/")
username = os.environ["MLFLOW_TRACKING_USERNAME"]
response = requests.patch(
    f"{uri}/api/2.0/mlflow/users/update-password",
    auth=(username, os.environ["MLFLOW_TRACKING_PASSWORD"]),
    json={"username": username, "password": os.environ["MLFLOW_NEW_PASSWORD"]},
    timeout=30,
)
response.raise_for_status()
print("Password updated.")
PY
```

请求成功后，请同步更新客户端中的 `MLFLOW_TRACKING_PASSWORD`。SQL 认证存储会在重启后继续保留新密码。

### 连接 MLflow 客户端

```bash
export MLFLOW_TRACKING_URI='https://<your-mlflow-host>'
export MLFLOW_TRACKING_USERNAME='<username>'
export MLFLOW_TRACKING_PASSWORD='<password>'
```

MLflow 客户端会使用这些变量访问跟踪 API 和产物代理接口。

## 配置

- **数据库模式**：关闭 `Enable PostgreSQL` 时，系统使用 `/mlflow/data` 下的 SQLite 文件；开启后会创建 PostgreSQL，并将跟踪和认证数据写入托管数据库。
- **产物模式**：关闭 `Enable S3 Storage` 时，系统使用 `/mlflow/local-artifacts`；开启后会创建私有存储桶，并将凭据注入服务端。
- **管理员凭据**：表单会生成高强度初始密码。认证存储在首次初始化时应用这些引导值。
- **Canvas 运维**：通过 AI 对话框或资源卡片调整资源、查看日志并管理存储。

请在记录生产运行前确定数据库和产物模式。切换任一选项后，MLflow 会连接新选择的数据平面；跨模式迁移时，请显式迁移元数据、用户、权限和产物对象。

## 备份与恢复

- **SQLite 与本地产物**：备份 MLflow 持久卷资源卡片，其中同时包含 SQLite 文件和产物。
- **SQLite 与 S3**：备份持久卷中的元数据和认证数据，同时保留保存产物的私有存储桶。
- **PostgreSQL 与本地产物**：在数据库资源卡片中配置 PostgreSQL 备份，同时备份保存产物的持久卷。
- **PostgreSQL 与 S3**：配置 PostgreSQL 备份并保留私有存储桶。持久卷中保存自动生成的认证配置。

请一并恢复元数据和与其匹配的产物存储，确保实验中的产物引用能够正常解析。

## 扩缩容

SQLite 和 `ReadWriteOnce` 持久卷方案采用单写入者访问，因此模板保持一个 MLflow 副本。请求量增长后，可在 Deployment 资源卡片中提高 CPU 和内存。多副本架构需要共享 SQL 元数据、共享对象存储、共享 Flask secret，以及支持并发副本的存储设计。

## 故障排查

### 浏览器反复弹出登录提示

确认用户名和密码来自部署表单。通过 API 修改密码后，SQL 中保存的新密码会成为当前有效凭据。

### 新用户只能看到少量资源

使用管理员账号登录，通过 Admin UI 分配工作区角色或直接资源权限。模板要求管理员为新用户显式配置 RBAC 权限。

### 产物上传失败

检查 MLflow Deployment 日志和所选存储资源。本地模式依赖健康的持久卷；S3 模式依赖处于就绪状态的私有 Object Storage 存储桶。

### 获取帮助

- [MLflow 文档](https://mlflow.org/docs/latest/)
- [MLflow GitHub Issues](https://github.com/mlflow/mlflow/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 其他资源

- [MLflow REST API](https://mlflow.org/docs/latest/api_reference/rest-api.html)
- [MLflow Authentication REST API](https://mlflow.org/docs/latest/api_reference/auth/rest-api.html)
- [MLflow Python API](https://mlflow.org/docs/latest/python_api/)
- [Sealos 应用商店](https://sealos.io/products/app-store)

## 许可证

此 Sealos 模板遵循 Sealos templates 仓库的许可证。MLflow 本身使用 Apache License 2.0。
