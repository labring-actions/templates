#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml


class ValidationError(Exception):
    pass


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


def load_yaml_docs(path: Path) -> list[dict]:
    try:
        return [doc for doc in yaml.safe_load_all(path.read_text(encoding="utf-8")) if doc is not None]
    except yaml.YAMLError as exc:
        raise ValidationError(f"{path}: invalid YAML: {exc}") from exc


def get_nested(value: dict | None, *keys: str):
    node = value
    for key in keys:
        if not isinstance(node, dict) or key not in node:
            return None
        node = node[key]
    return node


def headings(text: str) -> list[dict]:
    results = []
    for match in HEADING_RE.finditer(text):
        results.append(
            {
                "level": len(match.group(1)),
                "text": match.group(2).strip(),
                "start": match.start(),
                "end": match.end(),
            }
        )
    return results


def section_text(text: str, items: list[dict], index: int) -> str:
    start = items[index]["end"]
    level = items[index]["level"]
    end = len(text)
    for item in items[index + 1 :]:
        if item["level"] <= level:
            end = item["start"]
            break
    return text[start:end].strip()


def first_numbered_step(text: str) -> str | None:
    for line in text.splitlines():
        if re.match(r"^\s*1\.\s+", line):
            return line.strip()
    return None


def stepwise_match(items: list[dict], patterns: list[re.Pattern[str]]) -> list[int] | None:
    cursor = 0
    indices: list[int] = []
    for pattern in patterns:
        found = None
        for index in range(cursor, len(items)):
            item = items[index]
            if item["level"] == 2 and pattern.search(item["text"]):
                found = index
                cursor = index + 1
                break
        if found is None:
            return None
        indices.append(found)
    return indices


def detect_multi_service(resource_docs: list[dict]) -> bool:
    kinds = [doc.get("kind") for doc in resource_docs if isinstance(doc, dict)]
    if any(kind in {"Cluster", "Job", "ObjectStorageBucket"} for kind in kinds):
        return True
    return sum(1 for kind in kinds if kind in {"Deployment", "StatefulSet"}) > 1


