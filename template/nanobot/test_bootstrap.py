"""Run with Python and PyYAML to verify first-run config and restart persistence."""

import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

import yaml


docs = list(yaml.safe_load_all(Path(__file__).with_name("index.yaml").read_text()))
config = next(doc for doc in docs if doc["kind"] == "ConfigMap")
workload = next(doc for doc in docs if doc["kind"] == "StatefulSet")
initial = json.loads(config["data"]["vn-appvn-sealosvn-configvn-json"])
assert initial["agents"]["defaults"]["model"] == "${NANOBOT_MODEL}"
assert initial["channels"]["websocket"]["tokenIssueSecret"] == "${NANOBOT_WEB_TOKEN}"
assert initial["tools"]["restrictToWorkspace"] is True

with TemporaryDirectory() as directory:
    root = Path(directory)
    source, target = root / "initial.json", root / "config.json"
    source.write_text(json.dumps(initial))
    command = workload["spec"]["template"]["spec"]["initContainers"][0]["command"][-1]
    # Tokenizer warmup is covered by the live init-container validation.
    command = command.split("\npython -c")[0]
    command = command.replace("/app/sealos-config.json", str(source))
    command = command.replace("/home/nanobot/.nanobot/config.json", str(target))
    subprocess.run(["/bin/sh", "-c", command], check=True)
    assert target.read_bytes() == source.read_bytes()
    assert target.stat().st_mode & 0o777 == 0o600
    custom = {**initial, "userSetting": "preserve after restart"}
    target.write_text(json.dumps(custom))
    subprocess.run(["/bin/sh", "-c", command], check=True)
    assert json.loads(target.read_text()) == custom

print("PASS: private first-run configuration and preserved user edits on restart")
