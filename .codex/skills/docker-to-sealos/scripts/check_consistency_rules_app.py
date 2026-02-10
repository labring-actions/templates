#!/usr/bin/env python3
"""Application-centric consistency rules."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from check_consistency_models import LATEST_IMAGE_PATTERN, TEMPLATE_NAME_PATTERN, Rule, ScanContext, Violation
from check_consistency_helpers_violations import (
    add_doc_violation,
    check_managed_workload_setting,
)
from check_consistency_helpers_workload import (
    get_template_spec,
    has_managed_workload_marker,
    is_app_workload_document,
    iter_documents_by_kind,
)


TEMPLATE_ARTIFACT_SUFFIXES = {".yaml", ".yml"}
TEMPLATE_REQUIRED_SPEC_FIELDS = {
    "title": str,
    "url": str,
    "gitRepo": str,
    "author": str,
    "description": str,
    "icon": str,
    "templateType": str,
    "locale": str,
    "i18n": dict,
    "categories": list,
}
FLOATING_TAG_ALIASES = {"latest", "stable", "main", "master", "edge", "nightly", "dev"}
FLOATING_NUMERIC_TAG_RE = re.compile(r"^v?\d+(?:\.\d+)?$")
COMPOSE_VAR_IN_IMAGE_RE = re.compile(r"\$(?:\{[^}]+\}|[A-Za-z_][A-Za-z0-9_]*)")
ZH_CHAR_RE = re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF]")
ALLOWED_TEMPLATE_CATEGORIES = {
    "tool",
    "ai",
    "game",
    "database",
    "low-code",
    "monitor",
    "dev-ops",
    "blog",
    "storage",
    "frontend",
    "backend",
}
TEMPLATE_README_BASE = "https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template"
HTTP_INGRESS_REQUIRED_ANNOTATIONS: Dict[str, str] = {
    "kubernetes.io/ingress.class": "nginx",
    "nginx.ingress.kubernetes.io/proxy-body-size": "32m",
    "nginx.ingress.kubernetes.io/server-snippet": (
        "client_header_buffer_size 64k;\n"
        "large_client_header_buffers 4 128k;"
    ),
    "nginx.ingress.kubernetes.io/ssl-redirect": "true",
    "nginx.ingress.kubernetes.io/backend-protocol": "HTTP",
    "nginx.ingress.kubernetes.io/client-body-buffer-size": "64k",
    "nginx.ingress.kubernetes.io/proxy-buffer-size": "64k",
    "nginx.ingress.kubernetes.io/proxy-send-timeout": "300",
    "nginx.ingress.kubernetes.io/proxy-read-timeout": "300",
    "nginx.ingress.kubernetes.io/configuration-snippet": (
        "if ($request_uri ~* \\.(js|css|gif|jpe?g|png)) {\n"
        "  expires 30d;\n"
        "  add_header Cache-Control \"public\";\n"
        "}"
    ),
}
OFFICIAL_HEALTH_HTTP_EXPECTATIONS: Dict[str, Dict[str, str]] = {
    "goauthentik/server": {
        "liveness_path": "/-/health/live/",
        "readiness_path": "/-/health/ready/",
        "startup_path": "/-/health/ready/",
    }
}
OFFICIAL_HEALTH_WORKER_EXEC_EXPECTATIONS: Dict[str, Dict[str, str]] = {
    "goauthentik/server": {
        "liveness_command": "ak healthcheck",
        "readiness_command": "ak healthcheck",
        "startup_command": "ak healthcheck",
    },
}


def _iter_template_artifact_documents(context: ScanContext) -> Iterable:
    for doc in iter_documents_by_kind(context, "Template"):
        if doc.path.suffix.lower() in TEMPLATE_ARTIFACT_SUFFIXES:
            yield doc


def _is_non_empty_value(value: Any, expected_type: type) -> bool:
    if expected_type is str:
        return isinstance(value, str) and bool(value.strip())
    if expected_type is dict:
        return isinstance(value, dict) and len(value) > 0
    if expected_type is list:
        return isinstance(value, list) and len(value) > 0
    return isinstance(value, expected_type)


def _extract_template_directory_name(path: Path) -> str:
    parts = path.parts
    if "template" not in parts:
        return ""
    index = parts.index("template")
    if index + 1 >= len(parts):
        return ""
    return parts[index + 1]


def check_no_latest_tags(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    for doc in context.yaml_documents:
        if doc.skip_checks:
            continue
        for line_no, line in enumerate(doc.source.splitlines(), start=doc.start_line):
            if LATEST_IMAGE_PATTERN.search(line):
                violations.append(
                    Violation(
                        rule_id="R001",
                        path=doc.path,
                        line=line_no,
                        message="forbidden ':latest' image tag",
                    )
                )
    return violations


def _extract_image_tag(image: str) -> Optional[str]:
    text = image.strip()
    if not text or "@sha256:" in text:
        return None
    without_digest = text.split("@", 1)[0]
    last_segment = without_digest.rsplit("/", 1)[-1]
    if ":" not in last_segment:
        return None
    return last_segment.rsplit(":", 1)[-1].strip()


def _is_floating_tag(tag: str) -> bool:
    normalized = tag.strip().lower()
    if normalized in FLOATING_TAG_ALIASES:
        return True
    return FLOATING_NUMERIC_TAG_RE.fullmatch(normalized) is not None


def check_no_floating_image_tags(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    for doc in context.yaml_documents:
        if doc.skip_checks or not isinstance(doc.data, dict):
            continue
        if not is_app_workload_document(doc):
            continue
        if not has_managed_workload_marker(doc.data):
            continue

        metadata = doc.data.get("metadata")
        annotations = metadata.get("annotations") if isinstance(metadata, dict) else None
        origin_image = annotations.get("originImageName") if isinstance(annotations, dict) else None
        values: List[tuple[str, str]] = []
        if isinstance(origin_image, str) and origin_image.strip():
            values.append(("originImageName", origin_image.strip()))

        template_spec = get_template_spec(doc.data)
        containers = template_spec.get("containers") if isinstance(template_spec, dict) else None
        if isinstance(containers, list):
            for container in containers:
                if not isinstance(container, dict):
                    continue
                image = container.get("image")
                if isinstance(image, str) and image.strip():
                    values.append(("image", image.strip()))

        for field_name, image_value in values:
            tag = _extract_image_tag(image_value)
            if tag is None or not _is_floating_tag(tag):
                continue
            pattern = r"originImageName" if field_name == "originImageName" else r"^\s*image\s*:"
            add_doc_violation(
                violations,
                rule_id="R016",
                doc=doc,
                pattern=pattern,
                default_pattern=r"^\s*metadata\s*:" if field_name == "originImageName" else r"^\s*containers\s*:",
                message=(
                    f"floating image tag '{tag}' is not allowed; "
                    "use an explicit version tag (e.g. v2.2.0) or digest"
                ),
            )

    return violations


def check_no_compose_image_variables(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    for doc in context.yaml_documents:
        if doc.skip_checks or not isinstance(doc.data, dict):
            continue
        if not is_app_workload_document(doc):
            continue
        if not has_managed_workload_marker(doc.data):
            continue

        metadata = doc.data.get("metadata")
        annotations = metadata.get("annotations") if isinstance(metadata, dict) else None
        origin_image = annotations.get("originImageName") if isinstance(annotations, dict) else None
        values: List[tuple[str, str]] = []
        if isinstance(origin_image, str) and origin_image.strip():
            values.append(("originImageName", origin_image.strip()))

        template_spec = get_template_spec(doc.data)
        containers = template_spec.get("containers") if isinstance(template_spec, dict) else None
        if isinstance(containers, list):
            for container in containers:
                if not isinstance(container, dict):
                    continue
                image = container.get("image")
                if isinstance(image, str) and image.strip():
                    values.append(("image", image.strip()))

        for field_name, image_value in values:
            if COMPOSE_VAR_IN_IMAGE_RE.search(image_value) is None:
                continue
            pattern = r"originImageName" if field_name == "originImageName" else r"^\s*image\s*:"
            add_doc_violation(
                violations,
                rule_id="R018",
                doc=doc,
                pattern=pattern,
                default_pattern=r"^\s*metadata\s*:" if field_name == "originImageName" else r"^\s*containers\s*:",
                message=(
                    "image references must be concrete and must not contain Compose-style variables; "
                    "resolve to explicit tag or digest before emitting template artifacts"
                ),
            )
    return violations


def check_app_no_spec_template(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    for doc in iter_documents_by_kind(context, "App"):
        spec = doc.data.get("spec") if isinstance(doc.data, dict) else None
        if isinstance(spec, dict) and "template" in spec:
            add_doc_violation(
                violations,
                rule_id="R002",
                doc=doc,
                pattern=r"^\s*template\s*:",
                default_pattern=r"^\s*spec\s*:",
                message="App resource must not use spec.template",
            )
    return violations


def check_app_has_spec_data_url(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    for doc in iter_documents_by_kind(context, "App"):
        spec = doc.data.get("spec") if isinstance(doc.data, dict) else None
        data = spec.get("data") if isinstance(spec, dict) else None
        url = data.get("url") if isinstance(data, dict) else None
        if not isinstance(url, str) or not url.strip():
            add_doc_violation(
                violations,
                rule_id="R003",
                doc=doc,
                pattern=r"^\s*data\s*:",
                default_pattern=r"^\s*spec\s*:",
                message="App resource must define spec.data.url",
            )
    return violations


def check_template_name_is_hardcoded_lowercase(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    for doc in iter_documents_by_kind(context, "Template"):
        metadata = doc.data.get("metadata") if isinstance(doc.data, dict) else None
        name = metadata.get("name") if isinstance(metadata, dict) else None

        if not isinstance(name, str):
            add_doc_violation(
                violations,
                rule_id="R004",
                doc=doc,
                pattern=r"^\s*metadata\s*:",
                message="Template metadata.name must be a hardcoded lowercase string",
            )
            continue

        if "${{" in name or not TEMPLATE_NAME_PATTERN.fullmatch(name):
            add_doc_violation(
                violations,
                rule_id="R004",
                doc=doc,
                pattern=r"^\s*name\s*:",
                message="Template metadata.name must be hardcoded lowercase and must not use variables",
            )

    return violations


def check_template_required_metadata_fields(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    for doc in _iter_template_artifact_documents(context):
        spec = doc.data.get("spec") if isinstance(doc.data, dict) else None
        if not isinstance(spec, dict):
            add_doc_violation(
                violations,
                rule_id="R012",
                doc=doc,
                pattern=r"^\s*spec\s*:",
                message="Template must define spec with required metadata fields",
            )
            continue

        for field, expected_type in TEMPLATE_REQUIRED_SPEC_FIELDS.items():
            if _is_non_empty_value(spec.get(field), expected_type):
                continue
            add_doc_violation(
                violations,
                rule_id="R012",
                doc=doc,
                pattern=rf"^\s*{re.escape(field)}\s*:",
                default_pattern=r"^\s*spec\s*:",
                message=f"Template spec.{field} must be defined and non-empty",
            )
    return violations


def check_template_folder_matches_name(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    for doc in _iter_template_artifact_documents(context):
        if doc.path.name != "index.yaml":
            continue
        expected_name = _extract_template_directory_name(doc.path.resolve())
        if not expected_name:
            continue

        metadata = doc.data.get("metadata") if isinstance(doc.data, dict) else None
        actual_name = metadata.get("name") if isinstance(metadata, dict) else None
        if not isinstance(actual_name, str):
            continue
        if expected_name == actual_name:
            continue
        add_doc_violation(
            violations,
            rule_id="R013",
            doc=doc,
            pattern=r"^\s*name\s*:",
            default_pattern=r"^\s*metadata\s*:",
            message=f"Template folder name '{expected_name}' must match metadata.name '{actual_name}'",
        )
    return violations


def check_template_icon_paths(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    for doc in _iter_template_artifact_documents(context):
        metadata = doc.data.get("metadata") if isinstance(doc.data, dict) else None
        spec = doc.data.get("spec") if isinstance(doc.data, dict) else None
        app_name = metadata.get("name") if isinstance(metadata, dict) else None
        if not isinstance(app_name, str) or not isinstance(spec, dict):
            continue

        icon = spec.get("icon")
        if isinstance(icon, str):
            icon_pattern = re.compile(
                rf"^https://raw\.githubusercontent\.com/.+/kb-0\.9/template/{re.escape(app_name)}/logo\.[A-Za-z0-9]+$"
            )
            if icon_pattern.fullmatch(icon.strip()) is None:
                add_doc_violation(
                    violations,
                    rule_id="R014",
                    doc=doc,
                    pattern=r"^\s*icon\s*:",
                    default_pattern=r"^\s*spec\s*:",
                    message="Template spec.icon must point to raw.githubusercontent.com/.../kb-0.9/template/<app-name>/logo.<ext>",
                )
    return violations


def check_template_readme_paths(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    for doc in _iter_template_artifact_documents(context):
        metadata = doc.data.get("metadata") if isinstance(doc.data, dict) else None
        spec = doc.data.get("spec") if isinstance(doc.data, dict) else None
        app_name = metadata.get("name") if isinstance(metadata, dict) else None
        if not isinstance(app_name, str) or not isinstance(spec, dict):
            continue

        expected_readme = f"{TEMPLATE_README_BASE}/{app_name}/README.md"
        expected_zh_readme = f"{TEMPLATE_README_BASE}/{app_name}/README_zh.md"

        readme = spec.get("readme")
        if not (isinstance(readme, str) and readme.strip() == expected_readme):
            add_doc_violation(
                violations,
                rule_id="R025",
                doc=doc,
                pattern=r"^\s*readme\s*:",
                default_pattern=r"^\s*spec\s*:",
                message=f"Template spec.readme must be '{expected_readme}'",
            )

        i18n = spec.get("i18n") if isinstance(spec, dict) else None
        zh = i18n.get("zh") if isinstance(i18n, dict) else None
        zh_readme = zh.get("readme") if isinstance(zh, dict) else None
        if not (isinstance(zh_readme, str) and zh_readme.strip() == expected_zh_readme):
            add_doc_violation(
                violations,
                rule_id="R025",
                doc=doc,
                pattern=r"^\s*i18n\s*:",
                default_pattern=r"^\s*spec\s*:",
                message=f"Template spec.i18n.zh.readme must be '{expected_zh_readme}'",
            )

    return violations


def check_template_i18n_zh_description_chinese(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    for doc in _iter_template_artifact_documents(context):
        spec = doc.data.get("spec") if isinstance(doc.data, dict) else None
        i18n = spec.get("i18n") if isinstance(spec, dict) else None
        zh = i18n.get("zh") if isinstance(i18n, dict) else None
        description = zh.get("description") if isinstance(zh, dict) else None

        if isinstance(description, str) and description.strip() and ZH_CHAR_RE.search(description):
            continue

        add_doc_violation(
            violations,
            rule_id="R021",
            doc=doc,
            pattern=r"^\s*i18n\s*:",
            default_pattern=r"^\s*spec\s*:",
            message="Template spec.i18n.zh.description must be provided in Simplified Chinese",
        )
    return violations


def check_template_i18n_zh_title_absent(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    for doc in _iter_template_artifact_documents(context):
        spec = doc.data.get("spec") if isinstance(doc.data, dict) else None
        i18n = spec.get("i18n") if isinstance(spec, dict) else None
        zh = i18n.get("zh") if isinstance(i18n, dict) else None
        if not isinstance(zh, dict):
            continue
        if "title" not in zh:
            continue

        add_doc_violation(
            violations,
            rule_id="R022",
            doc=doc,
            pattern=r"^\s*i18n\s*:",
            default_pattern=r"^\s*spec\s*:",
            message="Template spec.i18n.zh.title should be omitted when it is identical to spec.title",
        )
    return violations


def check_template_categories_allowed(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    allowed = ", ".join(sorted(ALLOWED_TEMPLATE_CATEGORIES))
    for doc in _iter_template_artifact_documents(context):
        spec = doc.data.get("spec") if isinstance(doc.data, dict) else None
        categories = spec.get("categories") if isinstance(spec, dict) else None
        if not isinstance(categories, list):
            continue
        for item in categories:
            if isinstance(item, str) and item in ALLOWED_TEMPLATE_CATEGORIES:
                continue
            add_doc_violation(
                violations,
                rule_id="R023",
                doc=doc,
                pattern=r"^\s*categories\s*:",
                default_pattern=r"^\s*spec\s*:",
                message=f"Template spec.categories entries must be from allowlist: {allowed}",
            )
            break
    return violations


def check_deploy_manager_label_match_name(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    label_key = "cloud.sealos.io/app-deploy-manager"

    for doc in context.yaml_documents:
        if doc.skip_checks or not isinstance(doc.data, dict):
            continue
        if not is_app_workload_document(doc):
            continue
        metadata = doc.data.get("metadata")
        if not isinstance(metadata, dict):
            continue
        name = metadata.get("name")
        labels = metadata.get("labels")
        if not isinstance(name, str):
            continue

        label_value = labels.get(label_key) if isinstance(labels, dict) else None
        if label_value is None:
            add_doc_violation(
                violations,
                rule_id="R008",
                doc=doc,
                pattern=r"^\s*labels\s*:",
                default_pattern=r"^\s*metadata\s*:",
                message=f"{label_key} label is required and must exactly match metadata.name",
            )
            continue
        if label_value != name:
            add_doc_violation(
                violations,
                rule_id="R008",
                doc=doc,
                pattern=re.escape(label_key),
                message=f"{label_key} must exactly match metadata.name",
            )

    return violations


def check_origin_image_name_matches_container(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    for doc in context.yaml_documents:
        if doc.skip_checks or not isinstance(doc.data, dict):
            continue
        if doc.path.suffix.lower() not in TEMPLATE_ARTIFACT_SUFFIXES:
            continue
        if not is_app_workload_document(doc):
            continue
        if not has_managed_workload_marker(doc.data):
            continue

        metadata = doc.data.get("metadata")
        annotations = metadata.get("annotations") if isinstance(metadata, dict) else None
        origin_image = annotations.get("originImageName") if isinstance(annotations, dict) else None
        template_spec = get_template_spec(doc.data)
        containers = template_spec.get("containers") if isinstance(template_spec, dict) else None
        images = [item.get("image") for item in containers or [] if isinstance(item, dict)]
        image_values = [image.strip() for image in images if isinstance(image, str) and image.strip()]
        if not image_values:
            continue

        if not isinstance(origin_image, str) or not origin_image.strip():
            add_doc_violation(
                violations,
                rule_id="R015",
                doc=doc,
                pattern=r"originImageName",
                default_pattern=r"^\s*metadata\s*:",
                message="managed app workloads must define metadata.annotations.originImageName",
            )
            continue
        if origin_image.strip() not in image_values:
            add_doc_violation(
                violations,
                rule_id="R015",
                doc=doc,
                pattern=r"originImageName",
                default_pattern=r"^\s*metadata\s*:",
                message="metadata.annotations.originImageName must match a container image in the workload",
            )
    return violations


def check_service_ports_have_names(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    for doc in iter_documents_by_kind(context, "Service"):
        if doc.path.suffix.lower() not in TEMPLATE_ARTIFACT_SUFFIXES:
            continue
        if doc.path.name != "index.yaml":
            continue
        spec = doc.data.get("spec") if isinstance(doc.data, dict) else None
        ports = spec.get("ports") if isinstance(spec, dict) else None
        if not isinstance(ports, list):
            continue
        for entry in ports:
            if not isinstance(entry, dict):
                continue
            port_value = entry.get("port")
            name = entry.get("name")
            if isinstance(name, str) and name.strip():
                continue
            pattern = (
                rf"^\s*port\s*:\s*{re.escape(str(port_value))}\s*$"
                if port_value is not None
                else r"^\s*ports\s*:"
            )
            add_doc_violation(
                violations,
                rule_id="R020",
                doc=doc,
                pattern=pattern,
                default_pattern=r"^\s*ports\s*:",
                message="Service spec.ports entries must define a non-empty name",
            )
    return violations


def _normalize_annotation_value(value: Any) -> Optional[str]:
    if isinstance(value, str):
        return "\n".join(line.rstrip() for line in value.strip().splitlines())
    if value is None:
        return None
    return str(value).strip()


def check_http_ingress_annotations(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    for doc in iter_documents_by_kind(context, "Ingress"):
        if doc.path.suffix.lower() not in TEMPLATE_ARTIFACT_SUFFIXES:
            continue
        if doc.path.name != "index.yaml":
            continue
        if not isinstance(doc.data, dict):
            continue

        metadata = doc.data.get("metadata")
        annotations = metadata.get("annotations") if isinstance(metadata, dict) else None
        if not isinstance(annotations, dict):
            add_doc_violation(
                violations,
                rule_id="R026",
                doc=doc,
                pattern=r"^\s*annotations\s*:",
                default_pattern=r"^\s*metadata\s*:",
                message="Ingress metadata.annotations must define the required HTTP annotation set",
            )
            continue

        backend_protocol = _normalize_annotation_value(
            annotations.get("nginx.ingress.kubernetes.io/backend-protocol")
        )
        if backend_protocol is not None and backend_protocol.upper() != "HTTP":
            continue

        for key, expected in HTTP_INGRESS_REQUIRED_ANNOTATIONS.items():
            actual_normalized = _normalize_annotation_value(annotations.get(key))
            expected_normalized = _normalize_annotation_value(expected)
            if actual_normalized == expected_normalized:
                continue
            add_doc_violation(
                violations,
                rule_id="R026",
                doc=doc,
                pattern=re.escape(key),
                default_pattern=r"^\s*annotations\s*:",
                message=f"Ingress annotation '{key}' must match the required HTTP default",
            )
    return violations


def _is_worker_args(args: Any) -> bool:
    if not isinstance(args, list) or not args:
        return False
    first = str(args[0]).strip().lower()
    return first == "worker"


def _probe_has_http_path(probe: Any, expected_path: str) -> bool:
    if not isinstance(probe, dict):
        return False
    http_get = probe.get("httpGet")
    if not isinstance(http_get, dict):
        return False
    if http_get.get("path") != expected_path:
        return False
    port = http_get.get("port")
    return isinstance(port, (int, str)) and bool(str(port).strip())


def _probe_has_exec_command(probe: Any, expected_fragment: str) -> bool:
    if not isinstance(probe, dict):
        return False
    exec_probe = probe.get("exec")
    if not isinstance(exec_probe, dict):
        return False
    command = exec_probe.get("command")
    if not isinstance(command, list) or not command:
        return False
    merged = " ".join(str(item) for item in command)
    return expected_fragment in merged


def check_official_health_probes(context: ScanContext) -> List[Violation]:
    violations: List[Violation] = []
    for doc in context.yaml_documents:
        if doc.skip_checks or not isinstance(doc.data, dict):
            continue
        if not is_app_workload_document(doc):
            continue
        if not has_managed_workload_marker(doc.data):
            continue

        template_spec = get_template_spec(doc.data)
        containers = template_spec.get("containers") if isinstance(template_spec, dict) else None
        if not isinstance(containers, list) or not containers:
            continue
        if not isinstance(containers[0], dict):
            continue
        container = containers[0]
        image = container.get("image")
        if not isinstance(image, str) or not image.strip():
            continue
        image_lower = image.strip().lower()

        worker_marker = next((m for m in OFFICIAL_HEALTH_WORKER_EXEC_EXPECTATIONS if m in image_lower), None)
        if worker_marker and _is_worker_args(container.get("args")):
            expected = OFFICIAL_HEALTH_WORKER_EXEC_EXPECTATIONS[worker_marker]
            liveness = container.get("livenessProbe")
            readiness = container.get("readinessProbe")
            startup = container.get("startupProbe")
            if not _probe_has_exec_command(liveness, expected["liveness_command"]):
                add_doc_violation(
                    violations,
                    rule_id="R024",
                    doc=doc,
                    pattern=r"^\s*livenessProbe\s*:",
                    default_pattern=r"^\s*containers\s*:",
                    message=(
                        "workloads with official health checks must define livenessProbe; "
                        "expected exec command containing 'ak healthcheck'"
                    ),
                )
            if not _probe_has_exec_command(readiness, expected["readiness_command"]):
                add_doc_violation(
                    violations,
                    rule_id="R024",
                    doc=doc,
                    pattern=r"^\s*readinessProbe\s*:",
                    default_pattern=r"^\s*containers\s*:",
                    message=(
                        "workloads with official health checks must define readinessProbe; "
                        "expected exec command containing 'ak healthcheck'"
                    ),
                )
            if not _probe_has_exec_command(startup, expected["startup_command"]):
                add_doc_violation(
                    violations,
                    rule_id="R024",
                    doc=doc,
                    pattern=r"^\s*startupProbe\s*:",
                    default_pattern=r"^\s*containers\s*:",
                    message=(
                        "workloads with slow startup and official health checks must define startupProbe; "
                        "expected exec command containing 'ak healthcheck'"
                    ),
                )
            continue

        http_marker = next((m for m in OFFICIAL_HEALTH_HTTP_EXPECTATIONS if m in image_lower), None)
        if not http_marker:
            continue

        expected = OFFICIAL_HEALTH_HTTP_EXPECTATIONS[http_marker]
        liveness = container.get("livenessProbe")
        readiness = container.get("readinessProbe")
        startup = container.get("startupProbe")
        if not _probe_has_http_path(liveness, expected["liveness_path"]):
            add_doc_violation(
                violations,
                rule_id="R024",
                doc=doc,
                pattern=r"^\s*livenessProbe\s*:",
                default_pattern=r"^\s*containers\s*:",
                message=(
                    "workloads with official health checks must define livenessProbe "
                    "with the official endpoint path"
                ),
            )
        if not _probe_has_http_path(readiness, expected["readiness_path"]):
            add_doc_violation(
                violations,
                rule_id="R024",
                doc=doc,
                pattern=r"^\s*readinessProbe\s*:",
                default_pattern=r"^\s*containers\s*:",
                message=(
                    "workloads with official health checks must define readinessProbe "
                    "with the official endpoint path"
                ),
            )
        if not _probe_has_http_path(startup, expected["startup_path"]):
            add_doc_violation(
                violations,
                rule_id="R024",
                doc=doc,
                pattern=r"^\s*startupProbe\s*:",
                default_pattern=r"^\s*containers\s*:",
                message=(
                    "workloads with slow startup and official health checks must define startupProbe "
                    "with the official endpoint path"
                ),
            )
    return violations


def check_revision_history_limit(context: ScanContext) -> List[Violation]:
    return check_managed_workload_setting(
        context,
        rule_id="R009",
        value_extractor=lambda data: data.get("spec", {}).get("revisionHistoryLimit")
        if isinstance(data.get("spec"), dict)
        else None,
        expected=1,
        value_pattern=r"^\s*revisionHistoryLimit\s*:",
        fallback_pattern=r"^\s*spec\s*:",
        missing_message="managed app workloads must explicitly set revisionHistoryLimit: 1",
        mismatch_message="revisionHistoryLimit must be set to 1 for managed app workloads",
    )


def _extract_automount_service_account_token(data: dict) -> object:
    template_spec = get_template_spec(data)
    if not isinstance(template_spec, dict):
        return None
    return template_spec.get("automountServiceAccountToken")


def check_automount_service_account_token(context: ScanContext) -> List[Violation]:
    return check_managed_workload_setting(
        context,
        rule_id="R010",
        value_extractor=_extract_automount_service_account_token,
        expected=False,
        value_pattern=r"^\s*automountServiceAccountToken\s*:",
        fallback_pattern=r"^\s*template\s*:",
        missing_message="managed app workloads must explicitly set automountServiceAccountToken: false",
        mismatch_message="automountServiceAccountToken must be false for managed app workloads",
    )


APP_RULES: Dict[str, Rule] = {
    "R001": Rule("R001", check_no_latest_tags),
    "R016": Rule("R016", check_no_floating_image_tags),
    "R018": Rule("R018", check_no_compose_image_variables),
    "R002": Rule("R002", check_app_no_spec_template),
    "R003": Rule("R003", check_app_has_spec_data_url),
    "R004": Rule("R004", check_template_name_is_hardcoded_lowercase),
    "R012": Rule("R012", check_template_required_metadata_fields),
    "R013": Rule("R013", check_template_folder_matches_name),
    "R014": Rule("R014", check_template_icon_paths),
    "R025": Rule("R025", check_template_readme_paths),
    "R021": Rule("R021", check_template_i18n_zh_description_chinese),
    "R022": Rule("R022", check_template_i18n_zh_title_absent),
    "R023": Rule("R023", check_template_categories_allowed),
    "R024": Rule("R024", check_official_health_probes),
    "R015": Rule("R015", check_origin_image_name_matches_container),
    "R020": Rule("R020", check_service_ports_have_names),
    "R026": Rule("R026", check_http_ingress_annotations),
    "R008": Rule("R008", check_deploy_manager_label_match_name),
    "R009": Rule("R009", check_revision_history_limit),
    "R010": Rule("R010", check_automount_service_account_token),
}
