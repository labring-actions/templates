# 在 Sealos 上部署和托管 Stirling-PDF

Stirling-PDF 是一个自托管 PDF 工具箱，支持合并、拆分、转换、OCR、压缩、涂黑和其他文档处理流程。此模板会在 Sealos Cloud 上部署 Stirling-PDF，并提供持久化存储、可选 PostgreSQL 和 HTTPS 访问入口。

![Stirling-PDF 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/s-pdf/website-screenshot.webp)

## 关于托管 Stirling-PDF

Stirling-PDF 作为 Web 应用运行，监听 `8080` 端口。Sealos 模板会创建 StatefulSet、用于 OCR 数据和工作目录的持久卷、Service、Ingress 和 Sealos App 入口。

默认部署会直接打开 PDF 工具箱。需要登录时，将 `DOCKER_ENABLE_SECURITY` 设置为 `true`，并将 `SECURITY_ENABLELOGIN` 设置为 `true`。全新数据卷首次登录时，使用 `SECURITY_INITIALLOGIN_USERNAME` 和 `SECURITY_INITIALLOGIN_PASSWORD`。

## 常见使用场景

- **PDF 操作入口**：在浏览器中合并、拆分、旋转、压缩、加水印和涂黑 PDF。
- **文档转换**：启用高级工具后转换 PDF、Office、图片和电子书格式。
- **OCR 流程**：使用语言包处理扫描件和多语言文本提取。
- **团队内部工具**：运行带密码登录和持久化配置的私有文档工具箱。

## 部署指南

1. 打开 [Stirling-PDF 模板](https://sealos.io/products/app-store/s-pdf)，点击 **Deploy Now**。
2. 个人轻量使用保持 `use_postgresql=false`；生产或团队场景设置 `use_postgresql=true`，使用独立 PostgreSQL 数据库。
3. 启用登录时配置：
   - `DISABLE_ADDITIONAL_FEATURES=false`
   - `DOCKER_ENABLE_SECURITY=true`
   - `SECURITY_ENABLELOGIN=true`
   - `SECURITY_INITIALLOGIN_USERNAME`：初始管理员用户名
   - `SECURITY_INITIALLOGIN_PASSWORD`：初始管理员密码
4. 根据文档工作负载选择 `SYSTEM_DEFAULTLOCALE`、`LANGS` 和高级转换选项。
5. 等待 StatefulSet 和可选 PostgreSQL 集群就绪，然后从 Sealos Canvas 打开生成的 HTTPS 地址。

## 配置说明

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `use_postgresql` | 创建并使用 PostgreSQL 数据库，适合生产工作负载。 | `否` | `false` |
| `DOCKER_ENABLE_SECURITY` | 启用 Stirling-PDF 登录所需的安全组件。 | `否` | `false` |
| `DISABLE_ADDITIONAL_FEATURES` | 保持认证和附加功能可用。 | `否` | `false` |
| `SECURITY_ENABLELOGIN` | 启用登录页面。 | `否` | `false` |
| `SECURITY_INITIALLOGIN_USERNAME` | 登录开启且数据卷为空时使用的初始管理员用户名。 | `否` | `admin` |
| `SECURITY_INITIALLOGIN_PASSWORD` | 登录开启且数据卷为空时使用的初始管理员密码。 | `否` | `<已隐藏>` |
| `LANGS` | 文档转换使用的字体和 OCR 语言包。 | `否` | `en-GB,en-US,zh-CN,zh-TW` |
| `INSTALL_BOOK_AND_ADVANCED_HTML_OPS` | 安装 Calibre，用于电子书转换和高级 HTML 转换。 | `否` | `true` |
| `SYSTEM_DEFAULTLOCALE` | 默认界面语言。 | `否` | `en-US` |
| `UI_APPNAME` | 应用显示名称。 | `否` | `Stirling-PDF` |
| `UI_HOMEDESCRIPTION` | 首页短描述。 | `否` | `Demo site for Stirling-PDF` |
| `UI_APPNAMENAVBAR` | 导航栏显示名称。 | `否` | `Stirling-PDF` |
| `METRICS_ENABLED` | 启用 `/api/*` 信息接口。 | `否` | `true` |
| `SYSTEM_GOOGLEVISIBILITY` | 发布允许搜索引擎可见的 robots.txt 规则。 | `否` | `true` |

请将私有密码保存在 Sealos 管理的输入项中。

## PostgreSQL 选项

当 `use_postgresql=true` 时，模板会创建 Kubeblocks 管理的 PostgreSQL `postgresql-16.4.0` 集群，并通过幂等初始化 Job 创建 `stirling_pdf` 数据库。Stirling-PDF 会从 Sealos 管理的 Secret 中读取数据库地址、端口、用户名和密码。

## 扩展

模板资源覆盖常见 PDF 和 OCR 路径。执行大文件 OCR、电子书转换或团队并发使用前，可在 Sealos Canvas 中提高 CPU 和内存。

## 故障排查

### 出现登录页面

使用配置的 `SECURITY_INITIALLOGIN_USERNAME` 和 `SECURITY_INITIALLOGIN_PASSWORD` 登录。全新数据卷的上游默认值是 `admin` 和 `stirling`。

### OCR 或转换较慢

提高 StatefulSet 的 CPU 和内存后重试。大 PDF 和多语言 OCR 任务需要的内存高于基础合并或拆分操作。

### PostgreSQL 启动耗时

等待 PostgreSQL 集群和初始化 Job 完成后再打开应用。Stirling-PDF 能响应状态接口后，应用探针会变为健康。

## 更多资源

- [Stirling-PDF 官网](https://www.stirlingpdf.com/)
- [Stirling-PDF 源代码](https://github.com/Stirling-Tools/Stirling-PDF)
- [Stirling-PDF 安全文档](https://docs.stirlingpdf.com/Configuration/System%20and%20Security/)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板遵循模板仓库许可证提供。Stirling-PDF 遵循上游项目许可证。
