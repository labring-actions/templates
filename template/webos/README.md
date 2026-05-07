# Webos

## Overview

Webos 是一个支持挂载各种云盘的私有云盘/企业网盘，仿 win11 界面，无需下载客户端。

This Sealos template deploys **Webos** as the `webos` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

This template does not define extra user inputs; the default settings are enough to deploy it.

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://os.tenfell.cn/
- Source repository: https://github.com/fs185085781/webos
