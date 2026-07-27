# 在 Sealos 上部署和托管 PDFMathTranslate

PDFMathTranslate 可以在翻译 PDF 文档的同时保留公式、表格和页面排版。本模板在 Sealos 上运行官方 WebUI，并持久化配置、模型缓存和生成文件。

![PDFMathTranslate WebUI 中已完成的英译中任务](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/pdf2zh/website-screenshot.webp)

## 托管 PDFMathTranslate

模板会部署以下资源：

- **PDFMathTranslate `1.9.11`**：使用固定摘要的多架构镜像
- **单副本 WebUI**：以 StatefulSet 运行，监听 `7860` 端口
- **运行时凭据文件**：用于 Gradio 登录流程
- **`1Gi` 持久卷**：挂载到 `/data`
- **认证 HTTPS**：由 Sealos 管理 Service 和 Ingress，并通过 PDFMathTranslate 登录凭据保护
- **健康探针**：启动、就绪和存活探针统一检查 WebUI 根路径
- **受限容器安全上下文**：使用 UID 和 GID `1000` 运行

WebUI 需要使用部署时填写的用户名和密码登录。PDFMathTranslate 没有注册流程，请仅向需要访问上传文档和已保存翻译服务配置的人员共享凭据。官方运行拓扑只有一个服务，也不依赖数据库和对象存储。

## 常见使用场景

- 翻译科研论文并保留原有视觉结构
- 生成纯译文 PDF 和双语 PDF
- 阅读外语技术文档
- 只翻译大型文档中的指定页面
- 接入 Google、Bing、DeepL、OpenAI 兼容服务或自托管翻译服务

## 托管依赖

- Sealos 账号和工作区
- 能够访问所选翻译服务的公网连接
- 首次启动时可访问模型和字体下载地址
- 使用需要密钥的服务时，准备对应的服务商凭据

Google 和 Bing 可以直接使用，无需填写用户 API 密钥。可用性和限流策略由相应公共端点决定。

## 实现细节

| 组件 | 配置 |
| --- | --- |
| 镜像 | `byaidu/pdf2zh:1.9.11`，固定到 `sha256:8e083e...` |
| 工作负载 | 单副本 StatefulSet |
| 公网端口 | `7860` |
| 持久化挂载点 | `/data` |
| 运行时主目录 | `/data/home` |
| 官方配置路径 | `~/.config/PDFMathTranslate/config.json` |
| 部署后的配置路径 | `/data/home/.config/PDFMathTranslate/config.json` |
| 输出目录 | `/data/pdf2zh_files` |
| 访问控制 | 从运行时专用的 `0600` 权限文件加载 Gradio 登录凭据 |
| 健康检查 | HTTP `GET /` |

模板把两个必填部署凭据注入容器环境。一个小型 ConfigMap 启动脚本先执行 `umask 077`，写入 `/tmp/pdf2zh-auth.csv`，再执行 `pdf2zh -i --authorized /tmp/pdf2zh-auth.csv`。生成的认证文件权限为 `0600`，位于持久卷之外，并随容器销毁。工作目录设为 `/data`，生成的 PDF 会写入持久卷；`HOME=/data/home` 则让配置、字体、模型和翻译缓存能够跨 Pod 重启保留。

## 使用 Sealos 部署的优势

- **一键部署**：一个模板即可创建工作负载、存储、HTTPS 入口和应用链接。
- **工作数据持久化**：Pod 重建后仍会保留配置、下载资源、缓存和生成的 PDF。
- **内置可观测性**：可以直接在 Sealos 中查看状态、事件、资源用量和日志。
- **资源调整简单**：提高 CPU 即可加快文档处理，无需重新构建镜像。

## 部署指南

