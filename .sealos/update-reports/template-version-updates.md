# Sealos Template Version Update Report

Generated: 2026-06-25 09:55:19 UTC
Repo: `/Users/longnv/.codex/worktrees/template-version-refresh-20260625/templates`

## Summary

| Action | Count |
|--------|-------|
| update | 257 |
| manual | 215 |
| blocked | 24 |
| skip | 60 |

## Candidates

| Template | Current image | Candidate | Action | Confidence | Reason | Evidence |
|----------|---------------|-----------|--------|------------|--------|----------|
| AllinSSL | `docker.io/allinssl/allinssl` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| AllinSSL | `docker.io/allinssl/allinssl:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| OpenDeepWiki | `${{ inputs.wiki_image }}` |  | manual | low | templated or unparseable image requires manual release check | local parse |
| OpenDeepWiki | `${{ inputs.wiki_web_image }}` |  | manual | low | templated or unparseable image requires manual release check | local parse |
| Reactive-Resume | `amruthpillai/reactive-resume:v4.1.2` | `amruthpillai/reactive-resume:v5.1.9` | update | high | newer compatible semver tag found | crane ls |
| Reactive-Resume | `bitnamilegacy/postgresql:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| Reactive-Resume | `ghcr.io/browserless/chromium:v2.11.0` | `ghcr.io/browserless/chromium:v2.54.1` | update | high | newer compatible semver tag found | crane ls |
| Reactive-Resume | `quay.io/minio/minio` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| Reactive-Resume | `quay.io/minio/minio:RELEASE.2023-03-22T06-36-24Z` |  | manual | low | unsupported tag family | tag parser |
| Readeck | `codeberg.org/readeck/readeck:0.16.0` | `codeberg.org/readeck/readeck:0.22.3` | update | high | newer compatible semver tag found | crane ls |
| Ruiqi-Waf | `limbo2342/ruiqi-waf:sha-32b359f` |  | manual | low | unsupported tag family | tag parser |
| ace-step | `ghcr.io/ace-step/ace-step-1.5:v0.1.0` |  | skip | high | no newer compatible tag found | crane ls |
| affine | `ghcr.io/toeverything/affine:0.26.6` | `ghcr.io/toeverything/affine:0.26.7` | update | high | newer compatible semver tag found | crane ls |
| affine | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| agora | `agoracn/token:0.1.2023053011` |  | skip | high | no newer compatible tag found | crane ls |
| airbyte | `airbyte/bootloader:0.63.11` | `airbyte/bootloader:2.1.0` | update | high | newer compatible semver tag found | crane ls |
| airbyte | `airbyte/connector-builder-server:0.63.11` | `airbyte/connector-builder-server:2.0.1` | update | high | newer compatible semver tag found | crane ls |
| airbyte | `airbyte/cron:0.63.11` | `airbyte/cron:2.1.0` | update | high | newer compatible semver tag found | crane ls |
| airbyte | `airbyte/server:0.63.11` |  | blocked | low | crane ls timed out after 20s | crane ls |
| airbyte | `airbyte/webapp:0.63.11` |  | blocked | low | crane ls timed out after 20s | crane ls |
| airbyte | `airbyte/worker:0.63.11` | `airbyte/worker:2.1.0` | update | high | newer compatible semver tag found | crane ls |
| airbyte | `docker.io/apecloud/spilo:16.4.0` |  | skip | high | no newer compatible tag found | crane ls |
| airbyte | `temporalio/auto-setup:1.23.0` | `temporalio/auto-setup:1.29.7` | update | high | newer compatible semver tag found | crane ls |
| anki-sync-server | `ghcr.io/yangchuansheng/anki-sync-server:24.06.3` |  | manual | low | unsupported tag family | tag parser |
| apitable | `apitable/backend-server:v1.13.0-beta.1_2016` |  | skip | high | no newer compatible tag found | crane ls |
| apitable | `apitable/databus-server@sha256:462fa8bea11df94642b80a58d683aaf9995d79061588843a9d6b7ee66a421600` |  | manual | low | digest-only image requires manual release check | image digest |
| apitable | `apitable/imageproxy-server:v0.13.4-alpha_build13` |  | skip | high | no newer compatible tag found | crane ls |
| apitable | `apitable/init-appdata@sha256:4fa2ed5d1a5a3e2f7bd449352ec3054747127aabe4f91c62fc13f4660b25558b` |  | manual | low | digest-only image requires manual release check | image digest |
| apitable | `apitable/init-db:v1.13.0-beta.1_2016` |  | skip | high | no newer compatible tag found | crane ls |
| apitable | `apitable/room-server:v1.13.0-beta.1_2016` |  | skip | high | no newer compatible tag found | crane ls |
| apitable | `apitable/web-server:v1.13.0-beta.1_2016` |  | skip | high | no newer compatible tag found | crane ls |
| apitable | `busybox:1.36.1` | `busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| apitable | `mysql:8.0.32` | `mysql:9.7.1` | update | high | newer compatible semver tag found | crane ls |
| apitable | `nginx:1.27.5-alpine` | `nginx:1.31.2-alpine` | update | high | newer compatible semver tag found | crane ls |
| apitable | `rabbitmq:3.11.9-management` | `rabbitmq:4.3.2-management` | update | high | newer compatible semver tag found | crane ls |
| appflowy | `appflowyinc/appflowy_cloud:0.15.22` | `appflowyinc/appflowy_cloud:0.16.5` | update | high | newer compatible semver tag found | crane ls |
| appflowy | `appflowyinc/appflowy_web:0.14.9` | `appflowyinc/appflowy_web:0.15.4` | update | high | newer compatible semver tag found | crane ls |
| appflowy | `appflowyinc/appflowy_worker:0.15.22` | `appflowyinc/appflowy_worker:0.16.5` | update | high | newer compatible semver tag found | crane ls |
| appflowy | `appflowyinc/gotrue:0.15.22` | `appflowyinc/gotrue:0.16.5` | update | high | newer compatible semver tag found | crane ls |
| appflowy | `postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| appsmith | `appsmith/appsmith-ce:v1.29` |  | manual | low | unsupported tag family | tag parser |
| artalk | `artalk/artalk-go:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| asktable | `postgres:14-alpine` |  | manual | low | unsupported tag family | tag parser |
| asktable | `registry.cn-shanghai.aliyuncs.com/datamini/asktable-all-in-one:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| asktable | `registry.cn-shanghai.aliyuncs.com/datamini/asktable-atbox:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| authentik | `ghcr.io/goauthentik/server:2025.12.3` | `ghcr.io/goauthentik/server:2026.5.3` | update | high | newer compatible semver tag found | crane ls |
| authentik | `postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| banana-slides | `anoinex/banana-slides-backend:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| banana-slides | `anoinex/banana-slides-frontend:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| billionmail | `alpine/openssl:3.5.4` | `alpine/openssl:3.5.7` | update | high | newer compatible semver tag found | crane ls |
| billionmail | `alpine/socat:1.8.0.0@sha256:a6be4c0262b339c53ddad723cdd178a1a13271e1137c65e27f90a08c16de02b8` |  | manual | low | unsupported tag family | tag parser |
| billionmail | `billionmail/core:4.9.3@sha256:b97c71b463e99368f0fb50a4f3088139c2f04a37171d3b660b92f946a3076692` | `billionmail/core:4.9.5` | update | high | newer compatible semver tag found | crane ls |
| billionmail | `billionmail/dovecot:1.6@sha256:bbf5c304f248141768d1dbdf26b190fd28b69de6969b90e994ee81f54b942fab` |  | manual | low | unsupported tag family | tag parser |
| billionmail | `billionmail/postfix:1.6@sha256:870656c055c83f4e4b83fcd4c2f9cecfbcd0d8e3a963ab7d0c9c88bd6b348342` |  | manual | low | unsupported tag family | tag parser |
| billionmail | `billionmail/rspamd:1.2@sha256:bed48c106e8b8fcbf0a133c86e90900e7e17d4dec14cc30a9ddf989ada74f058` |  | manual | low | unsupported tag family | tag parser |
| billionmail | `public.ecr.aws/docker/library/postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| billionmail | `python:3.12.12-alpine` | `python:3.14.6-alpine` | update | high | newer compatible semver tag found | crane ls |
| billionmail | `roundcube/roundcubemail:1.6.11-fpm-alpine` | `roundcube/roundcubemail:1.7.1-fpm-alpine` | update | high | newer compatible semver tag found | crane ls |
| blossom | `docker.io/arey/mysql-client:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| blossom | `jasminexzzz/blossom:1.16.0` |  | skip | high | no newer compatible tag found | crane ls |
| btpanel | `btpanel/baota:nas` |  | manual | low | unsupported tag family | tag parser |
| budibase | `budibase/apps:3.15.0` | `budibase/apps:3.39.22` | update | high | newer compatible semver tag found | crane ls |
| budibase | `budibase/couchdb:v3.3.3-sqs-v2.1.1` |  | skip | high | no newer compatible tag found | crane ls |
| budibase | `budibase/proxy:3.15.0` | `budibase/proxy:3.39.22` | update | high | newer compatible semver tag found | crane ls |
| budibase | `budibase/worker:3.15.0` | `budibase/worker:3.39.22` | update | high | newer compatible semver tag found | crane ls |
| budibase | `busybox:1.37.0` | `busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| bunkerweb | `docker.io/bunkerity/bunkerweb-scheduler:1.6.11` |  | skip | high | no newer compatible tag found | crane ls |
| bunkerweb | `docker.io/bunkerity/bunkerweb-ui:1.6.11` |  | skip | high | no newer compatible tag found | crane ls |
| bunkerweb | `docker.io/bunkerity/bunkerweb:1.6.11` |  | skip | high | no newer compatible tag found | crane ls |
| bunkerweb | `docker.io/library/busybox:1.36.1` | `docker.io/library/busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| bunkerweb | `docker.io/library/postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| bunkerweb | `docker.io/traefik/whoami:v1.11.0` |  | skip | high | no newer compatible tag found | crane ls |
| bytebase | `bytebase/bytebase:3.6.1` | `bytebase/bytebase:3.19.1` | update | high | newer compatible semver tag found | crane ls |
| calcom | `calcom.docker.scarf.sh/calcom/cal.com:v6.2.0` |  | skip | high | no newer compatible tag found | crane ls |
| calcom | `public.ecr.aws/docker/library/postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| cap | `ghcr.io/capsoftware/cap-media-server@sha256:243b69c5d8b132a425641b6e6ada79c119467cc88a6b9446dd4f8dea6b579fad` |  | manual | low | digest-only image requires manual release check | image digest |
| cap | `ghcr.io/capsoftware/cap-web@sha256:8d2e21251b404e2b15772ded7bbf129cf980e6446102ea9b1326567647891e57` |  | manual | low | digest-only image requires manual release check | image digest |
| cap | `mysql:8.0.46-debian` |  | skip | high | no newer compatible tag found | crane ls |
| casdoor | `casbin/casdoor:v1.702.0` | `casbin/casdoor:v2.190.0` | update | high | newer compatible semver tag found | crane ls |
| casdoor | `casbin/casdoor:v2.32.0` | `casbin/casdoor:v2.190.0` | update | high | newer compatible semver tag found | crane ls |
| casdoor | `mysql:8.0` |  | manual | low | unsupported tag family | tag parser |
| casdoor | `postgres:14-alpine` |  | manual | low | unsupported tag family | tag parser |
| changedetection | `ghcr.io/dgtlmoon/changedetection.io:0.50.43` | `ghcr.io/dgtlmoon/changedetection.io:0.55.7` | update | high | newer compatible semver tag found | crane ls |
| chatany | `licoy/chatany:v3.5.0` |  | skip | high | no newer compatible tag found | crane ls |
| chatbot-ui | `ghcr.io/mckaywrigley/chatbot-ui:main` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| chatgpt-next-web | `yidadaa/chatgpt-next-web:v2.12.4` | `yidadaa/chatgpt-next-web:v2.16.1` | update | high | newer compatible semver tag found | crane ls |
| chatgpt-on-wechat | `zhayujie/chatgpt-on-wechat:1.6.8` | `zhayujie/chatgpt-on-wechat:2.1.2` | update | high | newer compatible semver tag found | crane ls |
| chatgpt-web | `chenzhaoyu94/chatgpt-web` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| chatnio | `joseluisq/mysql-client:8.0.30` | `joseluisq/mysql-client:8.0.44` | update | high | newer compatible semver tag found | crane ls |
| chatnio | `programzmh/chatnio@sha256:97587b5cdd85a4f5a9aee509304c594c9d66fa5f71b2164b78c064cec9feed2d` |  | manual | low | digest-only image requires manual release check | image digest |
| chatwoot | `chatwoot/chatwoot:v4.7.0` | `chatwoot/chatwoot:v4.15.1` | update | high | newer compatible semver tag found | crane ls |
| chatwoot | `postgres:14-alpine` |  | manual | low | unsupported tag family | tag parser |
| chrome | `lscr.io/linuxserver/chrome:148.0.7778.178-1-ls95` |  | manual | low | unsupported tag family | tag parser |
| cloudreve | `arey/mysql-client:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| cloudreve | `cloudreve/cloudreve` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| cobalt | `ghcr.io/imputnet/cobalt:7.13.3` | `ghcr.io/imputnet/cobalt:11.7.1` | update | high | newer compatible semver tag found | crane ls |
| code-server | `codercom/code-server:4.90.3-39` | `codercom/code-server:4.126.0-39` | update | high | newer compatible semver tag found | crane ls |
| coze-studio | `alpine/curl:8.12.1` | `alpine/curl:8.20.0` | update | high | newer compatible semver tag found | crane ls |
| coze-studio | `alpine/git@sha256:d453f54c83320412aa89c391b076930bd8569bc1012285e8c68ce2d4435826a3` |  | manual | low | digest-only image requires manual release check | image digest |
| coze-studio | `bitnamilegacy/elasticsearch:8.18.0` | `bitnamilegacy/elasticsearch:9.1.2` | update | high | newer compatible semver tag found | crane ls |
| coze-studio | `bitnamilegacy/etcd@sha256:1b9977cf4cce7546873e0ee50e684c38a38a4e7a27d22086fbd2b8a1b44a69d0` |  | manual | low | digest-only image requires manual release check | image digest |
| coze-studio | `busybox:1.36.1` | `busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| coze-studio | `cozedev/coze-studio-server:0.5.1` |  | skip | high | no newer compatible tag found | crane ls |
| coze-studio | `cozedev/coze-studio-web:0.5.1` |  | skip | high | no newer compatible tag found | crane ls |
| coze-studio | `milvusdb/milvus:v2.5.10` |  | blocked | low | crane ls timed out after 20s | crane ls |
| coze-studio | `minio/mc:RELEASE.2025-05-21T01-59-54Z-cpuv1` |  | manual | low | unsupported tag family | tag parser |
| coze-studio | `mysql:8.0.36` | `mysql:9.7.1` | update | high | newer compatible semver tag found | crane ls |
| coze-studio | `nsqio/nsq:v1.2.1` | `nsqio/nsq:v1.3.0` | update | high | newer compatible semver tag found | crane ls |
| crmeb | `ghcr.io/yangchuansheng/crmeb:v5.4.0` |  | skip | high | no newer compatible tag found | crane ls |
| crmeb | `joseluisq/mysql-client:8.0.30` | `joseluisq/mysql-client:8.0.44` | update | high | newer compatible semver tag found | crane ls |
| crmeb | `nginx:alpine3.20` |  | manual | low | unsupported tag family | tag parser |
| cronicle | `soulteary/cronicle:0.9.46` | `soulteary/cronicle:0.9.80` | update | high | newer compatible semver tag found | crane ls |
| dataease | `busybox:1.36.1` | `busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| dataease | `docker.io/arey/mysql-client:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| dataease | `registry.cn-qingdao.aliyuncs.com/dataease/dataease:v2.10.12` | `registry.cn-qingdao.aliyuncs.com/dataease/dataease:v2.10.25` | update | high | newer compatible semver tag found | crane ls |
| dbgate | `dbgate/dbgate:5.3.1-alpine` | `dbgate/dbgate:7.2.1-alpine` | update | high | newer compatible semver tag found | crane ls |
| deeplx | `ghcr.io/owo-network/deeplx:v0.9.5` | `ghcr.io/owo-network/deeplx:v1.2.2` | update | high | newer compatible semver tag found | crane ls |
| derper | `bitnamilegacy/kubectl:1.28.9` | `bitnamilegacy/kubectl:1.33.4` | update | high | newer compatible semver tag found | crane ls |
| derper | `ghcr.io/yangchuansheng/derper:v1.99.0-pre` | `ghcr.io/yangchuansheng/derper:v1.101.0-pre` | update | high | newer compatible semver tag found | crane ls |
| dify | `busybox:1.37.0` | `busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| dify | `langgenius/dify-api:1.11.2` |  | blocked | low | crane ls timed out after 20s | crane ls |
| dify | `langgenius/dify-plugin-daemon:0.5.2-local` | `langgenius/dify-plugin-daemon:0.6.3-local` | update | high | newer compatible semver tag found | crane ls |
| dify | `langgenius/dify-sandbox:0.2.12` | `langgenius/dify-sandbox:0.2.15` | update | high | newer compatible semver tag found | crane ls |
| dify | `langgenius/dify-web:1.11.2` |  | blocked | low | crane ls timed out after 20s | crane ls |
| dify | `postgres:14-alpine` |  | manual | low | unsupported tag family | tag parser |
| dify | `semitechnologies/weaviate:1.27.0` |  | blocked | low | crane ls timed out after 20s | crane ls |
| directus | `directus/directus:11.17.4` | `directus/directus:12.0.2` | update | high | newer compatible semver tag found | crane ls |
| directus | `public.ecr.aws/docker/library/busybox:1.36.1` | `public.ecr.aws/docker/library/busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| directus | `public.ecr.aws/docker/library/postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| directus | `public.ecr.aws/docker/library/redis:7.2.7-alpine` | `public.ecr.aws/docker/library/redis:8.8.0-alpine` | update | high | newer compatible semver tag found | crane ls |
| docker-stacks | `jupyter/scipy-notebook:2023-10-20` |  | skip | high | no newer compatible tag found | crane ls |
| docuseal | `docuseal/docuseal:3.0.1` | `docuseal/docuseal:3.1.1` | update | high | newer compatible semver tag found | crane ls |
| docuseal | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| dolibarr | `dolibarr/dolibarr:23.0.3-php8.2@sha256:c3c17731287f1a6a30ec7e0a3e7a82adda7bc93abd79af94714709704c8a4865` |  | skip | high | no newer compatible tag found | crane ls |
| dolibarr | `mysql:8.0.30` | `mysql:9.7.1` | update | high | newer compatible semver tag found | crane ls |
| drawdb | `ghcr.io/drawdb-io/drawdb:v1.5.0` | `ghcr.io/drawdb-io/drawdb:v1.7.0` | update | high | newer compatible semver tag found | crane ls |
| drizzle-studio | `ghcr.io/drizzle-team/gateway:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| eaglercraft-server | `ghcr.io/yangchuansheng/eaglerx1.8server:1.12.1` |  | skip | high | no newer compatible tag found | crane ls |
| edgequake | `ghcr.io/raphaelmansuy/edgequake-frontend:0.12.2` | `ghcr.io/raphaelmansuy/edgequake-frontend:0.12.11` | update | high | newer compatible semver tag found | crane ls |
| edgequake | `ghcr.io/raphaelmansuy/edgequake:0.12.2` | `ghcr.io/raphaelmansuy/edgequake:0.12.11` | update | high | newer compatible semver tag found | crane ls |
| edgequake | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| elasticsearch | `busybox:1.37.0` | `busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| elasticsearch | `docker.elastic.co/elasticsearch/elasticsearch:9.4.1` |  | blocked | low | crane ls timed out after 20s | crane ls |
| emqx | `emqx/emqx:5.8.9` | `emqx/emqx:6.2.1` | update | high | newer compatible semver tag found | crane ls |
| enshrouded | `alpine` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| enshrouded | `bitnamilegacy/kubectl` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| enshrouded | `registry.cn-hangzhou.aliyuncs.com/luanshaotong/enshrouded:v0.2` |  | manual | low | unsupported tag family | tag parser |
| erpnext | `frappe/erpnext:v16.21.1` | `frappe/erpnext:v16.25.0` | update | high | newer compatible semver tag found | crane ls |
| erpnext | `mariadb:11.4.7` | `mariadb:12.3.2` | update | high | newer compatible semver tag found | crane ls |
| erpnext | `public.ecr.aws/docker/library/busybox:1.36.1` | `public.ecr.aws/docker/library/busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| erpnext | `public.ecr.aws/docker/library/redis:7.2.7-alpine` | `public.ecr.aws/docker/library/redis:8.8.0-alpine` | update | high | newer compatible semver tag found | crane ls |
| ever-gauzy | `busybox:1.36.1` | `busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| ever-gauzy | `ghcr.io/ever-co/gauzy-api-demo@sha256:9c7efab08c8f48892486099e0cd6edda4eddfa27743b09dd953145d8ff5a5cc4` |  | manual | low | digest-only image requires manual release check | image digest |
| ever-gauzy | `ghcr.io/ever-co/gauzy-webapp-demo@sha256:6370fc7dcc8eeba67cc75f8a88afb9f85552be1602769af78d4da0c23f42e493` |  | manual | low | digest-only image requires manual release check | image digest |
| ever-gauzy | `postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| evolution-api | `evoapicloud/evolution-api:v2.3.7` |  | skip | high | no newer compatible tag found | crane ls |
| evolution-api | `public.ecr.aws/docker/library/busybox:1.36.1` | `public.ecr.aws/docker/library/busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| evolution-api | `public.ecr.aws/docker/library/postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| evolution-api | `public.ecr.aws/docker/library/redis:7.2.7-alpine` | `public.ecr.aws/docker/library/redis:8.8.0-alpine` | update | high | newer compatible semver tag found | crane ls |
| excalidraw | `excalidraw/excalidraw@sha256:36cd9a135e25b17e7e0b1b1d64df5fc1dad651eac72b6f2aa9c1d5401eddc68f` |  | manual | low | digest-only image requires manual release check | image digest |
| fast-poster | `fastposter/fastposter:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| fastgpt | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| fastgpt | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-code-sandbox:v4.14.22` | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-code-sandbox:v4.14.23` | update | high | newer compatible semver tag found | crane ls |
| fastgpt | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-mcp_server:v4.14.22` | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-mcp_server:v4.14.23` | update | high | newer compatible semver tag found | crane ls |
| fastgpt | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-plugin:v0.6.2` | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-plugin:v0.6.3` | update | high | newer compatible semver tag found | crane ls |
| fastgpt | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt:v4.14.22` | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt:v4.14.26` | update | high | newer compatible semver tag found | crane ls |
| fastgpt | `registry.cn-hangzhou.aliyuncs.com/labring/aiproxy:v0.5.8` | `registry.cn-hangzhou.aliyuncs.com/labring/aiproxy:v0.6.3` | update | high | newer compatible semver tag found | crane ls |
| fastgpt-milvus | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| fastgpt-milvus | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-code-sandbox:v4.14.22` | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-code-sandbox:v4.14.23` | update | high | newer compatible semver tag found | crane ls |
| fastgpt-milvus | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-mcp_server:v4.14.22` | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-mcp_server:v4.14.23` | update | high | newer compatible semver tag found | crane ls |
| fastgpt-milvus | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-plugin:v0.6.2` | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-plugin:v0.6.3` | update | high | newer compatible semver tag found | crane ls |
| fastgpt-milvus | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt:v4.14.22` | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt:v4.14.26` | update | high | newer compatible semver tag found | crane ls |
| fastgpt-milvus | `registry.cn-hangzhou.aliyuncs.com/labring/aiproxy:v0.5.8` | `registry.cn-hangzhou.aliyuncs.com/labring/aiproxy:v0.6.3` | update | high | newer compatible semver tag found | crane ls |
| fastgpt-pro | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| fastgpt-pro | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-code-sandbox:v4.14.22` | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-code-sandbox:v4.14.23` | update | high | newer compatible semver tag found | crane ls |
| fastgpt-pro | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-mcp_server:v4.14.22` | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-mcp_server:v4.14.23` | update | high | newer compatible semver tag found | crane ls |
| fastgpt-pro | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-plugin:v0.6.2` | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-plugin:v0.6.3` | update | high | newer compatible semver tag found | crane ls |
| fastgpt-pro | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-pro:v4.14.22` | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-pro:v4.14.26` | update | high | newer compatible semver tag found | crane ls |
| fastgpt-pro | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt:v4.14.22` | `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt:v4.14.26` | update | high | newer compatible semver tag found | crane ls |
| fastgpt-pro | `registry.cn-hangzhou.aliyuncs.com/labring/aiproxy:v0.5.8` | `registry.cn-hangzhou.aliyuncs.com/labring/aiproxy:v0.6.3` | update | high | newer compatible semver tag found | crane ls |
| featbit-standard | `featbit/featbit-api-server:5.0.5` | `featbit/featbit-api-server:5.4.2` | update | high | newer compatible semver tag found | crane ls |
| featbit-standard | `featbit/featbit-data-analytics-server:5.0.5` | `featbit/featbit-data-analytics-server:5.4.2` | update | high | newer compatible semver tag found | crane ls |
| featbit-standard | `featbit/featbit-evaluation-server:5.0.5` | `featbit/featbit-evaluation-server:5.4.2` | update | high | newer compatible semver tag found | crane ls |
| featbit-standard | `featbit/featbit-ui:5.0.5` | `featbit/featbit-ui:5.4.2` | update | high | newer compatible semver tag found | crane ls |
| featbit-standard | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| filecodebox | `lanol/filecodebox@sha256:e3609361ae7dfb7b72fef94d97e58ea268b960c3dc70719b7221277612946ad2` |  | manual | low | digest-only image requires manual release check | image digest |
| fireboom | `fireboomapi/fireboom_server@sha256:27ff832760dec9cf205f02b3516ad6663fa7cbfcf35da1b49196acd00efb598f` |  | manual | low | digest-only image requires manual release check | image digest |
| firefox | `jlesage/firefox:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| flarum | `crazymax/flarum:1.8.10` |  | skip | high | no newer compatible tag found | crane ls |
| flarum | `mysql:8.0.30` | `mysql:9.7.1` | update | high | newer compatible semver tag found | crane ls |
| flowise | `flowiseai/flowise:3.0.5` | `flowiseai/flowise:3.1.2` | update | high | newer compatible semver tag found | crane ls |
| flowise | `postgres:14-alpine` |  | manual | low | unsupported tag family | tag parser |
| formbricks | `ghcr.io/formbricks/formbricks:4.9.7` | `ghcr.io/formbricks/formbricks:5.1.4` | update | high | newer compatible semver tag found | crane ls |
| formbricks | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| frp | `bitnamilegacy/kubectl:1.28.9` | `bitnamilegacy/kubectl:1.33.4` | update | high | newer compatible semver tag found | crane ls |
| frp | `snowdreamtech/frps:0.59` |  | manual | low | unsupported tag family | tag parser |
| full-stack-fastapi | `ghcr.io/yangchuansheng/full-stack-fastapi-backend:0.8.0` |  | skip | high | no newer compatible tag found | crane ls |
| full-stack-fastapi | `ghcr.io/yangchuansheng/full-stack-fastapi-frontend:0.8.0` |  | skip | high | no newer compatible tag found | crane ls |
| full-stack-fastapi | `postgres:14-alpine` |  | manual | low | unsupported tag family | tag parser |
| ghost | `ghost:6.44.1-alpine` | `ghost:6.47.0-alpine` | update | high | newer compatible semver tag found | crane ls |
| ghost | `public.ecr.aws/docker/library/mysql:8.0.30` | `public.ecr.aws/docker/library/mysql:9.7.1` | update | high | newer compatible semver tag found | crane ls |
| ghost | `public.ecr.aws/docker/library/node:22-alpine` |  | manual | low | unsupported tag family | tag parser |
| gitea | `gitea/gitea:1.22.0-rootless` | `gitea/gitea:1.26.4-rootless` | update | high | newer compatible semver tag found | crane ls |
| glance | `glanceapp/glance` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| glance | `glanceapp/glance:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| glitchtip | `glitchtip/glitchtip:v4.1.5` | `glitchtip/glitchtip:v6.0.3` | update | high | newer compatible semver tag found | crane ls |
| glitchtip | `senzing/postgresql-client:2.2.4` |  | blocked | low | Error: reading tags for index.docker.io/senzing/postgresql-client: GET https://index.docker.io/v2/senzing/postgresql-client/tags/list?n=1000: UNAUTHORIZED: authentication required; [map[Action:pull Class: Name:senzing/postgresql-client Type:repository]] | crane ls |
| gpt-academic | `ghcr.io/binary-husky/gpt_academic_nolocal:master` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| grafana-otel | `busybox` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| grafana-otel | `grafana/grafana:12.3.0` | `grafana/grafana:13.1.0` | update | high | newer compatible semver tag found | crane ls |
| grafana-otel | `otel/opentelemetry-collector:0.99.0` | `otel/opentelemetry-collector:0.155.0` | update | high | newer compatible semver tag found | crane ls |
| grafana-otel | `prom/prometheus:v3.8.0` | `prom/prometheus:v3.12.0` | update | high | newer compatible semver tag found | crane ls |
| halo | `halohub/halo:2.18.0` | `halohub/halo:2.25.4` | update | high | newer compatible semver tag found | crane ls |
| halo | `senzing/postgresql-client:2.2.4` |  | blocked | low | Error: reading tags for index.docker.io/senzing/postgresql-client: GET https://index.docker.io/v2/senzing/postgresql-client/tags/list?n=1000: UNAUTHORIZED: authentication required; [map[Action:pull Class: Name:senzing/postgresql-client Type:repository]] | crane ls |
| happy-server | `ghcr.io/yangchuansheng/happy-server@sha256:6986ce15ac7c00604ab4aea89c9f9831b44746ec20da5cb5812ff1ab40317cfe` |  | manual | low | digest-only image requires manual release check | image digest |
| happy-server | `postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| harbor | `goharbor/harbor-core:v2.14.4` | `goharbor/harbor-core:v2.15.1` | update | high | newer compatible semver tag found | crane ls |
| harbor | `goharbor/harbor-jobservice:v2.14.4` | `goharbor/harbor-jobservice:v2.15.1` | update | high | newer compatible semver tag found | crane ls |
| harbor | `goharbor/harbor-portal:v2.14.4` | `goharbor/harbor-portal:v2.15.1` | update | high | newer compatible semver tag found | crane ls |
| harbor | `goharbor/harbor-registryctl:v2.14.4` | `goharbor/harbor-registryctl:v2.15.1` | update | high | newer compatible semver tag found | crane ls |
| harbor | `goharbor/registry-photon:v2.14.4` | `goharbor/registry-photon:v2.15.1` | update | high | newer compatible semver tag found | crane ls |
| harbor | `goharbor/trivy-adapter-photon:v2.14.4` | `goharbor/trivy-adapter-photon:v2.15.1` | update | high | newer compatible semver tag found | crane ls |
| harbor | `postgres:16.4` |  | manual | low | unsupported tag family | tag parser |
| hasura | `hasura/graphql-data-connector:v2.48.11` | `hasura/graphql-data-connector:v2.49.3` | update | high | newer compatible semver tag found | crane ls |
| hasura | `hasura/graphql-engine:v2.48.11` |  | blocked | low | crane ls timed out after 20s | crane ls |
| headscale | `alpine` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| headscale | `ghcr.io/tale/headplane:0.6.3` |  | skip | high | no newer compatible tag found | crane ls |
| headscale | `headscale/headscale:0.29.0-beta.1-debug` |  | skip | high | no newer compatible tag found | crane ls |
| headscale | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| heyform | `heyform/community-edition:v3.0.0-rc.7` |  | skip | high | no newer compatible tag found | crane ls |
| illa-builder | `illasoft/illa-builder:v4.8.2` | `illasoft/illa-builder:v4.8.5` | update | high | newer compatible semver tag found | crane ls |
| immich | `ghcr.io/immich-app/immich-machine-learning:v2.7.5` |  | blocked | low | crane ls timed out after 20s | crane ls |
| immich | `ghcr.io/immich-app/immich-server:v2.7.5` |  | skip | high | no newer compatible tag found | crane ls |
| immich | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| influxdb | `docker.io/library/influxdb:2.9.1` |  | skip | high | no newer compatible tag found | crane ls |
| inpaint-web | `yangchuansheng/inpaint-web` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| insforge | `apecloud/kubeblocks-tools:0.9.3` | `apecloud/kubeblocks-tools:1.0.2` | update | high | newer compatible semver tag found | crane ls |
| insforge | `ghcr.io/insforge/deno-runtime:2.0.6` |  | skip | high | no newer compatible tag found | crane ls |
| insforge | `ghcr.io/insforge/insforge-oss:v2.1.8` | `ghcr.io/insforge/insforge-oss:v2.2.2` | update | high | newer compatible semver tag found | crane ls |
| insforge | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| insforge | `postgrest/postgrest:v12.2.12` | `postgrest/postgrest:v13.0.8` | update | high | newer compatible semver tag found | crane ls |
| it-tools | `ghcr.io/corentinth/it-tools:2024.5.13-a0bc346` |  | skip | high | no newer compatible tag found | crane ls |
| jsoncrack | `shokohsc/jsoncrack@sha256:4360a0659ed2fc301904477b9eb3454f8ab7b67af611b1f25e79acfb6165c8ef` |  | manual | low | digest-only image requires manual release check | image digest |
| kanboard | `kanboard/kanboard:v1.2.50` | `kanboard/kanboard:v1.2.52` | update | high | newer compatible semver tag found | crane ls |
| kaneo | `ghcr.io/usekaneo/api:1.1.8` | `ghcr.io/usekaneo/api:2.7.7` | update | high | newer compatible semver tag found | crane ls |
| kaneo | `ghcr.io/usekaneo/web:1.1.8` | `ghcr.io/usekaneo/web:2.7.7` | update | high | newer compatible semver tag found | crane ls |
| kaneo | `postgres:14-alpine` |  | manual | low | unsupported tag family | tag parser |
| keycloak | `postgres:14-alpine` |  | manual | low | unsupported tag family | tag parser |
| keycloak | `quay.io/keycloak/keycloak:26.3.2` | `quay.io/keycloak/keycloak:26.6.3` | update | high | newer compatible semver tag found | crane ls |
| keystone | `node:22.22.1-alpine` | `node:26.3.1-alpine` | update | high | newer compatible semver tag found | crane ls |
| keystone | `postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| kitten-tts | `ghcr.io/yangchuansheng/kitten-tts-server:cpu-v1.2` |  | manual | low | unsupported tag family | tag parser |
| kodcloud | `kodcloud/kodbox:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| kuboard | `eipwork/kuboard:v3` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| kuvasz | `kuvaszmonitoring/kuvasz:3.11.0` | `kuvaszmonitoring/kuvasz:4.0.1` | update | high | newer compatible semver tag found | crane ls |
| kuvasz | `postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| laf | `docker.io/lafyun/laf-server:sha-ef30cd9` |  | manual | low | unsupported tag family | tag parser |
| laf | `docker.io/lafyun/laf-web:sha-e9d012d` |  | manual | low | unsupported tag family | tag parser |
| laf | `docker.io/lafyun/runtime-node-init:sha-67b3cd6` |  | manual | low | unsupported tag family | tag parser |
| laf | `docker.io/lafyun/runtime-node:sha-67b3cd6` |  | manual | low | unsupported tag family | tag parser |
| laf | `docker.io/library/nginx:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| laf | `quay.io/minio/mc:RELEASE.2022-11-07T23-47-39Z` |  | manual | low | unsupported tag family | tag parser |
| laf | `quay.io/minio/minio` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| laf | `quay.io/minio/minio:RELEASE.2023-03-22T06-36-24Z` |  | manual | low | unsupported tag family | tag parser |
| laf | `quay.io/prometheus/prometheus:v2.45.0` | `quay.io/prometheus/prometheus:v3.12.0` | update | high | newer compatible semver tag found | crane ls |
| langflow | `langflowai/langflow:1.9.5` | `langflowai/langflow:1.10.1` | update | high | newer compatible semver tag found | crane ls |
| langflow | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| langfuse | `clickhouse/clickhouse-server:25.4.2` | `clickhouse/clickhouse-server:26.5.3` | update | high | newer compatible semver tag found | crane ls |
| langfuse | `docker.io/langfuse/langfuse-worker:3.180.0` | `docker.io/langfuse/langfuse-worker:3.197.1` | update | high | newer compatible semver tag found | crane ls |
| langfuse | `docker.io/langfuse/langfuse:3.180.0` | `docker.io/langfuse/langfuse:3.197.1` | update | high | newer compatible semver tag found | crane ls |
| langfuse | `minio/minio:RELEASE.2025-09-07T16-13-09Z` |  | manual | low | unsupported tag family | tag parser |
| langfuse | `public.ecr.aws/docker/library/postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| langfuse | `public.ecr.aws/docker/library/redis:7.2.7-alpine` | `public.ecr.aws/docker/library/redis:8.8.0-alpine` | update | high | newer compatible semver tag found | crane ls |
| librechat | `getmeili/meilisearch:v1.5` |  | manual | low | unsupported tag family | tag parser |
| librechat | `ghcr.io/danny-avila/librechat:v0.7.3` | `ghcr.io/danny-avila/librechat:v0.8.7` | update | high | newer compatible semver tag found | crane ls |
| liebianbao | `busybox:1.36.1` | `busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| liebianbao | `docker.io/arey/mysql-client:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| liebianbao | `docker.io/labring4docker/php-custom:7.2-fpm` |  | manual | low | unsupported tag family | tag parser |
| liebianbao | `labring4docker/php-custom:7.2-fpm` |  | manual | low | unsupported tag family | tag parser |
| liebianbao | `nginx:1.25.2` | `nginx:1.31.2` | update | high | newer compatible semver tag found | crane ls |
| listmonk | `busybox:1.37.0` | `busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| listmonk | `listmonk/listmonk:v6.1.0` |  | skip | high | no newer compatible tag found | crane ls |
| listmonk | `postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| llama2-chinese | `luanshaotong/text-generation-webui-cpu:dev` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| llama3-8b-chinese | `registry.cn-hangzhou.aliyuncs.com/yangchuansheng/llama-3-8b-chinese:q4_k_m` |  | manual | low | unsupported tag family | tag parser |
| llmgateway | `ghcr.io/theopenco/llmgateway-api:v1.3.0` | `ghcr.io/theopenco/llmgateway-api:v1.5.0` | update | high | newer compatible semver tag found | crane ls |
| llmgateway | `ghcr.io/theopenco/llmgateway-docs:v1.3.0` | `ghcr.io/theopenco/llmgateway-docs:v1.5.0` | update | high | newer compatible semver tag found | crane ls |
| llmgateway | `ghcr.io/theopenco/llmgateway-gateway:v1.3.0` | `ghcr.io/theopenco/llmgateway-gateway:v1.5.0` | update | high | newer compatible semver tag found | crane ls |
| llmgateway | `ghcr.io/theopenco/llmgateway-ui:v1.3.0` | `ghcr.io/theopenco/llmgateway-ui:v1.5.0` | update | high | newer compatible semver tag found | crane ls |
| llmgateway | `ghcr.io/theopenco/llmgateway-worker:v1.3.0` | `ghcr.io/theopenco/llmgateway-worker:v1.5.0` | update | high | newer compatible semver tag found | crane ls |
| llmgateway | `public.ecr.aws/docker/library/postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| llmgateway | `public.ecr.aws/docker/library/redis:7.2.7-alpine` | `public.ecr.aws/docker/library/redis:8.8.0-alpine` | update | high | newer compatible semver tag found | crane ls |
| lobe-chat | `lobehub/lobe-chat:1.143.3` |  | skip | high | no newer compatible tag found | crane ls |
| lobe-chat-db | `lobehub/lobe-chat-database:1.143.2` | `lobehub/lobe-chat-database:1.143.3` | update | high | newer compatible semver tag found | crane ls |
| lobe-chat-db | `postgres:14-alpine` |  | manual | low | unsupported tag family | tag parser |
| logto | `postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| logto | `svhd/logto:1.40.1` |  | skip | high | no newer compatible tag found | crane ls |
| loki | `busybox:1.37.0` | `busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| loki | `docker.io/grafana/loki:3.7.2` |  | blocked | low | crane ls timed out after 20s | crane ls |
| mage-ai | `mageai/mageai:0.9.79` |  | skip | high | no newer compatible tag found | crane ls |
| mage-ai | `postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| mastodon | `ghcr.io/mastodon/mastodon-streaming:v4.5.11` | `ghcr.io/mastodon/mastodon-streaming:v4.6.2` | update | high | newer compatible semver tag found | crane ls |
| mastodon | `ghcr.io/mastodon/mastodon:v4.5.11` | `ghcr.io/mastodon/mastodon:v4.6.2` | update | high | newer compatible semver tag found | crane ls |
| mastodon | `postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| mastodon | `public.ecr.aws/docker/library/postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| mastodon | `public.ecr.aws/docker/library/redis:7-alpine` |  | manual | low | unsupported tag family | tag parser |
| matomo | `matomo:5.10.0-apache` | `matomo:5.11.2-apache` | update | high | newer compatible semver tag found | crane ls |
| matomo | `mysql:8.0.44` | `mysql:9.7.1` | update | high | newer compatible semver tag found | crane ls |
| matrixgorilla | `${{ defaults.app_name }}-api` |  | manual | low | templated or unparseable image requires manual release check | local parse |
| matrixgorilla | `${{ defaults.app_name }}-web` |  | manual | low | templated or unparseable image requires manual release check | local parse |
| matrixgorilla | `registry.cn-beijing.aliyuncs.com/juliangxingqiu/sealos-java-api:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| matrixgorilla | `registry.cn-beijing.aliyuncs.com/juliangxingqiu/sealos-java-web:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| mautic | `busybox:1.36.1` | `busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| mautic | `mautic/mautic:7.1.2-apache` |  | skip | high | no newer compatible tag found | crane ls |
| mautic | `mysql:8.4.2` | `mysql:9.7.1` | update | high | newer compatible semver tag found | crane ls |
| mazanoke | `ghcr.io/civilblur/mazanoke:v1.1.6` |  | skip | high | no newer compatible tag found | crane ls |
| meilisearch | `eyeix/meilisearch-ui:v0.15.1-lite` |  | skip | high | no newer compatible tag found | crane ls |
| meilisearch | `getmeili/meilisearch:v1.45.1` | `getmeili/meilisearch:v1.48.2` | update | high | newer compatible semver tag found | crane ls |
| memos | `ghcr.io/usememos/memos:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| metabase | `metabase/metabase:v0.61.3` | `metabase/metabase:v0.62.3` | update | high | newer compatible semver tag found | crane ls |
| metabase | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| midjourney-ui | `erictik/midjourney-ui:1.1.47` |  | skip | high | no newer compatible tag found | crane ls |
| mindoc | `registry.cn-hangzhou.aliyuncs.com/mindoc-org/mindoc:v2.2-beta.1` |  | manual | low | unsupported tag family | tag parser |
| mindoc | `senzing/postgresql-client:2.2.4` |  | blocked | low | Error: reading tags for index.docker.io/senzing/postgresql-client: GET https://index.docker.io/v2/senzing/postgresql-client/tags/list?n=1000: UNAUTHORIZED: authentication required; [map[Action:pull Class: Name:senzing/postgresql-client Type:repository]] | crane ls |
| mindsdb | `mindsdb/mindsdb:v26.1.0` |  | skip | high | no newer compatible tag found | crane ls |
| mindsdb | `public.ecr.aws/docker/library/postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| minecraft | `alpine:3.22.4` | `alpine:3.24.1` | update | high | newer compatible semver tag found | crane ls |
| minecraft | `itzg/minecraft-server:2026.5.3-java25` | `itzg/minecraft-server:2026.6.1-java8` | update | high | newer compatible semver tag found | crane ls |
| minio | `quay.io/minio/minio` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| mlflow | `ghcr.io/mlflow/mlflow:v3.12.0` | `ghcr.io/mlflow/mlflow:v3.14.0` | update | high | newer compatible semver tag found | crane ls |
| mlflow | `senzing/postgresql-client:2.2.4` |  | blocked | low | Error: reading tags for index.docker.io/senzing/postgresql-client: GET https://index.docker.io/v2/senzing/postgresql-client/tags/list?n=1000: UNAUTHORIZED: authentication required; [map[Action:pull Class: Name:senzing/postgresql-client Type:repository]] | crane ls |
| moneyprinterturbo | `ghcr.io/yangchuansheng/moneyprinterturbo:20240510083200` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| mongo-express | `mongo-express:1.0.2-20-alpine3.19` |  | skip | high | no newer compatible tag found | crane ls |
| n8n | `alpine` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| n8n | `busybox:1.36` |  | manual | low | unsupported tag family | tag parser |
| n8n | `n8nio/n8n:2.22.4` | `n8nio/n8n:2.28.1` | update | high | newer compatible semver tag found | crane ls |
| n8n | `n8nio/runners:2.22.4` | `n8nio/runners:2.28.1` | update | high | newer compatible semver tag found | crane ls |
| n8n | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| nacos | `mysql:8.0.44` | `mysql:9.7.1` | update | high | newer compatible semver tag found | crane ls |
| nacos | `nacos/nacos-server:v3.2.2` |  | skip | high | no newer compatible tag found | crane ls |
| nakama | `busybox:1.36` |  | manual | low | unsupported tag family | tag parser |
| nakama | `heroiclabs/nakama:3.39.0` |  | skip | high | no newer compatible tag found | crane ls |
| nakama | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| netbird | `netbirdio/dashboard:v2.38.1` | `netbirdio/dashboard:v2.80.0` | update | high | newer compatible semver tag found | crane ls |
| netbird | `netbirdio/management:0.71.4` | `netbirdio/management:0.73.2` | update | high | newer compatible semver tag found | crane ls |
| netbird | `netbirdio/relay:0.71.4` | `netbirdio/relay:0.73.2` | update | high | newer compatible semver tag found | crane ls |
| netbird | `netbirdio/signal:0.71.4` | `netbirdio/signal:0.73.2` | update | high | newer compatible semver tag found | crane ls |
| new-api | `calciumion/new-api:v0.13.2` |  | skip | high | no newer compatible tag found | crane ls |
| new-api | `postgres:16.4` |  | manual | low | unsupported tag family | tag parser |
| nexus | `alpine:3.22.2` | `alpine:3.24.1` | update | high | newer compatible semver tag found | crane ls |
| nexus | `sonatype/nexus3:3.92.3` | `sonatype/nexus3:3.93.1` | update | high | newer compatible semver tag found | crane ls |
| nocodb | `nocodb/nocodb:2026.05.2` | `nocodb/nocodb:2026.06.1` | update | medium | newer compatible date tag found | crane ls |
| node-red | `nodered/node-red:4.1.10` | `nodered/node-red:5.0.0` | update | high | newer compatible semver tag found | crane ls |
| nofx | `alpine/openssl:3.5.4` | `alpine/openssl:3.5.7` | update | high | newer compatible semver tag found | crane ls |
| nofx | `ghcr.io/nofxaios/nofx/nofx-backend@sha256:32d77ff9761ba8b068f95a5a4c8fee0a7745c8a927300b7d658e593b1e654ae7` |  | manual | low | digest-only image requires manual release check | image digest |
| nofx | `ghcr.io/nofxaios/nofx/nofx-frontend@sha256:6c1e56336433e82eb5e750034d2991a8dbebd89a6b19119c4b12601ef1842887` |  | manual | low | digest-only image requires manual release check | image digest |
| nofx | `public.ecr.aws/docker/library/postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| notifuse | `notifuse/notifuse:v32.1@sha256:fdee58fc36e50cf3f64c007dbf07549842280022828fd6c051f6454084a66cfb` |  | manual | low | unsupported tag family | tag parser |
| notifuse | `postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| nsfw | `ethandai4869/nsfw-auth` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| one-api | `ghcr.io/songquanpeng/one-api:v0.6.10` |  | skip | high | no newer compatible tag found | crane ls |
| open-design | `docker.io/vanjayak/open-design@sha256:a3b0f7b043aec134e857513f1480b2da6aaaab641af2d7337999c9090a5c1e13` |  | manual | low | digest-only image requires manual release check | image digest |
| open-design | `nginxinc/nginx-unprivileged:1.25-alpine-slim` |  | manual | low | unsupported tag family | tag parser |
| open-webui | `ghcr.io/open-webui/open-webui:v0.5.4` | `ghcr.io/open-webui/open-webui:v0.9.6` | update | high | newer compatible semver tag found | crane ls |
| openagents | `ghcr.io/openagents-org/openagents:sha-48764c0` |  | manual | low | unsupported tag family | tag parser |
| openai-proxy | `unickcheng/openai-proxy` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| opencart | `ghcr.io/yangchuansheng/opencart:4.1.0.3@sha256:eb92c3f24fe3a2b44a09af51dcd8c2ba9aeb2454b26dcae9e85036afb1d04d94` |  | manual | low | unsupported tag family | tag parser |
| openclaw | `busybox:1.36` |  | manual | low | unsupported tag family | tag parser |
| openclaw | `ghcr.io/openclaw/openclaw:2026.3.8` | `ghcr.io/openclaw/openclaw:2026.6.10` | update | high | newer compatible semver tag found | crane ls |
| openlist | `openlistteam/openlist:v4.0.9-aria2` | `openlistteam/openlist:v4.2.2-aria2` | update | high | newer compatible semver tag found | crane ls |
| openobserve | `public.ecr.aws/zinclabs/openobserve:v0.90.3` | `public.ecr.aws/zinclabs/openobserve:v0.91.0` | update | high | newer compatible semver tag found | crane ls |
| outline | `outlinewiki/outline:1.8.0-1` | `outlinewiki/outline:1.8.2-0` | update | high | newer compatible semver tag found | crane ls |
| outline | `postgres:16.4` |  | manual | low | unsupported tag family | tag parser |
| overleaf | `sharelatex/sharelatex:6.1.2` | `sharelatex/sharelatex:6.2.0` | update | high | newer compatible semver tag found | crane ls |
| pageplug | `cloudtogouser/pageplug-ce:v1.9.35` | `cloudtogouser/pageplug-ce:v1.9.37` | update | high | newer compatible semver tag found | crane ls |
| palacms | `ghcr.io/palacms/palacms:v3.0.0-beta.1` |  | blocked | low | 2026/06/25 17:48:35 No matching credentials were found for "ghcr.io"
Error: reading tags for ghcr.io/palacms/palacms: GET https://ghcr.io/token?scope=repository%3Apalacms%2Fpalacms%3Apull&service=ghcr.io: DENIED: requested access to the resource is denied | crane ls |
| palworld | `alpine` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| palworld | `hurlenko/filebrowser` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| palworld | `thijsvanloef/palworld-server-docker` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| palworld-autobackup | `bitnamilegacy/kubectl` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| palworld-export | `bitnamilegacy/kubectl` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| palworld-export | `hurlenko/filebrowser` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| palworld-management | `registry.cn-hangzhou.aliyuncs.com/bxy4543/palworld-server-tool:2024-02-18` |  | skip | high | no newer compatible tag found | crane ls |
| pangolin | `docker.io/fosrl/pangolin:1.15.2` | `docker.io/fosrl/pangolin:1.19.2` | update | high | newer compatible semver tag found | crane ls |
| paperclip | `ghcr.io/paperclipai/paperclip:sha-b8725c5` |  | manual | low | unsupported tag family | tag parser |
| paperclip | `public.ecr.aws/docker/library/busybox:1.36.1` | `public.ecr.aws/docker/library/busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| paperclip | `public.ecr.aws/docker/library/postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| paperless-ngx | `ghcr.io/paperless-ngx/paperless-ngx:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| paperless-ngx | `postgres:14-alpine` |  | manual | low | unsupported tag family | tag parser |
| payload | `ghcr.io/yangchuansheng/payload:3.82.1-a7dd17c9be0c` |  | skip | high | no newer compatible tag found | crane ls |
| payload | `public.ecr.aws/docker/library/postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| pdf2zh | `byaidu/pdf2zh:1.9.6` | `byaidu/pdf2zh:1.9.11` | update | high | newer compatible semver tag found | crane ls |
| penpot | `penpotapp/backend:2.1.2` | `penpotapp/backend:2.16.1` | update | high | newer compatible semver tag found | crane ls |
| penpot | `penpotapp/exporter:2.1.2` | `penpotapp/exporter:2.16.1` | update | high | newer compatible semver tag found | crane ls |
| penpot | `penpotapp/frontend:2.1.2` | `penpotapp/frontend:2.16.1` | update | high | newer compatible semver tag found | crane ls |
| penpot | `senzing/postgresql-client:2.2.4` |  | blocked | low | Error: reading tags for index.docker.io/senzing/postgresql-client: GET https://index.docker.io/v2/senzing/postgresql-client/tags/list?n=1000: UNAUTHORIZED: authentication required; [map[Action:pull Class: Name:senzing/postgresql-client Type:repository]] | crane ls |
| perplexica | `itzcrazykns1337/perplexica:v1.10.2` | `itzcrazykns1337/perplexica:v1.12.0` | update | high | newer compatible semver tag found | crane ls |
| perplexica | `searxng/searxng:2025.2.20-28d1240fc` |  | skip | high | no newer compatible tag found | crane ls |
| pgadmin4 | `dpage/pgadmin4:8.9` |  | manual | low | unsupported tag family | tag parser |
| photoprism | `photoprism/photoprism:240711` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| phpmyadmin | `phpmyadmin:5.2.1` | `phpmyadmin:5.2.3` | update | high | newer compatible semver tag found | crane ls |
| plane | `makeplane/plane-admin:v0.22-dev` |  | manual | low | unsupported tag family | tag parser |
| plane | `makeplane/plane-backend:v0.22-dev` |  | manual | low | unsupported tag family | tag parser |
| plane | `makeplane/plane-frontend:v0.22-dev` |  | manual | low | unsupported tag family | tag parser |
| plane | `makeplane/plane-space:v0.22-dev` |  | manual | low | unsupported tag family | tag parser |
| plane | `senzing/postgresql-client:2.2.4` |  | blocked | low | Error: reading tags for index.docker.io/senzing/postgresql-client: GET https://index.docker.io/v2/senzing/postgresql-client/tags/list?n=1000: UNAUTHORIZED: authentication required; [map[Action:pull Class: Name:senzing/postgresql-client Type:repository]] | crane ls |
| planka | `busybox:1.36.1` | `busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| planka | `ghcr.io/plankanban/planka:2.1.1` |  | skip | high | no newer compatible tag found | crane ls |
| planka | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| plausible | `clickhouse/clickhouse-server:23.3.7.5-alpine` |  | manual | low | unsupported tag family | tag parser |
| plausible | `plausible/analytics:v2.0` |  | manual | low | unsupported tag family | tag parser |
| pocket-id | `ghcr.io/pocket-id/pocket-id:v2.2.0` | `ghcr.io/pocket-id/pocket-id:v2.9.0` | update | high | newer compatible semver tag found | crane ls |
| pocketbase | `adrianmusante/pocketbase:0.29.3` | `adrianmusante/pocketbase:0.39.4` | update | high | newer compatible semver tag found | crane ls |
| pocketbase | `busybox:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| posthog | `clickhouse/clickhouse-server:25.8.12.129` |  | manual | low | unsupported tag family | tag parser |
| posthog | `docker.redpanda.com/redpandadata/redpanda:v25.1.9` | `docker.redpanda.com/redpandadata/redpanda:v26.1.10` | update | high | newer compatible semver tag found | crane ls |
| posthog | `ghcr.io/posthog/posthog-node@sha256:fd156e690ca1bb7cc1abd370e513ac532c57726ee11029721623f0db5b90b72a` |  | manual | low | digest-only image requires manual release check | image digest |
| posthog | `ghcr.io/posthog/posthog/capture@sha256:864754478dbbd589f17cb4543d07e1b0f63acbca8e0bceca13de10669500375b` |  | manual | low | digest-only image requires manual release check | image digest |
| posthog | `ghcr.io/posthog/posthog/feature-flags@sha256:1e79e6e7e5b58da18e27ebdf0ef9b41d6c04136eac42bb9490e73a9a62f94f65` |  | manual | low | digest-only image requires manual release check | image digest |
| posthog | `ghcr.io/posthog/posthog:86d6812c7de75c6c869b935e17baf45bf295bfd5` |  | blocked | low | crane ls timed out after 20s | crane ls |
| posthog | `postgres:16.4` |  | manual | low | unsupported tag family | tag parser |
| posthog | `zookeeper:3.9.3` | `zookeeper:3.9.5` | update | high | newer compatible semver tag found | crane ls |
| postiz | `busybox:1.36.1` | `busybox:1.38.0` | update | high | newer compatible semver tag found | crane ls |
| postiz | `elasticsearch:7.17.27` | `elasticsearch:9.4.2` | update | high | newer compatible semver tag found | crane ls |
| postiz | `ghcr.io/gitroomhq/postiz-app:v2.21.8` | `ghcr.io/gitroomhq/postiz-app:v2.21.10` | update | high | newer compatible semver tag found | crane ls |
| postiz | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| postiz | `temporalio/auto-setup:1.28.1` | `temporalio/auto-setup:1.29.7` | update | high | newer compatible semver tag found | crane ls |
| presenton | `ghcr.io/presenton/presenton:v0.8.2-beta` | `ghcr.io/presenton/presenton:v0.8.9-beta` | update | high | newer compatible semver tag found | crane ls |
| prestashop | `mysql:8.0.30` | `mysql:9.7.1` | update | high | newer compatible semver tag found | crane ls |
| prestashop | `prestashop/prestashop:9.1.3-apache` | `prestashop/prestashop:9.1.4-apache` | update | high | newer compatible semver tag found | crane ls |
| privatebin | `alpine` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| privatebin | `frooodle/privatebin:0.26.1-fat` |  | blocked | low | Error: reading tags for index.docker.io/frooodle/privatebin: GET https://index.docker.io/v2/frooodle/privatebin/tags/list?n=1000: UNAUTHORIZED: authentication required; [map[Action:pull Class: Name:frooodle/privatebin Type:repository]] | crane ls |
| privatebin | `ghcr.io/privatebin/fs:1.7.4` | `ghcr.io/privatebin/fs:2.0.4` | update | high | newer compatible semver tag found | crane ls |
| pterodactyl | `ghcr.io/pterodactyl/panel:v1.12.4` | `ghcr.io/pterodactyl/panel:v1.14.0` | update | high | newer compatible semver tag found | crane ls |
| pterodactyl | `public.ecr.aws/docker/library/mysql:8.0.30` | `public.ecr.aws/docker/library/mysql:9.7.1` | update | high | newer compatible semver tag found | crane ls |
| pterodactyl | `public.ecr.aws/docker/library/redis:7.2.7-alpine` | `public.ecr.aws/docker/library/redis:8.8.0-alpine` | update | high | newer compatible semver tag found | crane ls |
| qinglong | `whyour/qinglong:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| quay | `postgres:16.4` |  | manual | low | unsupported tag family | tag parser |
| quay | `python:3.12.8-alpine3.20` | `python:3.14.6-alpine3.24` | update | high | newer compatible semver tag found | crane ls |
| quay | `quay.io/projectquay/quay:v3.9.8` | `quay.io/projectquay/quay:v3.17.3` | update | high | newer compatible semver tag found | crane ls |
| redisinsight | `redislabs/redisinsight:2.52` |  | manual | low | unsupported tag family | tag parser |
| refly | `mautic/mautic:5.2.3-fpm` | `mautic/mautic:7.1.2-fpm` | update | high | newer compatible semver tag found | crane ls |
| refly | `reflyai/elasticsearch:7.10.2` |  | skip | high | no newer compatible tag found | crane ls |
| refly | `reflyai/qdrant:v1.13.1` |  | skip | high | no newer compatible tag found | crane ls |
| refly | `reflyai/refly-api:8d870210470801f62a4d2adb3423c947afddf400` |  | manual | low | unsupported tag family | tag parser |
| refly | `reflyai/refly-web:8d870210470801f62a4d2adb3423c947afddf400` |  | manual | low | unsupported tag family | tag parser |
| refly | `senzing/postgresql-client:2.2.4` |  | blocked | low | Error: reading tags for index.docker.io/senzing/postgresql-client: GET https://index.docker.io/v2/senzing/postgresql-client/tags/list?n=1000: UNAUTHORIZED: authentication required; [map[Action:pull Class: Name:senzing/postgresql-client Type:repository]] | crane ls |
| registry | `joxit/docker-registry-ui:2.5.6-debian` | `joxit/docker-registry-ui:2.6.0-debian` | update | high | newer compatible semver tag found | crane ls |
| registry | `registry:2.8.3` | `registry:3.1.1` | update | high | newer compatible semver tag found | crane ls |
| rocketchat | `mongo:6.0` |  | manual | low | unsupported tag family | tag parser |
| rocketchat | `registry.rocket.chat/rocketchat/rocket.chat:7.9.0` | `registry.rocket.chat/rocketchat/rocket.chat:8.5.1` | update | high | newer compatible semver tag found | crane ls |
| rocketchat-micro | `mongo:6.0` |  | manual | low | unsupported tag family | tag parser |
| rocketchat-micro | `nats:2.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| rocketchat-micro | `natsio/nats-server-config-reloader:0.6.3` | `natsio/nats-server-config-reloader:0.23.0` | update | high | newer compatible semver tag found | crane ls |
| rocketchat-micro | `rocketchat/account-service:7.9.0` | `rocketchat/account-service:8.5.1` | update | high | newer compatible semver tag found | crane ls |
| rocketchat-micro | `rocketchat/authorization-service:7.9.0` | `rocketchat/authorization-service:8.5.1` | update | high | newer compatible semver tag found | crane ls |
| rocketchat-micro | `rocketchat/ddp-streamer-service:7.9.0` | `rocketchat/ddp-streamer-service:8.5.1` | update | high | newer compatible semver tag found | crane ls |
| rocketchat-micro | `rocketchat/presence-service:7.9.0` | `rocketchat/presence-service:8.5.1` | update | high | newer compatible semver tag found | crane ls |
| rocketchat-micro | `rocketchat/rocket.chat:7.9.0` | `rocketchat/rocket.chat:8.5.1` | update | high | newer compatible semver tag found | crane ls |
| rocketchat-micro | `rocketchat/stream-hub-service:7.9.0` | `rocketchat/stream-hub-service:7.13.9` | update | high | newer compatible semver tag found | crane ls |
| rsshub | `browserless/chrome:1.61.1-chrome-stable` |  | skip | high | no newer compatible tag found | crane ls |
| rsshub | `diygod/rsshub:2024-07-06` | `diygod/rsshub:2026-06-24` | update | medium | newer compatible date tag found | crane ls |
| rustdesk | `rustdesk/rustdesk-server-s6:1.1.15` |  | skip | high | no newer compatible tag found | crane ls |
| rustfs | `busybox` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| rustfs | `rustfs/rustfs:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| rybbit | `clickhouse/clickhouse-server:25.4.2` | `clickhouse/clickhouse-server:26.5.3` | update | high | newer compatible semver tag found | crane ls |
| rybbit | `ghcr.io/rybbit-io/rybbit-backend:sha-aa404ba` |  | manual | low | unsupported tag family | tag parser |
| rybbit | `ghcr.io/rybbit-io/rybbit-client:sha-aa404ba` |  | manual | low | unsupported tag family | tag parser |
| rybbit | `postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| s-pdf | `alpine` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| s-pdf | `ghcr.io/stirling-tools/stirling-pdf:1.2.0-fat` | `ghcr.io/stirling-tools/stirling-pdf:2.13.2-fat` | update | high | newer compatible semver tag found | crane ls |
| s-pdf | `postgres:14-alpine` |  | manual | low | unsupported tag family | tag parser |
| samarium | `ghcr.io/yangchuansheng/samarium:0.0.0-9514fcadb867` |  | skip | high | no newer compatible tag found | crane ls |
| signoz | `busybox` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| signoz | `busybox:1.28` |  | manual | low | unsupported tag family | tag parser |
| signoz | `clickhouse/clickhouse-server:25.5.6` | `clickhouse/clickhouse-server:26.5.3` | update | high | newer compatible semver tag found | crane ls |
| signoz | `signoz/signoz-otel-collector:v0.144.2` | `signoz/signoz-otel-collector:v0.144.5` | update | high | newer compatible semver tag found | crane ls |
| signoz | `signoz/signoz:v0.117.0` | `signoz/signoz:v0.130.1` | update | high | newer compatible semver tag found | crane ls |
| signoz | `signoz/zookeeper:3.7.1` | `signoz/zookeeper:3.9.3` | update | high | newer compatible semver tag found | crane ls |
| sillytavern | `ghcr.io/sillytavern/sillytavern:1.18.0` |  | skip | high | no newer compatible tag found | crane ls |
| skardi | `ghcr.io/skardilabs/skardi/skardi-server:0.3.0` | `ghcr.io/skardilabs/skardi/skardi-server:0.4.0` | update | high | newer compatible semver tag found | crane ls |
| stalwart | `public.ecr.aws/docker/library/postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| stalwart | `stalwartlabs/stalwart:v0.16.7` | `stalwartlabs/stalwart:v0.16.10` | update | high | newer compatible semver tag found | crane ls |
| steel-browser | `ghcr.io/steel-dev/steel-browser@sha256:cbf4a44d575c0ae83d00d4ba6bb455d24980de0ced2b06fe8b890e835c923bd1` |  | manual | low | digest-only image requires manual release check | image digest |
| strapi | `postgres:14-alpine` |  | manual | low | unsupported tag family | tag parser |
| strapi | `vshadbolt/strapi:5.33.0` | `vshadbolt/strapi:5.49.0` | update | high | newer compatible semver tag found | crane ls |
| sub2api | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| sub2api | `weishaw/sub2api:0.1.104` | `weishaw/sub2api:0.1.138` | update | high | newer compatible semver tag found | crane ls |
| supabase | `darthsim/imgproxy:v3.30.1` | `darthsim/imgproxy:v4.0.6` | update | high | newer compatible semver tag found | crane ls |
| supabase | `kong:2.8.1` | `kong:3.9.3` | update | high | newer compatible semver tag found | crane ls |
| supabase | `postgres:16.4` |  | manual | low | unsupported tag family | tag parser |
| supabase | `postgrest/postgrest@sha256:b574528fe109c8343c1247155734d03df8c34b462f342dca0ccc20244fc36ef9` |  | manual | low | digest-only image requires manual release check | image digest |
| supabase | `supabase/edge-runtime:v1.70.3` | `supabase/edge-runtime:v1.74.2` | update | high | newer compatible semver tag found | crane ls |
| supabase | `supabase/gotrue:v2.186.0` | `supabase/gotrue:v2.191.0` | update | high | newer compatible semver tag found | crane ls |
| supabase | `supabase/logflare:1.31.2` | `supabase/logflare:1.45.4` | update | high | newer compatible semver tag found | crane ls |
| supabase | `supabase/postgres-meta:v0.95.2` | `supabase/postgres-meta:v0.96.6` | update | high | newer compatible semver tag found | crane ls |
| supabase | `supabase/realtime:v2.76.5` | `supabase/realtime:v2.111.7` | update | high | newer compatible semver tag found | crane ls |
| supabase | `supabase/storage-api:v1.37.8` | `supabase/storage-api:v1.61.3` | update | high | newer compatible semver tag found | crane ls |
| supabase | `supabase/studio:2026.02.16-sha-26c615c` | `supabase/studio:2026.06.22-sha-2207d7f` | update | medium | newer compatible date tag found | crane ls |
| supabase | `supabase/supavisor:2.7.4` | `supabase/supavisor:2.9.7` | update | high | newer compatible semver tag found | crane ls |
| supabase | `timberio/vector:0.53.0-alpine` | `timberio/vector:0.56.0-alpine` | update | high | newer compatible semver tag found | crane ls |
| surveyking | `joseluisq/mysql-client:8.0.30` | `joseluisq/mysql-client:8.0.44` | update | high | newer compatible semver tag found | crane ls |
| surveyking | `surveyking/surveyking:v1.9.0` | `surveyking/surveyking:v1.12.0` | update | high | newer compatible semver tag found | crane ls |
| tailchat | `minio/minio` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| tailchat | `moonrailgun/tailchat:1.11.5` | `moonrailgun/tailchat:1.11.11` | update | high | newer compatible semver tag found | crane ls |
| teable | `registry.cn-shenzhen.aliyuncs.com/teable/teable-ee:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| teable | `senzing/postgresql-client:2.2.4` |  | blocked | low | Error: reading tags for index.docker.io/senzing/postgresql-client: GET https://index.docker.io/v2/senzing/postgresql-client/tags/list?n=1000: UNAUTHORIZED: authentication required; [map[Action:pull Class: Name:senzing/postgresql-client Type:repository]] | crane ls |
| tentix | `limbo2342/tentix:dev-2025-10-23-x.3` |  | manual | low | unsupported tag family | tag parser |
| tentix | `limbo2342/tentix:migrate.10.22.x1` |  | manual | low | unsupported tag family | tag parser |
| tianji | `moonrailgun/tianji:1.18.5` | `moonrailgun/tianji:1.32.7` | update | high | newer compatible semver tag found | crane ls |
| tianji | `senzing/postgresql-client:2.2.4` |  | blocked | low | Error: reading tags for index.docker.io/senzing/postgresql-client: GET https://index.docker.io/v2/senzing/postgresql-client/tags/list?n=1000: UNAUTHORIZED: authentication required; [map[Action:pull Class: Name:senzing/postgresql-client Type:repository]] | crane ls |
| tolgee | `senzing/postgresql-client:2.2.4` |  | blocked | low | Error: reading tags for index.docker.io/senzing/postgresql-client: GET https://index.docker.io/v2/senzing/postgresql-client/tags/list?n=1000: UNAUTHORIZED: authentication required; [map[Action:pull Class: Name:senzing/postgresql-client Type:repository]] | crane ls |
| tolgee | `tolgee/tolgee:v3.113.0` | `tolgee/tolgee:v3.205.5` | update | high | newer compatible semver tag found | crane ls |
| tooljet | `postgres:16-alpine` |  | manual | low | unsupported tag family | tag parser |
| tooljet | `postgrest/postgrest:v12.0.2` | `postgrest/postgrest:v13.0.8` | update | high | newer compatible semver tag found | crane ls |
| tooljet | `tooljet/tooljet-ce:v3.20.170-lts` | `tooljet/tooljet-ce:v3.20.186-lts` | update | high | newer compatible semver tag found | crane ls |
| tududi | `chrisvel/tududi:1.1.0` | `chrisvel/tududi:1.1.1` | update | high | newer compatible semver tag found | crane ls |
| twenty | `busybox:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| twenty | `postgres:14-alpine` |  | manual | low | unsupported tag family | tag parser |
| twenty | `twentycrm/twenty:v1.12.0` | `twentycrm/twenty:v2.16.0` | update | high | newer compatible semver tag found | crane ls |
| typebot | `axllent/mailpit:v1.30.1` | `axllent/mailpit:v1.30.2` | update | high | newer compatible semver tag found | crane ls |
| typebot | `baptistearno/typebot-builder:3.17.1` | `baptistearno/typebot-builder:3.17.2` | update | high | newer compatible semver tag found | crane ls |
| typebot | `baptistearno/typebot-viewer:3.17.1` | `baptistearno/typebot-viewer:3.17.2` | update | high | newer compatible semver tag found | crane ls |
| typebot | `public.ecr.aws/docker/library/postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| typebot | `public.ecr.aws/docker/library/redis:7.2.7-alpine` | `public.ecr.aws/docker/library/redis:8.8.0-alpine` | update | high | newer compatible semver tag found | crane ls |
| typesense | `typesense/typesense:29.0` |  | manual | low | unsupported tag family | tag parser |
| typo3 | `martinhelmich/typo3:13.4@sha256:7436d068b583c1dae2dd37ebca973b957de5371fe2acfdf9239598c3a8dbda25` |  | manual | low | unsupported tag family | tag parser |
| typo3 | `mysql:8.0.30` | `mysql:9.7.1` | update | high | newer compatible semver tag found | crane ls |
| ubuntu-sshd | `takeyamajp/ubuntu-sshd:ubuntu22.04` |  | manual | low | unsupported tag family | tag parser |
| umami | `ghcr.io/umami-software/umami:3.0.2` | `ghcr.io/umami-software/umami:3.2.0` | update | high | newer compatible semver tag found | crane ls |
| umami | `postgres:14-alpine` |  | manual | low | unsupported tag family | tag parser |
| uptime-kuma | `louislam/uptime-kuma:1.23.13` | `louislam/uptime-kuma:2.4.0` | update | high | newer compatible semver tag found | crane ls |
| vaultwarden | `vaultwarden/server:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| waha | `devlikeapro/waha:chrome-2026.5.1` |  | manual | low | unsupported tag family | tag parser |
| waha | `public.ecr.aws/docker/library/postgres:16.4-alpine` |  | manual | low | unsupported tag family | tag parser |
| webos | `fs185085781/webos:v1.4.1` | `fs185085781/webos:v1.4.4` | update | high | newer compatible semver tag found | crane ls |
| wechat | `ricwang/docker-wechat:4.0.0.30` |  | manual | low | unsupported tag family | tag parser |
| wechat2rss | `ttttmr/wechat2rss:latest` |  | manual | low | floating or missing tag requires manual pinning | image tag |
| wewe-rss | `cooderl/wewe-rss:v2.6.1` |  | skip | high | no newer compatible tag found | crane ls |
| wewe-rss | `joseluisq/mysql-client:8.0.30` | `joseluisq/mysql-client:8.0.44` | update | high | newer compatible semver tag found | crane ls |
| woocommerce | `mysql:8.0.30` | `mysql:9.7.1` | update | high | newer compatible semver tag found | crane ls |
| woocommerce | `wordpress:6.9.1-php8.3-apache` | `wordpress:7.0.0-php8.5-apache` | update | high | newer compatible semver tag found | crane ls |
| woocommerce | `wordpress:cli-2.9.0-php8.3` |  | manual | low | unsupported tag family | tag parser |
| wordpress | `wordpress:6.5.4` | `wordpress:7.0.0` | update | high | newer compatible semver tag found | crane ls |
| wrenai | `ghcr.io/canner/wren-ai-service:0.15.17` | `ghcr.io/canner/wren-ai-service:0.29.3` | update | high | newer compatible semver tag found | crane ls |
| wrenai | `ghcr.io/canner/wren-bootstrap:0.1.5` |  | skip | high | no newer compatible tag found | crane ls |
| wrenai | `ghcr.io/canner/wren-engine-ibis:0.14.3` | `ghcr.io/canner/wren-engine-ibis:0.25.0` | update | high | newer compatible semver tag found | crane ls |
| wrenai | `ghcr.io/canner/wren-engine:0.14.3` | `ghcr.io/canner/wren-engine:0.24.6` | update | high | newer compatible semver tag found | crane ls |
| wrenai | `ghcr.io/canner/wren-ui:0.20.1` | `ghcr.io/canner/wren-ui:0.32.2` | update | high | newer compatible semver tag found | crane ls |
| wrenai | `qdrant/qdrant:v1.13.4` | `qdrant/qdrant:v1.18.2` | update | high | newer compatible semver tag found | crane ls |
| wrenai | `senzing/postgresql-client:2.2.4` |  | blocked | low | Error: reading tags for index.docker.io/senzing/postgresql-client: GET https://index.docker.io/v2/senzing/postgresql-client/tags/list?n=1000: UNAUTHORIZED: authentication required; [map[Action:pull Class: Name:senzing/postgresql-client Type:repository]] | crane ls |
| yourls | `mysql:8.0.30` | `mysql:9.7.1` | update | high | newer compatible semver tag found | crane ls |
| yourls | `yourls:1.10.1` | `yourls:1.10.4` | update | high | newer compatible semver tag found | crane ls |
| zitadel | `ghcr.io/zitadel/zitadel:v4.10.1` | `ghcr.io/zitadel/zitadel:v4.15.3` | update | high | newer compatible semver tag found | crane ls |
| zot | `ghcr.io/project-zot/zot:v2.1.14` | `ghcr.io/project-zot/zot:v2.1.18` | update | high | newer compatible semver tag found | crane ls |
| zot | `httpd:2.4.63-alpine3.22` | `httpd:2.4.68-alpine3.24` | update | high | newer compatible semver tag found | crane ls |

