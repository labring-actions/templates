# Zot Registry

## Overview

OCI-native container image registry with basic auth and optional S3-compatible object storage backend.

This Sealos template deploys **Zot Registry** as the `zot` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `zot_admin_htpasswd_hash` | Admin htpasswd hash for object storage mode (bcrypt or SHA-crypt hash, not plain password). | `true` | `<redacted>` |
| `zot_admin_password` | Zot basic auth admin password. | `true` | `<redacted>` |
| `zot_admin_user` | Zot basic auth admin username. | `true` | `admin` |
| `zot_s3_region` | Region for S3-compatible object storage backend. | `true` | `us-east-1` |
| `zot_storage_backend` | Storage backend for image layers and manifests. | `true` | `filesystem` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://zotregistry.dev
- Source repository: https://github.com/project-zot/zot
