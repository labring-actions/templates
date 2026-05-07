# Supabase

## Overview

Open source Firebase alternative with Postgres database, authentication, realtime, storage, and edge functions.

This Sealos template deploys **Supabase** as the `supabase` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `anon_key` | Anonymous API key in JWT format (must be signed by jwt_secret). | `true` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNlYWxvcyIsInJvbGUiOiJhbm9uIiwiaWF0IjoxNzA0MDY3MjAwLCJleHAiOjIwNTEyMjI0MDB9.V5KvFbM6nMq-n8Ic1-9662IR7z4l00fNZD1mk4q8l84` |
| `jwt_secret` | JWT signing secret for Auth, PostgREST, Studio, and Storage API. | `true` | `<redacted>` |
| `service_role_key` | Service role API key in JWT format (must be signed by jwt_secret). | `true` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNlYWxvcyIsInJvbGUiOiJzZXJ2aWNlX3JvbGUiLCJpYXQiOjE3MDQwNjcyMDAsImV4cCI6MjA1MTIyMjQwMH0.gSHZ4wBeDMAbjjmkQ3TEoyOoqq7GR5F36krGv81PQLY` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://supabase.com
- Source repository: https://github.com/supabase/supabase