## Record Locations

### AllinSSL: `docker.io/allinssl/allinssl`
- `originImageName` at `template/AllinSSL/index.yaml:52`

### AllinSSL: `docker.io/allinssl/allinssl:latest`
- `image` at `template/AllinSSL/index.yaml:70`

### OpenDeepWiki: `${{ inputs.wiki_image }}`
- `originImageName` at `template/OpenDeepWiki/index.yaml:132`
- `image` at `template/OpenDeepWiki/index.yaml:159`

### OpenDeepWiki: `${{ inputs.wiki_web_image }}`
- `originImageName` at `template/OpenDeepWiki/index.yaml:302`
- `image` at `template/OpenDeepWiki/index.yaml:327`

### Reactive-Resume: `amruthpillai/reactive-resume:v4.1.2`
- `image` at `template/Reactive-Resume/index.yaml:351`

### Reactive-Resume: `bitnamilegacy/postgresql:latest`
- `image` at `template/Reactive-Resume/index.yaml:541`
- `image` at `template/Reactive-Resume/index.yaml:563`

### Reactive-Resume: `ghcr.io/browserless/chromium:v2.11.0`
- `image` at `template/Reactive-Resume/index.yaml:290`

### Reactive-Resume: `quay.io/minio/minio`
- `originImageName` at `template/Reactive-Resume/index.yaml:165`

