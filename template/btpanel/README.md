# 宝塔面板

## Overview

宝塔面板是一个安全高效的服务器运维面板，一键配置：LAMP/LNMP、网站、数据库、FTP、SSL，通过Web端轻松管理服务器。

This Sealos template deploys **宝塔面板** as the `btpanel` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

This template does not define extra user inputs; the default settings are enough to deploy it.

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://www.bt.cn/
- Source repository: https://cnb.cool/btpanel/BaoTa
