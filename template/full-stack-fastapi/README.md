# Full Stack FastAPI

## Overview

Production-ready FastAPI + PostgreSQL + Frontend stack

This Sealos template deploys **Full Stack FastAPI** as the `full-stack-fastapi` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `EMAILS_FROM_EMAIL` | Sender email for SMTP (optional) | `false` | `` |
| `FIRST_SUPERUSER` | Initial superuser email for backend | `true` | `` |
| `FIRST_SUPERUSER_PASSWORD` | Initial superuser password for backend | `true` | `<redacted>` |
| `SECRET_KEY` | Backend secret key (JWT signing) | `true` | `<redacted>` |
| `SENTRY_DSN` | Sentry DSN (optional) | `false` | `` |
| `SMTP_HOST` | SMTP host (optional) | `false` | `` |
| `SMTP_PASSWORD` | SMTP password (optional) | `false` | `<redacted>` |
| `SMTP_USER` | SMTP user (optional) | `false` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/yangchuansheng/full-stack-fastapi-template
- Source repository: https://github.com/yangchuansheng/full-stack-fastapi-template
