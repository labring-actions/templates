# Supabase

## 应用概览

Firebase 开源替代方案，支持 Postgres 数据库，认证，realtime，storage，与 edge functions。

此 Sealos 模板会将 **Supabase** 部署为 `supabase` 应用。部署、网络和存储配置都由仓库中的 Sealos 模板维护。

## 在 Sealos 上部署

在 Sealos 应用商店打开此模板，检查配置项后点击 **部署**。Sealos 会渲染模板变量，创建所需的 Kubernetes 资源，并为应用管理公网访问入口。

## 访问方式

部署完成后，打开 `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`。实际域名由 `defaults.app_host` 和当前 Sealos Cloud 域名生成。

## 配置说明

部署时可以配置以下用户可见输入项：

| 名称 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `anon_key` | `anon_key` 部署参数。 | `是` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNlYWxvcyIsInJvbGUiOiJhbm9uIiwiaWF0IjoxNzA0MDY3MjAwLCJleHAiOjIwNTEyMjI0MDB9.V5KvFbM6nMq-n8Ic1-9662IR7z4l00fNZD1mk4q8l84` |
| `jwt_secret` | `jwt_secret` 部署参数。 | `是` | `<已隐藏>` |
| `service_role_key` | `service_role_key` 部署参数。 | `是` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNlYWxvcyIsInJvbGUiOiJzZXJ2aWNlX3JvbGUiLCJpYXQiOjE3MDQwNjcyMDAsImV4cCI6MjA1MTIyMjQwMH0.gSHZ4wBeDMAbjjmkQ3TEoyOoqq7GR5F36krGv81PQLY` |

请将敏感信息保存在 Sealos 管理的输入项或生成默认值中，不要把私有凭据提交到模板仓库。

## 官方链接

- 官方网站: https://supabase.com
- 源码仓库: https://github.com/supabase/supabase
