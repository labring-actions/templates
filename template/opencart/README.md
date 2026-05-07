# OpenCart

## Overview

Open-source eCommerce platform for building online stores.

This Sealos template deploys **OpenCart** as the `opencart` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `OPENCART_ADMIN_EMAIL` | OpenCart admin email for initial setup. | `true` | `admin@example.com` |
| `OPENCART_PASSWORD` | OpenCart admin password for initial setup. | `true` | `<redacted>` |
| `OPENCART_USERNAME` | OpenCart admin username for initial setup. | `true` | `admin` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://www.opencart.com/
- Source repository: https://github.com/opencart/opencart
