# Deploy and Host LiteLLM on Sealos

LiteLLM is an OpenAI-compatible AI gateway for routing model traffic, managing virtual keys, enforcing budgets, and tracking spend. This template deploys LiteLLM with PostgreSQL-backed metadata, optional external PostgreSQL, optional S3-compatible config storage, and public HTTPS access on Sealos Cloud.

![LiteLLM Screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/litellm/website-screenshot.webp)

## About Hosting LiteLLM

LiteLLM gives teams one gateway endpoint for 100+ model providers while keeping client integrations compatible with the OpenAI API format. The admin UI lets operators create virtual keys, add model credentials, review usage, and set budget controls.

This Sealos template runs the `litellm/litellm-database:v1.88.1` image and provisions PostgreSQL 16 by default. You can also choose an external PostgreSQL URL during deployment, and you can enable Sealos S3-compatible object storage for LiteLLM config objects when you want config stored outside the container.

## Common Use Cases

- **Central AI gateway**: Route applications through one OpenAI-compatible endpoint.
- **Virtual key management**: Issue scoped keys for teams, services, or customers.
- **Spend tracking**: Monitor model usage and budget consumption from the admin UI.
- **Provider failover**: Manage multiple LLM providers behind one proxy.

## Dependencies for LiteLLM Hosting

The Sealos template includes the LiteLLM application container, bundled PostgreSQL 16 resources by default, optional ObjectStorageBucket support, HTTPS Ingress, Service, and App resources.

### Deployment Dependencies

- [LiteLLM Documentation](https://docs.litellm.ai/) - Proxy, UI, and provider configuration
- [LiteLLM GitHub Repository](https://github.com/BerriAI/litellm) - Source code and issue tracker
- [LiteLLM Docker Images](https://hub.docker.com/r/litellm/litellm) - Runtime image tags

### Implementation Details

**Architecture Components:**

- **LiteLLM Deployment**: Serves the gateway API and admin UI on port `4000`.
- **PostgreSQL Cluster**: Stores LiteLLM metadata, virtual keys, usage, and model configuration.
- **PostgreSQL Init Job**: Creates the `litellm` database for bundled PostgreSQL deployments.
- **Optional ObjectStorageBucket**: Stores LiteLLM config objects when `config_storage=sealos-s3`.
- **Ingress and App Entry**: Exposes the gateway and UI through the generated Sealos HTTPS URL.

**Configuration:**

- `ui_username` and `ui_password` set the admin UI credentials.
- `database_mode` selects bundled PostgreSQL or `external_database_url`.
- `config_storage` selects local config behavior or Sealos S3-compatible storage.
- The template generates `LITELLM_MASTER_KEY` and `LITELLM_SALT_KEY` automatically.

**License Information:**

LiteLLM is licensed under the MIT License. This Sealos template provides deployment configuration for running LiteLLM on Sealos Cloud.

## Why Deploy LiteLLM on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies application deployment and operations. By deploying LiteLLM on Sealos, you get one-click deployment, automatic HTTPS, managed database provisioning, persistent storage, resource controls, and Canvas-based updates.

## Deployment Guide

1. Open the [LiteLLM template](https://sealos.io/products/app-store/litellm) and click **Deploy Now**.
2. Configure the admin UI credentials and choose bundled or external PostgreSQL.
3. Wait for deployment to complete, typically 2-3 minutes. After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the AI dialog, or click the relevant resource cards to modify settings.
4. Open the generated public URL and log in with `ui_username` and `ui_password`.
5. Add a model provider credential in the LiteLLM admin UI.
6. Create a virtual key and use the generated URL as your OpenAI-compatible base URL.

## Configuration

After deployment, configure LiteLLM through:

- **LiteLLM Admin UI**: Add model providers, create virtual keys, review spend, and manage teams.
- **AI Dialog**: Describe environment or resource changes and let Sealos apply updates.
- **Resource Cards**: Adjust CPU, memory, environment variables, and storage from the Canvas.
- **Database Mode**: Use bundled PostgreSQL for a complete default setup, or provide `external_database_url` for an existing PostgreSQL database.

## Scaling

Start with the default single LiteLLM replica. Increase CPU and memory from the Canvas when request volume grows, then review PostgreSQL capacity if usage and key-management data increase.

## Troubleshooting

### Admin UI login fails

- Cause: The entered credentials do not match `ui_username` and `ui_password`.
- Solution: Use the values from the deployment form, or update the Deployment environment variables from the Canvas.

### Gateway is not ready

- Cause: LiteLLM is still connecting to PostgreSQL or running startup checks.
- Solution: Check the LiteLLM Deployment logs and PostgreSQL Cluster readiness from the Canvas.

### Model calls fail

- Cause: Provider credentials or model names are missing in the LiteLLM UI.
- Solution: Add a provider credential, configure the model, and test with a virtual key.

## Additional Resources

- [LiteLLM Proxy Docs](https://docs.litellm.ai/docs/simple_proxy)
- [LiteLLM Admin UI Docs](https://docs.litellm.ai/docs/proxy/ui)
- [LiteLLM GitHub Issues](https://github.com/BerriAI/litellm/issues)
- [Sealos Documentation](https://sealos.io/docs)

## License

This Sealos template is provided as deployment configuration for Sealos users. LiteLLM itself is licensed under the [MIT License](https://github.com/BerriAI/litellm/blob/main/LICENSE).
