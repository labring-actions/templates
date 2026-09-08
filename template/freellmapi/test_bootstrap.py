"""Run with Python and PyYAML: python template/freellmapi/test_bootstrap.py."""
import os
from pathlib import Path
import re
import subprocess
import tempfile

import yaml


documents = list(yaml.safe_load_all(Path(__file__).with_name("index.yaml").read_text()))
scripts = next(doc["data"] for doc in documents if doc["kind"] == "ConfigMap")
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    paths = {}
    for name, content in scripts.items():
        paths[name] = root / name
        paths[name].write_text(content.replace("/app/server/data", str(root / "data")))
    init = paths["vn-appvn-sealosvn-initvn-sh"]
    start = paths["vn-appvn-sealosvn-startvn-sh"]
    key = root / "data/runtime/.encryption-key"
    probe = root / "node"
    probe.write_text("#!/bin/sh\n[ ${#ENCRYPTION_KEY} -eq 64 ]\n")
    probe.chmod(0o700)
    environment = {**os.environ, "PATH": str(root) + os.pathsep + os.environ["PATH"]}

    def run(script):
        result = subprocess.run(["/bin/sh", str(script)], env=environment, capture_output=True)
        assert not result.stdout
        return result.returncode

    assert run(init) == 0
    original = key.read_bytes()
    assert re.fullmatch(rb"[0-9a-f]{64}", original)
    assert key.stat().st_mode & 0o777 == 0o600
    assert run(init) == 0 and key.read_bytes() == original
    assert run(start) == 0
    for invalid in (b"x" * 64, b"a" * 63, b"a" * 65, b"a" * 64 + b"\n"):
        key.write_bytes(invalid)
        assert run(init) != 0 and run(start) != 0
        assert key.read_bytes() == invalid
    key.unlink()
    (key.parent / "freeapi.db").touch()
    assert run(init) != 0 and not key.exists()
    assert not list(key.parent.glob("*.tmp.*"))

print("PASS: key format, 0600 permissions, persistence, startup export, invalid input, and lost-key protection")