### Reactive-Resume: `quay.io/minio/minio:RELEASE.2023-03-22T06-36-24Z`
- `image` at `template/Reactive-Resume/index.yaml:198`

### Readeck: `codeberg.org/readeck/readeck:0.16.0`
- `originImageName` at `template/Readeck/index.yaml:36`
- `image` at `template/Readeck/index.yaml:64`

### Ruiqi-Waf: `limbo2342/ruiqi-waf:sha-32b359f`
- `image` at `template/Ruiqi-Waf/index.yaml:164`

### ace-step: `ghcr.io/ace-step/ace-step-1.5:v0.1.0`
- `originImageName` at `template/ace-step/index.yaml:91`
- `image` at `template/ace-step/index.yaml:114`

### affine: `ghcr.io/toeverything/affine:0.26.6`
- `image` at `template/affine/index.yaml:358`
- `originImageName` at `template/affine/index.yaml:420`
- `image` at `template/affine/index.yaml:486`

### affine: `postgres:16-alpine`
- `image` at `template/affine/index.yaml:254`
- `image` at `template/affine/index.yaml:318`
- `image` at `template/affine/index.yaml:445`

### agora: `agoracn/token:0.1.2023053011`
- `originImageName` at `template/agora/index.yaml:49`
- `image` at `template/agora/index.yaml:69`

