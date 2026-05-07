# Immich

## Overview

High performance self-hosted photo and video management solution. Store, organize, and share your memories with machine learning-powered features like face recognition and smart search.

This Sealos template deploys **Immich** as the `immich` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `enable_machine_learning` | Enable machine learning features (face recognition, object detection) | `false` | `true` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://immich.app/
- Source repository: https://github.com/immich-app/immich
