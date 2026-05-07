# FastGPT

This template updates FastGPT to the topology used by the upstream `deploy/docker/cn/docker-compose.pg.yml` release line and maps it onto Sealos-native resources.

It deploys:

- FastGPT main app
- FastGPT Plugin
- FastGPT Code Sandbox
- FastGPT MCP Server
- AIProxy
- MongoDB
- PostgreSQL for FastGPT vector storage
- PostgreSQL for AIProxy
- Redis
- Sealos object storage buckets for public and private assets

## Notes

1. Wait a few minutes after deployment so the database clusters and the AIProxy database init job can finish.
2. Sign in with username `root` and the `root_password` you entered at deploy time.
3. AI models still need to be configured after deployment. AIProxy is deployed internally and is consumed through FastGPT's built-in integration.
4. The MCP public address is preconfigured in `config.json`.
5. Agent sandbox integration is disabled by default because the upstream Docker topology depends on Docker-socket-based services. If you already have a hosted sandbox service, fill `agent_sandbox_baseurl` and `agent_sandbox_token` during deployment.
6. The ingress annotations follow the shared Sealos template defaults. If you need uploads larger than 32 MB, change the ingress `nginx.ingress.kubernetes.io/proxy-body-size` after deployment.

## Storage

This template uses Sealos object storage instead of the upstream embedded MinIO service. Public and private buckets are provisioned automatically and wired into FastGPT and FastGPT Plugin.

## Databases

The FastGPT PostgreSQL database runs on Sealos Database and is intended for the pgvector-backed FastGPT deployment path represented by the upstream compose file.
