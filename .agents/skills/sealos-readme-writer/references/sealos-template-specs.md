# Sealos 模板开发规范详细说明

本文档包含 Sealos 模板开发的完整技术规范，供创建 README 文档时参考。

## 模板文件组织规范

### 目录结构要求

所有模板必须按照以下目录结构组织：

```
templates/
└── template/
    └── <template-name>/    # 文件夹名称必须与模板的 name 字段一致
        └── index.yaml       # 模板文件必须命名为 index.yaml
```

### 命名规则

1. 文件夹名称必须与模板 Template CR 中的 `metadata.name` 字段保持一致
2. 模板文件必须命名为 `index.yaml`
3. 文件夹名称应该使用小写字母和连字符，避免使用下划线或其他特殊字符
4. **Template CR 的 `metadata.name` 必须硬编码为小写字母**，不能使用变量

## 资源创建顺序规范

模板内各个资源必须按照以下顺序创建：

1. **Template CR** - 首先创建 Template 元数据定义
2. **对象存储** - ObjectStorageBucket
3. **数据库资源** - ServiceAccount → Role → RoleBinding → Cluster → Job (初始化)
4. **应用资源** - Secret → ConfigMap → Deployment/StatefulSet → Service → Ingress → App

## Defaults 和 Inputs 配置规范

### 基本原则

- `defaults`：用于存放**自动生成**的值（如随机字符串、随机端口等）
- `inputs`：用于存放**需要用户输入**的值（如邮箱、API Key、自定义配置等）

### Defaults 配置要点

1. `app_host` 必须带应用名称前缀（如 `typesense-${{ random(8) }}`）
2. `app_name` 必须包含 `${{ random(8) }}` 以确保唯一性
3. 随机生成的配置（密钥、密码等）放在 `defaults` 中

## 国际化（i18n）配置

模板需要添加 `locale` 和 `i18n` 配置来支持多语言：

```yaml
spec:
  locale: en  # 默认语言
  i18n:
    zh:
      title: '中文标题'
      description: '中文描述'
```

支持的翻译字段：
- `title` - 应用标题
- `description` - 应用描述

## Categories 类别

预定义的类别选项：
- `tool` - 工具类应用
- `ai` - AI/机器学习相关应用
- `game` - 游戏类应用
- `database` - 数据库类应用
- `low-code` - 低代码平台
- `monitor` - 监控类应用
- `dev-ops` - DevOps 工具
- `blog` - 博客/内容管理系统
- `storage` - 存储类应用
- `frontend` - 前端类应用
- `backend` - 后端类应用

## 存储规范

### 重要限制

1. **⚠️ Sealos 不支持 emptyDir！** 所有需要临时存储的场景都必须转换为持久化存储
2. 存储不能单独创建 PersistentVolumeClaim，必须在 Deployment 或 StatefulSet 中使用 `volumeClaimTemplates`

### volumeClaimTemplates 命名规则

`metadata.name` 将复用 `metadata.annotations.path` 的值，并将特殊字符替换为 "vn-"：
- `/` 替换为 `vn-`
- `-` 替换为 `vn-`
- 其他特殊字符也替换为 `vn-`

示例：
- `/var/lib/headscale` → `vn-varvn-libvn-headscale`
- `/usr/src/app/upload` → `vn-usrvn-srcvn-appvn-upload`

## ConfigMap 配置规范

### 命名规则

ConfigMap 的名称必须和挂载该 ConfigMap 的应用的 `metadata.name` 值一样。

### 文件存储规则（极其重要！）

**⚠️ ConfigMap 的 data 字段中的所有键名（key）必须严格遵循 vn- 转换规则！**

转换规则：
- 将路径中的 `/` 替换为 `vn-`
- 将路径中的 `-` 替换为 `vn-`
- 将路径中的 `.` 替换为 `vn-`
- 其他特殊字符也替换为 `vn-`

示例：
- 原路径: `/etc/nginx/conf.d/default.conf`
- 转换后: `vn-etcvn-nginxvn-confvn-dvn-defaultvn-conf`

## 标签和命名规范

### app-deploy-manager 标签规则

1. `cloud.sealos.io/app-deploy-manager` 的值必须和资源的 `metadata.name` 的值保持一致
2. 每个模板的主应用的 `metadata.name` 必须是 `${{ defaults.app_name }}`
3. 其他组件的命名应该基于 `${{ defaults.app_name }}` 加上组件标识

### 容器命名规则

`containers.name` 的名称必须和 `metadata.name` 的值保持一致。

### 特殊情况：数据库资源

数据库资源使用特殊的标签 `sealos-db-provider-cr` 而不是 `cloud.sealos.io/app-deploy-manager`。

## 对象存储配置

### 环境变量设置要点

1. `object-storage-key` 是固定的 secret 名称（不包含应用名称）
2. 只有 bucket 的 secret 名称包含应用名称：`object-storage-key-${{ SEALOS_SERVICE_ACCOUNT }}-${{ defaults.app_name }}`
3. S3_ENDPOINT 和 S3_PUBLIC_DOMAIN 使用环境变量引用：`$(BACKEND_STORAGE_MINIO_EXTERNAL_ENDPOINT)`
4. S3_ENABLE_PATH_STYLE 必须设置为 "1"

