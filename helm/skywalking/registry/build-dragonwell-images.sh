#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SKYWALKING_VERSION="${SKYWALKING_VERSION:-10.4.0}"
IMAGE_TAG="${IMAGE_TAG:-${SKYWALKING_VERSION}-dragonwell21}"
DRAGONWELL_IMAGE="${DRAGONWELL_IMAGE:-alibabadragonwell/dragonwell:21-alinux}"
REGISTRY="${REGISTRY:-}"

if [[ -z "${REGISTRY}" ]]; then
  echo "REGISTRY is required, for local builds use: REGISTRY=localhost:5000 $0" >&2
  exit 1
fi

IMAGE_PREFIX="${REGISTRY%/}/"
OAP_IMAGE_REPOSITORY="${IMAGE_PREFIX}skywalking-oap-server-dragonwell"
UI_IMAGE_REPOSITORY="${IMAGE_PREFIX}skywalking-ui-dragonwell"

docker build \
  --platform linux/amd64 \
  --build-arg SKYWALKING_VERSION="${SKYWALKING_VERSION}" \
  --build-arg DRAGONWELL_IMAGE="${DRAGONWELL_IMAGE}" \
  -t "${OAP_IMAGE_REPOSITORY}:${IMAGE_TAG}" \
  "${SCRIPT_DIR}/oap"

docker build \
  --platform linux/amd64 \
  --build-arg SKYWALKING_VERSION="${SKYWALKING_VERSION}" \
  --build-arg DRAGONWELL_IMAGE="${DRAGONWELL_IMAGE}" \
  -t "${UI_IMAGE_REPOSITORY}:${IMAGE_TAG}" \
  "${SCRIPT_DIR}/ui"

docker push "${OAP_IMAGE_REPOSITORY}:${IMAGE_TAG}"
docker push "${UI_IMAGE_REPOSITORY}:${IMAGE_TAG}"

REGISTRY="${REGISTRY}" IMAGE_TAG="${IMAGE_TAG}" "${SCRIPT_DIR}/update-chart-images.sh"
