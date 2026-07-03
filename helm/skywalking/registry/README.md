# SkyWalking Dragonwell Images

This directory contains the Dockerfiles used to rebuild SkyWalking OAP and UI on a Dragonwell base image.

Default base image:

```text
alibabadragonwell/dragonwell:21-alinux
```

For local Sealos image builds, start a local registry first:

```bash
docker run -d --restart=always -p 5000:5000 --name local-registry registry:2
```

Build, push, and update chart defaults:

```bash
REGISTRY=localhost:5000 ./build-dragonwell-images.sh
```

Override versions:

```bash
SKYWALKING_VERSION=10.4.0 \
IMAGE_TAG=10.4.0-dragonwell21 \
DRAGONWELL_IMAGE=alibabadragonwell/dragonwell:21-alinux \
REGISTRY=localhost:5000 \
./build-dragonwell-images.sh
```

`REGISTRY` is required. Use `localhost:5000` for local-only builds, or a real remote registry prefix for shared builds. The Sealos cluster image build reads image references from the chart and tries to save those images. Unqualified local names such as `skywalking-ui-dragonwell:10.4.0-dragonwell21` are resolved as `docker.io/library/...` and will fail unless they exist in Docker Hub.

Before `sealos build`, verify the rendered images:

```bash
helm template skywalking ../charts/skywalking --namespace ns-admin | grep 'image:'
```

If Docker image build/push happens on one machine and `sealos build` runs on another machine, run this on the `sealos build` machine to update the chart only:

```bash
REGISTRY=crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey ./update-chart-images.sh
```