## Ingress 配置规范

### 标准格式要点

1. `metadata.name` 必须是 `${{ defaults.app_name }}`
2. 必须包含 `cloud.sealos.io/app-deploy-manager-domain` 标签
3. `ssl-redirect` 默认为 `'true'`
4. 包含静态资源缓存的 configuration-snippet
5. backend service name 必须是 `${{ defaults.app_name }}`
6. 域名格式：`${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`
7. TLS secret：`${{ SEALOS_CERT_SECRET_NAME }}`

## 数据库连接配置

### PostgreSQL 环境变量

Secret 名称格式：`${{ defaults.app_name }}-pg-conn-credential`

包含的 keys：
- `endpoint`: 完整的连接端点（host:port）
- `host`: 主机名
- `password`: 密码
- `port`: 端口号
- `username`: 用户名（通常是 postgres）

### 其他数据库

- Redis: `${{ defaults.app_name }}-redis-conn-credential`
- MySQL: `${{ defaults.app_name }}-mysql-conn-credential`
- MongoDB: `${{ defaults.app_name }}-mongo-conn-credential`

### PostgreSQL 数据库初始化

如果应用需要自定义数据库，必须通过 Job 来创建。

重要规范：
- 数据库名称应该使用应用的默认值，不应该作为用户输入参数
- 数据库名称应该与应用名称相关
- Job 名称使用 `${{ defaults.app_name }}-pg-init` 格式
- 使用 `postgres:14-alpine` 镜像
- `ttlSecondsAfterFinished: 300` 确保 Job 完成后 5 分钟自动清理
- `backoffLimit: 0` 表示失败后不重试

## 应用配置规范

### 服务间通信规则

服务之间相互引用必须使用全域名（FQDN），不能直接使用服务名。

全域名格式：`<service-name>.${{ SEALOS_NAMESPACE }}.svc.cluster.local`

### 环境变量依赖顺序规则

如果一个环境变量引用了另一个环境变量，被引用的变量必须定义在引用它的变量之前。

### 必需的安全和资源管理配置

所有应用的 Deployment 或 StatefulSet 必须包含：

1. **automountServiceAccountToken**: 必须设置为 `false`
2. **revisionHistoryLimit**: 必须设置为 `1`
3. **metadata.annotations**: 必须包含：
   - `originImageName`: 原始镜像名称
   - `deploy.cloud.sealos.io/minReplicas`: 最小副本数（通常为 `'1'`）
   - `deploy.cloud.sealos.io/maxReplicas`: 最大副本数（通常为 `'1'`）

## 镜像配置规范

### 镜像拉取策略

所有容器的镜像拉取策略必须设置为 `IfNotPresent`。

这样可以：
- 减少不必要的镜像拉取，提高部署速度
- 降低对镜像仓库的压力
- 节省网络带宽

## Sealos 平台特性

### 部署特性

- **一键部署**：通过 App Launchpad 实现一键部署
- **自动扩展**：基于资源使用自动扩展
- **内置服务**：集成数据库、对象存储等
- **成本优化**：按使用付费，透明定价
- **高可用性**：基于 Kubernetes 构建，确保可靠性
- **易于管理**：通过单一仪表板管理所有服务

### 标准部署流程

1. 访问 [Sealos Cloud](https://cloud.sealos.io)
2. 点击桌面中的 "App Launchpad"
3. 在模板市场中搜索应用
4. 点击 "Deploy" 并配置必要参数
5. 等待部署完成（通常 2-3 分钟）
6. 通过提供的 URL 访问应用

### 扩展操作

1. 打开 App Launchpad
2. 选择部署的应用
3. 调整 CPU/内存资源或副本数
4. 点击 "Update" 应用更改

## 常见架构模式

### 单服务应用

适用于简单的独立应用：
- 一个主应用容器
- 可选的持久化存储
- Ingress 用于外部访问

### 多服务应用

适用于复杂的分布式应用：
- 主服务（Web UI/API）
- Worker 服务（后台任务处理）
- 数据库（PostgreSQL/MySQL/MongoDB）
- 缓存（Redis）
- 对象存储（S3-compatible）

### 微服务架构

适用于大型应用：
- 多个独立的服务组件
- 服务间使用 FQDN 通信
- 共享数据库和缓存
- 统一的 Ingress 网关

## 文档写作注意事项

### 必须包含的信息

- 应用的准确技术描述
- 清晰的架构说明
- 现实的使用场景
- 相关的外部链接（官方文档、社区资源）

### 必须避免的内容

- 营销性的夸大宣传
- 对用户知识的假设（不加解释）
- 不完整或不清晰的说明
- 损坏的或占位符链接

### Sealos 特定要求

1. 强调一键部署功能
2. 提及 Kubernetes 基础（增加可信度）
3. 突出成本优势（按需付费定价）
4. 始终使用 "App Launchpad"（不要用 "dashboard" 或 "control panel"）
5. 包含 Sealos Cloud URL：https://cloud.sealos.io
6. 提及标准部署时间：2-3 分钟

### 多服务应用的文档要点

1. 清晰列出所有服务组件
2. 解释服务间如何交互
3. 记录依赖关系
4. 包含所有自动配置的资源（数据库、Redis、对象存储等）
