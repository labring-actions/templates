---
name: sealos-helm-cluster-image
description: Use when building or updating a Sealos cluster image that deploys software via Helm charts instead of Template CRs, deploy go-templates, or raw manifest bundles. Covers docker-to-sealos aligned Sealos platform rules for Kubefile packaging, chart layout, values/env wiring, labels/selectors, Ingress/App exposure, image pinning, storage/config handling, database integration, and validation.
---

# Sealos Helm Cluster Image

Use this skill when packaging an application as a Sealos cluster image backed by a Helm chart under `helm/<service>`.

This skill adapts the Sealos platform rules from `docker-to-sealos` to Helm-based cluster images. Do not copy Template CR syntax directly into Helm charts: `defaults`, `inputs`, `${{ SEALOS_CLOUD_DOMAIN }}`, `${{ SEALOS_CERT_SECRET_NAME }}`, and `${{ random(...) }}` are Template CR features, not Helm cluster-image inputs. Model those as `values.yaml` entries and wire them from `Kubefile` `ENV` values.

## Rule Priority

Use this precedence to prevent rule drift:

1. This `SKILL.md` Helm cluster-image rules.
2. Sealos platform MUST rules from `docker-to-sealos` for labels, App, Ingress, storage, images, resources, secrets, and validation.
3. Official Kubernetes manifests or installation docs for the target application.
4. Existing repository patterns under `helm/<service>`.

If official Kubernetes docs and Docker Compose examples conflict, keep Sealos platform constraints and prefer official Kubernetes runtime semantics for probes, bootstrap envs, external URL assumptions, protocol, and startup flow.

## Scope

This skill is for:

- `helm/<service>/Kubefile`
- `helm/<service>/charts/<service>`
- Helm chart manifests rendered by `helm template`
- Sealos cluster images installed with `helm upgrade --install`

It is not for:

- `template/<service>/index.yaml` Template CRs
- `deploy/<service>` go-template manifests
- plain `kubectl apply` bundles

## Required Output Layout

Create or update one package per service:

```text
helm/<service>/
├── Kubefile
├── README.md
├── registry/
│   └── .gitkeep
└── charts/
    └── <service>/
        ├── Chart.yaml
        ├── values.yaml
        └── templates/
            ├── configmap.yaml
            ├── deployment.yaml | statefulset.yaml | daemonset.yaml
            ├── service.yaml
            ├── ingress.yaml
            └── app.yaml
```

Add `serviceaccount.yaml`, `rbac.yaml`, database resources, Jobs, or extra components only when the application requires them.

## Standard Workflow

1. Inspect Docker Compose, upstream Helm chart, and official Kubernetes docs if available.
2. Decide whether a Helm cluster image is appropriate; use Template CR tooling only when the user asks for `template/<app>/index.yaml`.
3. Normalize runtime behavior to Sealos: `ClusterIP + Ingress + App` for UI services, persistent storage instead of `emptyDir`, explicit image versions, and Sealos labels.
4. Build a self-contained chart under `charts/<service>` with values for images, resources, storage, ingress, public URL, credentials, and feature toggles.
5. Wire runtime overrides from `Kubefile` `ENV` to Helm values with `--set-string` unless a value is clearly boolean or numeric.
6. Validate rendered YAML, labels/selectors, public URLs, storage, resources, and image tags before handing off.

## Kubefile Pattern

Use this shape unless the service has a strong reason to differ:

```dockerfile
FROM scratch

ENV NAMESPACE ns-admin
ENV APP_HOST <service>
ENV SEALOS_CLOUD_DOMAIN 127.0.0.1.nip.io
ENV SEALOS_CERT_SECRET_NAME wildcard-cert
ENV IMAGE_TAG <pinned-version>

COPY charts charts
COPY registry registry

CMD ["helm upgrade --install <service> charts/<service> --namespace=$(NAMESPACE) --create-namespace --set-string image.tag=$(IMAGE_TAG) --set-string sealos.hostPrefix=$(APP_HOST) --set-string sealos.cloudDomain=$(SEALOS_CLOUD_DOMAIN) --set-string sealos.certSecretName=$(SEALOS_CERT_SECRET_NAME)"]
```

