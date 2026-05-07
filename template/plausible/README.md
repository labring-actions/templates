# plausible

## Overview

Simple, open-source, lightweight (< 1 KB) and privacy-friendly web analytics alternative to Google Analytics.

This Sealos template deploys **plausible** as the `plausible` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `CLICKHOUSE_PASSWORD` | clickhouse password | `true` | `<redacted>` |
| `CLICKHOUSE_USER` | clickhouse user name | `true` | `` |
| `DISABLE_REGISTRATION` | true or false | `true` | `` |
| `SECRET_KEY_BASE` | You can generate it using the following command: openssl rand -base64 64 | tr -d '
' ; echo | `true` | `<redacted>` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/plausible/analytics
- Source repository: https://github.com/plausible/analytics
