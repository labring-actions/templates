# Nacos

## Overview

Dynamic Naming and Configuration Service - an easy-to-use platform designed for dynamic service discovery and configuration and service management

This Sealos template deploys **Nacos** as the `nacos` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `auth_token` | JWT secret key for authentication (Base64 encoded, must be at least 32 characters) | `false` | `<redacted>` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://nacos.io/
- Source repository: https://github.com/nacos-group/nacos-docker
