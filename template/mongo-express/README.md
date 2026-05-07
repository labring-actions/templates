# mongo-express

## Overview

A web-based MongoDB admin interface written with Node.js, Express, and Bootstrap3

This Sealos template deploys **mongo-express** as the `mongo-express` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `custom_express_password` | User-defined mongo express login account password (non-database). The default is `sealos`. | `false` | `<redacted>` |
| `custom_express_user` | User-defined mongo express login account user (non-database). The default is `admin`. | `false` | `admin` |
| `mongodb_conn_credential` | mongodb conn credential, ex. mongodb://user:password@host:port/dbname | `true` | `<redacted>` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/mongo-express/mongo-express
- Source repository: https://github.com/mongo-express/mongo-express
