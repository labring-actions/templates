# Sealos 模板仓库

[English](README.md) | [在线使用](https://os.sealos.io)

通过本仓库的模板可以轻松在 Sealos 上运行各种应用，无需关心应用之间的依赖关系，只需一键轻松部署。

![](docs/images/homepage_zh.png)

## 🚀 快速开始

### 3 步部署你的第一个应用

1. **浏览可用模板**，找到你喜欢的应用
2. **点击模板文档中的 "Deploy on Sealos" 按钮**
3. **配置并部署** - 只需填写必要的参数

模板编写快速入口:
- 基于 [template.yaml](template.yaml)（或 Create Template(TODO) 按钮）开始。
- 内置变量/函数使用类似 `GitHub Actions` 的语法，详见 [example.md](example.md)。
- FastGPT 完整示例见 [example.md](example.md)；数据库 Cluster YAML 示例（MongoDB/PostgreSQL/MySQL/Redis/Kafka/Milvus/ClickHouse）见 [example_zh.md](example_zh.md)。

就这么简单！你的应用几分钟内就能运行起来。

### 热门模板

| 模板 | 描述 | 部署 |
|------|------|------|
| FastGPT | 使用 AI 构建你自己的知识库 | [![Deploy](https://sealos.io/Deploy-on-Sealos.svg)](https://sealos.io/products/app-store/fastgpt) |
| ChatGPT-Next-Web | 搭配你自己的 API Key 的 ChatGPT Web 界面 | [![Deploy](https://sealos.io/Deploy-on-Sealos.svg)](https://sealos.io/products/app-store/chatgpt-next-web) |
| Code-Server | 浏览器中的 VS Code | [![Deploy](https://sealos.io/Deploy-on-Sealos.svg)](https://sealos.io/products/app-store/code-server) |
| Cloudreve | 云存储系统 | [![Deploy](https://sealos.io/Deploy-on-Sealos.svg)](https://sealos.io/products/app-store/cloudreve) |
| Appsmith | 低代码应用构建平台 | [![Deploy](https://sealos.io/Deploy-on-Sealos.svg)](https://sealos.io/products/app-store/appsmith) |

[查看所有模板 →](template/)

## 📚 文档

- **[如何创建模板](#如何创建模板)** - 创建你自己的应用模板
- **[模板使用教程](https://os.sealos.io)** - 模板使用指南
- **[example.md](example.md)** - 详细的模板开发教程
- **[template.yaml](template.yaml)** - 模板参考文件

## 🛠️ 如何创建模板

你可以通过现有的模板文件或 UI（TODO 按钮）来创建应用模板。

### 1. 从模板参考文件开始

复制 [template.yaml](template.yaml) 作为起点：

```bash
cp template.yaml my-app-template.yaml
```

### 2. 理解模板结构

模板文件主要分为两部分：

- **元数据 CR**：模板信息、默认值和用户输入
- **Kubernetes 资源**：StatefulSet、Service、Ingress 等

详细说明请查看 [example.md](example.md)。

### 3. 使用变量和函数

系统提供了内置的环境变量和函数。使用类似 `GitHub Actions` 的语法：

```yaml
# 系统内置变量
${{ SEALOS_NAMESPACE }}

# 生成随机字符串的函数
${{ random(8) }}

# 用户输入变量
${{ inputs.your_parameter }}
```

完整参考请查看 [内置系统变量和函数](example.md#built-in-system-variables-and-functions)。

### 4. 示例：FastGPT 模板

[FastGPT](example.md) 示例展示了如何创建完整的模板，包括：
- 默认应用名称和主机名
- 用户可配置的输入（API 密钥、密码、数据库类型）
- 多个 Kubernetes 资源（数据库、应用、Ingress）

## 🤖 使用 Agent Skill 转换应用

本仓库内置了 `docker-to-sealos` skill（`.codex/skills/docker-to-sealos/SKILL.md`），可在 **Codex**、**Claude Code**、**OpenCode**、**OpenClaw** 中直接调用，把 GitHub 仓库转换为 Sealos 模板。

### 跨 Agent 最简 Prompt

在 Agent 中直接使用下面这段提示词：

```text
使用 `docker-to-sealos` skill，将这个 GitHub 仓库转换为 Sealos 模板：
https://github.com/<owner>/<repo>
```

### 调用说明

- 将 URL 替换为你的目标仓库地址。
- 如果 Agent 支持显式 skill 调用，可直接写 `$docker-to-sealos`。
- 如果 Agent 走自动路由，在提示词里提到 `docker-to-sealos` 通常就够用。
- 这套写法可直接复用在 Codex、Claude Code、OpenCode、OpenClaw。

## 🔗 使用 "Deploy on Sealos" 按钮

你可以在项目的 README 中添加 "Deploy on Sealos" 按钮：

### Markdown

```markdown
[![](https://sealos.io/Deploy-on-Sealos.svg)](https://sealos.io/products/app-store/your-app-name)
```

### HTML

```html
<a href="https://sealos.io/products/app-store/your-app-name">
  <img src="https://sealos.io/Deploy-on-Sealos.svg" alt="Deploy on Sealos"/>
</a>
```

将 `your-app-name` 替换为你的模板中 Template CR 的 `metadata.name`。

## 🤝 贡献指南

欢迎贡献！请按照以下步骤：

1. **Fork** 本仓库
2. **创建分支** 用于你的模板或改进
3. **遵循模板结构** - 参考 [template.yaml](template.yaml)
4. **在提交前测试** 你的模板
5. **提交 Pull Request** 并清晰描述改动

### 模板规范

- **命名**：使用小写、连字符分隔的名称（如 `my-awesome-app`）
- **描述**：编写清晰、简洁的描述
- **文档**：如需要，包含应用特定的使用说明
- **默认值**：为所有输入提供合理的默认值
- **资源**：设置合理的资源限制（CPU/内存）

## 📖 相关资源

- [Sealos 官方文档](https://sealos.io/docs/Intro)
- [Sealos 应用商店](https://sealos.io/products/app-store)
- [问题反馈](https://github.com/labring-actions/templates/issues) - 报告问题或请求新功能
- [讨论区](https://github.com/labring-actions/templates/discussions) - 提问和分享想法

## 📄 许可证

本仓库遵循与 Sealos 相同的许可证。详见 [LICENSE](LICENSE)。
