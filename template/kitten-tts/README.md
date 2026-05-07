# Kitten TTS

## Overview

Kitten-TTS-Server hosts the Kitten TTS model behind a small, fast API. It includes a built-in Web UI, audiobook-grade text handling, and GPU support. Use it for prototypes, research, or self-hosted TTS services.

This Sealos template deploys **Kitten TTS** as the `kitten-tts` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `hf_hub_enable_transfer` | Enable faster Hugging Face downloads | `false` | `true` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://github.com/SamThinks-Com/Kitten-TTS-Server
- Source repository: https://github.com/SamThinks-Com/Kitten-TTS-Server
