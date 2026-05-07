# Kanboard

Kanboard 是一个开源的看板项目管理应用。

## 模板说明

该 Sealos 模板会部署：
- Kanboard（`kanboard/kanboard:v1.2.50`）
- PostgreSQL 集群（Kubeblocks `postgresql-16.4.0`）
- 持久化存储目录：
  - `/var/www/app/data`
  - `/var/www/app/plugins`
  - `/etc/nginx/ssl`

## 在 Sealos 上部署

1. 打开 Sealos 应用市场。
2. 搜索 `Kanboard`。
3. 点击部署并等待应用就绪。
4. 从应用卡片进入系统分配的访问地址。

## 说明

- 数据库连接信息由 Kubeblocks Secret 注入。
- 使用 PVC 持久化，重启 Pod 后数据仍会保留。
