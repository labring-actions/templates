# WooCommerce

## Overview

WooCommerce is an open-source ecommerce platform built on WordPress.

This Sealos template deploys **WooCommerce** as the `woocommerce` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `WP_ADMIN_EMAIL` | WordPress admin email for initial setup. | `true` | `admin@example.com` |
| `WP_ADMIN_PASSWORD` | WordPress admin password for initial setup. | `true` | `<redacted>` |
| `WP_ADMIN_USER` | WordPress admin username for initial setup. | `true` | `admin` |
| `WP_SITE_TITLE` | WordPress site title for initial setup. | `false` | `WooCommerce Store` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://woocommerce.com
- Source repository: https://github.com/woocommerce/woocommerce
