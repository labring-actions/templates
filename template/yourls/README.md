# YOURLS

## Overview

YOURLS is a set of PHP scripts that will allow you to run Your Own URL Shortener, on your server.

This Sealos template deploys **YOURLS** as the `yourls` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `YOURLS_PASS` | YOURLS instance password. | `true` | `` |
| `YOURLS_USER` | YOURLS instance username. | `true` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://yourls.org/
- Source repository: https://github.com/YOURLS/YOURLS