### airbyte: `airbyte/bootloader:0.63.11`
- `image` at `template/airbyte/index.yaml:371`

### airbyte: `airbyte/connector-builder-server:0.63.11`
- `originImageName` at `template/airbyte/index.yaml:422`
- `image` at `template/airbyte/index.yaml:443`

### airbyte: `airbyte/cron:0.63.11`
- `originImageName` at `template/airbyte/index.yaml:1126`
- `image` at `template/airbyte/index.yaml:1147`

### airbyte: `airbyte/server:0.63.11`
- `originImageName` at `template/airbyte/index.yaml:521`
- `image` at `template/airbyte/index.yaml:544`

### airbyte: `airbyte/webapp:0.63.11`
- `originImageName` at `template/airbyte/index.yaml:1359`
- `image` at `template/airbyte/index.yaml:1380`

### airbyte: `airbyte/worker:0.63.11`
- `originImageName` at `template/airbyte/index.yaml:813`
- `image` at `template/airbyte/index.yaml:834`

### airbyte: `docker.io/apecloud/spilo:16.4.0`
- `image` at `template/airbyte/index.yaml:328`

### airbyte: `temporalio/auto-setup:1.23.0`
- `originImageName` at `template/airbyte/index.yaml:1260`
- `image` at `template/airbyte/index.yaml:1281`

### anki-sync-server: `ghcr.io/yangchuansheng/anki-sync-server:24.06.3`
- `originImageName` at `template/anki-sync-server/index.yaml:45`
- `image` at `template/anki-sync-server/index.yaml:68`

### apitable: `apitable/backend-server:v1.13.0-beta.1_2016`
- `originImageName` at `template/apitable/index.yaml:965`
- `image` at `template/apitable/index.yaml:1013`

### apitable: `apitable/databus-server@sha256:462fa8bea11df94642b80a58d683aaf9995d79061588843a9d6b7ee66a421600`
- `originImageName` at `template/apitable/index.yaml:1458`
- `image` at `template/apitable/index.yaml:1503`

### apitable: `apitable/imageproxy-server:v0.13.4-alpha_build13`
- `originImageName` at `template/apitable/index.yaml:1587`
- `image` at `template/apitable/index.yaml:1609`

### apitable: `apitable/init-appdata@sha256:4fa2ed5d1a5a3e2f7bd449352ec3054747127aabe4f91c62fc13f4660b25558b`
- `originImageName` at `template/apitable/index.yaml:865`
- `image` at `template/apitable/index.yaml:923`

### apitable: `apitable/init-db:v1.13.0-beta.1_2016`
- `originImageName` at `template/apitable/index.yaml:761`
- `image` at `template/apitable/index.yaml:819`

### apitable: `apitable/room-server:v1.13.0-beta.1_2016`
- `originImageName` at `template/apitable/index.yaml:1170`
- `image` at `template/apitable/index.yaml:1218`

### apitable: `apitable/web-server:v1.13.0-beta.1_2016`
- `originImageName` at `template/apitable/index.yaml:1378`
- `image` at `template/apitable/index.yaml:1400`

### apitable: `busybox:1.36.1`
- `image` at `template/apitable/index.yaml:988`
- `image` at `template/apitable/index.yaml:1193`
- `image` at `template/apitable/index.yaml:1480`

### apitable: `mysql:8.0.32`
- `originImageName` at `template/apitable/index.yaml:579`
- `image` at `template/apitable/index.yaml:596`
- `image` at `template/apitable/index.yaml:779`
- `image` at `template/apitable/index.yaml:883`

### apitable: `nginx:1.27.5-alpine`
- `originImageName` at `template/apitable/index.yaml:1672`
- `image` at `template/apitable/index.yaml:1694`

### apitable: `rabbitmq:3.11.9-management`
- `originImageName` at `template/apitable/index.yaml:649`
- `image` at `template/apitable/index.yaml:674`

### appflowy: `appflowyinc/appflowy_cloud:0.15.22`
- `originImageName` at `template/appflowy/index.yaml:491`
- `image` at `template/appflowy/index.yaml:511`

### appflowy: `appflowyinc/appflowy_web:0.14.9`
- `originImageName` at `template/appflowy/index.yaml:820`
- `image` at `template/appflowy/index.yaml:840`

### appflowy: `appflowyinc/appflowy_worker:0.15.22`
- `originImageName` at `template/appflowy/index.yaml:692`
- `image` at `template/appflowy/index.yaml:712`

### appflowy: `appflowyinc/gotrue:0.15.22`
- `originImageName` at `template/appflowy/index.yaml:356`
- `image` at `template/appflowy/index.yaml:376`

### appflowy: `postgres:16.4-alpine`
- `image` at `template/appflowy/index.yaml:205`

### appsmith: `appsmith/appsmith-ce:v1.29`
- `originImageName` at `template/appsmith/index.yaml:36`
- `image` at `template/appsmith/index.yaml:59`

### artalk: `artalk/artalk-go:latest`
- `originImageName` at `template/artalk/index.yaml:43`
- `image` at `template/artalk/index.yaml:66`

### asktable: `postgres:14-alpine`
- `image` at `template/asktable/index.yaml:71`

### asktable: `registry.cn-shanghai.aliyuncs.com/datamini/asktable-all-in-one:latest`
- `image` at `template/asktable/index.yaml:113`

### asktable: `registry.cn-shanghai.aliyuncs.com/datamini/asktable-atbox:latest`
- `image` at `template/asktable/index.yaml:209`

### authentik: `ghcr.io/goauthentik/server:2025.12.3`
- `originImageName` at `template/authentik/index.yaml:175`
- `image` at `template/authentik/index.yaml:195`
- `originImageName` at `template/authentik/index.yaml:290`
- `image` at `template/authentik/index.yaml:310`

### authentik: `postgres:16.4-alpine`
- `image` at `template/authentik/index.yaml:130`

### banana-slides: `anoinex/banana-slides-backend:latest`
- `originImageName` at `template/banana-slides/index.yaml:112`
- `image` at `template/banana-slides/index.yaml:132`

### banana-slides: `anoinex/banana-slides-frontend:latest`
- `originImageName` at `template/banana-slides/index.yaml:212`
- `image` at `template/banana-slides/index.yaml:231`

### billionmail: `alpine/openssl:3.5.4`
- `image` at `template/billionmail/index.yaml:6468`

### billionmail: `alpine/socat:1.8.0.0@sha256:a6be4c0262b339c53ddad723cdd178a1a13271e1137c65e27f90a08c16de02b8`
- `image` at `template/billionmail/index.yaml:6692`
- `image` at `template/billionmail/index.yaml:6723`
- `image` at `template/billionmail/index.yaml:6755`

### billionmail: `billionmail/core:4.9.3@sha256:b97c71b463e99368f0fb50a4f3088139c2f04a37171d3b660b92f946a3076692`
- `originImageName` at `template/billionmail/index.yaml:6434`
- `image` at `template/billionmail/index.yaml:7033`

### billionmail: `billionmail/dovecot:1.6@sha256:bbf5c304f248141768d1dbdf26b190fd28b69de6969b90e994ee81f54b942fab`
- `image` at `template/billionmail/index.yaml:6822`

### billionmail: `billionmail/postfix:1.6@sha256:870656c055c83f4e4b83fcd4c2f9cecfbcd0d8e3a963ab7d0c9c88bd6b348342`
- `image` at `template/billionmail/index.yaml:6901`

### billionmail: `billionmail/rspamd:1.2@sha256:bed48c106e8b8fcbf0a133c86e90900e7e17d4dec14cc30a9ddf989ada74f058`
- `image` at `template/billionmail/index.yaml:6775`

### billionmail: `public.ecr.aws/docker/library/postgres:16.4-alpine`
- `image` at `template/billionmail/index.yaml:153`
- `image` at `template/billionmail/index.yaml:6509`

### billionmail: `python:3.12.12-alpine`
- `image` at `template/billionmail/index.yaml:6672`

### billionmail: `roundcube/roundcubemail:1.6.11-fpm-alpine`
- `image` at `template/billionmail/index.yaml:6974`

### blossom: `docker.io/arey/mysql-client:latest`
- `image` at `template/blossom/index.yaml:315`

### blossom: `jasminexzzz/blossom:1.16.0`
- `originImageName` at `template/blossom/index.yaml:46`
- `image` at `template/blossom/index.yaml:69`

### btpanel: `btpanel/baota:nas`
- `originImageName` at `template/btpanel/index.yaml:38`
- `image` at `template/btpanel/index.yaml:56`

### budibase: `budibase/apps:3.15.0`
- `originImageName` at `template/budibase/index.yaml:429`
- `image` at `template/budibase/index.yaml:449`

### budibase: `budibase/couchdb:v3.3.3-sqs-v2.1.1`
- `originImageName` at `template/budibase/index.yaml:254`
- `image` at `template/budibase/index.yaml:290`

### budibase: `budibase/proxy:3.15.0`
- `originImageName` at `template/budibase/index.yaml:821`
- `image` at `template/budibase/index.yaml:841`

### budibase: `budibase/worker:3.15.0`
- `originImageName` at `template/budibase/index.yaml:625`
- `image` at `template/budibase/index.yaml:645`

### budibase: `busybox:1.37.0`
- `image` at `template/budibase/index.yaml:276`

### bunkerweb: `docker.io/bunkerity/bunkerweb-scheduler:1.6.11`
- `originImageName` at `template/bunkerweb/index.yaml:607`
- `image` at `template/bunkerweb/index.yaml:680`

### bunkerweb: `docker.io/bunkerity/bunkerweb-ui:1.6.11`
- `originImageName` at `template/bunkerweb/index.yaml:855`
- `image` at `template/bunkerweb/index.yaml:937`

### bunkerweb: `docker.io/bunkerity/bunkerweb:1.6.11`
- `originImageName` at `template/bunkerweb/index.yaml:418`
- `image` at `template/bunkerweb/index.yaml:511`

