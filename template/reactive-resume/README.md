# Reactive-Resume

## Overview

A free and open-source resume builder that simplifies the process of creating, updating, and sharing your resume.

This Sealos template deploys **Reactive-Resume** as the `Reactive-Resume` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `minio_storage` | Storage size for minio in Gi | `true` | `5` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://rxresu.me/
- Source repository: https://github.com/AmruthPillai/Reactive-Resume
