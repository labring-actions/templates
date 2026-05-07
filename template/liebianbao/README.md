# 慧动裂变宝

## Overview

一款基于微信全生态运营场景开发的系统工具，助力企业打造获客·运营·转化·管理为一体的私域增长闭环。更好地通过微信公众号+社群+企业微信+视频号进行快速裂变获客、宣传推广、拓客到店，从而达到销售业绩的提升。

This Sealos template deploys **慧动裂变宝** as the `liebianbao` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `admin_password` | 管理员密码 | `true` | `<redacted>` |
| `admin_username` | 管理员账户 | `true` | `admin` |
| `reg_token` | 注册码 | `true` | `<redacted>` |
| `url` | 注册域名-需要 cname 到 ${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }} | `true` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: http://www.liebianbao.vip/