### bunkerweb: `docker.io/library/busybox:1.36.1`
- `image` at `template/bunkerweb/index.yaml:487`
- `image` at `template/bunkerweb/index.yaml:633`
- `image` at `template/bunkerweb/index.yaml:656`

### bunkerweb: `docker.io/library/postgres:16.4-alpine`
- `image` at `template/bunkerweb/index.yaml:174`
- `image` at `template/bunkerweb/index.yaml:446`
- `image` at `template/bunkerweb/index.yaml:881`

### bunkerweb: `docker.io/traefik/whoami:v1.11.0`
- `originImageName` at `template/bunkerweb/index.yaml:349`
- `image` at `template/bunkerweb/index.yaml:369`

### bytebase: `bytebase/bytebase:3.6.1`
- `originImageName` at `template/bytebase/index.yaml:45`
- `image` at `template/bytebase/index.yaml:68`

### calcom: `calcom.docker.scarf.sh/calcom/cal.com:v6.2.0`
- `originImageName` at `template/calcom/index.yaml:217`
- `image` at `template/calcom/index.yaml:237`

### calcom: `public.ecr.aws/docker/library/postgres:16.4-alpine`
- `image` at `template/calcom/index.yaml:173`

### cap: `ghcr.io/capsoftware/cap-media-server@sha256:243b69c5d8b132a425641b6e6ada79c119467cc88a6b9446dd4f8dea6b579fad`
- `originImageName` at `template/cap/index.yaml:342`
- `image` at `template/cap/index.yaml:362`

### cap: `ghcr.io/capsoftware/cap-web@sha256:8d2e21251b404e2b15772ded7bbf129cf980e6446102ea9b1326567647891e57`
- `originImageName` at `template/cap/index.yaml:207`
- `image` at `template/cap/index.yaml:227`

### cap: `mysql:8.0.46-debian`
- `image` at `template/cap/index.yaml:165`

### casdoor: `casbin/casdoor:v1.702.0`
- `image` at `template/casdoor/index.yaml:425`

### casdoor: `casbin/casdoor:v2.32.0`
- `originImageName` at `template/casdoor/index.yaml:334`
- `image` at `template/casdoor/index.yaml:355`

### casdoor: `mysql:8.0`
- `image` at `template/casdoor/index.yaml:165`

### casdoor: `postgres:14-alpine`
- `image` at `template/casdoor/index.yaml:308`

### changedetection: `ghcr.io/dgtlmoon/changedetection.io:0.50.43`
- `originImageName` at `template/changedetection/index.yaml:43`
- `image` at `template/changedetection/index.yaml:64`

### chatany: `licoy/chatany:v3.5.0`
- `originImageName` at `template/chatany/index.yaml:81`
- `image` at `template/chatany/index.yaml:106`

### chatbot-ui: `ghcr.io/mckaywrigley/chatbot-ui:main`
- `originImageName` at `template/chatbot-ui/index.yaml:41`
- `image` at `template/chatbot-ui/index.yaml:66`

### chatgpt-next-web: `yidadaa/chatgpt-next-web:v2.12.4`
- `originImageName` at `template/chatgpt-next-web/index.yaml:89`
- `image` at `template/chatgpt-next-web/index.yaml:114`

### chatgpt-on-wechat: `zhayujie/chatgpt-on-wechat:1.6.8`
- `originImageName` at `template/chatgpt-on-wechat/index.yaml:78`
- `image` at `template/chatgpt-on-wechat/index.yaml:98`

### chatgpt-web: `chenzhaoyu94/chatgpt-web`
- `originImageName` at `template/chatgpt-web/index.yaml:83`
- `image` at `template/chatgpt-web/index.yaml:108`

### chatnio: `joseluisq/mysql-client:8.0.30`
- `image` at `template/chatnio/index.yaml:290`

### chatnio: `programzmh/chatnio@sha256:97587b5cdd85a4f5a9aee509304c594c9d66fa5f71b2164b78c064cec9feed2d`
- `originImageName` at `template/chatnio/index.yaml:37`
- `image` at `template/chatnio/index.yaml:60`

### chatwoot: `chatwoot/chatwoot:v4.7.0`
- `image` at `template/chatwoot/index.yaml:171`
- `originImageName` at `template/chatwoot/index.yaml:383`
- `image` at `template/chatwoot/index.yaml:404`
- `originImageName` at `template/chatwoot/index.yaml:507`
- `image` at `template/chatwoot/index.yaml:528`

### chatwoot: `postgres:14-alpine`
- `image` at `template/chatwoot/index.yaml:141`

### chrome: `lscr.io/linuxserver/chrome:148.0.7778.178-1-ls95`
- `originImageName` at `template/chrome/index.yaml:75`
- `image` at `template/chrome/index.yaml:104`

### cloudreve: `arey/mysql-client:latest`
- `image` at `template/cloudreve/index.yaml:77`

### cloudreve: `cloudreve/cloudreve`
- `originImageName` at `template/cloudreve/index.yaml:54`
- `image` at `template/cloudreve/index.yaml:109`

### cobalt: `ghcr.io/imputnet/cobalt:7.13.3`
- `originImageName` at `template/cobalt/index.yaml:62`
- `image` at `template/cobalt/index.yaml:83`

### code-server: `codercom/code-server:4.90.3-39`
- `originImageName` at `template/code-server/index.yaml:45`
- `image` at `template/code-server/index.yaml:72`

### coze-studio: `alpine/curl:8.12.1`
- `image` at `template/coze-studio/index.yaml:1042`

### coze-studio: `alpine/git@sha256:d453f54c83320412aa89c391b076930bd8569bc1012285e8c68ce2d4435826a3`
- `image` at `template/coze-studio/index.yaml:915`

### coze-studio: `bitnamilegacy/elasticsearch:8.18.0`
- `originImageName` at `template/coze-studio/index.yaml:633`
- `image` at `template/coze-studio/index.yaml:666`

### coze-studio: `bitnamilegacy/etcd@sha256:1b9977cf4cce7546873e0ee50e684c38a38a4e7a27d22086fbd2b8a1b44a69d0`
- `originImageName` at `template/coze-studio/index.yaml:518`
- `image` at `template/coze-studio/index.yaml:551`

### coze-studio: `busybox:1.36.1`
- `image` at `template/coze-studio/index.yaml:540`
- `image` at `template/coze-studio/index.yaml:655`
- `image` at `template/coze-studio/index.yaml:908`
- `image` at `template/coze-studio/index.yaml:982`
- `image` at `template/coze-studio/index.yaml:989`
- `image` at `template/coze-studio/index.yaml:996`
- `image` at `template/coze-studio/index.yaml:1148`

### coze-studio: `cozedev/coze-studio-server:0.5.1`
- `originImageName` at `template/coze-studio/index.yaml:888`
- `image` at `template/coze-studio/index.yaml:1156`

### coze-studio: `cozedev/coze-studio-web:0.5.1`
- `originImageName` at `template/coze-studio/index.yaml:1361`
- `image` at `template/coze-studio/index.yaml:1379`

### coze-studio: `milvusdb/milvus:v2.5.10`
- `originImageName` at `template/coze-studio/index.yaml:755`
- `image` at `template/coze-studio/index.yaml:775`

### coze-studio: `minio/mc:RELEASE.2025-05-21T01-59-54Z-cpuv1`
- `image` at `template/coze-studio/index.yaml:1003`

### coze-studio: `mysql:8.0.36`
- `image` at `template/coze-studio/index.yaml:937`

### coze-studio: `nsqio/nsq:v1.2.1`
- `originImageName` at `template/coze-studio/index.yaml:378`
- `image` at `template/coze-studio/index.yaml:394`
- `originImageName` at `template/coze-studio/index.yaml:447`
- `image` at `template/coze-studio/index.yaml:463`

### crmeb: `ghcr.io/yangchuansheng/crmeb:v5.4.0`
- `originImageName` at `template/crmeb/index.yaml:350`
- `image` at `template/crmeb/index.yaml:373`
- `image` at `template/crmeb/index.yaml:404`

### crmeb: `joseluisq/mysql-client:8.0.30`
- `image` at `template/crmeb/index.yaml:129`

### crmeb: `nginx:alpine3.20`
- `image` at `template/crmeb/index.yaml:381`

### cronicle: `soulteary/cronicle:0.9.46`
- `originImageName` at `template/cronicle/index.yaml:34`
- `image` at `template/cronicle/index.yaml:62`

### dataease: `busybox:1.36.1`
- `image` at `template/dataease/index.yaml:63`

### dataease: `docker.io/arey/mysql-client:latest`
- `image` at `template/dataease/index.yaml:358`

### dataease: `registry.cn-qingdao.aliyuncs.com/dataease/dataease:v2.10.12`
- `originImageName` at `template/dataease/index.yaml:39`
- `image` at `template/dataease/index.yaml:113`

### dbgate: `dbgate/dbgate:5.3.1-alpine`
- `originImageName` at `template/dbgate/index.yaml:50`
- `image` at `template/dbgate/index.yaml:78`

### deeplx: `ghcr.io/owo-network/deeplx:v0.9.5`
- `originImageName` at `template/deeplx/index.yaml:40`
- `image` at `template/deeplx/index.yaml:65`

### derper: `bitnamilegacy/kubectl:1.28.9`
- `image` at `template/derper/index.yaml:196`

### derper: `ghcr.io/yangchuansheng/derper:v1.99.0-pre`
- `originImageName` at `template/derper/index.yaml:110`
- `image` at `template/derper/index.yaml:132`

### dify: `busybox:1.37.0`
- `image` at `template/dify/index.yaml:112`

### dify: `langgenius/dify-api:1.11.2`
- `originImageName` at `template/dify/index.yaml:54`
- `image` at `template/dify/index.yaml:131`
- `image` at `template/dify/index.yaml:273`

### dify: `langgenius/dify-plugin-daemon:0.5.2-local`
- `originImageName` at `template/dify/index.yaml:681`
- `image` at `template/dify/index.yaml:740`

### dify: `langgenius/dify-sandbox:0.2.12`
- `originImageName` at `template/dify/index.yaml:601`
- `image` at `template/dify/index.yaml:624`

### dify: `langgenius/dify-web:1.11.2`
- `originImageName` at `template/dify/index.yaml:414`
- `image` at `template/dify/index.yaml:470`

### dify: `postgres:14-alpine`
- `image` at `template/dify/index.yaml:77`
- `image` at `template/dify/index.yaml:434`
- `image` at `template/dify/index.yaml:704`
- `image` at `template/dify/index.yaml:965`

### dify: `semitechnologies/weaviate:1.27.0`
- `originImageName` at `template/dify/index.yaml:1120`
- `image` at `template/dify/index.yaml:1141`

### directus: `directus/directus:11.17.4`
- `originImageName` at `template/directus/index.yaml:332`
- `image` at `template/directus/index.yaml:449`

### directus: `public.ecr.aws/docker/library/busybox:1.36.1`
- `image` at `template/directus/index.yaml:357`

### directus: `public.ecr.aws/docker/library/postgres:16.4-alpine`
- `image` at `template/directus/index.yaml:165`
- `image` at `template/directus/index.yaml:380`

### directus: `public.ecr.aws/docker/library/redis:7.2.7-alpine`
- `image` at `template/directus/index.yaml:421`

### docker-stacks: `jupyter/scipy-notebook:2023-10-20`
- `originImageName` at `template/docker-stacks/index.yaml:36`
- `image` at `template/docker-stacks/index.yaml:57`

### docuseal: `docuseal/docuseal:3.0.1`
- `originImageName` at `template/docuseal/index.yaml:184`
- `image` at `template/docuseal/index.yaml:207`

### docuseal: `postgres:16-alpine`
- `image` at `template/docuseal/index.yaml:139`

### dolibarr: `dolibarr/dolibarr:23.0.3-php8.2@sha256:c3c17731287f1a6a30ec7e0a3e7a82adda7bc93abd79af94714709704c8a4865`
- `originImageName` at `template/dolibarr/index.yaml:213`
- `image` at `template/dolibarr/index.yaml:234`

### dolibarr: `mysql:8.0.30`
- `image` at `template/dolibarr/index.yaml:161`

### drawdb: `ghcr.io/drawdb-io/drawdb:v1.5.0`
- `originImageName` at `template/drawdb/index.yaml:60`
- `image` at `template/drawdb/index.yaml:81`

### drizzle-studio: `ghcr.io/drizzle-team/gateway:latest`
- `originImageName` at `template/drizzle-studio/index.yaml:42`
- `image` at `template/drizzle-studio/index.yaml:63`

### eaglercraft-server: `ghcr.io/yangchuansheng/eaglerx1.8server:1.12.1`
- `originImageName` at `template/eaglercraft-server/index.yaml:40`
- `image` at `template/eaglercraft-server/index.yaml:67`

### edgequake: `ghcr.io/raphaelmansuy/edgequake-frontend:0.12.2`
- `originImageName` at `template/edgequake/index.yaml:380`
- `image` at `template/edgequake/index.yaml:400`

### edgequake: `ghcr.io/raphaelmansuy/edgequake:0.12.2`
- `originImageName` at `template/edgequake/index.yaml:282`
- `image` at `template/edgequake/index.yaml:302`

### edgequake: `postgres:16-alpine`
- `image` at `template/edgequake/index.yaml:163`

### elasticsearch: `busybox:1.37.0`
- `image` at `template/elasticsearch/index.yaml:63`

### elasticsearch: `docker.elastic.co/elasticsearch/elasticsearch:9.4.1`
- `originImageName` at `template/elasticsearch/index.yaml:37`
- `image` at `template/elasticsearch/index.yaml:84`

### emqx: `emqx/emqx:5.8.9`
- `originImageName` at `template/emqx/index.yaml:57`
- `image` at `template/emqx/index.yaml:91`

### enshrouded: `alpine`
- `image` at `template/enshrouded/index.yaml:90`

### enshrouded: `bitnamilegacy/kubectl`
- `image` at `template/enshrouded/index.yaml:102`
- `image` at `template/enshrouded/index.yaml:211`

### enshrouded: `registry.cn-hangzhou.aliyuncs.com/luanshaotong/enshrouded:v0.2`
- `originImageName` at `template/enshrouded/index.yaml:68`
- `image` at `template/enshrouded/index.yaml:143`

### erpnext: `frappe/erpnext:v16.21.1`
- `image` at `template/erpnext/index.yaml:374`
- `image` at `template/erpnext/index.yaml:530`
- `originImageName` at `template/erpnext/index.yaml:666`
- `image` at `template/erpnext/index.yaml:731`
- `originImageName` at `template/erpnext/index.yaml:786`
- `image` at `template/erpnext/index.yaml:882`
- `originImageName` at `template/erpnext/index.yaml:962`
- `image` at `template/erpnext/index.yaml:1027`
- `originImageName` at `template/erpnext/index.yaml:1118`
- `image` at `template/erpnext/index.yaml:1214`
- `originImageName` at `template/erpnext/index.yaml:1275`
- `image` at `template/erpnext/index.yaml:1371`
- `originImageName` at `template/erpnext/index.yaml:1432`
- `image` at `template/erpnext/index.yaml:1497`

### erpnext: `mariadb:11.4.7`
- `originImageName` at `template/erpnext/index.yaml:66`
- `image` at `template/erpnext/index.yaml:89`

### erpnext: `public.ecr.aws/docker/library/busybox:1.36.1`
- `image` at `template/erpnext/index.yaml:319`
- `image` at `template/erpnext/index.yaml:475`
- `image` at `template/erpnext/index.yaml:687`
- `image` at `template/erpnext/index.yaml:710`
- `image` at `template/erpnext/index.yaml:807`
- `image` at `template/erpnext/index.yaml:861`
- `image` at `template/erpnext/index.yaml:983`
- `image` at `template/erpnext/index.yaml:1006`
- `image` at `template/erpnext/index.yaml:1139`
- `image` at `template/erpnext/index.yaml:1193`
- `image` at `template/erpnext/index.yaml:1296`
- `image` at `template/erpnext/index.yaml:1350`
- `image` at `template/erpnext/index.yaml:1453`
- `image` at `template/erpnext/index.yaml:1476`

### erpnext: `public.ecr.aws/docker/library/redis:7.2.7-alpine`
- `image` at `template/erpnext/index.yaml:342`
- `image` at `template/erpnext/index.yaml:498`
- `image` at `template/erpnext/index.yaml:830`
- `image` at `template/erpnext/index.yaml:1162`
- `image` at `template/erpnext/index.yaml:1319`

### ever-gauzy: `busybox:1.36.1`
- `image` at `template/ever-gauzy/index.yaml:208`

### ever-gauzy: `ghcr.io/ever-co/gauzy-api-demo@sha256:9c7efab08c8f48892486099e0cd6edda4eddfa27743b09dd953145d8ff5a5cc4`
- `originImageName` at `template/ever-gauzy/index.yaml:186`
- `image` at `template/ever-gauzy/index.yaml:271`

### ever-gauzy: `ghcr.io/ever-co/gauzy-webapp-demo@sha256:6370fc7dcc8eeba67cc75f8a88afb9f85552be1602769af78d4da0c23f42e493`
- `originImageName` at `template/ever-gauzy/index.yaml:516`
- `image` at `template/ever-gauzy/index.yaml:537`

### ever-gauzy: `postgres:16.4-alpine`
- `image` at `template/ever-gauzy/index.yaml:149`
- `image` at `template/ever-gauzy/index.yaml:228`

### evolution-api: `evoapicloud/evolution-api:v2.3.7`
- `originImageName` at `template/evolution-api/index.yaml:315`
- `image` at `template/evolution-api/index.yaml:424`

### evolution-api: `public.ecr.aws/docker/library/busybox:1.36.1`
- `image` at `template/evolution-api/index.yaml:340`

### evolution-api: `public.ecr.aws/docker/library/postgres:16.4-alpine`
- `image` at `template/evolution-api/index.yaml:152`
- `image` at `template/evolution-api/index.yaml:361`

### evolution-api: `public.ecr.aws/docker/library/redis:7.2.7-alpine`
- `image` at `template/evolution-api/index.yaml:393`

### excalidraw: `excalidraw/excalidraw@sha256:36cd9a135e25b17e7e0b1b1d64df5fc1dad651eac72b6f2aa9c1d5401eddc68f`
- `originImageName` at `template/excalidraw/index.yaml:36`
- `image` at `template/excalidraw/index.yaml:63`

### fast-poster: `fastposter/fastposter:latest`
- `originImageName` at `template/fast-poster/index.yaml:34`
- `image` at `template/fast-poster/index.yaml:52`

### fastgpt: `postgres:16-alpine`
- `image` at `template/fastgpt/index.yaml:369`

### fastgpt: `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-code-sandbox:v4.14.22`
- `originImageName` at `template/fastgpt/index.yaml:1013`
- `image` at `template/fastgpt/index.yaml:1033`

### fastgpt: `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-mcp_server:v4.14.22`
- `originImageName` at `template/fastgpt/index.yaml:1126`
- `image` at `template/fastgpt/index.yaml:1146`

### fastgpt: `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-plugin:v0.6.2`
- `originImageName` at `template/fastgpt/index.yaml:852`
- `image` at `template/fastgpt/index.yaml:872`

### fastgpt: `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt:v4.14.22`
- `originImageName` at `template/fastgpt/index.yaml:562`
- `image` at `template/fastgpt/index.yaml:582`

### fastgpt: `registry.cn-hangzhou.aliyuncs.com/labring/aiproxy:v0.5.8`
- `originImageName` at `template/fastgpt/index.yaml:1238`
- `image` at `template/fastgpt/index.yaml:1258`

### fastgpt-milvus: `postgres:16-alpine`
- `image` at `template/fastgpt-milvus/index.yaml:1176`

### fastgpt-milvus: `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-code-sandbox:v4.14.22`
- `originImageName` at `template/fastgpt-milvus/index.yaml:678`
- `image` at `template/fastgpt-milvus/index.yaml:704`

### fastgpt-milvus: `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-mcp_server:v4.14.22`
- `originImageName` at `template/fastgpt-milvus/index.yaml:774`
- `image` at `template/fastgpt-milvus/index.yaml:800`

### fastgpt-milvus: `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-plugin:v0.6.2`
- `originImageName` at `template/fastgpt-milvus/index.yaml:417`
- `image` at `template/fastgpt-milvus/index.yaml:443`

### fastgpt-milvus: `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt:v4.14.22`
- `originImageName` at `template/fastgpt-milvus/index.yaml:136`
- `image` at `template/fastgpt-milvus/index.yaml:156`

### fastgpt-milvus: `registry.cn-hangzhou.aliyuncs.com/labring/aiproxy:v0.5.8`
- `originImageName` at `template/fastgpt-milvus/index.yaml:580`
- `image` at `template/fastgpt-milvus/index.yaml:606`

### fastgpt-pro: `postgres:16-alpine`
- `image` at `template/fastgpt-pro/index.yaml:370`

### fastgpt-pro: `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-code-sandbox:v4.14.22`
- `originImageName` at `template/fastgpt-pro/index.yaml:1161`
- `image` at `template/fastgpt-pro/index.yaml:1181`

### fastgpt-pro: `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-mcp_server:v4.14.22`
- `originImageName` at `template/fastgpt-pro/index.yaml:1274`
- `image` at `template/fastgpt-pro/index.yaml:1294`

### fastgpt-pro: `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-plugin:v0.6.2`
- `originImageName` at `template/fastgpt-pro/index.yaml:1000`
- `image` at `template/fastgpt-pro/index.yaml:1020`

### fastgpt-pro: `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt-pro:v4.14.22`
- `originImageName` at `template/fastgpt-pro/index.yaml:855`
- `image` at `template/fastgpt-pro/index.yaml:875`

### fastgpt-pro: `registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt:v4.14.22`
- `originImageName` at `template/fastgpt-pro/index.yaml:563`
- `image` at `template/fastgpt-pro/index.yaml:583`

### fastgpt-pro: `registry.cn-hangzhou.aliyuncs.com/labring/aiproxy:v0.5.8`
- `originImageName` at `template/fastgpt-pro/index.yaml:1386`
- `image` at `template/fastgpt-pro/index.yaml:1406`

### featbit-standard: `featbit/featbit-api-server:5.0.5`
- `originImageName` at `template/featbit-standard/index.yaml:1118`
- `image` at `template/featbit-standard/index.yaml:1179`

### featbit-standard: `featbit/featbit-data-analytics-server:5.0.5`
- `originImageName` at `template/featbit-standard/index.yaml:1247`
- `image` at `template/featbit-standard/index.yaml:1308`

