# RustDesk

## Overview

An open-source remote desktop application designed for self-hosting, as an alternative to TeamViewer.

This Sealos template deploys **RustDesk** as the `rustdesk` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `ENCRYPTED_ONLY` | 1: Restricted to secure data transmission with public key only, 0: Allows for unsecure data transmission | `true` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://rustdesk.com/
- Source repository: https://github.com/rustdesk/rustdesk
