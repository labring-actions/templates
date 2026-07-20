# 在 Sealos 上部署和托管 code-server

code-server 可以在浏览器中运行 VS Code，并提供持久化工作区卷。此模板会在 Sealos Cloud 上部署带密码认证、持久化 home 存储和 HTTPS 访问入口的 code-server 4.128.0。

![code-server 截图](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/code-server/website-screenshot.webp)

## 关于托管 code-server

code-server 在 `8080` 端口提供 VS Code Web UI。Sealos 模板会创建采用 `Recreate` 更新策略的单副本 Deployment、持久化 `/home/coder` 卷、Service、Ingress 和 App 入口。

认证方式是密码登录。部署完成后，打开生成的 HTTPS 地址，并输入部署表单中的 `PASSWORD`。

## 常见使用场景

- **浏览器 IDE**：在浏览器中编辑文件、使用终端并运行开发命令。
- **远程工作区**：将项目文件和 VS Code 设置保存在 Sealos 持久卷中。
- **轻量管理控制台**：通过安全的 Web IDE 执行日常维护命令。
- **教学和演示**：用一个 URL 和一个密码提供可用的编码环境。

## 部署指南

1. 打开 [code-server 模板](https://sealos.io/products/app-store/code-server)，点击 **Deploy Now**。
2. 将 `PASSWORD` 设置为强密码。
3. 等待 Deployment 就绪，然后从 Sealos Canvas 打开生成的 HTTPS 地址。
4. 在登录页输入 `PASSWORD`。
5. 将项目保存在 `/home/coder` 下，确保项目位于持久化存储中。

## 配置说明

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `PASSWORD` | code-server 登录页使用的密码。 | `是` | 无 |

请将密码保存在 Sealos 管理的输入项中，需要变更访问权限时可在 Canvas 中轮换。

## 扩展

模板以 `200m` CPU 和 `512Mi` 内存支持小型交互式 IDE 会话。使用 ReadWriteOnce 卷时保持单副本；运行语言服务器、安装依赖或执行较重终端任务时，可在 Sealos Canvas 中提高资源。

## 故障排查

### 密码校验失败

确认 Deployment 输入中的当前 `PASSWORD`，需要时从 Canvas 更新该值并重启 Deployment。

### 终端或语言服务器较慢

提高 code-server Deployment 的 CPU 和内存。大型仓库和语言服务器需要的内存高于基础编辑器。

### 工作区文件丢失

确认文件保存于 `/home/coder`。该路径由持久化存储保存。

## 更多资源

- [code-server 文档](https://coder.com/docs/code-server)
- [code-server 源代码](https://github.com/coder/code-server)
- [Sealos 文档](https://sealos.io/docs)

## 许可证

此 Sealos 模板遵循模板仓库许可证提供。code-server 遵循上游项目许可证。