### featbit-standard: `featbit/featbit-evaluation-server:5.0.5`
- `originImageName` at `template/featbit-standard/index.yaml:1370`
- `image` at `template/featbit-standard/index.yaml:1431`

### featbit-standard: `featbit/featbit-ui:5.0.5`
- `originImageName` at `template/featbit-standard/index.yaml:1497`
- `image` at `template/featbit-standard/index.yaml:1519`

### featbit-standard: `postgres:16-alpine`
- `image` at `template/featbit-standard/index.yaml:240`
- `image` at `template/featbit-standard/index.yaml:1140`
- `image` at `template/featbit-standard/index.yaml:1269`
- `image` at `template/featbit-standard/index.yaml:1392`

### filecodebox: `lanol/filecodebox@sha256:e3609361ae7dfb7b72fef94d97e58ea268b960c3dc70719b7221277612946ad2`
- `originImageName` at `template/filecodebox/index.yaml:126`
- `image` at `template/filecodebox/index.yaml:147`

### fireboom: `fireboomapi/fireboom_server@sha256:27ff832760dec9cf205f02b3516ad6663fa7cbfcf35da1b49196acd00efb598f`
- `originImageName` at `template/fireboom/index.yaml:38`
- `image` at `template/fireboom/index.yaml:61`

### firefox: `jlesage/firefox:latest`
- `originImageName` at `template/firefox/index.yaml:37`
- `image` at `template/firefox/index.yaml:60`

### flarum: `crazymax/flarum:1.8.10`
- `originImageName` at `template/flarum/index.yaml:129`
- `image` at `template/flarum/index.yaml:202`

### flarum: `mysql:8.0.30`
- `image` at `template/flarum/index.yaml:155`

### flowise: `flowiseai/flowise:3.0.5`
- `originImageName` at `template/flowise/index.yaml:195`
- `image` at `template/flowise/index.yaml:257`

### flowise: `postgres:14-alpine`
- `image` at `template/flowise/index.yaml:157`
- `image` at `template/flowise/index.yaml:217`

### formbricks: `ghcr.io/formbricks/formbricks:4.9.7`
- `originImageName` at `template/formbricks/index.yaml:344`
- `image` at `template/formbricks/index.yaml:370`
- `image` at `template/formbricks/index.yaml:426`

### formbricks: `postgres:16-alpine`
- `image` at `template/formbricks/index.yaml:165`

### frp: `bitnamilegacy/kubectl:1.28.9`
- `image` at `template/frp/index.yaml:299`

### frp: `snowdreamtech/frps:0.59`
- `originImageName` at `template/frp/index.yaml:79`
- `image` at `template/frp/index.yaml:104`

### full-stack-fastapi: `ghcr.io/yangchuansheng/full-stack-fastapi-backend:0.8.0`
- `image` at `template/full-stack-fastapi/index.yaml:232`
- `originImageName` at `template/full-stack-fastapi/index.yaml:300`
- `image` at `template/full-stack-fastapi/index.yaml:320`

### full-stack-fastapi: `ghcr.io/yangchuansheng/full-stack-fastapi-frontend:0.8.0`
- `originImageName` at `template/full-stack-fastapi/index.yaml:429`
- `image` at `template/full-stack-fastapi/index.yaml:449`

### full-stack-fastapi: `postgres:14-alpine`
- `image` at `template/full-stack-fastapi/index.yaml:183`

### ghost: `ghost:6.44.1-alpine`
- `originImageName` at `template/ghost/index.yaml:250`
- `image` at `template/ghost/index.yaml:339`

### ghost: `public.ecr.aws/docker/library/mysql:8.0.30`
- `image` at `template/ghost/index.yaml:155`
- `image` at `template/ghost/index.yaml:300`

### ghost: `public.ecr.aws/docker/library/node:22-alpine`
- `image` at `template/ghost/index.yaml:277`

### gitea: `gitea/gitea:1.22.0-rootless`
- `originImageName` at `template/gitea/index.yaml:36`
- `image` at `template/gitea/index.yaml:63`

### glance: `glanceapp/glance`
- `originImageName` at `template/glance/index.yaml:146`

### glance: `glanceapp/glance:latest`
- `image` at `template/glance/index.yaml:164`

### glitchtip: `glitchtip/glitchtip:v4.1.5`
- `originImageName` at `template/glitchtip/index.yaml:61`
- `image` at `template/glitchtip/index.yaml:86`
- `image` at `template/glitchtip/index.yaml:175`
- `image` at `template/glitchtip/index.yaml:265`

### glitchtip: `senzing/postgresql-client:2.2.4`
- `image` at `template/glitchtip/index.yaml:623`

### gpt-academic: `ghcr.io/binary-husky/gpt_academic_nolocal:master`
- `originImageName` at `template/gpt-academic/index.yaml:63`
- `image` at `template/gpt-academic/index.yaml:88`

### grafana-otel: `busybox`
- `image` at `template/grafana-otel/index.yaml:242`
- `image` at `template/grafana-otel/index.yaml:372`

### grafana-otel: `grafana/grafana:12.3.0`
- `originImageName` at `template/grafana-otel/index.yaml:351`
- `image` at `template/grafana-otel/index.yaml:384`

### grafana-otel: `otel/opentelemetry-collector:0.99.0`
- `originImageName` at `template/grafana-otel/index.yaml:70`
- `image` at `template/grafana-otel/index.yaml:91`

### grafana-otel: `prom/prometheus:v3.8.0`
- `originImageName` at `template/grafana-otel/index.yaml:221`
- `image` at `template/grafana-otel/index.yaml:254`

### halo: `halohub/halo:2.18.0`
- `originImageName` at `template/halo/index.yaml:48`
- `image` at `template/halo/index.yaml:71`

### halo: `senzing/postgresql-client:2.2.4`
- `image` at `template/halo/index.yaml:271`

### happy-server: `ghcr.io/yangchuansheng/happy-server@sha256:6986ce15ac7c00604ab4aea89c9f9831b44746ec20da5cb5812ff1ab40317cfe`
- `originImageName` at `template/happy-server/index.yaml:704`
- `image` at `template/happy-server/index.yaml:724`

### happy-server: `postgres:16.4-alpine`
- `image` at `template/happy-server/index.yaml:523`

### harbor: `goharbor/harbor-core:v2.14.4`
- `originImageName` at `template/harbor/index.yaml:606`
- `image` at `template/harbor/index.yaml:628`

### harbor: `goharbor/harbor-jobservice:v2.14.4`
- `originImageName` at `template/harbor/index.yaml:739`
- `image` at `template/harbor/index.yaml:762`

### harbor: `goharbor/harbor-portal:v2.14.4`
- `originImageName` at `template/harbor/index.yaml:840`
- `image` at `template/harbor/index.yaml:862`

### harbor: `goharbor/harbor-registryctl:v2.14.4`
- `originImageName` at `template/harbor/index.yaml:1041`
- `image` at `template/harbor/index.yaml:1063`

### harbor: `goharbor/registry-photon:v2.14.4`
- `originImageName` at `template/harbor/index.yaml:903`
- `image` at `template/harbor/index.yaml:926`

### harbor: `goharbor/trivy-adapter-photon:v2.14.4`
- `originImageName` at `template/harbor/index.yaml:1121`
- `image` at `template/harbor/index.yaml:1146`

### harbor: `postgres:16.4`
- `image` at `template/harbor/index.yaml:163`

### hasura: `hasura/graphql-data-connector:v2.48.11`
- `originImageName` at `template/hasura/index.yaml:215`
- `image` at `template/hasura/index.yaml:235`

### hasura: `hasura/graphql-engine:v2.48.11`
- `originImageName` at `template/hasura/index.yaml:121`
- `image` at `template/hasura/index.yaml:141`

### headscale: `alpine`
- `image` at `template/headscale/index.yaml:945`

### headscale: `ghcr.io/tale/headplane:0.6.3`
- `image` at `template/headscale/index.yaml:1042`

### headscale: `headscale/headscale:0.29.0-beta.1-debug`
- `originImageName` at `template/headscale/index.yaml:879`
- `image` at `template/headscale/index.yaml:998`

### headscale: `postgres:16-alpine`
- `image` at `template/headscale/index.yaml:140`
- `image` at `template/headscale/index.yaml:906`

### heyform: `heyform/community-edition:v3.0.0-rc.7`
- `originImageName` at `template/heyform/index.yaml:271`
- `image` at `template/heyform/index.yaml:293`

### illa-builder: `illasoft/illa-builder:v4.8.2`
- `originImageName` at `template/illa-builder/index.yaml:38`
- `image` at `template/illa-builder/index.yaml:61`

### immich: `ghcr.io/immich-app/immich-machine-learning:v2.7.5`
- `originImageName` at `template/immich/index.yaml:506`
- `image` at `template/immich/index.yaml:529`

### immich: `ghcr.io/immich-app/immich-server:v2.7.5`
- `originImageName` at `template/immich/index.yaml:319`
- `image` at `template/immich/index.yaml:388`

### immich: `postgres:16-alpine`
- `image` at `template/immich/index.yaml:255`
- `image` at `template/immich/index.yaml:342`

### influxdb: `docker.io/library/influxdb:2.9.1`
- `originImageName` at `template/influxdb/index.yaml:47`
- `image` at `template/influxdb/index.yaml:71`

### inpaint-web: `yangchuansheng/inpaint-web`
- `originImageName` at `template/inpaint-web/index.yaml:35`
- `image` at `template/inpaint-web/index.yaml:60`

### insforge: `apecloud/kubeblocks-tools:0.9.3`
- `image` at `template/insforge/index.yaml:265`
- `image` at `template/insforge/index.yaml:352`

### insforge: `ghcr.io/insforge/deno-runtime:2.0.6`
- `originImageName` at `template/insforge/index.yaml:767`
- `image` at `template/insforge/index.yaml:787`

### insforge: `ghcr.io/insforge/insforge-oss:v2.1.8`
- `originImageName` at `template/insforge/index.yaml:420`
- `image` at `template/insforge/index.yaml:500`

### insforge: `postgres:16-alpine`
- `image` at `template/insforge/index.yaml:441`

### insforge: `postgrest/postgrest:v12.2.12`
- `originImageName` at `template/insforge/index.yaml:675`
- `image` at `template/insforge/index.yaml:695`

### it-tools: `ghcr.io/corentinth/it-tools:2024.5.13-a0bc346`
- `originImageName` at `template/it-tools/index.yaml:36`
- `image` at `template/it-tools/index.yaml:61`

### jsoncrack: `shokohsc/jsoncrack@sha256:4360a0659ed2fc301904477b9eb3454f8ab7b67af611b1f25e79acfb6165c8ef`
- `originImageName` at `template/jsoncrack/index.yaml:37`
- `image` at `template/jsoncrack/index.yaml:65`

### kanboard: `kanboard/kanboard:v1.2.50`
- `originImageName` at `template/kanboard/index.yaml:121`
- `image` at `template/kanboard/index.yaml:141`

### kaneo: `ghcr.io/usekaneo/api:1.1.8`
- `originImageName` at `template/kaneo/index.yaml:170`
- `image` at `template/kaneo/index.yaml:190`

### kaneo: `ghcr.io/usekaneo/web:1.1.8`
- `originImageName` at `template/kaneo/index.yaml:234`
- `image` at `template/kaneo/index.yaml:254`

### kaneo: `postgres:14-alpine`
- `image` at `template/kaneo/index.yaml:132`

### keycloak: `postgres:14-alpine`
- `image` at `template/keycloak/index.yaml:152`

### keycloak: `quay.io/keycloak/keycloak:26.3.2`
- `originImageName` at `template/keycloak/index.yaml:177`
- `image` at `template/keycloak/index.yaml:198`

### keystone: `node:22.22.1-alpine`
- `originImageName` at `template/keystone/index.yaml:479`
- `image` at `template/keystone/index.yaml:544`
- `image` at `template/keystone/index.yaml:620`

### keystone: `postgres:16.4-alpine`
- `image` at `template/keystone/index.yaml:149`

### kitten-tts: `ghcr.io/yangchuansheng/kitten-tts-server:cpu-v1.2`
- `originImageName` at `template/kitten-tts/index.yaml:44`
- `image` at `template/kitten-tts/index.yaml:65`
- `image` at `template/kitten-tts/index.yaml:76`

### kodcloud: `kodcloud/kodbox:latest`
- `originImageName` at `template/kodcloud/index.yaml:44`
- `image` at `template/kodcloud/index.yaml:67`

### kuboard: `eipwork/kuboard:v3`
- `originImageName` at `template/kuboard/index.yaml:39`
- `image` at `template/kuboard/index.yaml:62`

### kuvasz: `kuvaszmonitoring/kuvasz:3.11.0`
- `originImageName` at `template/kuvasz/index.yaml:201`
- `image` at `template/kuvasz/index.yaml:277`

### kuvasz: `postgres:16.4-alpine`
- `image` at `template/kuvasz/index.yaml:143`
- `image` at `template/kuvasz/index.yaml:231`

### laf: `docker.io/lafyun/laf-server:sha-ef30cd9`
- `image` at `template/laf/index.yaml:209`

### laf: `docker.io/lafyun/laf-web:sha-e9d012d`
- `image` at `template/laf/index.yaml:328`

### laf: `docker.io/lafyun/runtime-node-init:sha-67b3cd6`
- `image` at `template/laf/index.yaml:1418`

### laf: `docker.io/lafyun/runtime-node:sha-67b3cd6`
- `image` at `template/laf/index.yaml:1396`

### laf: `docker.io/library/nginx:latest`
- `image` at `template/laf/index.yaml:1441`

### laf: `quay.io/minio/mc:RELEASE.2022-11-07T23-47-39Z`
- `image` at `template/laf/index.yaml:1094`
- `image` at `template/laf/index.yaml:1148`

### laf: `quay.io/minio/minio`
- `originImageName` at `template/laf/index.yaml:975`

### laf: `quay.io/minio/minio:RELEASE.2023-03-22T06-36-24Z`
- `image` at `template/laf/index.yaml:1008`

### laf: `quay.io/prometheus/prometheus:v2.45.0`
- `image` at `template/laf/index.yaml:519`

### langflow: `langflowai/langflow:1.9.5`
- `originImageName` at `template/langflow/index.yaml:219`
- `image` at `template/langflow/index.yaml:247`

### langflow: `postgres:16-alpine`
- `image` at `template/langflow/index.yaml:157`

### langfuse: `clickhouse/clickhouse-server:25.4.2`
- `originImageName` at `template/langfuse/index.yaml:385`
- `image` at `template/langfuse/index.yaml:409`

### langfuse: `docker.io/langfuse/langfuse-worker:3.180.0`
- `originImageName` at `template/langfuse/index.yaml:528`
- `image` at `template/langfuse/index.yaml:622`

### langfuse: `docker.io/langfuse/langfuse:3.180.0`
- `originImageName` at `template/langfuse/index.yaml:786`
- `image` at `template/langfuse/index.yaml:839`

### langfuse: `minio/minio:RELEASE.2025-09-07T16-13-09Z`
- `originImageName` at `template/langfuse/index.yaml:1042`
- `image` at `template/langfuse/index.yaml:1065`

### langfuse: `public.ecr.aws/docker/library/postgres:16.4-alpine`
- `image` at `template/langfuse/index.yaml:184`
- `image` at `template/langfuse/index.yaml:550`

### langfuse: `public.ecr.aws/docker/library/redis:7.2.7-alpine`
- `image` at `template/langfuse/index.yaml:591`
- `image` at `template/langfuse/index.yaml:808`

### librechat: `getmeili/meilisearch:v1.5`
- `originImageName` at `template/librechat/index.yaml:260`
- `image` at `template/librechat/index.yaml:283`

### librechat: `ghcr.io/danny-avila/librechat:v0.7.3`
- `originImageName` at `template/librechat/index.yaml:52`
- `image` at `template/librechat/index.yaml:75`

### liebianbao: `busybox:1.36.1`
- `image` at `template/liebianbao/index.yaml:99`

### liebianbao: `docker.io/arey/mysql-client:latest`
- `image` at `template/liebianbao/index.yaml:712`

### liebianbao: `docker.io/labring4docker/php-custom:7.2-fpm`
- `image` at `template/liebianbao/index.yaml:135`

### liebianbao: `labring4docker/php-custom:7.2-fpm`
- `originImageName` at `template/liebianbao/index.yaml:78`

### liebianbao: `nginx:1.25.2`
- `image` at `template/liebianbao/index.yaml:253`

### listmonk: `busybox:1.37.0`
- `image` at `template/listmonk/index.yaml:252`

### listmonk: `listmonk/listmonk:v6.1.0`
- `originImageName` at `template/listmonk/index.yaml:224`
- `image` at `template/listmonk/index.yaml:274`
- `image` at `template/listmonk/index.yaml:343`

### listmonk: `postgres:16.4-alpine`
- `image` at `template/listmonk/index.yaml:151`

### llama2-chinese: `luanshaotong/text-generation-webui-cpu:dev`
- `originImageName` at `template/llama2-chinese/index.yaml:64`
- `image` at `template/llama2-chinese/index.yaml:89`

### llama3-8b-chinese: `registry.cn-hangzhou.aliyuncs.com/yangchuansheng/llama-3-8b-chinese:q4_k_m`
- `originImageName` at `template/llama3-8b-chinese/index.yaml:35`
- `image` at `template/llama3-8b-chinese/index.yaml:59`

### llmgateway: `ghcr.io/theopenco/llmgateway-api:v1.3.0`
- `originImageName` at `template/llmgateway/index.yaml:357`
- `image` at `template/llmgateway/index.yaml:442`

### llmgateway: `ghcr.io/theopenco/llmgateway-docs:v1.3.0`
- `originImageName` at `template/llmgateway/index.yaml:1195`
- `image` at `template/llmgateway/index.yaml:1217`

### llmgateway: `ghcr.io/theopenco/llmgateway-gateway:v1.3.0`
- `originImageName` at `template/llmgateway/index.yaml:590`
- `image` at `template/llmgateway/index.yaml:716`

### llmgateway: `ghcr.io/theopenco/llmgateway-ui:v1.3.0`
- `originImageName` at `template/llmgateway/index.yaml:1066`
- `image` at `template/llmgateway/index.yaml:1087`

### llmgateway: `ghcr.io/theopenco/llmgateway-worker:v1.3.0`
- `originImageName` at `template/llmgateway/index.yaml:874`
- `image` at `template/llmgateway/index.yaml:1001`

### llmgateway: `public.ecr.aws/docker/library/postgres:16.4-alpine`
- `image` at `template/llmgateway/index.yaml:157`
- `image` at `template/llmgateway/index.yaml:378`
- `image` at `template/llmgateway/index.yaml:611`
- `image` at `template/llmgateway/index.yaml:652`
- `image` at `template/llmgateway/index.yaml:896`
- `image` at `template/llmgateway/index.yaml:937`

### llmgateway: `public.ecr.aws/docker/library/redis:7.2.7-alpine`
- `image` at `template/llmgateway/index.yaml:419`
- `image` at `template/llmgateway/index.yaml:693`
- `image` at `template/llmgateway/index.yaml:978`

### lobe-chat: `lobehub/lobe-chat:1.143.3`
- `originImageName` at `template/lobe-chat/index.yaml:61`
- `image` at `template/lobe-chat/index.yaml:87`

### lobe-chat-db: `lobehub/lobe-chat-database:1.143.2`
- `originImageName` at `template/lobe-chat-db/index.yaml:212`
- `image` at `template/lobe-chat-db/index.yaml:237`

### lobe-chat-db: `postgres:14-alpine`
- `image` at `template/lobe-chat-db/index.yaml:172`

### logto: `postgres:16.4-alpine`
- `image` at `template/logto/index.yaml:127`

### logto: `svhd/logto:1.40.1`
- `originImageName` at `template/logto/index.yaml:179`
- `image` at `template/logto/index.yaml:204`
- `image` at `template/logto/index.yaml:253`

### loki: `busybox:1.37.0`
- `image` at `template/loki/index.yaml:57`

### loki: `docker.io/grafana/loki:3.7.2`
- `originImageName` at `template/loki/index.yaml:36`
- `image` at `template/loki/index.yaml:77`

### mage-ai: `mageai/mageai:0.9.79`
- `originImageName` at `template/mage-ai/index.yaml:211`
- `image` at `template/mage-ai/index.yaml:233`
- `image` at `template/mage-ai/index.yaml:283`

### mage-ai: `postgres:16.4-alpine`
- `image` at `template/mage-ai/index.yaml:150`

### mastodon: `ghcr.io/mastodon/mastodon-streaming:v4.5.11`
- `originImageName` at `template/mastodon/index.yaml:937`
- `image` at `template/mastodon/index.yaml:1004`

### mastodon: `ghcr.io/mastodon/mastodon:v4.5.11`
- `image` at `template/mastodon/index.yaml:455`
- `originImageName` at `template/mastodon/index.yaml:572`
- `image` at `template/mastodon/index.yaml:639`
- `originImageName` at `template/mastodon/index.yaml:753`
- `image` at `template/mastodon/index.yaml:817`

### mastodon: `postgres:16.4-alpine`
- `image` at `template/mastodon/index.yaml:333`

### mastodon: `public.ecr.aws/docker/library/postgres:16.4-alpine`
- `image` at `template/mastodon/index.yaml:598`
- `image` at `template/mastodon/index.yaml:776`
- `image` at `template/mastodon/index.yaml:963`

### mastodon: `public.ecr.aws/docker/library/redis:7-alpine`
- `image` at `template/mastodon/index.yaml:434`

### matomo: `matomo:5.10.0-apache`
- `originImageName` at `template/matomo/index.yaml:179`
- `image` at `template/matomo/index.yaml:201`

### matomo: `mysql:8.0.44`
- `image` at `template/matomo/index.yaml:135`

### matrixgorilla: `${{ defaults.app_name }}-api`
- `originImageName` at `template/matrixgorilla/index.yaml:79`

### matrixgorilla: `${{ defaults.app_name }}-web`
- `originImageName` at `template/matrixgorilla/index.yaml:35`

### matrixgorilla: `registry.cn-beijing.aliyuncs.com/juliangxingqiu/sealos-java-api:latest`
- `image` at `template/matrixgorilla/index.yaml:101`

### matrixgorilla: `registry.cn-beijing.aliyuncs.com/juliangxingqiu/sealos-java-web:latest`
- `image` at `template/matrixgorilla/index.yaml:58`

