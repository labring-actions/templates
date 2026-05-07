# Cronicle

## Overview

Cronicle is a multi-server task scheduler and runner, with a web based front-end UI.It handles both scheduled, repeating and on-demand jobs, targeting any number of slave servers, with real-time stats and live log viewer.Written in Node.js, proudly open source and MIT licensed.default username and password is admin

This Sealos template deploys **Cronicle** as the `cronicle` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

This template does not define extra user inputs; the default settings are enough to deploy it.

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: http://cronicle.net
- Source repository: https://github.com/jhuckaby/Cronicle
