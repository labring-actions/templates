# 在 Sealos 上部署和托管 MiroFish

MiroFish 是开源群体智能仿真引擎，可创建数字世界、运行多智能体预测并生成场景报告。此模板在 Sealos Cloud 上部署 MiroFish 前端和后端，并配置持久化上传存储与统一 HTTPS 应用 URL。

![MiroFish 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/mirofish/website-screenshot.webp)

## 关于托管 MiroFish

MiroFish 作为双服务 Web 应用运行。前端提供浏览器工作台，后端处理文件上传、图谱构建、仿真状态、报告生成和 OpenAI 兼容 LLM 调用。

Sealos 模板将根路径暴露给前端，并把同一公开域名下的 `/api` 路由到后端。持久化存储会在 `/app/backend/uploads` 下保存上传材料、图谱数据、仿真文件和报告。

## 常见使用场景

- **场景预测**：上传报告或源材料，模拟未来发展。
- **舆情分析**：构建社会图谱，并运行基于智能体的讨论或反应仿真。
- **创意世界构建**：为故事、研究或推演规划生成可交互数字世界。
- **决策预演**：在多智能体沙盒中测试政策、传播或产品假设。

## MiroFish 托管依赖

此 Sealos 模板包含 MiroFish 前端、后端 API、持久化上传存储、Service、HTTPS Ingress 路由和 Sealos App 入口。

### 部署依赖

- [GitHub 仓库](https://github.com/666ghj/MiroFish) - 源码和容器工作流
- [在线演示](https://666ghj.github.io/mirofish-demo/) - 公开项目 Demo
- [Zep Cloud](https://www.getzep.com/) - MiroFish 使用的图谱记忆依赖
- [OpenAI API](https://platform.openai.com/docs) - LLM Provider 的兼容 API 契约

### 实现细节

**架构组件：**

此模板部署以下服务：

- **MiroFish 前端**：运行在 3000 端口的浏览器 UI。
- **MiroFish 后端**：运行在 5001 端口的 Flask API，处理上传、图谱、仿真和报告流程。
- **持久化上传存储**：保存上传文件、仿真、日志、报告和图谱数据。
- **Sealos Ingress**：通过 HTTPS 将 `/` 路由到前端，将 `/api` 路由到后端。

**配置：**

部署表单需要 OpenAI 兼容 LLM API Key、API Base URL、模型名和 Zep API Key。后端启动仿真和报告流程前需要这些值。

**许可证信息：**

MiroFish 使用 AGPL-3.0。此 Sealos 模板遵循 Sealos templates 仓库许可证。

## 为什么在 Sealos 上部署 MiroFish？

Sealos 是基于 Kubernetes 的 AI 辅助云操作系统，统一部署、存储、网络和日常运维。部署 MiroFish 到 Sealos 后，你可以获得：

- **一键部署**：从应用商店同时启动前端和后端。
- **统一 HTTPS URL**：用一个公开域名承载 UI 和 API 流量。
- **持久化工作区数据**：上传材料和生成报告可在重启后保留。
- **便捷 Provider 配置**：在部署表单中设置 LLM 和 Zep 凭据。
- **Canvas 运维**：通过 Canvas、AI 对话和资源卡调优资源、检查日志并更新运行设置。
- **按量资源使用**：从适中资源起步，并在仿真变重时扩容。

## 部署指南

1. 打开 [MiroFish 模板](https://sealos.io/products/app-store/mirofish)，点击 **Deploy Now**。
2. 在弹窗中配置必填参数：
   - **LLM API Key**
   - **LLM Base URL**
   - **LLM Model Name**
   - **Zep API Key**
3. 等待部署完成，通常需要 2-3 分钟。部署后会跳转到 Canvas。后续变更可以在对话框中描述需求让 AI 应用更新，也可以点击资源卡修改设置。
4. 通过提供的 URL 访问 MiroFish。
5. 上传种子材料，并按工作流面板构建图谱、准备仿真、运行仿真和生成报告。

## 登录和注册

此模板中的 MiroFish 不需要单独的 Web 账号。访问由 Sealos App URL 和部署时配置的 Provider 凭据控制。

第一个有效工作流是配置验证：打开应用、上传源材料并开始图谱生成。仿真和报告步骤需要有效的 LLM 与 Zep 凭据。

## 配置

部署后可以通过以下方式配置 MiroFish：

- **部署输入**：从模板参数更新 LLM 和 Zep 凭据。
- **Canvas 资源卡**：调整 CPU、内存、存储或环境值。
- **AI 对话**：描述变更并让 Sealos 更新资源。

## 扩容

扩容 MiroFish：

1. 打开部署对应的 Canvas。
2. 点击前端 Deployment 或后端 StatefulSet 资源卡。
3. 为更重的上传、图谱构建或长时间仿真增加 CPU 或内存。
4. 应用变更并观察日志。

## 故障排查

### 后端无法启动

- 原因：LLM 或 Zep 凭据缺失，或仍是占位值。
- 解决：用有效 API Key 更新部署输入，然后重启后端 StatefulSet。

### UI 可加载但仿真操作失败

- 原因：Provider 凭据、模型名或 API Base URL 可能无效。
- 解决：在 Canvas 中检查后端日志并核对 Provider 设置。

### 重启后上传或报告消失

- 原因：后端持久化卷可能已被删除。
- 解决：在 Canvas 中确认 `/app/backend/uploads` PVC 仍存在。

## 其他资源

- [MiroFish GitHub](https://github.com/666ghj/MiroFish)
- [MiroFish Demo](https://666ghj.github.io/mirofish-demo/)
- [Zep Cloud](https://www.getzep.com/)

## License

此 Sealos 模板遵循 Sealos templates 仓库许可证。MiroFish 本身使用 AGPL-3.0。
