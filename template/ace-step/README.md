# ACE-Step 1.5

## Overview

Open-source music generation AI. Commercial-grade quality, under 2s per song on A100. Supports text-to-music, cover generation, repainting, LoRA training, and 50+ languages.

This Sealos template deploys **ACE-Step 1.5** as the `ace-step` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `cpu_limit` | CPU limit (millicores, e.g. 4000 = 4 cores) | `false` | `4000` |
| `dit_model` | DiT model config: acestep-v15-turbo (fast) or acestep-v15 (quality) | `false` | `acestep-v15-turbo` |
| `gpu_count` | Number of GPUs (NVIDIA) | `true` | `1` |
| `init_service` | Auto-initialize models on startup (true/false). Set false to defer to UI button. | `false` | `true` |
| `llm_backend` | LLM backend: vllm (recommended for >=24GB VRAM) or pt (PyTorch, lower VRAM) | `false` | `pt` |
| `lm_model` | LM model: acestep-5Hz-lm-4B (best quality, >=24GB) / acestep-5Hz-lm-1.7B / acestep-5Hz-lm-0.6B (low VRAM) | `false` | `acestep-5Hz-lm-1.7B` |
| `memory_limit` | Memory limit (MiB) | `false` | `16384` |
| `output_volume_size` | Output storage size in GiB (generated audio files) | `false` | `10` |
| `startup_mode` | Startup mode: gradio (Web UI on port 7860) or api (REST API server on port 8001) | `true` | `gradio` |
| `volume_size` | Model storage size in GiB (checkpoints ~20GB) | `true` | `30` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://ace-step.github.io/ace-step-v1.5.github.io/
- Source repository: https://github.com/ace-step/ACE-Step