### mautic: `busybox:1.36.1`
- `image` at `template/mautic/index.yaml:473`
- `image` at `template/mautic/index.yaml:597`

### mautic: `mautic/mautic:7.1.2-apache`
- `originImageName` at `template/mautic/index.yaml:242`
- `image` at `template/mautic/index.yaml:266`
- `image` at `template/mautic/index.yaml:316`
- `image` at `template/mautic/index.yaml:343`
- `originImageName` at `template/mautic/index.yaml:440`
- `image` at `template/mautic/index.yaml:492`
- `originImageName` at `template/mautic/index.yaml:564`
- `image` at `template/mautic/index.yaml:616`

### mautic: `mysql:8.4.2`
- `image` at `template/mautic/index.yaml:141`

### mazanoke: `ghcr.io/civilblur/mazanoke:v1.1.6`
- `originImageName` at `template/mazanoke/index.yaml:37`
- `image` at `template/mazanoke/index.yaml:63`

### meilisearch: `eyeix/meilisearch-ui:v0.15.1-lite`
- `originImageName` at `template/meilisearch/index.yaml:133`
- `image` at `template/meilisearch/index.yaml:153`

### meilisearch: `getmeili/meilisearch:v1.45.1`
- `originImageName` at `template/meilisearch/index.yaml:44`
- `image` at `template/meilisearch/index.yaml:68`

### memos: `ghcr.io/usememos/memos:latest`
- `originImageName` at `template/memos/index.yaml:39`
- `image` at `template/memos/index.yaml:62`

### metabase: `metabase/metabase:v0.61.3`
- `originImageName` at `template/metabase/index.yaml:171`
- `image` at `template/metabase/index.yaml:194`

### metabase: `postgres:16-alpine`
- `image` at `template/metabase/index.yaml:128`

### midjourney-ui: `erictik/midjourney-ui:1.1.47`
- `originImageName` at `template/midjourney-ui/index.yaml:57`
- `image` at `template/midjourney-ui/index.yaml:82`

### mindoc: `registry.cn-hangzhou.aliyuncs.com/mindoc-org/mindoc:v2.2-beta.1`
- `originImageName` at `template/mindoc/index.yaml:274`
- `image` at `template/mindoc/index.yaml:299`

### mindoc: `senzing/postgresql-client:2.2.4`
- `image` at `template/mindoc/index.yaml:133`

### mindsdb: `mindsdb/mindsdb:v26.1.0`
- `originImageName` at `template/mindsdb/index.yaml:253`
- `image` at `template/mindsdb/index.yaml:323`
- `image` at `template/mindsdb/index.yaml:365`

### mindsdb: `public.ecr.aws/docker/library/postgres:16.4-alpine`
- `image` at `template/mindsdb/index.yaml:156`
- `image` at `template/mindsdb/index.yaml:276`

### minecraft: `alpine:3.22.4`
- `image` at `template/minecraft/index.yaml:71`

### minecraft: `itzg/minecraft-server:2026.5.3-java25`
- `originImageName` at `template/minecraft/index.yaml:48`
- `image` at `template/minecraft/index.yaml:91`

### minio: `quay.io/minio/minio`
- `originImageName` at `template/minio/index.yaml:57`
- `image` at `template/minio/index.yaml:80`

### mlflow: `ghcr.io/mlflow/mlflow:v3.12.0`
- `originImageName` at `template/mlflow/index.yaml:201`
- `image` at `template/mlflow/index.yaml:270`

### mlflow: `senzing/postgresql-client:2.2.4`
- `image` at `template/mlflow/index.yaml:151`
- `image` at `template/mlflow/index.yaml:222`

### moneyprinterturbo: `ghcr.io/yangchuansheng/moneyprinterturbo:20240510083200`
- `originImageName` at `template/moneyprinterturbo/index.yaml:37`
- `image` at `template/moneyprinterturbo/index.yaml:60`

### mongo-express: `mongo-express:1.0.2-20-alpine3.19`
- `originImageName` at `template/mongo-express/index.yaml:127`
- `image` at `template/mongo-express/index.yaml:147`

### n8n: `alpine`
- `image` at `template/n8n/index.yaml:362`

### n8n: `busybox:1.36`
- `image` at `template/n8n/index.yaml:605`

### n8n: `n8nio/n8n:2.22.4`
- `originImageName` at `template/n8n/index.yaml:337`
- `image` at `template/n8n/index.yaml:370`
- `originImageName` at `template/n8n/index.yaml:583`
- `image` at `template/n8n/index.yaml:624`

### n8n: `n8nio/runners:2.22.4`
- `originImageName` at `template/n8n/index.yaml:522`
- `image` at `template/n8n/index.yaml:544`
- `originImageName` at `template/n8n/index.yaml:711`
- `image` at `template/n8n/index.yaml:733`

### n8n: `postgres:16-alpine`
- `image` at `template/n8n/index.yaml:296`

### nacos: `mysql:8.0.44`
- `image` at `template/nacos/index.yaml:347`

### nacos: `nacos/nacos-server:v3.2.2`
- `originImageName` at `template/nacos/index.yaml:410`
- `image` at `template/nacos/index.yaml:432`
- `originImageName` at `template/nacos/index.yaml:545`
- `image` at `template/nacos/index.yaml:567`

### nakama: `busybox:1.36`
- `image` at `template/nakama/index.yaml:261`

### nakama: `heroiclabs/nakama:3.39.0`
- `originImageName` at `template/nakama/index.yaml:237`
- `image` at `template/nakama/index.yaml:327`
- `image` at `template/nakama/index.yaml:370`

### nakama: `postgres:16-alpine`
- `image` at `template/nakama/index.yaml:187`
- `image` at `template/nakama/index.yaml:278`

### netbird: `netbirdio/dashboard:v2.38.1`
- `originImageName` at `template/netbird/index.yaml:150`
- `image` at `template/netbird/index.yaml:170`

### netbird: `netbirdio/management:0.71.4`
- `originImageName` at `template/netbird/index.yaml:217`
- `image` at `template/netbird/index.yaml:238`

### netbird: `netbirdio/relay:0.71.4`
- `originImageName` at `template/netbird/index.yaml:356`
- `image` at `template/netbird/index.yaml:376`

### netbird: `netbirdio/signal:0.71.4`
- `originImageName` at `template/netbird/index.yaml:295`
- `image` at `template/netbird/index.yaml:316`

### new-api: `calciumion/new-api:v0.13.2`
- `originImageName` at `template/new-api/index.yaml:304`
- `image` at `template/new-api/index.yaml:326`

### new-api: `postgres:16.4`
- `image` at `template/new-api/index.yaml:252`

### nexus: `alpine:3.22.2`
- `image` at `template/nexus/index.yaml:61`

### nexus: `sonatype/nexus3:3.92.3`
- `originImageName` at `template/nexus/index.yaml:37`
- `image` at `template/nexus/index.yaml:79`

### nocodb: `nocodb/nocodb:2026.05.2`
- `originImageName` at `template/nocodb/index.yaml:132`
- `image` at `template/nocodb/index.yaml:156`

### node-red: `nodered/node-red:4.1.10`
- `originImageName` at `template/node-red/index.yaml:36`
- `image` at `template/node-red/index.yaml:61`

### nofx: `alpine/openssl:3.5.4`
- `image` at `template/nofx/index.yaml:210`

### nofx: `ghcr.io/nofxaios/nofx/nofx-backend@sha256:32d77ff9761ba8b068f95a5a4c8fee0a7745c8a927300b7d658e593b1e654ae7`
- `originImageName` at `template/nofx/index.yaml:189`
- `image` at `template/nofx/index.yaml:273`

### nofx: `ghcr.io/nofxaios/nofx/nofx-frontend@sha256:6c1e56336433e82eb5e750034d2991a8dbebd89a6b19119c4b12601ef1842887`
- `originImageName` at `template/nofx/index.yaml:427`
- `image` at `template/nofx/index.yaml:448`

### nofx: `public.ecr.aws/docker/library/postgres:16.4-alpine`
- `image` at `template/nofx/index.yaml:136`
- `image` at `template/nofx/index.yaml:231`

### notifuse: `notifuse/notifuse:v32.1@sha256:fdee58fc36e50cf3f64c007dbf07549842280022828fd6c051f6454084a66cfb`
- `originImageName` at `template/notifuse/index.yaml:175`
- `image` at `template/notifuse/index.yaml:250`

### notifuse: `postgres:16.4-alpine`
- `image` at `template/notifuse/index.yaml:138`
- `image` at `template/notifuse/index.yaml:196`

### nsfw: `ethandai4869/nsfw-auth`
- `originImageName` at `template/nsfw/index.yaml:40`
- `image` at `template/nsfw/index.yaml:65`

### one-api: `ghcr.io/songquanpeng/one-api:v0.6.10`
- `originImageName` at `template/one-api/index.yaml:51`
- `image` at `template/one-api/index.yaml:79`

### open-design: `docker.io/vanjayak/open-design@sha256:a3b0f7b043aec134e857513f1480b2da6aaaab641af2d7337999c9090a5c1e13`
- `originImageName` at `template/open-design/index.yaml:101`
- `image` at `template/open-design/index.yaml:130`

### open-design: `nginxinc/nginx-unprivileged:1.25-alpine-slim`
- `originImageName` at `template/open-design/index.yaml:222`
- `image` at `template/open-design/index.yaml:248`

### open-webui: `ghcr.io/open-webui/open-webui:v0.5.4`
- `originImageName` at `template/open-webui/index.yaml:36`
- `image` at `template/open-webui/index.yaml:59`
- `image` at `template/open-webui/index.yaml:65`
- `image` at `template/open-webui/index.yaml:74`

### openagents: `ghcr.io/openagents-org/openagents:sha-48764c0`
- `originImageName` at `template/openagents/index.yaml:52`
- `image` at `template/openagents/index.yaml:73`

### openai-proxy: `unickcheng/openai-proxy`
- `originImageName` at `template/openai-proxy/index.yaml:38`
- `image` at `template/openai-proxy/index.yaml:63`

### opencart: `ghcr.io/yangchuansheng/opencart:4.1.0.3@sha256:eb92c3f24fe3a2b44a09af51dcd8c2ba9aeb2454b26dcae9e85036afb1d04d94`
- `originImageName` at `template/opencart/index.yaml:139`
- `image` at `template/opencart/index.yaml:160`

### openclaw: `busybox:1.36`
- `image` at `template/openclaw/index.yaml:85`

### openclaw: `ghcr.io/openclaw/openclaw:2026.3.8`
- `originImageName` at `template/openclaw/index.yaml:62`
- `image` at `template/openclaw/index.yaml:102`
- `image` at `template/openclaw/index.yaml:160`

### openlist: `openlistteam/openlist:v4.0.9-aria2`
- `originImageName` at `template/openlist/index.yaml:49`
- `image` at `template/openlist/index.yaml:72`

### openobserve: `public.ecr.aws/zinclabs/openobserve:v0.90.3`
- `originImageName` at `template/openobserve/index.yaml:68`
- `image` at `template/openobserve/index.yaml:97`

### outline: `outlinewiki/outline:1.8.0-1`
- `originImageName` at `template/outline/index.yaml:427`
- `image` at `template/outline/index.yaml:448`

### outline: `postgres:16.4`
- `image` at `template/outline/index.yaml:384`

### overleaf: `sharelatex/sharelatex:6.1.2`
- `originImageName` at `template/overleaf/index.yaml:260`
- `image` at `template/overleaf/index.yaml:284`

### pageplug: `cloudtogouser/pageplug-ce:v1.9.35`
- `originImageName` at `template/pageplug/index.yaml:38`
- `image` at `template/pageplug/index.yaml:61`

### palacms: `ghcr.io/palacms/palacms:v3.0.0-beta.1`
- `originImageName` at `template/palacms/index.yaml:38`
- `image` at `template/palacms/index.yaml:59`

### palworld: `alpine`
- `image` at `template/palworld/index.yaml:85`

### palworld: `hurlenko/filebrowser`
- `image` at `template/palworld/index.yaml:158`

### palworld: `thijsvanloef/palworld-server-docker`
- `originImageName` at `template/palworld/index.yaml:62`
- `image` at `template/palworld/index.yaml:103`

### palworld-autobackup: `bitnamilegacy/kubectl`
- `image` at `template/palworld-autobackup/index.yaml:63`

### palworld-export: `bitnamilegacy/kubectl`
- `image` at `template/palworld-export/index.yaml:64`

### palworld-export: `hurlenko/filebrowser`
- `originImageName` at `template/palworld-export/index.yaml:42`
- `image` at `template/palworld-export/index.yaml:76`

### palworld-management: `registry.cn-hangzhou.aliyuncs.com/bxy4543/palworld-server-tool:2024-02-18`
- `originImageName` at `template/palworld-management/index.yaml:66`
- `image` at `template/palworld-management/index.yaml:90`

### pangolin: `docker.io/fosrl/pangolin:1.15.2`
- `originImageName` at `template/pangolin/index.yaml:102`
- `image` at `template/pangolin/index.yaml:122`

### paperclip: `ghcr.io/paperclipai/paperclip:sha-b8725c5`
- `originImageName` at `template/paperclip/index.yaml:231`
- `image` at `template/paperclip/index.yaml:319`
- `image` at `template/paperclip/index.yaml:470`
- `image` at `template/paperclip/index.yaml:692`

### paperclip: `public.ecr.aws/docker/library/busybox:1.36.1`
- `image` at `template/paperclip/index.yaml:257`

### paperclip: `public.ecr.aws/docker/library/postgres:16.4-alpine`
- `image` at `template/paperclip/index.yaml:178`
- `image` at `template/paperclip/index.yaml:278`

### paperless-ngx: `ghcr.io/paperless-ngx/paperless-ngx:latest`
- `originImageName` at `template/paperless-ngx/index.yaml:318`
- `image` at `template/paperless-ngx/index.yaml:339`

### paperless-ngx: `postgres:14-alpine`
- `image` at `template/paperless-ngx/index.yaml:294`

### payload: `ghcr.io/yangchuansheng/payload:3.82.1-a7dd17c9be0c`
- `originImageName` at `template/payload/index.yaml:178`
- `image` at `template/payload/index.yaml:200`

### payload: `public.ecr.aws/docker/library/postgres:16.4-alpine`
- `image` at `template/payload/index.yaml:134`

### pdf2zh: `byaidu/pdf2zh:1.9.6`
- `originImageName` at `template/pdf2zh/index.yaml:38`
- `image` at `template/pdf2zh/index.yaml:63`

### penpot: `penpotapp/backend:2.1.2`
- `originImageName` at `template/penpot/index.yaml:281`
- `image` at `template/penpot/index.yaml:307`

### penpot: `penpotapp/exporter:2.1.2`
- `originImageName` at `template/penpot/index.yaml:422`
- `image` at `template/penpot/index.yaml:447`

### penpot: `penpotapp/frontend:2.1.2`
- `originImageName` at `template/penpot/index.yaml:496`
- `image` at `template/penpot/index.yaml:523`

### penpot: `senzing/postgresql-client:2.2.4`
- `image` at `template/penpot/index.yaml:132`

### perplexica: `itzcrazykns1337/perplexica:v1.10.2`
- `originImageName` at `template/perplexica/index.yaml:261`
- `image` at `template/perplexica/index.yaml:284`

### perplexica: `searxng/searxng:2025.2.20-28d1240fc`
- `originImageName` at `template/perplexica/index.yaml:133`
- `image` at `template/perplexica/index.yaml:158`

### pgadmin4: `dpage/pgadmin4:8.9`
- `originImageName` at `template/pgadmin4/index.yaml:45`
- `image` at `template/pgadmin4/index.yaml:65`

### photoprism: `photoprism/photoprism:240711`
- `originImageName` at `template/photoprism/index.yaml:48`
- `image` at `template/photoprism/index.yaml:71`

### phpmyadmin: `phpmyadmin:5.2.1`
- `originImageName` at `template/phpmyadmin/index.yaml:35`
- `image` at `template/phpmyadmin/index.yaml:55`

### plane: `makeplane/plane-admin:v0.22-dev`
- `originImageName` at `template/plane/index.yaml:433`
- `image` at `template/plane/index.yaml:458`

### plane: `makeplane/plane-backend:v0.22-dev`
- `image` at `template/plane/index.yaml:193`
- `originImageName` at `template/plane/index.yaml:511`
- `image` at `template/plane/index.yaml:536`
- `originImageName` at `template/plane/index.yaml:678`
- `image` at `template/plane/index.yaml:703`
- `originImageName` at `template/plane/index.yaml:820`
- `image` at `template/plane/index.yaml:845`

### plane: `makeplane/plane-frontend:v0.22-dev`
- `originImageName` at `template/plane/index.yaml:1037`
- `image` at `template/plane/index.yaml:1062`

### plane: `makeplane/plane-space:v0.22-dev`
- `originImageName` at `template/plane/index.yaml:962`
- `image` at `template/plane/index.yaml:987`

### plane: `senzing/postgresql-client:2.2.4`
- `image` at `template/plane/index.yaml:145`

### planka: `busybox:1.36.1`
- `image` at `template/planka/index.yaml:219`

### planka: `ghcr.io/plankanban/planka:2.1.1`
- `originImageName` at `template/planka/index.yaml:198`
- `image` at `template/planka/index.yaml:249`

### planka: `postgres:16-alpine`
- `image` at `template/planka/index.yaml:153`

### plausible: `clickhouse/clickhouse-server:23.3.7.5-alpine`
- `originImageName` at `template/plausible/index.yaml:187`
- `image` at `template/plausible/index.yaml:208`

### plausible: `plausible/analytics:v2.0`
- `originImageName` at `template/plausible/index.yaml:282`
- `image` at `template/plausible/index.yaml:307`

### pocket-id: `ghcr.io/pocket-id/pocket-id:v2.2.0`
- `originImageName` at `template/pocket-id/index.yaml:40`
- `image` at `template/pocket-id/index.yaml:60`

### pocketbase: `adrianmusante/pocketbase:0.29.3`
- `originImageName` at `template/pocketbase/index.yaml:58`
- `image` at `template/pocketbase/index.yaml:87`

### pocketbase: `busybox:latest`
- `image` at `template/pocketbase/index.yaml:79`

### posthog: `clickhouse/clickhouse-server:25.8.12.129`
- `originImageName` at `template/posthog/index.yaml:1559`
- `image` at `template/posthog/index.yaml:1579`

### posthog: `docker.redpanda.com/redpandadata/redpanda:v25.1.9`
- `originImageName` at `template/posthog/index.yaml:339`
- `image` at `template/posthog/index.yaml:360`

### posthog: `ghcr.io/posthog/posthog-node@sha256:fd156e690ca1bb7cc1abd370e513ac532c57726ee11029721623f0db5b90b72a`
- `originImageName` at `template/posthog/index.yaml:968`
- `image` at `template/posthog/index.yaml:1005`
- `image` at `template/posthog/index.yaml:1068`

### posthog: `ghcr.io/posthog/posthog/capture@sha256:864754478dbbd589f17cb4543d07e1b0f63acbca8e0bceca13de10669500375b`
- `originImageName` at `template/posthog/index.yaml:1302`
- `image` at `template/posthog/index.yaml:1322`
- `originImageName` at `template/posthog/index.yaml:1359`
- `image` at `template/posthog/index.yaml:1379`

### posthog: `ghcr.io/posthog/posthog/feature-flags@sha256:1e79e6e7e5b58da18e27ebdf0ef9b41d6c04136eac42bb9490e73a9a62f94f65`
- `image` at `template/posthog/index.yaml:988`
- `originImageName` at `template/posthog/index.yaml:1414`
- `image` at `template/posthog/index.yaml:1434`

### posthog: `ghcr.io/posthog/posthog:86d6812c7de75c6c869b935e17baf45bf295bfd5`
- `originImageName` at `template/posthog/index.yaml:600`
- `image` at `template/posthog/index.yaml:620`
- `originImageName` at `template/posthog/index.yaml:784`
- `image` at `template/posthog/index.yaml:804`

### posthog: `postgres:16.4`
- `image` at `template/posthog/index.yaml:146`

### posthog: `zookeeper:3.9.3`
- `originImageName` at `template/posthog/index.yaml:481`
- `image` at `template/posthog/index.yaml:502`

### postiz: `busybox:1.36.1`
- `image` at `template/postiz/index.yaml:326`
- `image` at `template/postiz/index.yaml:531`

### postiz: `elasticsearch:7.17.27`
- `originImageName` at `template/postiz/index.yaml:305`
- `image` at `template/postiz/index.yaml:341`

### postiz: `ghcr.io/gitroomhq/postiz-app:v2.21.8`
- `originImageName` at `template/postiz/index.yaml:510`
- `image` at `template/postiz/index.yaml:583`

### postiz: `postgres:16-alpine`
- `image` at `template/postiz/index.yaml:129`

### postiz: `temporalio/auto-setup:1.28.1`
- `originImageName` at `template/postiz/index.yaml:400`
- `image` at `template/postiz/index.yaml:420`

### presenton: `ghcr.io/presenton/presenton:v0.8.2-beta`
- `originImageName` at `template/presenton/index.yaml:37`
- `image` at `template/presenton/index.yaml:59`

### prestashop: `mysql:8.0.30`
- `image` at `template/prestashop/index.yaml:141`

### prestashop: `prestashop/prestashop:9.1.3-apache`
- `originImageName` at `template/prestashop/index.yaml:216`
- `image` at `template/prestashop/index.yaml:237`

### privatebin: `alpine`
- `image` at `template/privatebin/index.yaml:272`

### privatebin: `frooodle/privatebin:0.26.1-fat`
- `originImageName` at `template/privatebin/index.yaml:249`

### privatebin: `ghcr.io/privatebin/fs:1.7.4`
- `image` at `template/privatebin/index.yaml:280`

### pterodactyl: `ghcr.io/pterodactyl/panel:v1.12.4`
- `image` at `template/pterodactyl/index.yaml:399`
- `originImageName` at `template/pterodactyl/index.yaml:545`
- `image` at `template/pterodactyl/index.yaml:677`

### pterodactyl: `public.ecr.aws/docker/library/mysql:8.0.30`
- `image` at `template/pterodactyl/index.yaml:183`
- `image` at `template/pterodactyl/index.yaml:568`
- `image` at `template/pterodactyl/index.yaml:636`