1. 打开 [PDFMathTranslate 模板](https://sealos.io/products/app-store/pdf2zh)，点击 **Deploy Now**。
2. 填写 WebUI 用户名和强唯一密码，然后开始部署。
3. 等待 StatefulSet 就绪。首次部署通常需要 2-3 分钟，期间 Sealos 会拉取镜像，PDFMathTranslate 会加载页面布局模型。
4. 打开 Sealos 显示的 HTTPS 应用地址。

两个 WebUI 凭据字段均为必填。建议使用密码管理器保存，因为 PDFMathTranslate 不提供注册或密码找回流程。上游以逗号分隔格式解析认证文件，因此用户名和密码需避开逗号与换行符。

## 登录

1. 打开 Sealos 显示的 HTTPS 应用地址。
2. 输入部署时填写的 WebUI 用户名和密码。
3. 进入翻译界面。

所有用户共享同一组部署级凭据。修改用户名或密码时，需要通过重新部署或模板更新来更新 StatefulSet 环境变量。

## 完成第一次 PDF 翻译

1. 登录部署后的 WebUI。
2. 保持选择 **File** 并上传 PDF，或选择 **Link** 后填写可直接访问的 PDF 地址。
3. 选择翻译服务、源语言、目标语言和页面范围。
4. 点击 **Translate**。
5. 下载 **Translation (Mono)** 获取纯译文文档，或下载 **Translation (Dual)** 获取双语文档。

**Experimental Options** 面板可以调整线程数、忽略翻译缓存、跳过字体子集、公式字体匹配规则和 BabelDOC 模式。

## 翻译服务与 API 密钥

选择服务后，WebUI 会显示该服务需要填写的字段。常见配置如下：

| 服务 | 常用字段 |
| --- | --- |
| Google 或 Bing | 无需用户密钥 |
| DeepL | `DEEPL_AUTH_KEY` |
| OpenAI | `OPENAI_BASE_URL`、`OPENAI_API_KEY`、`OPENAI_MODEL` |
| Gemini | `GEMINI_API_KEY`、`GEMINI_MODEL` |
| DeepSeek | `DEEPSEEK_API_KEY`、`DEEPSEEK_MODEL` |
| OpenAI-liked | 兼容服务的 Base URL、API 密钥和模型 |
| Ollama | 可访问的 `OLLAMA_HOST` 和模型名称 |

PDFMathTranslate 会把服务商配置保存到 `/data/home/.config/PDFMathTranslate/config.json`。WebUI 凭据会保护这份持久化配置、上传文档和付费服务额度的使用权限。请使用强唯一密码，将凭据共享范围限定在可信用户内，并使用权限范围受限的服务商密钥。

## 持久化

| 路径 | 用途 |
| --- | --- |
| `/data/home/.config/PDFMathTranslate` | 语言默认值和翻译服务配置 |
| `/data/home/.cache` | 页面布局模型、字体和翻译缓存 |
| `/data/pdf2zh_files` | 上传的源 PDF，以及生成的 Mono/Dual PDF |

这三个目录共享模板创建的 `1Gi` ReadWriteOnce 持久卷。批量处理或处理大型文档时，需要关注存储用量。

## 默认资源

| CPU limit | Memory limit | CPU request | Memory request |
| ---: | ---: | ---: | ---: |
| `100m` | `2048Mi` | `10m` | `204Mi` |

这些默认值来自真实冷启动和禁用缓存后的翻译测试。`512Mi` 容器在加载 ONNX 模型时触发 OOM，`1024Mi` 档的 cgroup 峰值达到上限的 92.93%，因此模板使用 `2048Mi` 保留运行余量。最低 CPU 档完成官方单页样例的禁用缓存翻译耗时 77.69 秒。

更大的 PDF、并发用户或 BabelDOC 工作负载可以将 CPU 提高到 `200m` 或 `500m`，以缩短处理时间。

## 扩缩容

模板使用单副本，因为配置、缓存和生成文件共享 ReadWriteOnce 持久卷。提高 CPU 是增加处理吞吐量的直接方式。多副本运行需要共享存储方案，以及与官方任务执行模型匹配的协调机制。

## 故障排查

### 应用仍在启动

在 Sealos 中查看 Pod 日志。首次启动时，应用可能先下载 DocLayout ONNX 模型和字体，然后 Gradio 才会监听 `7860` 端口。

### 翻译服务返回错误

可以先使用 Google 或 Bing 验证 PDF 处理链路。使用其他服务时，请重新打开对应的服务配置，检查端点、密钥和模型。

### WebUI 拒绝登录凭据

请使用部署时填写的准确用户名和密码。PDFMathTranslate 不提供注册或密码找回流程；需要修改凭据时，通过重新部署或模板更新来更新 StatefulSet 环境变量。

### 翻译速度较慢

在 Sealos 中提高 CPU limit。PDF 页面布局分析主要消耗 CPU，默认 `100m` 档侧重降低资源占用。

### 大文件上传失败

公网 Ingress 默认接受最大 `32m` 的请求体。可以压缩 PDF，或在 Ingress 中提高 `nginx.ingress.kubernetes.io/proxy-body-size`。

### 生成文件占满持久卷

清理 `/data/pdf2zh_files` 中的旧文件，并关注 `1Gi` 持久卷用量。`/data/home/.cache` 中的模型和字体也会占用这个持久卷。

## 更多资源

- [PDFMathTranslate 文档](https://pdf2zh.com/)
- [PDFMathTranslate GitHub 仓库](https://github.com/PDFMathTranslate/PDFMathTranslate)
- [GUI 使用指南](https://github.com/PDFMathTranslate/PDFMathTranslate/blob/v1.9.11/docs/README_GUI.md)
- [Sealos 应用商店](https://sealos.io/products/app-store)
- [Sealos Discord](https://discord.gg/wdUn538zVP)

## 许可证

PDFMathTranslate 采用 [GNU Affero General Public License v3.0](https://github.com/PDFMathTranslate/PDFMathTranslate/blob/v1.9.11/LICENSE)。本仓库只提供 Sealos 部署模板，不会改变上游许可证。
