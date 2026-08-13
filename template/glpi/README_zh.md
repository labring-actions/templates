# GLPI

GLPI 是一款开源 IT 资产管理和服务台平台，支持资产库存、许可证、工单、支持请求和 ITIL 流程。

## 模板内容

该模板会部署：

- GLPI `11.0.8` 应用 StatefulSet。
- Kubeblocks 管理的 MySQL `8.0.30` 集群和持久化存储。
- 自动创建 GLPI 数据库的初始化 Job。
- 挂载到 `/var/glpi` 的应用持久化存储。
- 使用 TLS 的 Sealos 公网 Ingress 和自动生成的访问域名。

数据库连接信息由 Kubeblocks 自动生成的 Secret 注入。应用和数据库使用同一个生成的应用名称，部署资源会在当前命名空间内隔离。

## 在 Sealos 上部署

1. 在 Sealos 应用市场打开 GLPI 模板，点击“立即部署”。
2. 保留自动生成的应用名称和域名前缀，或按需修改。
3. 等待数据库集群和 GLPI 应用就绪。
4. 从应用卡片打开生成的公网地址。
5. 完成 GLPI 初始化向导，并立即修改默认账号密码。

## 配置项

- `app_name`：GLPI 资源和数据库集群使用的名称。
- `app_host`：公网域名前缀。
- `glpi_database`：初始化 Job 创建的 MySQL 数据库名称。

GLPI 应用数据保存在 `/var/glpi` 持久化卷中，数据库使用独立持久化卷，Pod 重启后数据仍会保留。

## 故障排查

如果公网地址暂时无法访问，请等待 MySQL 集群、数据库初始化 Job 和 GLPI StatefulSet 全部就绪。如果出现数据库连接错误，请确认生成的 `*-mysql-conn-credential` Secret 存在，并检查初始化 Job 是否成功完成。

## 相关链接

- [GLPI 官网](https://glpi-project.org/)
- [GLPI 文档](https://glpi-project.org/documentation/)
- [GLPI GitHub 仓库](https://github.com/glpi-project/glpi)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

GLPI 使用 GNU 通用公共许可证（GPL）发布。本 Sealos 模板遵循模板仓库的许可证条款。
