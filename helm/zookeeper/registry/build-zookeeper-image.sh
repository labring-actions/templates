#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ZOOKEEPER_VERSION="${ZOOKEEPER_VERSION:-3.7.2}"
IMAGE_TAG="${IMAGE_TAG:-zookeeper-${ZOOKEEPER_VERSION}}"
BASE_IMAGE="${BASE_IMAGE:-crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey/sealos:base-dragonwell8-python3}"
REGISTRY="${REGISTRY:-}"

if [[ -z "${REGISTRY}" ]]; then
  echo "REGISTRY is required, for local builds use: REGISTRY=localhost:5000 $0" >&2
  exit 1
fi

IMAGE_REPOSITORY="${REGISTRY%/}/sealos"

docker build \
  --platform linux/amd64 \
  --build-arg ZOOKEEPER_VERSION="${ZOOKEEPER_VERSION}" \
  --build-arg BASE_IMAGE="${BASE_IMAGE}" \
  -t "${IMAGE_REPOSITORY}:${IMAGE_TAG}" \
  "${SCRIPT_DIR}/zookeeper"

docker push "${IMAGE_REPOSITORY}:${IMAGE_TAG}"

REGISTRY="${REGISTRY}" IMAGE_TAG="${IMAGE_TAG}" "${SCRIPT_DIR}/update-chart-image.sh"
