# 在 Sealos 上部署和托管 FeatBit Standard

FeatBit Standard 是一个开源的功能开关与实验平台，适合渐进式发布场景。此模板会在 Sealos Cloud 上部署一套多服务 FeatBit Standard 应用，包括 PostgreSQL、Redis、公共 UI、API 和评估服务入口。

![FeatBit Standard 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/featbit-standard/website-screenshot.webp)

## 关于 FeatBit Standard 托管

FeatBit 通过把“部署”和“发布”解耦，帮助团队更安全地上线功能。开发者可以创建功能开关，按用户或分组定向发布，控制灰度范围，并在不重新部署应用的情况下评估变更效果。

此 Sealos 模板以 Standard Edition 形态运行 FeatBit，包含四个应用服务：Web UI、API Server、Data Analytics Server 和 Evaluation Server。Sealos 还会自动创建 PostgreSQL 用于存储 FeatBit 数据，并创建 Redis 用于消息、缓存和运行时协同。

模板会为 UI、API 和评估服务自动配置公网 HTTPS 入口。数据库凭据与服务发现由 Sealos 托管的 Kubernetes 资源自动注入，因此无需手动准备基础设施即可部署完整服务栈。

## 常见使用场景

- **功能开关管理**：逐步发布新功能，快速关闭高风险变更，并让发布状态独立于代码部署。
- **渐进式交付**：先面向指定环境、用户或分组开放功能，再逐步扩大范围。
- **产品实验**：运行受控实验，对比不同用户群体下的功能表现。
- **快速熔断开关**：为高风险功能、外部集成或后端行为增加可操作的开关控制。
- **研发平台建设**：为产品和工程团队提供统一的功能管理平台。

## FeatBit Standard 托管依赖

此 Sealos 模板包含运行所需的全部依赖：FeatBit UI、API Server、Data Analytics Server、Evaluation Server、PostgreSQL 16.4、Redis 7.2、Kubernetes Service、Ingress 资源，以及用于初始化 FeatBit 数据库结构的 Job。

### 部署依赖

