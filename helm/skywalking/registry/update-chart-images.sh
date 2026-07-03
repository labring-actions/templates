#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKYWALKING_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
CHART_DIR="${SKYWALKING_DIR}/charts/skywalking"

SKYWALKING_VERSION="${SKYWALKING_VERSION:-10.4.0}"
IMAGE_TAG="${IMAGE_TAG:-${SKYWALKING_VERSION}-dragonwell21}"
REGISTRY="${REGISTRY:-}"

if [[ -z "${REGISTRY}" ]]; then
  echo "REGISTRY is required, for example: REGISTRY=crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey $0" >&2
  exit 1
fi

IMAGE_PREFIX="${REGISTRY%/}/"
OAP_IMAGE_REPOSITORY="${IMAGE_PREFIX}skywalking-oap-server-dragonwell"
UI_IMAGE_REPOSITORY="${IMAGE_PREFIX}skywalking-ui-dragonwell"

perl -0pi -e "s|ENV SKYWALKING_OAP_IMAGE_REPOSITORY .*|ENV SKYWALKING_OAP_IMAGE_REPOSITORY ${OAP_IMAGE_REPOSITORY}|; s|ENV SKYWALKING_UI_IMAGE_REPOSITORY .*|ENV SKYWALKING_UI_IMAGE_REPOSITORY ${UI_IMAGE_REPOSITORY}|; s|ENV SKYWALKING_IMAGE_TAG .*|ENV SKYWALKING_IMAGE_TAG ${IMAGE_TAG}|" "${SKYWALKING_DIR}/Kubefile"
perl -0pi -e "s|repository: .*skywalking-oap-server-dragonwell|repository: ${OAP_IMAGE_REPOSITORY}|; s|repository: .*skywalking-ui-dragonwell|repository: ${UI_IMAGE_REPOSITORY}|; s|tag: [^\\n]*dragonwell21|tag: ${IMAGE_TAG}|g" "${CHART_DIR}/values.yaml"

if ! grep -q "repository: ${OAP_IMAGE_REPOSITORY}" "${CHART_DIR}/values.yaml"; then
  echo "Failed to update OAP image repository in ${CHART_DIR}/values.yaml" >&2
  exit 1
fi

if ! grep -q "repository: ${UI_IMAGE_REPOSITORY}" "${CHART_DIR}/values.yaml"; then
  echo "Failed to update UI image repository in ${CHART_DIR}/values.yaml" >&2
  exit 1
fi

if command -v helm >/dev/null 2>&1; then
  if helm template skywalking "${CHART_DIR}" --namespace ns-admin | grep -q 'image: "skywalking-.*-dragonwell:'; then
    echo "Rendered chart still contains unqualified Dragonwell image names. Refusing to continue." >&2
    exit 1
  fi
fi

echo "Updated chart defaults:"
echo "  OAP: ${OAP_IMAGE_REPOSITORY}:${IMAGE_TAG}"
echo "  UI:  ${UI_IMAGE_REPOSITORY}:${IMAGE_TAG}"