### pterodactyl: `public.ecr.aws/docker/library/redis:7.2.7-alpine`
- `image` at `template/pterodactyl/index.yaml:368`
- `image` at `template/pterodactyl/index.yaml:606`

### qinglong: `whyour/qinglong:latest`
- `originImageName` at `template/qinglong/index.yaml:38`
- `image` at `template/qinglong/index.yaml:61`

### quay: `postgres:16.4`
- `image` at `template/quay/index.yaml:150`

### quay: `python:3.12.8-alpine3.20`
- `image` at `template/quay/index.yaml:541`

### quay: `quay.io/projectquay/quay:v3.9.8`
- `originImageName` at `template/quay/index.yaml:301`
- `image` at `template/quay/index.yaml:332`

### redisinsight: `redislabs/redisinsight:2.52`
- `originImageName` at `template/redisinsight/index.yaml:34`
- `image` at `template/redisinsight/index.yaml:54`

### refly: `mautic/mautic:5.2.3-fpm`
- `image` at `template/refly/index.yaml:409`

### refly: `reflyai/elasticsearch:7.10.2`
- `originImageName` at `template/refly/index.yaml:386`
- `image` at `template/refly/index.yaml:417`

### refly: `reflyai/qdrant:v1.13.1`
- `originImageName` at `template/refly/index.yaml:305`
- `image` at `template/refly/index.yaml:328`

### refly: `reflyai/refly-api:8d870210470801f62a4d2adb3423c947afddf400`
- `originImageName` at `template/refly/index.yaml:479`
- `image` at `template/refly/index.yaml:504`

### refly: `reflyai/refly-web:8d870210470801f62a4d2adb3423c947afddf400`
- `originImageName` at `template/refly/index.yaml:824`
- `image` at `template/refly/index.yaml:849`

### refly: `senzing/postgresql-client:2.2.4`
- `image` at `template/refly/index.yaml:165`

### registry: `joxit/docker-registry-ui:2.5.6-debian`
- `originImageName` at `template/registry/index.yaml:206`
- `image` at `template/registry/index.yaml:230`

### registry: `registry:2.8.3`
- `originImageName` at `template/registry/index.yaml:35`
- `image` at `template/registry/index.yaml:57`

### rocketchat: `mongo:6.0`
- `image` at `template/rocketchat/index.yaml:132`

### rocketchat: `registry.rocket.chat/rocketchat/rocket.chat:7.9.0`
- `originImageName` at `template/rocketchat/index.yaml:183`
- `image` at `template/rocketchat/index.yaml:203`

### rocketchat-micro: `mongo:6.0`
- `image` at `template/rocketchat-micro/index.yaml:130`

### rocketchat-micro: `nats:2.4-alpine`
- `originImageName` at `template/rocketchat-micro/index.yaml:332`
- `image` at `template/rocketchat-micro/index.yaml:367`

### rocketchat-micro: `natsio/nats-server-config-reloader:0.6.3`
- `image` at `template/rocketchat-micro/index.yaml:438`

### rocketchat-micro: `rocketchat/account-service:7.9.0`
- `originImageName` at `template/rocketchat-micro/index.yaml:517`
- `image` at `template/rocketchat-micro/index.yaml:542`

### rocketchat-micro: `rocketchat/authorization-service:7.9.0`
- `originImageName` at `template/rocketchat-micro/index.yaml:606`
- `image` at `template/rocketchat-micro/index.yaml:631`

### rocketchat-micro: `rocketchat/ddp-streamer-service:7.9.0`
- `originImageName` at `template/rocketchat-micro/index.yaml:695`
- `image` at `template/rocketchat-micro/index.yaml:720`

### rocketchat-micro: `rocketchat/presence-service:7.9.0`
- `originImageName` at `template/rocketchat-micro/index.yaml:793`
- `image` at `template/rocketchat-micro/index.yaml:818`

### rocketchat-micro: `rocketchat/rocket.chat:7.9.0`
- `originImageName` at `template/rocketchat-micro/index.yaml:224`
- `image` at `template/rocketchat-micro/index.yaml:249`

### rocketchat-micro: `rocketchat/stream-hub-service:7.9.0`
- `originImageName` at `template/rocketchat-micro/index.yaml:882`
- `image` at `template/rocketchat-micro/index.yaml:907`

### rsshub: `browserless/chrome:1.61.1-chrome-stable`
- `originImageName` at `template/rsshub/index.yaml:133`
- `image` at `template/rsshub/index.yaml:157`

### rsshub: `diygod/rsshub:2024-07-06`
- `originImageName` at `template/rsshub/index.yaml:46`
- `image` at `template/rsshub/index.yaml:71`

### rustdesk: `rustdesk/rustdesk-server-s6:1.1.15`
- `originImageName` at `template/rustdesk/index.yaml:45`
- `image` at `template/rustdesk/index.yaml:69`

### rustfs: `busybox`
- `image` at `template/rustfs/index.yaml:83`

### rustfs: `rustfs/rustfs:latest`
- `originImageName` at `template/rustfs/index.yaml:54`
- `image` at `template/rustfs/index.yaml:114`

### rybbit: `clickhouse/clickhouse-server:25.4.2`
- `originImageName` at `template/rybbit/index.yaml:234`
- `image` at `template/rybbit/index.yaml:258`
- `image` at `template/rybbit/index.yaml:419`

### rybbit: `ghcr.io/rybbit-io/rybbit-backend:sha-aa404ba`
- `originImageName` at `template/rybbit/index.yaml:392`
- `image` at `template/rybbit/index.yaml:464`

### rybbit: `ghcr.io/rybbit-io/rybbit-client:sha-aa404ba`
- `originImageName` at `template/rybbit/index.yaml:605`
- `image` at `template/rybbit/index.yaml:632`

### rybbit: `postgres:16.4-alpine`
- `image` at `template/rybbit/index.yaml:135`
- `image` at `template/rybbit/index.yaml:432`

### s-pdf: `alpine`
- `image` at `template/s-pdf/index.yaml:251`

### s-pdf: `ghcr.io/stirling-tools/stirling-pdf:1.2.0-fat`
- `originImageName` at `template/s-pdf/index.yaml:228`
- `image` at `template/s-pdf/index.yaml:259`

### s-pdf: `postgres:14-alpine`
- `image` at `template/s-pdf/index.yaml:203`

### samarium: `ghcr.io/yangchuansheng/samarium:0.0.0-9514fcadb867`
- `originImageName` at `template/samarium/index.yaml:142`
- `image` at `template/samarium/index.yaml:168`
- `image` at `template/samarium/index.yaml:332`

### signoz: `busybox`
- `image` at `template/signoz/index.yaml:447`

### signoz: `busybox:1.28`
- `image` at `template/signoz/index.yaml:566`
- `image` at `template/signoz/index.yaml:683`
- `image` at `template/signoz/index.yaml:740`
- `image` at `template/signoz/index.yaml:840`

### signoz: `clickhouse/clickhouse-server:25.5.6`
- `originImageName` at `template/signoz/index.yaml:524`
- `image` at `template/signoz/index.yaml:548`
- `image` at `template/signoz/index.yaml:570`

### signoz: `signoz/signoz-otel-collector:v0.144.2`
- `image` at `template/signoz/index.yaml:687`
- `originImageName` at `template/signoz/index.yaml:821`
- `image` at `template/signoz/index.yaml:844`

### signoz: `signoz/signoz:v0.117.0`
- `originImageName` at `template/signoz/index.yaml:719`
- `image` at `template/signoz/index.yaml:744`

### signoz: `signoz/zookeeper:3.7.1`
- `originImageName` at `template/signoz/index.yaml:421`
- `image` at `template/signoz/index.yaml:454`

### sillytavern: `ghcr.io/sillytavern/sillytavern:1.18.0`
- `originImageName` at `template/sillytavern/index.yaml:57`
- `image` at `template/sillytavern/index.yaml:80`
- `image` at `template/sillytavern/index.yaml:154`

### skardi: `ghcr.io/skardilabs/skardi/skardi-server:0.3.0`
- `originImageName` at `template/skardi/index.yaml:123`
- `image` at `template/skardi/index.yaml:143`

### stalwart: `public.ecr.aws/docker/library/postgres:16.4-alpine`
- `image` at `template/stalwart/index.yaml:156`
- `image` at `template/stalwart/index.yaml:259`

### stalwart: `stalwartlabs/stalwart:v0.16.7`
- `originImageName` at `template/stalwart/index.yaml:234`
- `image` at `template/stalwart/index.yaml:302`

### steel-browser: `ghcr.io/steel-dev/steel-browser@sha256:cbf4a44d575c0ae83d00d4ba6bb455d24980de0ced2b06fe8b890e835c923bd1`
- `originImageName` at `template/steel-browser/index.yaml:38`
- `image` at `template/steel-browser/index.yaml:62`

### strapi: `postgres:14-alpine`
- `image` at `template/strapi/index.yaml:164`

### strapi: `vshadbolt/strapi:5.33.0`
- `originImageName` at `template/strapi/index.yaml:611`
- `image` at `template/strapi/index.yaml:632`
- `image` at `template/strapi/index.yaml:706`

### sub2api: `postgres:16-alpine`
- `image` at `template/sub2api/index.yaml:218`

### sub2api: `weishaw/sub2api:0.1.104`
- `originImageName` at `template/sub2api/index.yaml:368`
- `image` at `template/sub2api/index.yaml:397`

### supabase: `darthsim/imgproxy:v3.30.1`
- `originImageName` at `template/supabase/index.yaml:1353`
- `image` at `template/supabase/index.yaml:1373`

### supabase: `kong:2.8.1`
- `originImageName` at `template/supabase/index.yaml:848`
- `image` at `template/supabase/index.yaml:868`

### supabase: `postgres:16.4`
- `image` at `template/supabase/index.yaml:272`

### supabase: `postgrest/postgrest@sha256:b574528fe109c8343c1247155734d03df8c34b462f342dca0ccc20244fc36ef9`
- `originImageName` at `template/supabase/index.yaml:1061`
- `image` at `template/supabase/index.yaml:1081`

### supabase: `supabase/edge-runtime:v1.70.3`
- `originImageName` at `template/supabase/index.yaml:1492`
- `image` at `template/supabase/index.yaml:1512`

### supabase: `supabase/gotrue:v2.186.0`
- `originImageName` at `template/supabase/index.yaml:934`
- `image` at `template/supabase/index.yaml:954`

### supabase: `supabase/logflare:1.31.2`
- `originImageName` at `template/supabase/index.yaml:1594`
- `image` at `template/supabase/index.yaml:1614`

### supabase: `supabase/postgres-meta:v0.95.2`
- `originImageName` at `template/supabase/index.yaml:1430`
- `image` at `template/supabase/index.yaml:1450`

### supabase: `supabase/realtime:v2.76.5`
- `originImageName` at `template/supabase/index.yaml:1133`
- `image` at `template/supabase/index.yaml:1153`

### supabase: `supabase/storage-api:v1.37.8`
- `originImageName` at `template/supabase/index.yaml:1234`
- `image` at `template/supabase/index.yaml:1254`

### supabase: `supabase/studio:2026.02.16-sha-26c615c`
- `originImageName` at `template/supabase/index.yaml:707`
- `image` at `template/supabase/index.yaml:727`

### supabase: `supabase/supavisor:2.7.4`
- `originImageName` at `template/supabase/index.yaml:1766`
- `image` at `template/supabase/index.yaml:1786`

### supabase: `timberio/vector:0.53.0-alpine`
- `originImageName` at `template/supabase/index.yaml:1700`
- `image` at `template/supabase/index.yaml:1720`

### surveyking: `joseluisq/mysql-client:8.0.30`
- `image` at `template/surveyking/index.yaml:129`

### surveyking: `surveyking/surveyking:v1.9.0`
- `originImageName` at `template/surveyking/index.yaml:170`
- `image` at `template/surveyking/index.yaml:193`

### tailchat: `minio/minio`
- `originImageName` at `template/tailchat/index.yaml:267`
- `image` at `template/tailchat/index.yaml:289`

### tailchat: `moonrailgun/tailchat:1.11.5`
- `originImageName` at `template/tailchat/index.yaml:66`
- `image` at `template/tailchat/index.yaml:86`

### teable: `registry.cn-shenzhen.aliyuncs.com/teable/teable-ee:latest`
- `originImageName` at `template/teable/index.yaml:47`
- `image` at `template/teable/index.yaml:69`
- `image` at `template/teable/index.yaml:96`

### teable: `senzing/postgresql-client:2.2.4`
- `image` at `template/teable/index.yaml:348`

### tentix: `limbo2342/tentix:dev-2025-10-23-x.3`
- `image` at `template/tentix/index.yaml:211`

### tentix: `limbo2342/tentix:migrate.10.22.x1`
- `image` at `template/tentix/index.yaml:188`

### tianji: `moonrailgun/tianji:1.18.5`
- `originImageName` at `template/tianji/index.yaml:50`
- `image` at `template/tianji/index.yaml:74`

### tianji: `senzing/postgresql-client:2.2.4`
- `image` at `template/tianji/index.yaml:259`

### tolgee: `senzing/postgresql-client:2.2.4`
- `image` at `template/tolgee/index.yaml:195`

### tolgee: `tolgee/tolgee:v3.113.0`
- `originImageName` at `template/tolgee/index.yaml:219`
- `image` at `template/tolgee/index.yaml:244`

### tooljet: `postgres:16-alpine`
- `image` at `template/tooljet/index.yaml:257`
- `image` at `template/tooljet/index.yaml:305`
- `image` at `template/tooljet/index.yaml:568`

### tooljet: `postgrest/postgrest:v12.0.2`
- `originImageName` at `template/tooljet/index.yaml:455`
- `image` at `template/tooljet/index.yaml:475`

### tooljet: `tooljet/tooljet-ce:v3.20.170-lts`
- `image` at `template/tooljet/index.yaml:333`
- `originImageName` at `template/tooljet/index.yaml:548`
- `image` at `template/tooljet/index.yaml:616`

### tududi: `chrisvel/tududi:1.1.0`
- `originImageName` at `template/tududi/index.yaml:50`
- `image` at `template/tududi/index.yaml:73`

### twenty: `busybox:latest`
- `image` at `template/twenty/index.yaml:337`

### twenty: `postgres:14-alpine`
- `image` at `template/twenty/index.yaml:155`

### twenty: `twentycrm/twenty:v1.12.0`
- `originImageName` at `template/twenty/index.yaml:316`
- `image` at `template/twenty/index.yaml:349`
- `originImageName` at `template/twenty/index.yaml:452`
- `image` at `template/twenty/index.yaml:472`

### typebot: `axllent/mailpit:v1.30.1`
- `originImageName` at `template/typebot/index.yaml:824`
- `image` at `template/typebot/index.yaml:846`

### typebot: `baptistearno/typebot-builder:3.17.1`
- `originImageName` at `template/typebot/index.yaml:431`
- `image` at `template/typebot/index.yaml:484`

### typebot: `baptistearno/typebot-viewer:3.17.1`
- `originImageName` at `template/typebot/index.yaml:656`
- `image` at `template/typebot/index.yaml:709`

### typebot: `public.ecr.aws/docker/library/postgres:16.4-alpine`
- `image` at `template/typebot/index.yaml:265`

### typebot: `public.ecr.aws/docker/library/redis:7.2.7-alpine`
- `image` at `template/typebot/index.yaml:453`
- `image` at `template/typebot/index.yaml:678`

### typesense: `typesense/typesense:29.0`
- `originImageName` at `template/typesense/index.yaml:41`
- `image` at `template/typesense/index.yaml:62`

### typo3: `martinhelmich/typo3:13.4@sha256:7436d068b583c1dae2dd37ebca973b957de5371fe2acfdf9239598c3a8dbda25`
- `originImageName` at `template/typo3/index.yaml:230`
- `image` at `template/typo3/index.yaml:254`
- `image` at `template/typo3/index.yaml:398`

### typo3: `mysql:8.0.30`
- `image` at `template/typo3/index.yaml:154`

### ubuntu-sshd: `takeyamajp/ubuntu-sshd:ubuntu22.04`
- `originImageName` at `template/ubuntu-sshd/index.yaml:38`
- `image` at `template/ubuntu-sshd/index.yaml:63`

### umami: `ghcr.io/umami-software/umami:3.0.2`
- `originImageName` at `template/umami/index.yaml:58`
- `image` at `template/umami/index.yaml:83`

### umami: `postgres:14-alpine`
- `image` at `template/umami/index.yaml:257`

### uptime-kuma: `louislam/uptime-kuma:1.23.13`
- `originImageName` at `template/uptime-kuma/index.yaml:38`
- `image` at `template/uptime-kuma/index.yaml:61`

### vaultwarden: `vaultwarden/server:latest`
- `originImageName` at `template/vaultwarden/index.yaml:38`
- `image` at `template/vaultwarden/index.yaml:61`

### waha: `devlikeapro/waha:chrome-2026.5.1`
- `originImageName` at `template/waha/index.yaml:162`
- `image` at `template/waha/index.yaml:230`

### waha: `public.ecr.aws/docker/library/postgres:16.4-alpine`
- `image` at `template/waha/index.yaml:186`

### webos: `fs185085781/webos:v1.4.1`
- `originImageName` at `template/webos/index.yaml:37`
- `image` at `template/webos/index.yaml:60`

### wechat: `ricwang/docker-wechat:4.0.0.30`
- `originImageName` at `template/wechat/index.yaml:47`
- `image` at `template/wechat/index.yaml:70`

### wechat2rss: `ttttmr/wechat2rss:latest`
- `originImageName` at `template/wechat2rss/index.yaml:54`
- `image` at `template/wechat2rss/index.yaml:73`

### wewe-rss: `cooderl/wewe-rss:v2.6.1`
- `originImageName` at `template/wewe-rss/index.yaml:174`
- `image` at `template/wewe-rss/index.yaml:193`

### wewe-rss: `joseluisq/mysql-client:8.0.30`
- `image` at `template/wewe-rss/index.yaml:134`

### woocommerce: `mysql:8.0.30`
- `image` at `template/woocommerce/index.yaml:150`

### woocommerce: `wordpress:6.9.1-php8.3-apache`
- `originImageName` at `template/woocommerce/index.yaml:194`
- `image` at `template/woocommerce/index.yaml:333`

### woocommerce: `wordpress:cli-2.9.0-php8.3`
- `image` at `template/woocommerce/index.yaml:214`

### wordpress: `wordpress:6.5.4`
- `originImageName` at `template/wordpress/index.yaml:48`
- `image` at `template/wordpress/index.yaml:71`

### wrenai: `ghcr.io/canner/wren-ai-service:0.15.17`
- `originImageName` at `template/wrenai/index.yaml:206`
- `image` at `template/wrenai/index.yaml:228`

### wrenai: `ghcr.io/canner/wren-bootstrap:0.1.5`
- `image` at `template/wrenai/index.yaml:313`

### wrenai: `ghcr.io/canner/wren-engine-ibis:0.14.3`
- `originImageName` at `template/wrenai/index.yaml:383`
- `image` at `template/wrenai/index.yaml:405`

### wrenai: `ghcr.io/canner/wren-engine:0.14.3`
- `originImageName` at `template/wrenai/index.yaml:291`
- `image` at `template/wrenai/index.yaml:325`

### wrenai: `ghcr.io/canner/wren-ui:0.20.1`
- `originImageName` at `template/wrenai/index.yaml:644`
- `image` at `template/wrenai/index.yaml:666`

### wrenai: `qdrant/qdrant:v1.13.4`
- `originImageName` at `template/wrenai/index.yaml:466`
- `image` at `template/wrenai/index.yaml:488`
- `image` at `template/wrenai/index.yaml:516`

### wrenai: `senzing/postgresql-client:2.2.4`
- `image` at `template/wrenai/index.yaml:864`

### yourls: `mysql:8.0.30`
- `image` at `template/yourls/index.yaml:140`

### yourls: `yourls:1.10.1`
- `originImageName` at `template/yourls/index.yaml:178`
- `image` at `template/yourls/index.yaml:203`

### zitadel: `ghcr.io/zitadel/zitadel:v4.10.1`
- `originImageName` at `template/zitadel/index.yaml:135`
- `image` at `template/zitadel/index.yaml:155`

### zot: `ghcr.io/project-zot/zot:v2.1.14`
- `originImageName` at `template/zot/index.yaml:144`
- `image` at `template/zot/index.yaml:234`
- `originImageName` at `template/zot/index.yaml:296`
- `image` at `template/zot/index.yaml:316`

### zot: `httpd:2.4.63-alpine3.22`
- `image` at `template/zot/index.yaml:164`

## Updated Templates
- `s-pdf`: `ghcr.io/stirling-tools/stirling-pdf:1.2.0-fat` -> `ghcr.io/stirling-tools/stirling-pdf:2.13.2-fat`; normalized PostgreSQL init, ConfigMap mounts, init resources, service labels, and locale metadata.
- `wordpress`: `wordpress:6.5.4` -> `wordpress:7.0.0`; normalized MySQL secret wiring, resources, service, ingress, locale, and database labels.
- `tolgee`: `tolgee/tolgee:v3.113.0` -> `tolgee/tolgee:v3.205.5`; normalized PostgreSQL init, object storage secret envs, resources, and service labels.
- `strapi`: `vshadbolt/strapi:5.33.0` -> `vshadbolt/strapi:5.49.0`; normalized PostgreSQL init, ConfigMap script mount, resources, PVC size, service, ingress, and README facts.
- `zot`: `ghcr.io/project-zot/zot:v2.1.14` -> `ghcr.io/project-zot/zot:v2.1.18`; normalized object storage input, ConfigMap ownership, object storage secrets, and ConfigMap mounts.
- `zot`: `httpd:2.4.63-alpine3.22` -> `httpd:2.4.68-alpine3.24`; kept filesystem-mode htpasswd generation in the init container.
- `surveyking`: `joseluisq/mysql-client:8.0.30` -> `joseluisq/mysql-client:8.0.44`; normalized MySQL init resources and database/service/ingress/app contract fields.
- `surveyking`: `surveyking/surveyking:v1.9.0` -> `surveyking/surveyking:v1.12.0`; kept StatefulSet storage and switched runtime wiring to dbprovider secrets.
- `wewe-rss`: `joseluisq/mysql-client:8.0.30` -> `joseluisq/mysql-client:8.0.44`; normalized MySQL init resources, dbprovider labels, secret-backed port wiring, service labels, ingress defaults, and app container naming.
