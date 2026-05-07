# Cal.com

## Overview

Open-source scheduling platform for individuals, teams, and enterprises.

This Sealos template deploys **Cal.com** as the `calcom` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `calcom_license_key` | Enterprise license key for enabling paid Cal.com features | `false` | `` |
| `email_from` | Sender email address used for notifications and verification emails | `false` | `` |
| `email_from_name` | Sender display name used for outbound emails | `false` | `Cal.com` |
| `email_server_host` | SMTP server hostname for outbound email delivery | `false` | `` |
| `email_server_password` | SMTP password for outbound email delivery | `false` | `<redacted>` |
| `email_server_port` | SMTP server port for outbound email delivery | `false` | `587` |
| `email_server_user` | SMTP username for outbound email delivery | `false` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://cal.com/
- Source repository: https://github.com/calcom/cal.com
