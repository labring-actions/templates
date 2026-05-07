# Project Quay

## Overview

Container registry for building, storing, and distributing container images.

This Sealos template deploys **Project Quay** as the `quay` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `initial_admin_email` | Initial Quay admin email | `true` | `admin@example.com` |
| `initial_admin_password` | Initial Quay admin password | `true` | `<redacted>` |
| `initial_admin_username` | Initial Quay admin username | `true` | `admin` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://quay.io
- Source repository: https://github.com/quay/quay