- [FeatBit 官方网站](https://www.featbit.co/) - 产品介绍与功能信息
- [FeatBit 文档](https://docs.featbit.co/) - 官方使用与管理文档
- [FeatBit GitHub 仓库](https://github.com/featbit/featbit) - 源码、版本发布与问题跟踪
- [Sealos 应用商店](https://sealos.run/products/app-store/featbit-standard) - 一键部署入口

### 实现细节

**架构组件：**

此模板会部署以下服务：

- **UI Service**：托管 FeatBit Web 控制台，用于管理功能开关、环境、定向规则和发布配置。
- **API Server**：提供 UI 和集成系统使用的后端 API。
- **Data Analytics Server**：处理 FeatBit 所需的分析与运行数据。
- **Evaluation Server**：为 SDK 和运行时访问提供功能评估服务。
- **PostgreSQL**：存储应用数据、配置、用户、环境、功能开关和数据库结构记录。
- **Redis**：为 FeatBit 服务提供缓存、消息和协同能力。

**配置：**

模板默认暴露三个公网入口：UI、API Server 和 Evaluation Server。部署时，UI 会自动写入生成后的 API 与评估服务 URL。

PostgreSQL 和 Redis 会作为托管数据库集群创建。应用服务通过 Sealos 托管的 Secret 获取数据库 host、port、username 和 password，内部服务则通过 Kubernetes 服务发现进行通信。

应用容器已调优到此模板验证过的最小 Sealos 资源档位：UI、API 和评估服务使用 `100m` CPU 与 `128Mi` 内存限制，Data Analytics Server 使用 `100m` CPU 与 `512Mi` 内存限制。PostgreSQL 和 Redis 使用 Sealos 数据库模板规则要求的数据库资源配置。

**许可证信息：**

FeatBit 是开源项目。请查看 [FeatBit 仓库](https://github.com/featbit/featbit) 获取当前应用许可证与组件声明。

## 为什么在 Sealos 上部署 FeatBit Standard？

Sealos 是基于 Kubernetes 构建的 AI 云操作系统，覆盖从云端开发、应用部署到生产运维的完整生命周期。它适合需要托管网络、存储和运维能力的 SaaS 平台、开发者工具和多服务应用。将 FeatBit Standard 部署到 Sealos，你可以获得：

- **一键部署**：直接从应用商店部署完整 FeatBit 服务栈，无需手写 Kubernetes YAML。
- **托管数据库**：PostgreSQL 和 Redis 会随应用一起创建，并通过托管 Secret 自动连接。
- **即时公网访问**：UI、API 和评估服务会自动获得公网 HTTPS 入口。
- **资源高效**：模板使用经过验证的 Sealos 资源档位，在保持服务可运行的同时帮助控制成本。
- **易于自定义**：部署后可在 Canvas 中调整环境变量、资源限制或副本数。
- **AI 辅助运维**：在 Sealos AI 对话框描述想要的变更，或打开资源卡片精确编辑指定工作负载。
- **Kubernetes 底座**：无需管理集群细节，也能在 Kubernetes 支撑的基础设施上运行 FeatBit。

在 Sealos 上部署 FeatBit Standard，把精力放在发布管理上，而不是基础设施搭建上。

## 部署指南

1. 打开 [FeatBit Standard 模板](https://sealos.run/products/app-store/featbit-standard)，点击 **Deploy Now**。
2. 在弹出的配置窗口中填写参数。标准部署保留默认生成的名称和域名即可。
3. 等待部署完成，通常需要 2-3 分钟。部署完成后，你会被重定向到 Canvas。后续如需修改，可以在对话框中描述需求让 AI 执行变更，也可以点击对应资源卡片调整配置。
4. 通过生成的 URL 访问应用：
   - **FeatBit UI**：打开生成的 UI URL，进入 FeatBit 控制台。
   - **API Endpoint**：使用生成的 API URL 进行后端或集成访问。
   - **Evaluation Endpoint**：使用生成的评估服务 URL 处理 SDK 或运行时评估流量。

## 配置

部署完成后，你可以通过以下方式配置 FeatBit Standard：

- **AI 对话框**：描述需要的变更，例如资源调整或环境变量更新，让 AI 帮你应用。
- **资源卡片**：打开 UI、API Server、Data Analytics Server、Evaluation Server、PostgreSQL 或 Redis 资源卡片，查看并修改配置。
- **FeatBit 控制台**：在 Web UI 中管理功能开关、环境、用户、分组和发布规则。
- **公网入口**：配置 SDK 或集成时，使用生成的 API 和评估服务 URL。

## 扩缩容

如需扩缩容 FeatBit Standard：

1. 打开当前部署的 Canvas。
2. 点击相关 Deployment 资源卡片，例如 API Server、Evaluation Server 或 UI。
3. 根据访问量和评估流量调整 CPU、内存或副本数。
4. 在对话框中应用变更，并观察工作负载状态。

如果需要调整数据库相关能力，请打开 PostgreSQL 或 Redis 资源卡片，查看可用的数据库选项后再应用变更。

## 故障排查

### 常见问题

**UI 可以打开，但 API 请求失败**
- 原因：API 入口或生成的 API 域名可能与实际部署的公网 URL 不一致。
- 解决方案：在 Canvas 中打开 UI 和 API 资源卡片，确认 UI 环境变量指向生成后的 API URL。

**SDK 评估请求失败**
- 原因：SDK 可能配置成了 UI URL，而不是评估服务入口。
- 解决方案：SDK 或运行时评估流量应使用生成的 Evaluation URL。

**服务一直等待数据库初始化**
- 原因：FeatBit 服务依赖初始化 Job 创建的 PostgreSQL 数据库结构。
- 解决方案：在 Canvas 中检查 PostgreSQL 集群和初始化 Job 状态，必要时重启依赖服务。

### 获取帮助

- [FeatBit 文档](https://docs.featbit.co/)
- [FeatBit GitHub Issues](https://github.com/featbit/featbit/issues)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 更多资源

- [FeatBit 官网](https://www.featbit.co/)
- [FeatBit 文档](https://docs.featbit.co/)
- [FeatBit GitHub 仓库](https://github.com/featbit/featbit)
- [Sealos](https://sealos.run/)

## 许可证

此 Sealos 模板遵循模板仓库使用的许可证。FeatBit 本身由 FeatBit 项目授权，请查看 [FeatBit GitHub 仓库](https://github.com/featbit/featbit) 获取当前许可证详情。
