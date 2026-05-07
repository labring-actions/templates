# TYPO3

## Overview

Open-source enterprise content management system for building and managing websites.

This Sealos template deploys **TYPO3** as the `typo3` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `TYPO3_PROJECT_NAME` | TYPO3 site name used during initial setup. | `false` | `TYPO3 Site` |
| `TYPO3_SETUP_ADMIN_EMAIL` | TYPO3 administrator email used during initial setup. | `true` | `admin@example.com` |
| `TYPO3_SETUP_ADMIN_PASSWORD` | TYPO3 administrator password used during initial setup. Must be at least 8 characters and include upper case, lower case, digit, and special character. | `true` | `<redacted>` |
| `TYPO3_SETUP_ADMIN_USERNAME` | TYPO3 administrator username used during initial setup. | `true` | `admin` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://typo3.org
- Source repository: https://github.com/TYPO3/typo3
