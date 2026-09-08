"""Run with Python and PyYAML to check persistent configuration initialization."""

from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

import yaml


template = Path(__file__).resolve().parents[1] / 'template/moneyprinterturbo/index.yaml'
workload = next(doc for doc in yaml.safe_load_all(template.read_text()) if doc['kind'] == 'StatefulSet')
pod = workload['spec']['template']['spec']

with TemporaryDirectory() as directory:
    root = Path(directory)
    storage = root / 'storage'
    storage.mkdir()
    (root / 'config.example.toml').write_text('[ui]\nlanguage = "en"\n')
    command = pod['initContainers'][0]['command'][:]
    command[-1] = command[-1].replace('/MoneyPrinterTurbo', directory)
    subprocess.run(command, check=True)
    saved = storage / 'config.toml'
    assert saved.read_text() == (root / 'config.example.toml').read_text()
    saved.write_text('[ui]\nlanguage = "fr"\n')
    subprocess.run(command, check=True)
    assert saved.read_text() == '[ui]\nlanguage = "fr"\n'

    config = SimpleNamespace(root_dir=str(root), config_file=str(root / 'config.toml'))
    config_module = ModuleType('app.config')
    config_module.config = config
    cli = ModuleType('streamlit.web.cli')
    calls = []

    def start_streamlit():
        # Atomic replacement requires temporary and target files on the same volume.
        assert Path(config.root_dir) == storage
        assert Path(config.config_file) == saved
        calls.append(True)

    cli.main = start_streamlit
    launcher = pod['containers'][0]['args'][0].replace('/MoneyPrinterTurbo', directory)
    with patch.dict(sys.modules, {'app.config': config_module, 'streamlit.web.cli': cli}):
        exec(launcher, {})
    assert calls == [True]

print('PASS: first boot, configuration preservation, and atomic-save directory routing')