def validate_template(template_dir: Path) -> list[str]:
    errors: list[str] = []
    index_path = template_dir / "index.yaml"
    readme_path = template_dir / "README.md"
    readme_zh_path = template_dir / "README_zh.md"

    for path in (index_path, readme_path, readme_zh_path):
        if not path.exists():
            errors.append(f"{template_dir.name}: missing {path.name}")

    if errors:
        return errors

    docs = load_yaml_docs(index_path)
    if not docs:
        return [f"{template_dir.name}: index.yaml is empty"]

    template_doc = docs[0]
    metadata = template_doc.get("metadata", {}) if isinstance(template_doc, dict) else {}
    spec = template_doc.get("spec", {}) if isinstance(template_doc, dict) else {}
    slug = metadata.get("name")
    title = spec.get("title")
    readme_ref = spec.get("readme")
    zh_readme_ref = get_nested(spec, "i18n", "zh", "readme")
    screenshots = spec.get("screenshots") or []
    defaults = spec.get("defaults") or {}
    locale = spec.get("locale")

    if slug != template_dir.name:
        errors.append(f"{template_dir.name}: metadata.name should match the folder name")
    if not title:
        errors.append(f"{template_dir.name}: spec.title is required")
    if locale != "en":
        errors.append(f"{template_dir.name}: spec.locale should be en")
    if not isinstance(readme_ref, str) or f"template/{slug}/README.md" not in readme_ref:
        errors.append(f"{template_dir.name}: spec.readme should point to README.md for this template")
    if not isinstance(zh_readme_ref, str) or f"template/{slug}/README_zh.md" not in zh_readme_ref:
        errors.append(f"{template_dir.name}: spec.i18n.zh.readme should point to README_zh.md for this template")
    if not isinstance(screenshots, list) or not any("website-screenshot.webp" in str(item) for item in screenshots):
        errors.append(f"{template_dir.name}: spec.screenshots should include website-screenshot.webp")
    if not isinstance(defaults, dict):
        errors.append(f"{template_dir.name}: spec.defaults should be a mapping")
    else:
        app_name = defaults.get("app_name", {})
        app_host = defaults.get("app_host", {})
        app_name_value = app_name.get("value") if isinstance(app_name, dict) else None
        app_host_value = app_host.get("value") if isinstance(app_host, dict) else None
        if not isinstance(app_name_value, str) or "${{ random(8) }}" not in app_name_value:
            errors.append(f"{template_dir.name}: spec.defaults.app_name should use random(8)")
        if not isinstance(app_host_value, str) or "${{ random(8) }}" not in app_host_value:
            errors.append(f"{template_dir.name}: spec.defaults.app_host should use random(8)")

    app_docs = [doc for doc in docs[1:] if isinstance(doc, dict) and doc.get("kind") == "App"]
    if not app_docs:
        errors.append(f"{template_dir.name}: index.yaml should include an App resource")
    else:
        app_url = get_nested(app_docs[0], "spec", "data", "url")
        if not isinstance(app_url, str):
            errors.append(f"{template_dir.name}: App resource should define spec.data.url")
        elif "${{ defaults.app_host }}" not in app_url or "${{ SEALOS_CLOUD_DOMAIN }}" not in app_url:
            errors.append(f"{template_dir.name}: App URL should use defaults.app_host and SEALOS_CLOUD_DOMAIN")

    english = readme_path.read_text(encoding="utf-8")
    chinese = readme_zh_path.read_text(encoding="utf-8")
    multi_service = detect_multi_service(docs[1:])
    if multi_service:
        if "Architecture Components" not in english:
            errors.append(f"{template_dir.name}: README.md should include Architecture Components")
        if "架构组件" not in chinese:
            errors.append(f"{template_dir.name}: README_zh.md should include 架构组件")

    english_headings = headings(english)
    if not english_headings or english_headings[0]["level"] != 1 or english_headings[0]["text"] != f"Deploy and Host {title} on Sealos":
        errors.append(f"{template_dir.name}: README.md H1 should be '# Deploy and Host {title} on Sealos'")

    english_patterns = [
        re.compile(r"^About Hosting\b"),
        re.compile(r"^Common Use Cases\b"),
        re.compile(r"^Dependencies for\b"),
        re.compile(r"^Why Deploy\b.*\bon Sealos\b"),
        re.compile(r"^Deployment Guide\b"),
        re.compile(r"^License\b"),
    ]
    english_sequence = stepwise_match(english_headings, english_patterns)
    if english_sequence is None:
        errors.append(f"{template_dir.name}: README.md is missing a required section or section order")
    else:
        deployment_section = section_text(english, english_headings, english_sequence[4])
        step1 = first_numbered_step(deployment_section)
        expected_url = f"https://sealos.io/products/app-store/{slug}"
        if not step1 or expected_url not in step1 or "Deploy Now" not in step1:
            errors.append(f"{template_dir.name}: README.md step 1 should open the template page and click Deploy Now")
        if not re.search(r"2\s*-\s*3\s*(?:minutes|mins?|分钟)", deployment_section, re.I):
            errors.append(f"{template_dir.name}: README.md should mention the typical 2-3 minute deployment time")

    if "website-screenshot.webp" not in english:
        errors.append(f"{template_dir.name}: README.md should reference website-screenshot.webp")

    chinese_headings = headings(chinese)
    if not chinese_headings or chinese_headings[0]["level"] != 1 or chinese_headings[0]["text"] != f"在 Sealos 上部署和托管 {title}":
        errors.append(f"{template_dir.name}: README_zh.md H1 should be '# 在 Sealos 上部署和托管 {title}'")

    chinese_patterns = [
        re.compile(r"托管"),
        re.compile(r"常见使用场景"),
        re.compile(r"依赖"),
        re.compile(r"为什么在 Sealos 上部署"),
        re.compile(r"部署指南"),
        re.compile(r"许可证"),
    ]
    chinese_sequence = stepwise_match(chinese_headings, chinese_patterns)
    if chinese_sequence is None:
        errors.append(f"{template_dir.name}: README_zh.md is missing a required section or section order")
    else:
        deployment_section = section_text(chinese, chinese_headings, chinese_sequence[4])
        step1 = first_numbered_step(deployment_section)
        expected_url = f"https://sealos.io/products/app-store/{slug}"
        if not step1 or expected_url not in step1 or ("Deploy Now" not in step1 and "立即部署" not in step1):
            errors.append(f"{template_dir.name}: README_zh.md step 1 should open the template page and click Deploy Now")
        if not re.search(r"2\s*-\s*3\s*(?:minutes|mins?|分钟)", deployment_section, re.I):
            errors.append(f"{template_dir.name}: README_zh.md should mention the typical 2-3 minute deployment time")

    expected_url = f"https://sealos.io/products/app-store/{slug}"
    if "sealos.run" in chinese:
        errors.append(f"{template_dir.name}: README_zh.md should use https://sealos.io for Sealos links")
    if expected_url not in chinese:
        errors.append(f"{template_dir.name}: README_zh.md should include the Sealos App Store slug")
    if "website-screenshot.webp" not in chinese:
        errors.append(f"{template_dir.name}: README_zh.md should reference website-screenshot.webp")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Sealos template READMEs.")
    parser.add_argument("template_dirs", nargs="+", type=Path)
    args = parser.parse_args()

    exit_code = 0
    for template_dir in args.template_dirs:
        try:
            errors = validate_template(template_dir)
        except ValidationError as exc:
            errors = [str(exc)]
        if errors:
            exit_code = 1
            print(f"{template_dir.name}: FAIL")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"{template_dir.name}: PASS")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
