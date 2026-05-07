# 聚量猩球

## Overview

多年服务500强企业体验管理经验沉淀，聚量猩球XM提供高效便捷的智能在线问卷系统、智能标签引擎及VR拟真实验能力，全面覆盖趋势洞察、概念验证、产品研发、产品试销、精益上市过程中的所有场景，让企业多快好省地获取消费者体验数据，降低企业生产投资决策风险，让每个研发决策反向赋能市场销售，实现口碑及业绩的双增长!

This Sealos template deploys **聚量猩球** as the `matrixgorilla` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

This template does not define extra user inputs; the default settings are enough to deploy it.

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://www.matrixgorilla.com/
- Source repository: https://github.com/hello-stars/MatrixGorilla.git
