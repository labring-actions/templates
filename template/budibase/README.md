# Budibase

## Overview

Budibase is an open-source low-code platform that helps you build and deploy modern business apps in minutes

This Sealos template deploys **Budibase** as the `budibase` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `admin_email` | Admin email address | `true` | `` |
| `admin_password` | Admin password (minimum 8 characters) | `true` | `<redacted>` |
| `enable_analytics` | Enable analytics | `false` | `false` |
| `smtp_enabled` | Enable SMTP for email notifications | `false` | `false` |
| `smtp_host` | SMTP server host | `false` | `` |
| `smtp_password` | SMTP password | `false` | `<redacted>` |
| `smtp_port` | SMTP server port | `false` | `587` |
| `smtp_user` | SMTP username | `false` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://budibase.com/
- Source repository: https://github.com/Budibase/budibase
