# FastGPT Pro

## Overview

FastGPT Pro is the commercial FastGPT stack for Sealos, adding the FastGPT Pro service alongside RAG retrieval, workflow orchestration, MCP access, and plugin extensibility.

This Sealos template deploys **FastGPT Pro** as the `fastgpt-pro` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `agent_sandbox_baseurl` | Hosted agent sandbox base URL | `false` | `` |
| `agent_sandbox_token` | Hosted agent sandbox access token | `false` | `<redacted>` |
| `root_password` | Root account password | `true` | `<redacted>` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://fastgpt.run/
- Source repository: https://github.com/labring/FastGPT
