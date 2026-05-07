# MinIO

## Overview

MinIO is a High Performance Object Storage released under GNU Affero General Public License v3.0. It is API compatible with Amazon S3 cloud storage service. Use MinIO to build high performance infrastructure for machine learning, analytics and application data workloads.

This Sealos template deploys **MinIO** as the `minio` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `important note` | Changing storage size of MinIO leads to unrecoverable crashes. | `false` | `` |
| `password` | MinIO Console Password (must be at least length 8) | `true` | `<redacted>` |
| `storage` | Storage size for each server in Gi (4 servers in total) | `true` | `` |
| `username` | MinIO Console Username (must be at least length 8) | `true` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://min.io/
- Source repository: https://github.com/minio/minio
