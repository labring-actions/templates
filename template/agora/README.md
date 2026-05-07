# Agora Token Service

## Overview

Agora Token Service for generating RTC and RTM tokens to authenticate users before they access the Agora service or join an RTC channel

This Sealos template deploys **Agora Token Service** as the `agora` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `app_certificate` | Login to the Agora Dashboard, and navigate to the "Projects" to copy APP_CERTIFICATE | `true` | `` |
| `app_id` | Login to the Agora Dashboard, and navigate to the "Projects" to copy APP_ID | `true` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/AgoraIO/Tools/tree/master/DynamicKey/AgoraDynamicKey
- Source repository: https://github.com/AgoraIO/Tools/tree/master/DynamicKey/AgoraDynamicKey