Rules:

- Use `FROM scratch`.
- Keep operator-facing overrides in `ENV`; every `ENV` used in `CMD` must have a documented default.
- Use `COPY charts charts` and `COPY registry registry`.
- Install with `helm upgrade --install <release> charts/<chart> --namespace=$(NAMESPACE) --create-namespace`.
- Default release name should equal the service name for single-instance internal tooling.
- Use `--set-string` for domains, passwords, secret names, resource strings, image tags, storage classes, and values that must not be type-coerced.
- Use plain `--set` only for obvious numeric or boolean values.
- Keep README build/run examples synchronized with the current `ENV` list.

## Helm Values Contract

Put all runtime knobs in `values.yaml`. Prefer this baseline:

```yaml
image:
  repository: example/app
  tag: "1.0.0"
  pullPolicy: IfNotPresent

replicaCount: 1

resources:
  requests:
    cpu: 20m
    memory: 25Mi
  limits:
    cpu: 200m
    memory: 256Mi

sealos:
  hostPrefix: <service>
  cloudDomain: 127.0.0.1.nip.io
  certSecretName: wildcard-cert
```

Helm replacements for Template CR concepts:

- `defaults.app_name` -> a stable Helm release/component name, usually `<service>` or `{{ .Release.Name }}`.
- `defaults.app_host` -> `.Values.sealos.hostPrefix`, wired from `APP_HOST`.
- `inputs.*` -> explicit `values.yaml` fields wired from `Kubefile` `ENV` when user-configurable.
- `${{ SEALOS_CLOUD_DOMAIN }}` -> `.Values.sealos.cloudDomain`, wired from `SEALOS_CLOUD_DOMAIN`.
- `${{ SEALOS_CERT_SECRET_NAME }}` -> `.Values.sealos.certSecretName`, wired from `SEALOS_CERT_SECRET_NAME`.
- `${{ random(...) }}` -> a user-provided value or a Kubernetes-safe persisted secret pattern; avoid Helm random functions that change on upgrade.

## Chart Metadata

Keep `Chart.yaml` minimal and version-aligned:

```yaml
apiVersion: v2
name: <service>
description: <service> Helm chart for Sealos cluster image
version: 0.1.0
appVersion: "<app-version>"
type: application
```

When the target app version changes, update both `appVersion` and every image tag in `values.yaml`, then review major-version-sensitive configuration.

## Resource Naming And Labels

Rendered manifests must satisfy Sealos label conventions. Helper templates are fine, but the final YAML must be consistent.

For each managed app component:

- `metadata.name` is the component name.
- `metadata.labels.app` equals `metadata.name`.
- `metadata.labels.cloud.sealos.io/app-deploy-manager` equals `metadata.name`.
- Workload `spec.selector.matchLabels.app` equals `metadata.name`.
- Pod template `metadata.labels.app` equals `metadata.name`.
- `containers[*].name` equals the workload `metadata.name` for the main container.
- Service `metadata.name`, `metadata.labels.app`, `metadata.labels.cloud.sealos.io/app-deploy-manager`, and `spec.selector.app` all use the same component name.
- Ingress `metadata.name`, `metadata.labels.cloud.sealos.io/app-deploy-manager`, and backend `service.name` all use the exposed service name.
- Every Service port has an explicit `name`.

Use release-scoped names for cluster-scoped resources:

```yaml
metadata:
  name: {{ printf "%s-reader" .Release.Name }}
```

Do not create fixed-name `ClusterRole`, `ClusterRoleBinding`, or webhook resources that collide across installs.

## Workload Baseline

For `Deployment`, `StatefulSet`, `DaemonSet`, `Job`, and `CronJob` pod specs:

