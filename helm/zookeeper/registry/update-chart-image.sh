#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHART_VALUES="${SCRIPT_DIR}/../charts/zookeeper/values.yaml"
KUBEFILE="${SCRIPT_DIR}/../Kubefile"

REGISTRY="${REGISTRY:-}"
IMAGE_TAG="${IMAGE_TAG:-zookeeper-3.7.2}"

if [[ -z "${REGISTRY}" ]]; then
  echo "REGISTRY is required" >&2
  exit 1
fi

IMAGE_REPOSITORY="${REGISTRY%/}/sealos"

python3 - "$CHART_VALUES" "$KUBEFILE" "$IMAGE_REPOSITORY" "$IMAGE_TAG" <<'PY'
from pathlib import Path
import sys

values_path = Path(sys.argv[1])
kubefile_path = Path(sys.argv[2])
repository = sys.argv[3]
tag = sys.argv[4]

values = values_path.read_text()
values = values.replace(
    "    repository: crpi-wsxiy5y9ovijxdks.cn-hangzhou.personal.cr.aliyuncs.com/jockey/sealos\n",
    f"    repository: {repository}\n",
)
values = values.replace("    tag: zookeeper-3.7.2\n", f"    tag: {tag}\n")
values_path.write_text(values)

kubefile = kubefile_path.read_text()
lines = []
for line in kubefile.splitlines():
    if line.startswith("ENV ZOOKEEPER_IMAGE_REPOSITORY "):
        lines.append(f"ENV ZOOKEEPER_IMAGE_REPOSITORY {repository}")
    elif line.startswith("ENV ZOOKEEPER_IMAGE_TAG "):
        lines.append(f"ENV ZOOKEEPER_IMAGE_TAG {tag}")
    else:
        lines.append(line)
kubefile_path.write_text("\n".join(lines) + "\n")
PY
