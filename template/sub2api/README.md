# Sub2API

## Overview

AI API gateway platform for distributing and managing subscription quota across upstream AI services.

This Sealos template deploys **Sub2API** as the `sub2api` application. It uses the repository-maintained Sealos manifest and keeps deployment, networking, and storage configuration inside the template.

## Deploy on Sealos

Open this template in the Sealos App Store, review the configuration values, and click **Deploy**. Sealos renders the template variables, creates the required Kubernetes resources, and manages the public endpoint for the application.

## Access

After deployment, open `https://${{ defaults.app_host }}.${{ SEALOS_CLOUD_DOMAIN }}`. The concrete hostname is generated from `defaults.app_host` and your Sealos Cloud domain.

## Configuration

The following user-facing inputs are available during deployment:

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `admin_email` | Administrator email address | `false` | `admin@sub2api.local` |
| `admin_password` | Administrator password (leave empty to auto-generate on first startup) | `false` | `<redacted>` |
| `antigravity_oauth_client_secret` | Antigravity OAuth client secret | `false` | `<redacted>` |
| `gemini_cli_oauth_client_secret` | Gemini CLI built-in OAuth client secret | `false` | `<redacted>` |
| `gemini_oauth_client_id` | Gemini OAuth client ID | `false` | `` |
| `gemini_oauth_client_secret` | Gemini OAuth client secret | `false` | `<redacted>` |
| `gemini_oauth_scopes` | Gemini OAuth scopes | `false` | `` |
| `gemini_quota_policy` | Gemini quota policy | `false` | `` |
| `run_mode` | Application run mode | `false` | `standard` |
| `security_url_allowlist_allow_insecure_http` | Allow insecure HTTP URLs when allowlist is disabled | `false` | `false` |
| `security_url_allowlist_allow_private_hosts` | Allow private IP addresses for upstream and pricing access | `false` | `false` |
| `security_url_allowlist_enabled` | Enable upstream URL allowlist validation | `false` | `false` |
| `security_url_allowlist_upstream_hosts` | Comma-separated upstream hosts allowlist | `false` | `` |
| `timezone` | Timezone used by the application | `false` | `Asia/Shanghai` |
| `update_proxy_url` | Proxy URL used for update checks and GitHub access | `false` | `` |

Keep sensitive values in Sealos-managed inputs or generated defaults. Do not commit private credentials to the template repository.

## Official Links

- Official website: https://demo.sub2api.org/
- Source repository: https://github.com/Wei-Shaw/sub2api
