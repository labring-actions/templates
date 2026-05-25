# Flarum

## Overview

Flarum is a delightfully simple discussion platform for your website.

This Sealos template deploys **Flarum** as a single application backed by an ApeCloud MySQL 8.0 database. It keeps deployment, networking, storage, and the first-run database bootstrap inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

You can set `FLARUM_FORUM_TITLE` to choose the initial forum title. The default value is `Flarum`.

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://flarum.org/
- Source repository: https://github.com/flarum/framework
- Container image: https://github.com/crazy-max/docker-flarum