- Set `imagePullPolicy: IfNotPresent` on every container.
- Pin images to explicit versions or digests; never use `:latest`, `:stable`, broad major/minor tags, or unresolved Compose variables.
- Add `resources.requests` and `resources.limits` for every container.
- Default lightweight app resources to `requests(cpu=20m,memory=25Mi)` and `limits(cpu=200m,memory=256Mi)` unless source docs justify more.
- Set `revisionHistoryLimit: 1` on Deployments/StatefulSets/DaemonSets that support it.
- Set `automountServiceAccountToken: false` unless the pod explicitly needs Kubernetes API access; if it does, create a dedicated ServiceAccount/RBAC.
- Add official `readinessProbe`, `livenessProbe`, and for slow boot apps `startupProbe` when official health checks exist.
- Add workload annotations for Sealos-managed apps:

```yaml
metadata:
  annotations:
    originImageName: {{ printf "%s:%s" .Values.image.repository .Values.image.tag | quote }}
    deploy.cloud.sealos.io/minReplicas: "1"
    deploy.cloud.sealos.io/maxReplicas: "1"
```

For `CronJob`, include these labels:

```yaml
metadata:
  labels:
    cloud.sealos.io/cronjob: <cronjob-name>
    cronjob-launchpad-name: ""
    cronjob-type: image
```

## Storage And Config Files

Sealos-oriented charts must not use `emptyDir`.

- Use `StatefulSet.volumeClaimTemplates` for persistent app data.
- Do not create standalone PVCs unless an upstream chart absolutely requires one and the tradeoff is documented.
- Default generic app storage to `1Gi`; expose larger sizes via values only when official requirements justify them.
- Use `ConfigMap` for config files and mount individual files with `subPath` when appropriate.
- When converting file paths from Compose/docs, use docker-to-sealos `vn-` naming for ConfigMap keys and volume names: replace `/`, `-`, `.`, and other special characters with `vn-`.
- Component-scoped ConfigMaps must have `metadata.name`, `metadata.labels.app`, and `metadata.labels.cloud.sealos.io/app-deploy-manager` all equal to the component name.
- If a config file is mounted with `subPath`, do not claim hot reload works unless the application actually reloads that file.

## Service Exposure

Default exposure model:

- internal service: `ClusterIP`
- external access: `Ingress`
- Sealos desktop entry: `app.sealos.io/v1` `App`

Do not add `NodePort` unless the user explicitly asks for it.

`App` does not replace `Ingress`. `App` is desktop metadata and a launch entry; browser access still needs a reachable URL backed by Ingress or another external path.

### Ingress Pattern

Use the Sealos public URL shape and standard nginx annotations:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: <component>
  namespace: {{ .Release.Namespace }}
  labels:
    app: <component>
    cloud.sealos.io/app-deploy-manager: <component>
    cloud.sealos.io/app-deploy-manager-domain: {{ .Values.sealos.hostPrefix | quote }}
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/proxy-body-size: 32m
    nginx.ingress.kubernetes.io/server-snippet: |
      client_header_buffer_size 64k;
      large_client_header_buffers 4 128k;
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/backend-protocol: HTTP
    nginx.ingress.kubernetes.io/client-body-buffer-size: 64k
    nginx.ingress.kubernetes.io/proxy-buffer-size: 64k
    nginx.ingress.kubernetes.io/proxy-send-timeout: "300"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
    nginx.ingress.kubernetes.io/configuration-snippet: |
      if ($request_uri ~* \.(js|css|gif|jpe?g|png)) {
        expires 30d;
        add_header Cache-Control "public";
      }
spec:
  tls:
    - hosts:
        - {{ .Values.sealos.hostPrefix }}.{{ .Values.sealos.cloudDomain }}
      secretName: {{ .Values.sealos.certSecretName }}
  rules:
    - host: {{ .Values.sealos.hostPrefix }}.{{ .Values.sealos.cloudDomain }}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: <component>
                port:
                  number: <port>
