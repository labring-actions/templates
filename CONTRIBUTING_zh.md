# 贡献指南

感谢你对 Sealos 模板仓库的贡献兴趣！本文档提供了贡献模板、文档或改进的指南和说明。

## 🎯 贡献类型

我们欢迎以下方面的贡献：

- **新应用模板** - 添加对新应用的支持
- **模板改进** - 优化现有模板（更好的默认值、资源配置等）
- **文档** - 改进指南、修复错别字、添加示例
- **Bug 修复** - 修复模板或文档中的问题
- **翻译** - 改进或添加文档的翻译

## 📝 添加新模板

### 前置要求

1. 应用必须积极维护
2. Docker 镜像必须公开可用（Docker Hub、GHCR 等）
3. 应用应该是生产就绪的
4. 你已在 Sealos 上测试过模板

### 分步指南

#### 1. 准备模板

```bash
# Fork 并克隆本仓库
git clone https://github.com/your-username/templates.git
cd templates

# 创建新分支
git checkout -b add-my-awesome-app

# 复制参考模板
cp template.yaml template/my-awesome-app.yaml
```

#### 2. 自定义模板

编辑 `template/my-awesome-app.yaml`：

```yaml
spec:
  title: "我的应用"                         # 显示名称
  url: "https://myapp.example.com"         # 官方网站
  gitRepo: "https://github.com/myuser/my-awesome-app"  # 源代码
  author: "你的名字"                        # 你的名字
  description: "简短描述这个应用是做什么的"
  readme: "https://raw.githubusercontent.com/.../README.md"  # 可选
  icon: "https://..."                       # 应用图标 URL（推荐尺寸：96x96）
```

#### 3. 配置应用

- **Docker 镜像**：使用特定版本标签（如 `v1.2.3`），避免使用 `latest`
- **环境变量**：设置必要的 env vars，记录可选的 env vars
- **资源限制**：根据实际需求调整 CPU/内存
- **持久化存储**：如需要，配置数据持久化
- **端口**：仅暴露必要的端口（Web 应用通常是 80）

#### 4. 测试模板

1. 将模板上传到你的 fork
2. 在 Sealos 上部署以验证其工作正常
3. 测试所有用户输入和配置
4. 验证数据持久化（如适用）
5. 检查应用是否可通过 Ingress 访问

#### 5. 提交 PR

```bash
git add template/my-awesome-app.yaml
git commit -m "Add template for My Awesome App"
git push origin add-my-awesome-app
```

然后打开 Pull Request，包含：
- 清晰的标题：`Add template for My Awesome App`
- 描述：包含应用信息、测试结果和任何说明

### 模板规范

#### 命名约定
- **文件名**：小写、连字符分隔（如 `my-awesome-app.yaml`）
- **defaults 中的应用名**：描述性前缀加随机后缀（如 `myawesomeapp-${{ random(8) }}`）

#### 必填字段
```yaml
spec:
  title: ""           # 应用显示名称
  url: ""             # 官方网站
  gitRepo: ""         # 源仓库
  author: ""          # 维护者
  description: ""     # 简短描述（1-2 句话）
  icon: ""            # 应用图标 URL
```

#### 最佳实践

- **特定镜像版本**：使用 `v1.2.3` 等标签，不要用 `latest`
- **合理的默认值**：为所有输入设置合理的默认值
- **清晰的描述**：解释每个输入的作用
- **资源效率**：不要过度分配 CPU/内存
- **安全性**：不要暴露不必要的端口或服务
- **文档**：在 `readme` 字段中链接到官方文档

#### 模板结构示例

```yaml
---
apiVersion: app.sealos.io/v1
kind: Template
metadata:
  name: ${{ defaults.app_name }}
spec:
  title: "示例应用"
  url: "https://example.com"
  gitRepo: "https://github.com/user/example-app"
  author: "你的名字"
  description: "一个示例应用模板"
  readme: "https://raw.githubusercontent.com/.../README.md"
  icon: "https://example.com/icon.png"
  templateType: inline
  
  defaults:
    app_name:
      type: string
      value: exampleapp-${{ random(8) }}
    app_host:
      type: string
      value: ${{ random(8) }}
  
  inputs:
    admin_password:
      description: "管理员账户密码"
      type: string
      required: true
    api_key:
      description: "外部服务的 API 密钥"
      type: string
      required: false
      default: ""

---
# Kubernetes 资源（StatefulSet、Service、Ingress）
apiVersion: apps/v1
kind: StatefulSet
# ... 其余配置
```

## 🐛 Bug 修复和改进

### 报告问题

报告 Bug 时，请包含：
- 模板名称
- 问题描述
- 重现步骤
- 预期行为 vs 实际行为
- 如适用，提供截图/日志

### 提交修复

1. 创建 issue 讨论修复方案（如果不是微不足道的修复）
2. 为修复创建分支：`git checkout -b fix-template-name-issue`
3. 进行更改并彻底测试
4. 提交 PR 并清晰描述更改

## 📖 文档贡献

### 改进文档

- 修复错别字和语法错误
- 澄清令人困惑的部分
- 添加示例或用例
- 改进结构和格式
- 添加图表或可视化辅助

### 添加示例

如果你有复杂的用例，可以从中受益：
1. 在 `docs/` 目录中创建新文件
2. 清晰记录场景
3. 提供分步说明
4. 从主 README 链接到它

## 🤝 行为准则

- 尊重和建设性
- 以社区的最佳利益为重点
- 对其他社区成员表现出同理心
- 优雅地接受反馈

## 📋 Pull Request 检查清单

提交 PR 前，请确保：

- [ ] 模板已在 Sealos 上测试
- [ ] 所有必填字段已填写
- [ ] Docker 镜像使用特定版本标签（不是 `latest`）
- [ ] 资源限制合理
- [ ] 文档清晰准确
- [ ] PR 描述解释了更改
- [ ] 不包含无关更改

## 🎉 认可

贡献者将在以下地方获得认可：
- 仓库的贡献者列表
- 发布说明（针对重要贡献）
- 可选：模板元数据中的作者署名

## 📧 获取帮助

- **讨论区**：[GitHub Discussions](https://github.com/labring-actions/templates/discussions)
- **问题反馈**：[GitHub Issues](https://github.com/labring-actions/templates/issues)
- **Discord**：[Sealos Discord 服务器](https://discord.gg/sealos)

## 📄 许可证

通过贡献，你同意你的贡献将按照仓库的相同许可证进行许可。

---

感谢你的贡献！🙏
