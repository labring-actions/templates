# Paperless-ngx

## Overview

Paperless-ngx is a community-supported open-source document management system that transforms your physical documents into a searchable online archive so you can keep, well, less paper.

This Sealos template deploys **Paperless-ngx** as the `paperless-ngx` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `admin_mail` | Admin email for initial setup | `true` | `admin@example.com` |
| `admin_password` | Admin password for initial setup | `true` | `<redacted>` |
| `admin_user` | Admin username for initial setup | `true` | `` |
| `paperless_ocr_language` | Default language to use for OCR. Default: eng | `false` | `eng` |
| `paperless_ocr_languages` | Additional languages for text recognition (e.g., tur ces) | `false` | `` |
| `paperless_secret_key` | Should be a very long sequence of random characters | `false` | `<redacted>` |
| `paperless_time_zone` | Set timezone (e.g., America/Los_Angeles). Default: UTC | `false` | `UTC` |
| `usermap_gid` | GID of the user used to run paperless in the container | `false` | `1000` |
| `usermap_uid` | UID of the user used to run paperless in the container | `false` | `1000` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://paperless-ngx.com/
- Source repository: https://github.com/paperless-ngx/paperless-ngx