```

If Compose exposes both 80 and 443 and official Kubernetes docs do not require HTTPS backend traffic, terminate TLS at Sealos Ingress, keep the HTTP backend port, and remove in-container certificate mounts. Use `backend-protocol: HTTPS` only when the backend truly serves HTTPS.

### App Pattern

Use `spec.data.url`; never use `spec.template`.

```yaml
apiVersion: app.sealos.io/v1
kind: App
metadata:
  name: <component>
  namespace: {{ .Release.Namespace }}
  labels:
    app: <component>
    cloud.sealos.io/app-deploy-manager: <component>
spec:
  data:
    url: https://{{ .Values.sealos.hostPrefix }}.{{ .Values.sealos.cloudDomain }}/
  displayType: normal
  icon: "<square-or-circular-bitmap-icon-url>"
  name: "<Display Name>"
  type: link
```

Rules:

- Point `url` to the actual user entry path, such as `/login` when that is the real landing route.
- Prefer square or circular icon-first bitmap assets; avoid rectangular wordmarks and SVGs that render poorly in the target UI.
- Keep `type: link` unless iframe embedding is specifically desired and known to work.
- The App URL and Ingress host/path must match.

## Environment And Secrets

- Declare env vars before other env vars reference them with `$(VAR)`.
- Follow official app env names; do not invent prefixes if the app already documents names.
- Use Kubernetes FQDNs for service-to-service references: `<service>.<namespace>.svc.cluster.local`.
- For database connection fields (`host`, `port`, `endpoint`, `username`, `password`), use approved Kubeblocks secret names when the chart creates or consumes Sealos-managed databases.
- Do not redefine reserved Kubeblocks database secrets with custom `Secret` resources.
- Non-database sensitive values may be passed from `values.yaml` as direct env values when matching Sealos template behavior; if an upstream app requires a Secret resource, make its name release-scoped and preserve values across upgrades.

Common database secret names:

- PostgreSQL: `<app>-pg-conn-credential`
- MongoDB: `<app>-mongodb-account-root`
- MySQL: `<app>-mysql-conn-credential`
- Redis: `<app>-redis-redis-account-default`
- Kafka: `<app>-broker-account-admin`

When constructing a URL/DSN, inject the secret-backed parts first:

```yaml
env:
  - name: DB_HOST
    valueFrom:
      secretKeyRef:
        name: <app>-pg-conn-credential
        key: host
  - name: DB_PORT
    valueFrom:
      secretKeyRef:
        name: <app>-pg-conn-credential
        key: port
  - name: DB_USERNAME
    valueFrom:
      secretKeyRef:
        name: <app>-pg-conn-credential
        key: username
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: <app>-pg-conn-credential
        key: password
  - name: DATABASE_URL
    value: postgresql://$(DB_USERNAME):$(DB_PASSWORD)@$(DB_HOST):$(DB_PORT)/postgres
