# MoneyPrinterTurbo

## Overview

利用AI大模型，一键生成高清短视频。只需提供一个视频 主题 或 关键词 ，就可以全自动生成视频文案、视频素材、视频字幕、视频背景音乐，然后合成一个高清的短视频。

This Sealos template deploys **MoneyPrinterTurbo** as the `moneyprinterturbo` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

This template does not define extra user inputs; the default settings are enough to deploy it.

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/harry0703/MoneyPrinterTurbo
- Source repository: https://github.com/harry0703/MoneyPrinterTurbo
