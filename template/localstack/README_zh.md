# 在 Sealos 上部署和托管 LocalStack

LocalStack 是面向开发与测试场景的 AWS 兼容云服务模拟器。此模板会通过自动生成的 Sealos HTTPS 端点部署最后一个传统 Community 版本 LocalStack 4.14.0。

![LocalStack 官网](website-screenshot.webp)

## LocalStack 托管说明

LocalStack 提供兼容 AWS 的 API，涵盖 S3、SQS、SNS、DynamoDB、CloudFormation 和 API Gateway 等服务。应用可以把 AWS SDK 或 CLI 指向自动生成的端点，在隔离环境中验证云端工作流。

此模板会创建一个 LocalStack Deployment、一个 ClusterIP Service 和一个 TLS Ingress。端口 `4566` 承载公网网关，端口 `4510-4559` 为集群客户端保留官方定义的外部服务端口范围。

Community 4.14.0 在每次 Pod 替换后使用全新的模拟器状态。测试数据可以通过脚本、Terraform、AWS CDK 或 CloudFormation 重新创建。LocalStack Base 及以上计划通过账户版镜像与认证令牌提供本地状态持久化能力。

Lambda 执行等依赖容器运行时的服务需要 Docker 或 Kubernetes executor。此模板支持在 LocalStack 进程内运行的网关型服务。

## 常见使用场景

- **AWS SDK 开发**：通过隔离的 AWS 兼容端点测试应用集成。
- **基础设施验证**：在连接 AWS 账户前验证 Terraform、AWS CDK 和 CloudFormation 工作流。
- **集成测试**：创建可随时重建的 S3、SQS、SNS 和 DynamoDB 测试环境。
- **开发沙箱**：为团队提供带固定 HTTPS 入口的共享云服务模拟器。

## 托管 LocalStack 所需依赖

Sealos 模板已经包含 LocalStack Community 运行时、集群内网络和公网 HTTPS 网关。

### 部署依赖

