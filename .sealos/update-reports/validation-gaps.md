# Validation Gaps

Generated for branch `codex/template-version-refresh-20260720` against `upstream/kb-0.9`.

## Repository validator availability

- The templates checkout does not contain `scripts/check_consistency.py`.
- The templates checkout does not contain `scripts/quality_gate.py`.
- The docker-to-sealos validators from `/Users/longnv/.codex/plugins/cache/sealos/sealos/1.1.0/skills/docker-to-sealos` were used instead.
- The legacy path `/Users/longnv/.codex/plugins/cache/local-plugins/sealos/0.1.0/skills/docker-to-sealos` is absent.

## Runtime validation

No Sealos deployment was created for this batch. Static validation passed for all 25 changed artifacts. Cross-major image candidates remain runtime-sensitive and require focused acceptance before production rollout:

- `appwrite`: `appwrite/console:7.8.26` -> `appwrite/console:8.7.28`
- `derper`: `bitnamilegacy/kubectl:1.28.9` -> `bitnamilegacy/kubectl:1.33.4`
- `firecrawl`: `rabbitmq:3.13.7-management` -> `rabbitmq:4.3.2-management`
- `firecrawl`: `redis:7.2.7-alpine` -> `redis:8.8.0-alpine`
- `lobehub`: `redis:7.2.7-alpine` -> `redis:8.8.0-alpine`
- `node-red`: `nodered/node-red:4.1.10` -> `nodered/node-red:5.0.1`
- `strapi`: `node:22.17.1-bookworm-slim` -> `node:26.5.0-bookworm-slim`
