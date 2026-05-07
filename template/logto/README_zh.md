# Logto

## 应用概览

Logto 是一个开源的 身份与访问管理（IAM）平台，是 Auth0 的开源替代方案，旨在帮助开发者快速构建安全、可扩展的登录注册系统和用户身份体系。

此 Sealos 模板会将 **Logto** 部署为 `logto` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

此模板没有额外的用户输入项；保留默认配置即可完成部署。

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://logto.io/
- 源码仓库: https://github.com/logto-io/logto