- [LocalStack 文档](https://docs.localstack.cloud/) - 产品与配置文档
- [LocalStack 源码仓库](https://github.com/localstack/localstack) - 源码与版本发布
- [官方 Helm Chart](https://github.com/localstack/helm-charts/tree/main/charts/localstack) - Kubernetes 运行时参考
- [LocalStack 计划](https://docs.localstack.cloud/aws/licensing/) - 当前服务与功能权益

### 实现细节

**架构组件：**

- **LocalStack Deployment**：以单副本和 Recreate 更新策略运行 `localstack/localstack:4.14.0`。
- **临时工作目录**：创建可写的 `/tmp/localstack-user`，供非 root 进程保存临时服务状态。
- **Service**：在集群内开放网关端口 `4566` 和外部服务端口 `4510-4559`。
- **Ingress**：通过自动生成的 HTTPS 域名发布网关。
- **App 链接**：打开 `/_localstack/health`，直接显示运行版本、Community 类型和服务状态。

**配置：**

- `LOCALSTACK_HOST` 与 `USE_SSL=1` 会让服务返回的 URL 对齐 Sealos HTTPS 入口。
- `SQS_ENDPOINT_STRATEGY=path` 会让队列 URL 继续使用自动生成的域名和公网 TLS 路由。
- `TEMP=/tmp/localstack-user` 会把临时服务状态放入用户 `1000` 拥有的目录。
- `DNS_ADDRESS=0` 会使用集群 DNS，并让非 root 运行环境保持在非特权端口。
- 启动、就绪与存活检查均使用官方 `/_localstack/health` 路径。
- Pod 以 LocalStack 用户 `1000` 运行，并启用 RuntimeDefault seccomp 配置与 Linux capability 全量丢弃策略。
- 经过实测的起始规格为 `100m` CPU 和 `256Mi` 内存。

**版本与许可证信息：**

LocalStack 4.14.0 是最后一个传统 Community 版本，使用 Apache License 2.0。账户版 LocalStack 镜像为当前商业工作流提供持续维护版本与相应计划。

## 为什么在 Sealos 上部署 LocalStack？

Sealos 是基于 Kubernetes 的云操作系统，可通过可视化 Canvas 管理应用资源。在 Sealos 上部署 LocalStack 可以获得：

- **一键部署**：通过一个模板完成运行时、网络和 HTTPS 入口的创建。
- **托管 HTTPS**：使用平台生成的公网域名和 TLS 证书。
- **受限运行环境**：以非 root 用户和紧凑安全上下文启动 Community 镜像。
- **Canvas 运维**：通过资源卡片或 AI 对话调整配置并检查工作负载。
- **紧凑资源规格**：从实测通过的 `100m` CPU 和 `256Mi` 内存配置起步。

## 部署指南

1. 打开 [LocalStack 模板](https://sealos.io/products/app-store/localstack)，点击 **Deploy Now**。
2. 检查自动生成的应用名称和域名，然后开始部署。
3. 等待部署完成，通常需要 2-3 分钟。随后 Sealos 会打开新实例的 Canvas。
4. 从 App 资源卡片打开 LocalStack。健康响应会显示 Community 类型和运行版本。

自动生成的端点可以通过公网访问。请使用合成测试数据，并在每次测试会话结束后删除实例。

## 连接 AWS 客户端

设置标准 AWS 开发凭据，并让 AWS CLI 使用自动生成的 HTTPS 端点：

```bash
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export LOCALSTACK_URL=https://<generated-localstack-host>

aws --endpoint-url "$LOCALSTACK_URL" s3api create-bucket --bucket sealos-demo
aws --endpoint-url "$LOCALSTACK_URL" s3api list-buckets
aws --endpoint-url "$LOCALSTACK_URL" sqs create-queue --queue-name sealos-demo
aws --endpoint-url "$LOCALSTACK_URL" sqs list-queues
```

LocalStack Community 接受兼容 AWS 的请求凭据。`test` 这类开发值适合隔离测试工作负载。

## 状态生命周期

每次 Pod 替换都会创建全新的 Community 模拟器状态。建议把测试数据创建流程保存在版本控制内的初始化脚本或基础设施定义中，让每个测试环境保持一致。

LocalStack Base 及以上计划提供本地状态持久化能力。这些计划使用账户版镜像、认证令牌和挂载的 LocalStack 数据卷。

## 配置

部署完成后，可以通过 Sealos Canvas 调整 LocalStack 工作负载：

- **AI 对话**：描述环境变量或资源调整需求，由 Sealos 执行变更。
- **资源卡片**：直接打开 Deployment、Service 或 Ingress 设置。
- **服务选择**：为固定服务清单添加 `SERVICES` 和 `EAGER_SERVICE_LOADING=1`，改善启动表现。
- **容量调整**：大型集成测试可以通过 Deployment 资源卡片提高 CPU 或内存规格。

## 故障排查

### 客户端无法访问端点

使用 App 资源中显示的完整 HTTPS 地址，并通过客户端的端点参数传入它的源地址。AWS CLI 使用 `--endpoint-url`，各语言 SDK 也提供对应的端点设置。

### SQS 返回路径形式的队列 URL

路径形式会让队列 URL 继续使用自动生成的 Sealos 域名。SQS 操作可以直接使用返回的 `QueueUrl`。

### 某项服务需要容器运行时

Lambda 容器执行等运行时型功能需要 Docker 或具备相应权限的 Kubernetes executor。S3、SQS、SNS 和 DynamoDB 等网关型服务适合默认模板配置。

### 大型测试套件中的请求速度变慢

通过 Deployment 资源卡片提高 CPU 和内存规格。默认配置面向紧凑型开发工作流。

### 获取帮助

- [LocalStack 常见问题](https://docs.localstack.cloud/aws/getting-started/faq/)
- [LocalStack GitHub Issues](https://github.com/localstack/localstack/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [LocalStack 配置参考](https://docs.localstack.cloud/aws/customization/configuration-options/)
- [LocalStack 持久化](https://docs.localstack.cloud/aws/developer-tools/snapshots/persistence/)
- [AWS CLI 集成](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)

## 许可证

此 Sealos 模板遵循模板仓库的许可证。LocalStack Community 使用 [Apache License 2.0](https://github.com/localstack/localstack/blob/main/LICENSE.txt)。
