"""Run with Python and PyYAML to verify runtime upgrades and first-save startup."""

import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import Mock, patch
import zipfile

import yaml


template = Path(__file__).resolve().parents[1] / "template/eaglercraft-server/index.yaml"
workload = next(doc for doc in yaml.safe_load_all(template.read_text()) if doc["kind"] == "StatefulSet")
init = workload["spec"]["template"]["spec"]["initContainers"][0]

with TemporaryDirectory() as directory:
    root = Path(directory)
    image, runtime = root / "image", root / "runtime"
    assets = ("script/start_server.sh", "script/http_server.py", "web-1.8/admin.html", "web-1.12/admin-i18n.js")
    for asset in assets:
        path = image / asset
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("new release")
    jar = image / "server-1.8/plugins/Dynmap.jar"
    jar.parent.mkdir(parents=True)
    with zipfile.ZipFile(jar, "w") as archive:
        archive.writestr("configuration.txt", "    sendhealth: true\n    showplayerhealth: true\n    sendposition: true\n")
    command = init["args"][0].replace("/eaglerx-data/runtime", str(runtime))
    env = dict(os.environ, IMAGE_APP_DIR=str(image))
    runtime.mkdir()
    (runtime / "keep.txt").write_text("incomplete runtime")
    assert subprocess.run([*init["command"], command], env=env, capture_output=True).returncode != 0
    assert (runtime / "keep.txt").read_text() == "incomplete runtime"
    (runtime / "keep.txt").unlink()
    subprocess.run([*init["command"], command], env=env, check=True)
    assert all((runtime / asset).read_text() == "new release" for asset in assets)
    config = runtime / "server-1.8/plugins/dynmap/configuration.txt"
    assert config.read_text() == "    sendhealth: false\n    showplayerhealth: false\n    sendposition: true\n"
    config.write_text(config.read_text() + "custom-setting: preserved\n")

    for asset in assets:
        path = runtime / asset
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("previous release")
    preserved = ("server-1.12/world/level.dat", "server-1.12/server.properties", "server-data/plugins-1.12/LoginSecurity/users.db")
    for name in preserved:
        path = runtime / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"persistent user data")
    for _ in range(2):
        subprocess.run([*init["command"], command], env=env, check=True)
        assert all((runtime / asset).read_text() == "new release" for asset in assets)
        assert all((runtime / name).read_bytes() == b"persistent user data" for name in preserved)
        assert config.read_text().endswith("custom-setting: preserved\n")

    container = workload["spec"]["template"]["spec"]["containers"][0]
    guard = container["readinessProbe"]["exec"]["command"][-1].split("&&")[0]
    server = runtime / "server"
    (server / "custom world").mkdir(parents=True)
    (server / "server.properties").write_text("level-name=custom world\n")
    env["APP_DIR"] = str(runtime)
    assert subprocess.run(["/bin/sh", "-c", guard], env=env).returncode != 0
    startup = container["startupProbe"]["exec"]["command"][-1].split("<<'PY'\n", 1)[1].rsplit("\nPY", 1)[0]
    level = server / "custom world/level.dat"
    bridge = SimpleNamespace(SERVER_ROOT=str(server), get_level_name=lambda: "custom world", rcon_send=Mock())
    with patch.dict(sys.modules, {"http_server": bridge}), patch("socket.create_connection"):
        bridge.rcon_send.side_effect = RuntimeError("RCON unavailable")
        try:
            exec(startup, {})
        except RuntimeError as error:
            assert str(error) == "RCON unavailable"
        else:
            raise AssertionError("Startup passed while the first save failed")
        assert not level.exists()
        bridge.rcon_send.reset_mock()
        bridge.rcon_send.side_effect = lambda command, **kwargs: level.write_bytes(b"saved world") if command == "save-all" else "No players online"
        exec(startup, {})
        bridge.rcon_send.assert_called_once_with("save-all", retries=1)
        exec(startup, {})
        bridge.rcon_send.assert_called_with("list", retries=1)
        assert level.read_bytes() == b"saved world"
        level.write_bytes(b"")
        exec(startup, {})
        assert level.read_bytes() == b"saved world"
    subprocess.run(["/bin/sh", "-c", guard], env=env, check=True)

print("PASS: initialization, upgrade refresh, Dynmap compatibility, first-save startup, readiness, and data preservation")
