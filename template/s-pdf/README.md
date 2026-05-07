# Stirling-PDF

## Overview

1 Locally hosted web application that allows you to perform various operations on PDF files.

This Sealos template deploys **Stirling-PDF** as the `s-pdf` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `DOCKER_ENABLE_SECURITY` | download security jar (required as true for auth login) | `false` | `false` |
| `INSTALL_BOOK_AND_ADVANCED_HTML_OPS` | download calibre onto stirling-pdf enabling pdf to/from book and advanced html conversion | `false` | `true` |
| `LANGS` | define custom font libraries to install for use for document conversions | `false` | `en-GB,en-US,zh-CN,zh-TW` |
| `METRICS_ENABLED` | enable Info APIs (`/api/*`) endpoints | `false` | `true` |
| `SECURITY_ENABLELOGIN` | set to 'true' to enable login | `false` | `false` |
| `SYSTEM_DEFAULTLOCALE` | Set the default language | `false` | `en-US` |
| `SYSTEM_GOOGLEVISIBILITY` | allow Google visibility (via robots.txt) | `false` | `true` |
| `UI_APPNAME` | Application's visible name | `false` | `Stirling-PDF` |
| `UI_APPNAMENAVBAR` | Name displayed on the navigation bar | `false` | `Stirling-PDF` |
| `UI_HOMEDESCRIPTION` | Short description or tagline shown on homepage | `false` | `Demo site for Stirling-PDF` |
| `use_postgresql` | Use PostgreSQL database for production workloads (recommended for better performance and data persistence) | `false` | `false` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/Stirling-Tools/Stirling-PDF
- Source repository: https://github.com/Stirling-Tools/Stirling-PDF
