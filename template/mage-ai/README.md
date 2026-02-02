# Mage AI - 数据管道平台

[![Mage AI](https://img.shields.io/badge/Mage%20AI-000000?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxjaXJjbGUgY3g9IjEyIiBjeT0iMTIiIHI9IjEwIi8+PHBhdGggZD0ibTkgMTYgMy04IDMgOCIvPjwvc3ZnPg==)](https://www.mage.ai/)

## 简介

Mage AI 是一个自托管的数据管道开发环境，帮助团队创建生产级数据管道。它提供了快速、可视化的笔记本式界面，支持使用 Python、SQL 或 R 构建模块化的数据管道。

## 主要特性

- **模块化管道构建**：使用 Python、SQL 或 R 逐块构建管道
- **交互式笔记本界面**：在可视化界面中编写和记录逻辑
- **丰富的数据集成**：预置数据库、API 和云存储连接器
- **任务调度**：手动触发或按计划运行管道（支持 cron）
- **可视化调试**：日志、实时预览和错误处理
- **dbt 支持**：直接在 Mage 中构建和运行 dbt 模型

## 应用场景

- 使用 Python 将数据从 Google Sheets 迁移到 Snowflake
- 调度每日 SQL 管道来清理和聚合产品数据
- 在可视化笔记本界面中开发 dbt 模型
- 本地运行简单的 ETL/ELT 任务

## 部署说明

### 1. 部署应用

在 Sealos 平台上使用此模板一键部署 Mage AI。

### 2. 配置参数

部署时可配置以下参数：

- **Project Name**: Mage 项目名称（默认：default_project）
- **Require Authentication**: 是否启用用户认证（默认：false）

### 3. 访问应用

部署完成后，通过生成的域名访问 Mage AI 界面。

### 4. 数据库连接

- PostgreSQL 数据库会自动创建并初始化
- 数据库名称：`mage`
- 用户名：`postgres`
- 密码：自动生成并安全存储

## 资源配置

默认资源配置如下：

- **PostgreSQL 数据库**：
  - CPU: 500m / 50m (limit/request)
  - 内存: 512Mi / 51Mi (limit/request)
  - 存储: 10Gi

- **Mage Server（后端）**：
  - CPU: 1000m / 100m (limit/request)
  - 内存: 1Gi / 256Mi (limit/request)
  - 存储: 5Gi（用于 .mage_data 目录）

- **Mage App（前端）**：
  - CPU: 500m / 100m (limit/request)
  - 内存: 512Mi / 256Mi (limit/request)

## 环境变量

应用使用以下关键环境变量（已自动配置）：

- `MAGE_DATABASE_CONNECTION_URL`: PostgreSQL 数据库连接 URL
- `MAGE_SECRET_KEY`: 应用密钥（自动生成）
- `AUTHENTICATION_MODE`: 认证模式
- `REQUIRE_USER_AUTHENTICATION`: 是否要求用户认证
- `ENV`: 运行环境（production）

## 高级配置

### 自定义认证

如果需要启用用户认证，将 `Require Authentication` 设置为 `true`。认证模式可通过 `AUTHENTICATION_MODE` 环境变量进一步配置（支持 `username_password`、`ldap` 等）。

### 连接外部服务

Mage 支持连接多种外部服务，包括：

- AWS S3、Redshift、Glue
- Google Cloud Storage、BigQuery
- Snowflake、Databricks
- MySQL、MongoDB 等

相关环境变量可在 Deployment 中添加。

### SMTP 配置

如需邮件通知功能，可添加以下环境变量：

- `SMTP_EMAIL`: SMTP 发件人邮箱
- `SMTP_PASSWORD`: SMTP 密码
- `SMTP_HOST`: SMTP 服务器地址
- `SMTP_PORT`: SMTP 端口

## 故障排查

### 应用无法启动

1. 检查 Pod 日志：`kubectl logs -n <namespace> <pod-name>`
2. 确认数据库已就绪：检查初始化 Job 状态
3. 检查资源限制是否充足

### 无法访问界面

1. 确认 Ingress 已正确配置
2. 检查 TLS 证书是否有效
3. 验证 Service 是否正常工作

### 数据库连接失败

1. 检查 PostgreSQL Pod 状态
2. 确认数据库初始化 Job 已完成
3. 验证 Secret 中的连接信息是否正确

## 数据持久化

以下数据会被持久化存储：

- **PostgreSQL 数据**：存储在 PVC（10Gi）
- **Mage 用户数据**：存储在 /root/.mage_data（5Gi）

升级应用时，这些数据会自动保留。

## 升级说明

1. 在 Sealos 控制台点击升级按钮
2. 选择新的镜像版本（如有）
3. 确认升级，数据会自动保留

## 支持与文档

- [Mage AI 官方文档](https://docs.mage.ai)
- [GitHub 仓库](https://github.com/mage-ai/mage-ai)
- [Sealos 文档](https://sealos.io/docs)

## 开源协议

本项目基于 Mage AI 开源协议部署。Mage AI 的开源协议请参考：[GitHub License](https://github.com/mage-ai/mage-ai/blob/master/LICENSE)

## 注意事项

1. 首次部署可能需要几分钟初始化数据库
2. 建议在生产环境中启用认证功能
3. 根据实际使用情况调整资源配额
4. 定期备份 PostgreSQL 数据
5. 如需更多功能，可考虑升级到 [Mage Pro](https://mage.ai)