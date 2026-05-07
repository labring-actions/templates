# Loki

## 应用概览

Loki 是一个水平可扩展、高可用、多租户的日志聚合系统，灵感来自 Prometheus。

此 Sealos 模板会将 **Loki** 部署为 `loki` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

此模板没有额外的用户输入项；保留默认配置即可完成部署。

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://grafana.com/oss/loki/
- 源码仓库: https://github.com/grafana/loki
