# FastGPT

这个模板基于上游 `deploy/docker/cn/docker-compose.pg.yml` 的最新拓扑进行转换，并映射为 Sealos 原生资源。

它会部署：

- FastGPT 主应用
- FastGPT Plugin
- FastGPT Code Sandbox
- FastGPT MCP Server
- AIProxy
- MongoDB
- FastGPT 向量检索用 PostgreSQL
- AIProxy 用 PostgreSQL
- Redis
- Sealos 对象存储公共桶和私有桶

## 使用说明

1. 部署完成后请等待几分钟，让数据库集群和 AIProxy 的数据库初始化任务执行完成。
2. 登录用户名是 `root`，密码为部署时填写的 `root_password`。
3. 模型能力仍需要在部署后继续配置。AIProxy 会以内网服务方式部署，并通过 FastGPT 内置集成来调用。
4. MCP 的公网地址已经预写入 `config.json`。
5. Agent sandbox 默认不开启，因为上游 Docker 方案依赖 Docker Socket 相关服务，不能直接照搬到 Sealos。如果你已经有托管的沙盒服务，可在部署时填写 `agent_sandbox_baseurl` 和 `agent_sandbox_token`。
6. Ingress 注解遵循当前模板规范，默认上传上限是 32 MB。如果你需要更大的上传体积，请在部署后调整 ingress 的 `nginx.ingress.kubernetes.io/proxy-body-size`。

## 对象存储

这个模板使用 Sealos 对象存储来替代上游 compose 中内置的 MinIO。公共桶和私有桶会自动创建，并自动注入到 FastGPT 与 FastGPT Plugin 中。

## 数据库

FastGPT 使用的 PostgreSQL 运行在 Sealos Database 上，对应上游 `pgvector` 部署路径。