```

## Databases And Object Storage

If a Helm cluster image creates Sealos-managed databases, follow the same Kubeblocks structures and secret naming used by `docker-to-sealos`.

Condensed rules:

- PostgreSQL uses `apps.kubeblocks.io/v1alpha1`, `clusterVersionRef: postgresql-16.4.0`, and the `postgresql-16.4.0` label set.
- PostgreSQL RBAC names are unified as `<app>-pg`.
- PostgreSQL custom databases require an idempotent init Job that waits for readiness before creating the database.
- MongoDB uses `componentDef: mongodb` and `serviceVersion: 8.0.4`.
- MySQL uses `clusterDefinitionRef: apecloud-mysql` and `clusterVersionRef: ac-mysql-8.0.30-1`.
- Redis uses `componentDef: redis-7`, `componentDef: redis-sentinel-7`, `serviceVersion: 7.2.7`, and replication topology.
- Database component resources default to `requests(cpu=50m,memory=51Mi)` and `limits(cpu=500m,memory=512Mi)` unless source docs require more.

Object storage should use Sealos object-storage secrets rather than custom credentials. Preserve these environment conventions when needed:

- `object-storage-key` for access key, secret key, and external endpoint.
- `object-storage-key-<service-account>-<app>` for bucket-specific fields.
- S3 endpoints built from the injected external endpoint.
- Path-style access enabled when required by the source app.

## Migration From Template CRs

When converting an existing `template/<service>/index.yaml` to a Helm cluster image:

- Remove the `kind: Template` wrapper and Template metadata.
- Convert `${{ defaults.* }}` and `${{ inputs.* }}` to Helm values.
- Replace `${{ SEALOS_NAMESPACE }}` with `{{ .Release.Namespace }}` or a rendered FQDN using `.Release.Namespace`.
- Replace `${{ SEALOS_CLOUD_DOMAIN }}` and `${{ SEALOS_CERT_SECRET_NAME }}` with chart values wired from Kubefile envs.
- Move image tags, resources, storage sizes, hosts, secret names, and feature toggles into `values.yaml`.
- Keep the Sealos labels, App `spec.data.url`, Ingress annotations, storage, and image pinning rules.
- Preserve resource order conceptually: database/object storage first, config/RBAC before workloads, Service before Ingress, App last.

## ELK-Specific Lessons

These came from packaging Elasticsearch, Logstash, Filebeat, and Kibana.

### Elasticsearch

- Keep TLS secret names configurable.
- Do not reuse a persisted 8.x data volume when downgrading to 7.x.
- If targeting Elastic 7.x, make sure version metadata does not still say 8.x.
- StatefulSet PVC names are stable; deleting the release does not delete PVCs by default.

### Logstash

- If config is mounted with `subPath`, do not pretend automatic reload works.
- Set `config.reload.automatic: false` when using `subPath`-mounted config files.
- Leaving `stdout { codec => rubydebug }` is useful for debugging but risky in production because Filebeat may re-collect those logs if exclusions are weak.

### Filebeat

- Use release-scoped names for `ClusterRole` and `ClusterRoleBinding`.
- In containerd clusters, collect from `/var/log/containers` and `/var/log/pods`; do not assume Docker paths are needed.
- Exclude Filebeat and Logstash self-logs if the pipeline writes debug logs to stdout.

### Kibana

- Use `kibana_system`, not `elastic`, for Kibana-to-Elasticsearch service auth.
- If you add a desktop icon, keep both `Ingress` and `App`.
- Keep public access simple: `ClusterIP + Ingress + App`.
- Avoid extra host knobs unless the user explicitly needs them; `kibana.<domain>` is usually enough.

## Validation Checklist

Always run or manually perform equivalent checks before handing off:

1. `helm lint helm/<service>/charts/<service>`
2. `helm template <release> helm/<service>/charts/<service> --namespace ns-admin` with the same key `--set`/`--set-string` values used by `Kubefile`.
3. Parse the rendered YAML to catch syntax issues.
4. Check every templated value exists in `values.yaml` or is passed from `Kubefile`.
5. Check image tags are explicit and every container has `imagePullPolicy: IfNotPresent`.
6. Check workload resources, `revisionHistoryLimit`, `automountServiceAccountToken`, probes, labels, selectors, and container names.
7. Check there is no `emptyDir` and storage/config names follow the expected patterns.
8. Check cluster-scoped resources are release-scoped.
9. Check Service, Ingress, and App names/labels/URLs are consistent.
10. Check README examples match the current `Kubefile` env list.

## Good Defaults

Prefer these unless the user asks otherwise or official docs require a different value:

- namespace: `ns-admin`
- release name: service name
- service type: `ClusterIP`
- external exposure: Sealos Ingress
- desktop entry: App enabled when the service has a UI
- image pull policy: `IfNotPresent`
- app resources: `requests(cpu=20m,memory=25Mi)`, `limits(cpu=200m,memory=256Mi)`
- generic storage: `1Gi`
- README included with build, install, env, URL, and uninstall examples

## When To Push Back

Pause and confirm with the user if:

- preserving data across a major version downgrade is required
- the requested exposure mode removes Ingress but still expects browser access from Sealos desktop
- fixed cluster-scoped resource names would collide in a shared cluster
- the app needs `emptyDir`, privileged host access, or broad Kubernetes API permissions
- version changes introduce known auth, storage, security, or config model differences
