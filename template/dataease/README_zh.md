# 在 Sealos 上部署和托管 DataEase

DataEase 是一款开源商业智能与数据可视化平台，可用于构建数据集、仪表板和数据大屏。此 Sealos 模板会部署 DataEase 社区版 2.10.26，并配置独立 MySQL 数据库、持久化应用存储和托管 HTTPS 入口。

## 关于托管 DataEase

DataEase 提供浏览器工作台，支持连接数据源、准备数据集和构建交互式可视化。模板会持久化应用配置、上传资源、地图、插件、字体、导出文件和 MySQL 元数据。

部署过程会初始化一个本地管理员账号。管理员可在 DataEase 系统设置中创建并管理其他用户。

## 常见使用场景

- **运营仪表板**：跟踪销售、财务、客服和服务指标。
- **自助式分析**：让团队通过可视化界面探索统一管理的数据集。
- **嵌入式可视化**：向内部应用发布仪表板和数据大屏。
- **数据源整合**：连接 MySQL、PostgreSQL、SQL Server、API、文件及其他受支持的数据源。

## DataEase 托管依赖

模板包含独立 DataEase 部署所需的运行依赖：

- **DataEase 2.10.26**：运行 Web 应用和分析服务。
- **KubeBlocks MySQL 8.0.30**：保存用户、权限、数据集、仪表板和应用元数据。
- **持久化卷**：保存配置、日志、上传文件、地图、导出、插件、字体和本地化数据。
- **Sealos Ingress**：通过托管 HTTPS 入口发布应用。

### 部署依赖

- [DataEase 文档](https://dataease.io/docs/v2/)
- [DataEase 安装指南](https://dataease.io/docs/v2/installation/online_installation/)
- [DataEase GitHub 仓库](https://github.com/dataease/dataease)

## 实现细节

### 架构

模板会创建：

- 一个 DataEase StatefulSet 和 Service。
- 一个 KubeBlocks MySQL 集群。
- 一个数据库初始化 Job。
- 一个用于声明 DataEase 所需 MySQL 参数的 KubeBlocks Configuration 资源。
- 一个 Ingress 和一个 Sealos App 入口。

MySQL 配置包含 `max_connections=2000`、`max_connect_errors=6000` 和 `group_concat_max_len=1024000`，与 DataEase 官方部署配置要求一致。

### 持久化数据

DataEase StatefulSet 使用：

- `1Gi` 存储 `/opt/apps/config`。
- `1Gi` 存储 `/opt/dataease2.0`。

MySQL 集群使用独立的 `1Gi` 数据卷。完整备份需要同时覆盖 MySQL 集群和两个 DataEase 数据卷。

### 资源基线

应用默认限制为 `500m` CPU 和 `1024Mi` 内存。此档位已完成全新冷启动、管理员登录和内置销售仪表板加载，Pod 重启次数为零；仪表板场景的实测工作集约为 `768Mi`。

MySQL 组件使用 Sealos 数据库服务基线：`500m` CPU 和 `512Mi` 内存。

## 为什么在 Sealos 上部署 DataEase？

- **一键部署**：通过一个模板创建 DataEase、MySQL、持久化存储和 HTTPS 网络。
- **持久化分析工作区**：在重启后继续保留仪表板、数据集、账号和上传资源。
- **托管数据库生命周期**：通过 Sealos Canvas 中的 KubeBlocks 资源卡片管理 MySQL。
- **统一运维入口**：在同一个 Canvas 中查看日志、资源、存储和网络。
- **灵活调整资源**：随着仪表板使用量增长扩展 CPU、内存和存储。

## 部署指南

1. 打开 [DataEase 模板](https://sealos.io/products/app-store/dataease)。
2. 点击 **Deploy Now**。
3. 等待 DataEase 和 MySQL 就绪。全新部署通常需要 2-3 分钟。
4. 打开生成的 HTTPS 应用地址。

## 登录与首次使用

使用上游默认管理员凭据：

```text
用户名：admin
密码：DataEase@123456
```

登录后：

1. 打开右上角管理员菜单。
2. 选择 **修改密码**。
3. 设置私有管理员密码。
4. 打开 **数据准备 > 数据源** 连接数据源，或打开 **仪表板** 查看内置示例。

用户账号由管理员在 **系统设置** 中维护。

## 配置

部署后，可通过 Sealos Canvas 管理：

- **DataEase StatefulSet**：CPU、内存、探针、镜像版本和应用存储。
- **MySQL Cluster**：数据库资源、存储、运行状态和备份。
- **Ingress**：公网域名、TLS、上传大小和请求超时。
- **应用配置**：首次启动时生成并持久化的 `application.yml`。

## 扩容

面向更多用户或复杂仪表板时：

1. 在提高仪表板并发前增加 DataEase 内存。
2. 查询渲染或仪表板加载达到 CPU 上限时增加 CPU。
3. 在存储接近容量上限前扩展 DataEase 和 MySQL 数据卷。
4. 增加大量数据源后检查 MySQL 指标和连接使用量。

## 备份与恢复

完整备份包含：

1. KubeBlocks MySQL 数据卷。
2. DataEase 配置卷。
3. DataEase 应用数据卷。

恢复时使用同一备份时间点的数据库和两个应用卷，然后重启 DataEase StatefulSet。

## 故障排查

### 登录页返回 401

使用当前模板生成的空 servlet context path。DataEase 2.10.26 请求白名单会对字面值 `/` 进行前缀剥离，导致首页路径匹配失败。

### 数据源提示数据库连接数过多

打开 MySQL Configuration 资源并确认：

```text
max_connections=2000
max_connect_errors=6000
group_concat_max_len=1024000
```

模板会以声明方式应用这些参数，并在 MySQL Pod 替换后继续保留。

### DataEase 长时间停留在启动阶段

确认 MySQL 集群状态为 `Running`，数据库初始化 Job 状态为 `Complete`。DataEase Pod 会等待 `dataease` 数据库就绪后启动。

### 默认密码无法登录

默认密码用于全新数据库。恢复已有 MySQL 数据卷时，请使用管理员此前设置的密码。

## 其他资源

- [DataEase 用户手册](https://dataease.io/docs/v2/user_manual/)
- [DataEase Releases](https://github.com/dataease/dataease/releases)
- [Sealos 应用商店](https://sealos.io/products/app-store)

## 许可证

DataEase 社区版采用 GNU Affero General Public License v3.0。此 Sealos 模板遵循 Sealos templates 仓库的许可证。
