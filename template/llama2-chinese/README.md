# llama2-chinese

## Overview

全部开源，完全可商用的中文版 Llama2 模型及中英文 SFT 数据集，输入格式严格遵循 llama-2-chat 格式，兼容适配所有针对原版 llama-2-chat 模型的优化。

This Sealos template deploys **llama2-chinese** as the `llama2-chinese` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

This template does not define extra user inputs; the default settings are enough to deploy it.

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/LinkSoul-AI/Chinese-Llama-2-7b
- Source repository: https://github.com/luanshaotong/text-generation-webui-docker.git
