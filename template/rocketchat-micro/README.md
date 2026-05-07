# Rocket.Chat Microservices

## Overview

Rocket.Chat Microservices is an enterprise-grade, open-source communication platform built with a microservices architecture for superior scalability and performance. Ideal for organizations requiring high availability and horizontal scaling capabilities.

This Sealos template deploys **Rocket.Chat Microservices** as the `rocketchat-micro` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

This template does not define extra user inputs; the default settings are enough to deploy it.

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://rocket.chat/
- Source repository: https://github.com/RocketChat/Rocket.Chat
