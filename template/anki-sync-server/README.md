# anki-sync-server

## Overview

Self-Hosted Anki Sync Server

This Sealos template deploys **anki-sync-server** as the `anki-sync-server` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `MAX_SYNC_PAYLOAD_MEGS` | limit on uploads | `false` | `100` |
| `SYNC_USER1` | the first user and password for Anki Sync Server，format: "user:pass" | `false` | `user:pass` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://docs.ankiweb.net/sync-server.html
- Source repository: https://github.com/yangchuansheng/anki-sync-server
