# Tolgee

## Overview

An open-source localization platform that developers enjoy working with.

This Sealos template deploys **Tolgee** as the `tolgee` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `TOLGEE_AUTHENTICATION_INITIAL_PASSWORD` | The initial password for Tolgee authentication. | `true` | `<redacted>` |
| `TOLGEE_AUTHENTICATION_INITIAL_USERNAME` | The initial username for Tolgee authentication. | `true` | `admin` |
| `TOLGEE_SMTP_AUTH` | true: Enable SMTP authentication, false: Disable SMTP authentication | `false` | `false` |
| `TOLGEE_SMTP_FROM` | The email address to send emails from. | `false` | `test@test.com` |
| `TOLGEE_SMTP_HOST` | The SMTP host to send emails from. | `false` | `smtp.test.com` |
| `TOLGEE_SMTP_PASSWORD` | The SMTP password to send emails from. | `false` | `<redacted>` |
| `TOLGEE_SMTP_PORT` | The SMTP port to send emails from. | `false` | `0` |
| `TOLGEE_SMTP_SSL_ENABLED` | true: Enable SMTP SSL, false: Disable SMTP SSL | `false` | `false` |
| `TOLGEE_SMTP_USERNAME` | The SMTP user to send emails from. | `false` | `test` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://tolgee.io/
- Source repository: https://github.com/tolgee/tolgee-platform
